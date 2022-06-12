from employees import employees
from datahandlers import datahandlers
from employers import employers
from crypt import methods
import email
from pydoc import cli
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/?retryWrites=true&w=majority")
db = client.main

app = Flask(__name__)
app.register_blueprint(employees)
app.register_blueprint(datahandlers)
app.register_blueprint(employers)
app.secret_key = 'super secret key'

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/getstarted", methods=['GET'])
def getstarted():
    return render_template('getstarted.html')


# If the file is run directly,start the app.
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(Debug=True)

