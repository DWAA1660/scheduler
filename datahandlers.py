from unicodedata import name
from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

datahandlers = Blueprint("datahandlers", __name__)

# jobs
@datahandlers.route("/job_add_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
def job_add_employee(job_id_sent, owner_sent):
    id=request.form["Employee"]
    employee_id = db.main.employee.find_one({"id": id})
    print(owner_sent)
    print(employee_id)

    db.main.jobs.update_one({"id": job_id_sent}, {"$push": {"employees": employee_id["id"]}})
    return redirect(f"/jobmainemployer/{job_id_sent}/{owner_sent}")

@datahandlers.route("/jobcreate/<token_sent>", methods=['POST'])
def jobcreate(token_sent):
    job_name = request.form["job_name"]
    id = random.sample(characters, 10)
    job_id = "".join(id)
    db.main.jobs.insert_one({"owner": token_sent, "name": job_name, "id": job_id, "employees": []})

    return redirect(f"/jobmainemployer/{job_id}/{token_sent}")
    #employers

@datahandlers.route("/fireemployee/<employee_id_sent>/<employer_token_sent>", methods=['POST'])
def fire_employee(employee_id_sent, employer_token_sent):
    employer_results = db.main.employer.find_one({"token": employer_token_sent})
    if request.form['manage_employee'] == 'Fire':
        if employer_results is None:
            return 'employer results are invalid'
        employee_results = db.main.employee.find_one({"id": employee_id_sent, "employers": employer_results["id"]})
        if employee_results is None:
            return 'Not an employee'
        db.main.employer.update_one({"id": employer_results["id"]}, {"$pull": {"employees": employee_id_sent}})
        #adds employer to employees db
        db.main.employee.update_one({"id": employee_id_sent}, {"$pull": {"employers": employer_results['id']}})
        return redirect(f"/employermain/{employer_token_sent}")

@datahandlers.route("/employersignupdata", methods=['POST'])
def employersignupdata():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email'].lower()
    password = request.form['password']

    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)
        
    db.main.employer.insert_one({"name": name, "phone": phone, "email": email, "password": password, "token": token_done, "id": id_done, "employees": []})

    return redirect (f"/employermain/{token_done}")
    

@datahandlers.route("/employerlogindata", methods=['POST'])
def employerlogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employer.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employerlogin'>back to login</a>"
    

    return redirect(f"/employermain/{results['token']}")

#employees

@datahandlers.route("/employeesignupdata", methods=['POST'])
def employeesignupdata():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email'].lower()
    password = request.form['password']
    namesplit = name.split(" ")
    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)


    db.main.employee.insert_one({"name": name, "phone": phone, "email": email, "password": password, "id": id_done, "token": token_done, "employers": []})

    return redirect (f"/employeemain/{token_done}")
    
@datahandlers.route("/employeelogindata", methods=['POST'])
def employeelogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employee.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employeelogin'>back to login</a>"
    

    return redirect(f"/employeemain/{results['token']}")

@datahandlers.route("/addemployer/<token>", methods=['POST'])
def addemployer(token):
    employersid = request.form["employers_id"]
    results = db.main.employer.find_one({"id": employersid})
    resultsemployee = db.main.employee.find_one({"token": token})
    if results == None:
        return "Invalid id please try again"
    if resultsemployee == None:
        return "Your credentials are invalid please try again"
    employee_id = resultsemployee["id"]
    #adds employee to employers db
    db.main.employer.update_one({"id": employersid}, {"$push": {"employees": employee_id}})
    #adds employer to employees db
    db.main.employee.update_one({"id": resultsemployee["id"]}, {"$push": {"employers": employersid}})

    return redirect(f"/employeemain/{resultsemployee['token']}")
