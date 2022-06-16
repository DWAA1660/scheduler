from re import template
from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main


employers = Blueprint("employers", __name__, template_folder="templates/employers")

@employers.route("/employermain/<token>", methods=['GET'])
def employermain(token):
    results = db.main.employer.find_one({"token": token})
    jobs = db.main.jobs.find({"owner": token})
    return render_template("/employerportal.html", your_token=token, name=results["name"], your_id=results["id"], employees=results["employees"], db=db)


@employers.route("/employersignup", methods=['GET'])
def employersignup():
    return render_template('employer_signup.html')

@employers.route("/employerlogin", methods=['GET'])
def employerlogin():
    return render_template('employerlogin.html')
