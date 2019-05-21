#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import re

def scrape():
    nasa_news_url = "https://mars.nasa.gov/news/"
    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    root_images_url = "https://www.jpl.nasa.gov"
    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    mars_facts_url = "https://space-facts.com/mars/"
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_hemisphere_url_root = "https://astrogeology.usgs.gov"

    nasa_news_response = requests.get(nasa_news_url)


    # In[2]:

    soup = bs(nasa_news_response.text, 'html.parser')

    # In[ ]:

    first_title = soup.find('div', class_='content_title')
    print(first_title.text.strip())

    first_p = soup.find('div', class_='rollover_description_inner')

    print(first_p.text.strip())


    # In[ ]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(mars_images_url)


    # In[ ]:


    html = browser.html
    soup = bs(html, 'html.parser')
#    carousel_items = soup.select('.carousel_items')
    article = soup.find('article')
    article_style = article['style']

    first_match = re.findall(r"'(.*?)'", article_style)[0]
    featured_image_url = root_images_url + first_match
    print(featured_image_url)


    # In[ ]:


    browser.visit(mars_twitter_url)


    # In[ ]:


    html = browser.html
    soup = bs(html, 'html.parser')
    tweet = soup.find('p', class_='tweet-text')

    mars_weather = tweet.text
    print(mars_weather)


    # In[ ]:


    tables = pd.read_html(mars_facts_url)
    


    # In[ ]:


    mars_facts_df = tables[0]
    mars_facts_df.columns = ["stat", "value"]
    mars_facts_df.set_index("stat", inplace=True)



    # In[ ]:


    browser.visit(mars_hemisphere_url)


    # In[ ]:


    html = browser.html
    soup = bs(html, 'html.parser')
    content_section = soup.select("#results-accordian")[0]


    # In[ ]:


    hemisphere_image_urls = []
    for item in content_section.find_all('div', class_='item'):
        img_dict = {"title":"","img_url":""}
        description = item.find('div', class_='description')
        link = description.find('a', class_='itemLink')
        img_dict['title'] = link.text
        
        browser.visit(mars_hemisphere_url_root + link['href'])
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img = soup.find('img', class_='wide-image')['src']
        img_dict['img_url'] = mars_hemisphere_url_root + img
        hemisphere_image_urls.append(img_dict)
        
    dict_to_return = {
        'title': first_title.text.strip(),
        'description': first_p.text.strip(),
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts_df.to_dict('index'),
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return dict_to_return