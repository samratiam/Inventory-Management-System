from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/store'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.product
    for i in currentCollection.find({}, {'_id': 0 }):
        holder.append(i)
    return jsonify(holder)

@app.route('/<name>', methods = ['GET'])
@cross_origin()
def retrieveFromName(name):
    currentCollection = mongo.db.product
    data = currentCollection.find_one({"name" : name},{'_id':0})
    return jsonify(data)

@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.product
    name = request.json['name']
    price = request.json['price']
    brand = request.json['brand']
    quantity = request.json['quantity']
    date = request.json['date']
    currentCollection.insert_one({'name' : name, 'price' : price, 'quantity' : quantity,'brand':brand,'date':date})
    return jsonify({'name' : name, 'price' : price, 'quantity' : quantity,'brand':brand,'date':date})

@app.route('/deleteData/<name>', methods = ['DELETE'])
def deleteData(name):
    currentCollection = mongo.db.product
    currentCollection.delete_one({'name' : name})
    return redirect(url_for('retrieveAll'))

@app.route('/update/<name>', methods = ['PUT'])
def updateData(name):
    currentCollection = mongo.db.product
    updatedName = request.json['name']
    currentCollection.update_one({'name':name}, {"$set" : {'name' : updatedName}})
    return redirect(url_for('retrieveAll'))

if __name__ == '__main__':
    app.run(debug = True)