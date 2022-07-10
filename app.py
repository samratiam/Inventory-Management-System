from flask import Flask, jsonify, request, redirect,render_template,session,flash
from flask.helpers import url_for
from flask_pymongo import PyMongo
import json
import os
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

template_dir = os.path.abspath('./templates/')
STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__,template_folder=template_dir,static_folder=STATIC_DIR)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/store'

mongo = PyMongo(app)

from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

#####Inventory Products CRUD
productCollection = mongo.db.product
@app.route('/')
@login_required
def index():
    products = productCollection.find()
    return render_template('dashboard.html',products=products)
    
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
    
@app.route('/search/',methods=['POST'])
def search():
    if request.method=='POST':
        keyword = request.form.get('keyword')
        products = productCollection.find({ 'name':keyword })
        return render_template('search.html',products=products)

#####User signup and login

@app.route('/signup/',methods=['GET','POST'])
def signup():
    userCollection = mongo.db.users
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if userCollection.find_one({ "email": email }):
            flash("Email address already is in use")
            return redirect(url_for('signup'))
        elif password1 == password2:
            password = pbkdf2_sha256.hash(password1)
            user = {'fullname':fullname,'email':email,'password':password}
            userCollection.insert_one(user)
            flash("User account created successfully")
            return redirect(url_for('login'))
        elif password1 != password2:
            flash("Password didn't match")
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        userCollection = mongo.db.users
        user = userCollection.find_one({
        "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            session['email'] = request.form.get('email')
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    else:
        return render_template('login.html')

@app.route('/signout/')
def logout():
    session.pop('email',None)
    session.pop('logged_in',False)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)