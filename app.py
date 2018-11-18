from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html",mars=mars)


@app.route("/scrape")
def scraper():
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")
    # mars = mongo.db.mars
    # mars_dict = scrape_mars.scrape()
    # mars.update({}, mars_dict, upsert=True)
    # return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
