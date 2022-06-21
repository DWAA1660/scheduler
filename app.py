#employees
from employees.datahandlers.employee_datahandlers import employee_datahandlers
from employees.employee_routes import employee_routes
from employees.employee_login_and_signup.employee_login_and_signup import employee_login_and_signup
#employers
from employers.datahandlers.employer_datahandlers import employer_datahandlers
from employers.employer_signup_and_logins.employer_signup_and_login import employer_signup_and_login
from employers.employer_routes import employer_routes
#jobs
from jobs.datahandlers.job_datahandlers import job_datahandlers
from jobs.job_routes import job_routes
#global imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main

app = Flask(__name__)
#employees
app.register_blueprint(employee_routes)
app.register_blueprint(employee_datahandlers)
app.register_blueprint(employee_login_and_signup)
#employers
app.register_blueprint(employer_datahandlers)
app.register_blueprint(employer_signup_and_login)
app.register_blueprint(employer_routes)
#jobs
app.register_blueprint(job_datahandlers)

#configs
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
    app.run()

