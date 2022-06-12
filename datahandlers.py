from flask import Blueprint, redirect, request
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
    namesplit = name.split(" ")

    uniqieid = random.sample(characters, 20)
    uniqieiddone = "".join(uniqieid)
    

    db.main.employer.insert_one({"name": name, "phone": phone, "email": email, "password": password, "uniqueid": uniqieiddone, "employees": []})

    return redirect ("/getstarted")
    

@datahandlers.route("/employerlogindata", methods=['POST'])
def employerlogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employer.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employerlogin'>back to login</a>"
    

    return redirect(f"/employermain/{results['uniqueid']}")

#employees

@datahandlers.route("/employeesignupdata", methods=['POST'])
def employeesignupdata():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email'].lower()
    password = request.form['password']
    namesplit = name.split(" ")
    uniqieid = random.sample(characters, 20)
    uniqieiddone = "".join(uniqieid)

    db.main.employee.insert_one({"name": name, "phone": phone, "email": email, "password": password, "uniqueid": uniqieiddone})

    return redirect ("/getstarted")
    
@datahandlers.route("/employeelogindata", methods=['POST'])
def employeelogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employee.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employeelogin'>back to login</a>"
    

    return redirect(f"/employeemain/{results['uniqueid']}")

@datahandlers.route("/addemployer", methods=['POST'])
def addemployer():
    employersid = request.form["employers_id"]
    results = db.main.employer.find_one({"uniqueid": employersid})
    if results == None:
        return "Invalid id please try again"
    db.main.employer.updateOne({"uniqueid": employersid}, {"$push": {"employers": employee_id}})
