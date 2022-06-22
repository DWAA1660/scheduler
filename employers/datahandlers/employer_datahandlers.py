from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employer_datahandlers = Blueprint("employer_datahandlers", __name__)


@employer_datahandlers.route("/quitemployer/<employer_id_sent>/<employee_token_sent>", methods=['POST'])
def quit_employer(employer_id_sent, employee_token_sent):
    print(employee_token_sent)
    employee_results = db.main.employee.find_one({"token": employee_token_sent})
    if request.form['manage_employee'] == 'Quit':
        if employee_results is None:
            return 'Your not an employee'
        employer_results = db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results["id"]})
        if employer_results is None:
            return 'employer results are invalid'
        db.main.employer.update_one({"token": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        #removes employer to employees db
        db.main.jobs.update_many({"owner": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        db.main.employee.update_one({"token": employee_token_sent}, {"$pull": {"employers": employer_results['id']}})
        return redirect(f"/employeemain/{employee_token_sent}")

@employer_datahandlers.route("/fireemployee/<employee_id_sent>/<employer_token_sent>", methods=['POST'])
def fire_employee(employee_id_sent, employer_token_sent):
    employer_results = db.main.employer.find_one({"token": employer_token_sent})
    if request.form['manage_employee'] == 'Fire':
        if employer_results is None:
            return 'employer results are invalid'
        employee_results = db.main.employee.find_one({"id": employee_id_sent, "employers": employer_results["id"]})
        if employee_results is None:
            return 'Not an employee'
        db.main.employer.update_one({"id": employer_results["id"]}, {"$pull": {"employees": employee_id_sent}})
        db.main.employee.update_one({"id": employee_id_sent}, {"$pull": {"employers": employer_results['id']}})
        db.main.jobs.update_many({"owner": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        return redirect(f"/employermain/{employer_token_sent}")
    else: 
        return 'Whoops what'


    return redirect(f"/employermain/{results['token']}")