from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

DB = SQLAlchemy()

APP.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# how the database knows about the app
DB.init_app(APP)

@APP.route("/", methods=['POST', 'GET'])
# define home page
def home():
    return render_template("home.html", picture=images(), breeds = list_breed())

# function to get random cat pics
def images():
    image = requests.get("https://api.thecatapi.com/v1/images/search")
    cats = image.json()[0]["url"]
    return cats

# list of cat breeds put in a dictionary

def list_breed():
    breed_list = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = {}
    for breed_type in breed_list.json():
        breeds[breed_type["id"]] = breed_type['name']
    return breeds

# calling the api to search for cats by breed
def search_cat(cat = ''):
    search = requests.get(f"https://api.thecatapi.com/v1/images/search?breed_ids={cat}")
    result = search.json()[0]['url']
    return result

# page where submit (cats by category) button in home.html lands with the image of a new cat

@APP.route("/breed", methods=['POST'])
def breed():
    cat = request.values['category'] # get the values from the dictionary in home.html
    image = search_cat(cat) # call the search cat function and pass in the id(values) as the parameter
    breeds = list_breed() # just call the list_Breed function
    breed = breeds[cat] # call the id(key) from the list_breed() dictionary which returns the value
    return render_template("home.html", picture=image, breeds=breeds, breed=breed)

# database to save favorite cats
class fav_cats(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    link = DB.Column(DB.String(150))
    breed = DB.Column(DB.String(50))
    breed_id = DB.Column(DB.String(10))

@APP.route("/saved_cats", methods = ["POST", "Get"])
def saved_cats():
    name_id = str(request.values['category']) #get the breed id of the cat
    
    breeds = list_breed() # dictionary with breed name
    
    name = str(breeds[name_id]) # get the breed(value) of the cat from the name_id(key)
    
    link = str(request.values['CAT_URL']) # get the value from this name which is defined in home.html

    DB.session.add(fav_cats(link=link, breed=name, breed_id=name_id))

    DB.session.commit()

    return render_template("home.html", picture=images(), breeds = list_breed())


@APP.route("/reset")
def reset():
    DB.drop_all()
    DB.create_all()
    return "Database has been reset"