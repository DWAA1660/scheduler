from re import template
from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/?retryWrites=true&w=majority")
db = client.main


employers = Blueprint("employers", __name__, template_folder="templates/employers")

@employers.route("/employermain/<token>", methods=['GET'])
def employermain(token):
    results = db.main.employer.find_one({"token": token})
    return render_template("/employerportal.html", name=results["name"], your_id=results["id"], employees=results["employees"], db=db)


@employers.route("/employersignup", methods=['GET'])
def employersignup():
    return render_template('employer_signup.html')

@employers.route("/employerlogin", methods=['GET'])
def employerlogin():
    return render_template('employerlogin.html')
