from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Import scraping code
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)


# Set route
@app.route('/scrape')
# Scrape Function
def scraper():
    #mars = list(db.mars.find())
    mars = db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)
    #print(mars)

    # Return the template with the teams list passed in
    #return render_template('index.html', mars=mars)


if __name__ == "__main__":
    app.run(debug=True)