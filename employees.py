from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main


employees = Blueprint("employees", __name__, template_folder="templates/employees")

@employees.route("/manageemployee/<employee_token_sent>/<employer_id_sent>", methods=['GET'])
def manage_employee(employee_token_sent, employer_id_sent):
    employee_results = db.main.employee.find_one({"token": employee_token_sent})
    if employee_results is None:
        return 'Invalid credentials'
    employer_results = db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results['id']})
    if employer_results is None:
        return 'Your not an employee'
    return render_template("manage_employer.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

@employees.route("/employeesignup", methods=['GET'])
def employeesignup():
    return render_template("employee_signup.html")

@employees.route("/employeelogin", methods=['GET'])
def employeelogin():
    return render_template('employeelogin.html')

@employees.route("/employeemain/<token>", methods=['GET'])
def employeemain(token):
    results = db.main.employee.find_one({"token": token})
    
    return render_template("employeeportal.html", name=results["name"], employers=results["employers"], db=db, your_token=token)

