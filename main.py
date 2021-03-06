from flask import Flask, request, jsonify
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
dte = datetime.datetime.now()

Profile_DB = {
    "sucess": True,
    "data": {
        "last_updated": "2/7/2021, 4:32:43 PM",
        "username": "Ben Dover",
        "role": "Engineer in Training",
        "color": "red"
    }
}
Num = 0
tank_DB = []

@app.route("/")
def home():
    return "IoT LAB-2"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def profile():
    if request.method == "PATCH":
        Profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        
        tempDict = request.json
        attributes = tempDict.keys()
        
        for attribute in attributes:
            Profile_DB["data"][attribute] = tempDict[attribute]
  
        return jsonify(Profile_DB)
    if request.method == "POST":
        Profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        Profile_DB["data"]["username"] = (request.json["username"])
        Profile_DB["data"]["role"] = (request.json["role"])
        Profile_DB["data"]["color"] = (request.json["color"])
       
        return jsonify(Profile_DB)

    else:
        return jsonify(Profile_DB)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        global Num
        Num += 1     
        posts = {}
        posts["id"] = Num
        posts["location"] = (request.json["location"])
        posts["lat"] = (request.json["lat"])
        posts["long"] = (request.json["long"])
        posts["percentage_full"] = (request.json["percentage_full"])

        tank_DB.append(posts)
        return jsonify(tank_DB)

    else:
        return jsonify(tank_DB)

@app.route("/data/<int:tankID>", methods=["PATCH", "DELETE"])
def update(tankID):
     if request.method == "PATCH":
        for index in tank_DB:
            if index["id"] == tankID:
                    tempDict = request.json
                    attributes = tempDict.keys()
        
                    for attribute in attributes:
                        index[attribute] = tempDict[attribute]
        
        return jsonify(tank_DB) 

     elif request.method == "DELETE":
        for index in tank_DB:
            if index["id"] == tankID:
                tank_DB.remove(index)

        return jsonify(tank_DB)

if __name__ == '__main__':
      app.run(
     debug=True,
     port=3000,
     host="0.0.0.0"
  )