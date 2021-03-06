# Import Dependencies
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient as MC
import pandas as pd
print(pd.__version__)


# ESTABLISH DATABASE CONNECTION
# client = MC()
import pymongo
client = pymongo.MongoClient("mongodb://uatu:#watch!@uatu-cluster-shard-00-00.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-01.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-02.c4ylx.mongodb.net:27017/real_estate?ssl=true&replicaSet=atlas-10fsbj-shard-0&authSource=admin&retryWrites=true&w=majority")

DB = client.real_estate

# DEFINE FLASK APPLICATION
app = Flask(__name__)

#Define web route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api_home():
    return render_template("api_home.html", title=stuff)

@app.route("/api/cheapest_state")
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

@app.route("/api/get_data", methods=['GET', 'POST'])
def search():
    print("Search route accessed.")
    search_term = request.get_json(force=True)
    print(search_term)

    # Query database for search term.

    return "Server says you searched for: " + str(search_term['search'])


# RUN APPLICATION
if __name__ == "__main__":
	app.run(debug=True)