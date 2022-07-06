from flask import Flask
from app import app
from user.models import User


from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import json


@app.route('/u/signup/', methods=['POST'])
def signup():
  return User.signup()

@app.route('/user/signout/')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()