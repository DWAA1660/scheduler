from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main


employers = Blueprint("employers", __name__, template_folder="templates/employers")

@employers.route("/manageemployee/<employer_token_sent>/<employee_id_sent>", methods=['GET'])
def manage_employee(employer_token_sent, employee_id_sent):
    employer_results = db.main.employer.find_one({"token": employer_token_sent})
    employee_results = db.main.employee.find_one({"id": employee_id_sent, "employers": employer_results['id']})
    if employer_results is None:
        return 'Invalid credentials'
    if employee_results is None:
        return 'Not valid employee'
    return render_template("manage_employee.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

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
