from flask import Flask, jsonify, request, redirect,render_template
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json
from user.routes import *
import os
# from user import routes

template_dir = os.path.abspath('./templates/')
app = Flask(__name__,template_folder=template_dir)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/store'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)
productCollection = mongo.db.product

@app.route('/dashboard')
def index():
    products = productCollection.find()
    print("Products:",products)
    return render_template('dashboard.html',products=products)

@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    productCollection = mongo.db.product
    for i in productCollection.find({}, {'_id': 0 }):
        holder.append(i)
    

@app.route('/<name>/', methods = ['GET'])
@cross_origin()
def retrieveFromName(name):
    productCollection = mongo.db.product
    data = productCollection.find_one({"name" : name},{'_id':0})
    return jsonify(data)

@app.route('/postData/', methods = ['POST'])
def postData():
    # name = request.json['name']
    # price = request.json['price']
    # brand = request.json['brand']
    # quantity = request.json['quantity']
    # date = request.json['date']
    
    product_name = request.form.get('product_name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    brand = request.form.get('brand')
    date = request.form.get('date')
    

    productCollection.insert_one({'name' : product_name, 'price' : price, 'quantity' : quantity,'brand':brand,'date':date})
    # return jsonify({'name' : name, 'price' : price, 'quantity' : quantity,'brand':brand,'date':date})
    return redirect(url_for('index'))

@app.route('/deleteData/<name>/')
def deleteData(name):
    productCollection = mongo.db.product
    productCollection.delete_one({'name' :name})
    return redirect(url_for('index'))

# @app.route('/update/<oid>/', methods = ['PUT'])
# def updateData(oid):
#     productCollection = mongo.db.product
#     productName = productCollection.find_one({'oid':})
#     updatedName = request.form.get('product_name')
#     productCollection.update_one({'oid':oid}, {"$set" : {'name' : updatedName}})
#     return redirect(url_for('index'))
    # return redirect(url_for('retrieveAll'))


if __name__ == '__main__':
    app.run(debug = True)