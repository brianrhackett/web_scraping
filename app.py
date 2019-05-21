from flask import Flask, jsonify, render_template, redirect
import pymongo



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.MarsDB    
    data_out = db.mars.find()
    return render_template("index.html", data=data_out[0])

@app.route('/scrape')
def scrape_mars():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.MarsDB
    db.mars.remove()
    import scrape_mars
    data_in = scrape_mars.scrape()
    db.mars.insert_one(data_in)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)