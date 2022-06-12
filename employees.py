from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/?retryWrites=true&w=majority")
db = client.main


employees = Blueprint("employees", __name__, template_folder="templates/employees")

@employees.route("/employeesignup", methods=['GET'])
def employeesignup():
    return render_template("employee_signup.html")

@employees.route("/employeelogin", methods=['GET'])
def employeelogin():
    return render_template('employeelogin.html')

@employees.route("/employeemain/<id>", methods=['GET'])
def employeemain(id):
    results = db.main.employee.find_one({"uniqueid": id})
    return render_template("employers/employerportal.html", name=results["name"], employee_id=results["uniqieiddone"])

