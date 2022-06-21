from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employee_datahandlers = Blueprint("employee_datahandlers", __name__)


@employee_datahandlers.route("/addemployer/<token_sent>", methods=['POST'])
def addemployer(token_sent):
    employersid = request.form["employers_id"]
    results = db.main.employer.find_one({"id": employersid})
    resultsemployee = db.main.employee.find_one({"token": token_sent})
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
