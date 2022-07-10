from flask import Flask, jsonify, request, redirect,render_template,session
from flask.helpers import url_for
from flask_pymongo import PyMongo
import json
import os
from bson import ObjectId
from passlib.hash import pbkdf2_sha256


template_dir = os.path.abspath('./templates/')
app = Flask(__name__,template_folder=template_dir)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/store'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

#####Inventory Products CRUD
productCollection = mongo.db.product
@app.route('/')
def index():
    products = productCollection.find()
    print("Products:",products)
    return render_template('dashboard.html',products=products)

# @app.route('/', methods = ['GET'])
# def retrieveAll():
#     holder = list()
#     productCollection = mongo.db.product
#     for i in productCollection.find({}, {'_id': 0 }):
#         holder.append(i)
#     return render_template('dashboard.html')
    
@app.route('/viewData/<oid>/', methods = ['GET'])
def viewData(oid):
    productCollection = mongo.db.product
    product = productCollection.find_one({"_id" : ObjectId(oid)})
    return render_template('view.html',product=product)

@app.route('/retrieveData/<oid>/', methods = ['GET'])
def retrieveData(oid):
    productCollection = mongo.db.product
    product = productCollection.find_one({"_id" : ObjectId(oid)})
    return render_template('update.html',product=product)

@app.route('/postData/', methods = ['POST'])
def postData(): 
    product_name = request.form.get('product_name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    brand = request.form.get('brand')
    date = request.form.get('date')

    productCollection.insert_one({'name' : product_name, 'price' : price, 'quantity' : quantity,'brand':brand,'date':date})
    return redirect(url_for('index'))

@app.route('/deleteData/<oid>/')
def deleteData(oid):
    productCollection = mongo.db.product
    productCollection.delete_one({'_id' :ObjectId(oid)})
    return redirect(url_for('index'))

@app.route('/updateData/<oid>/',methods=['GET','POST'])
def updateData(oid):
    if request.method=='POST':
        product = productCollection.find_one({'_id':ObjectId(oid)})
        updatedName = request.form.get('product_name')
    
        productCollection.update_one({"_id":ObjectId(oid)}, {"$set" : {'name' : updatedName}})
        return render_template('update.html',product=product)
    else:
        product = productCollection.find_one({'_id':ObjectId(oid)})
        return render_template('update.html',product=product)

#####User signup and login

@app.route('/signup/',methods=['GET','POST'])
def signup():
    currentCollection = mongo.db.users
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if currentCollection.find_one({ "email": email }):
            print("Email address already in use")
        elif password1 == password2:
            password = pbkdf2_sha256.hash(password1)
            user = {'fullname':fullname,'email':email,'password':password}
            currentCollection.insert_one(user)
            print("User signed up successfully")
            return redirect(url_for('index'))
    else:
        return render_template('signup.html')

###Start a session
def start_session(user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        currentCollection = mongo.db.users
        user = currentCollection.find_one({
        "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            print("User:",user)
            session['email'] = request.form.get('email')
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    else:
        return render_template('login.html')

@app.route('/signout/')
def logout():
    session.pop('email',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)