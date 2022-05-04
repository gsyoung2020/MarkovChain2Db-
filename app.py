import os
import sqlite3
import flask
from flask import request, jsonify
import requests

connection = sqlite3.connect("Markov.db")
cursor = connection.cursor()

cursor.execute("select sentence from chatter") 
sentence = list(cursor)
dep = sentence[0]
acx = dep[0]
#ya gotta go down two layers boss
#print(acx)
cursor.execute("select max(RowId) from chatter") 
num = list(cursor)[0]
print(num[0])
number = num[0]

tweets = []

for x in range(number):
  layerOne = sentence[x]
  layerTWO = layerOne[0]
  tweets.append(layerTWO)
print("end")

app = flask.Flask(__name__)
sess = requests.Session()

#app.config["DEBUG"] = True


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "DELETE"])
def api_all(path):
    return jsonify(tweets)
app.run(host='0.0.0.0',port=5000)