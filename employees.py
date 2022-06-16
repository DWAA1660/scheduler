from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main


employees = Blueprint("employees", __name__, template_folder="templates/employees")

@employees.route("/employeesignup", methods=['GET'])
def employeesignup():
    return render_template("employee_signup.html")

@employees.route("/employeelogin", methods=['GET'])
def employeelogin():
    return render_template('employeelogin.html')

@employees.route("/employeemain/<token>", methods=['GET'])
def employeemain(token):
    results = db.main.employee.find_one({"token": token})
    
    return render_template("employeeportal.html", name=results["name"], employers=results["employers"], db=db, token=token)

