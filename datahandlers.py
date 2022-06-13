from lib2to3.pgen2 import token
from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/?retryWrites=true&w=majority")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

datahandlers = Blueprint("datahandlers", __name__)


    #employers
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
        return "Your credntials are invalid please try again"
    employee_id = resultsemployee["id"]
    #adds employee to employers db
    db.main.employer.update_one({"id": employersid}, {"$push": {"employees": employee_id}})
    #adds employer to employees db
    db.main.employee.update_one({"id": resultsemployee["id"]}, {"$push": {"employers": employersid}})

    return redirect(f"/employeemain/{resultsemployee['token']}")
