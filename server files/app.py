# Import Dependencies
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient as MC
import pandas as pd

# ESTABLISH DATABASE CONNECTION
client = MC()
DB = client.real_estate

# DEFINE FLASK APPLICATION
app = Flask(__name__)

#Define web route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api_home():
    return render_template("api_home.html")

@app.route("/cheapest_state")
def cheapest_state():
    states = []
    for coll in DB.collection_names():
        df = pd.DataFrame(DB[coll].find())
        median = df['price/acre'].median()
        states.append({
            "state": coll,
            "median": median
        })
    df = pd.DataFrame(states)

    minimum = df['median'].min()
    state = df['state'].loc[df['median'] == minimum].values[0]

    return jsonify({"state": state, "median": minimum})

# RUN APPLICATION
if __name__ == "__main__":
	app.run()