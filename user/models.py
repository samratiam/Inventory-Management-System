from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import uuid

from app import app

# cors = CORS(app)
# app.config['MONGO_URI'] = 'mongocurrentCollection://localhost:27017/store'
# app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

currentCollection = mongo.db.users

class User:

  # def start_session(self, user):
  #   del user['password']
  #   session['logged_in'] = True
  #   session['user'] = user
  #   return jsonify(user), 200

  def signup(self):
    # print(request.form)
    print("Database:",currentCollection)
    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.json['name'],
      "email": request.json['email'],
      "password": request.json['password']
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])
    print("USer:",user)

    # Check for existing email address
    if currentCollection.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if currentCollection.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = currentCollection.find_one({
      "email": request.json('email')
    })

    if user and pbkdf2_sha256.verify(request.json['password'], user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401