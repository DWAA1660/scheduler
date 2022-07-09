from quart import Blueprint, redirect, request
import motor
import random
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employee_datahandlers = Blueprint("employee_datahandlers", __name__)


@employee_datahandlers.route("/addemployer/<token_sent>", methods=['POST'])
async def addemployer(token_sent):
    #rest of stuff
    employersid = (await request.form) ["employers_id"]
    results = await db.main.employer.find_one({"id": employersid})
    resultsemployee = await db.main.employee.find_one({"token": token_sent})
    if results == None:
        return "Invalid id please try again"
    if resultsemployee == None:
        return "Your credentials are invalid please try again"
    employee_id = resultsemployee["id"]
    #adds employee to employers db
    await db.main.employer.update_one({"id": employersid}, {"$push": {"employees": employee_id}})
    #adds employer to employees db
    await db.main.employee.update_one({"id": resultsemployee["id"]}, {"$push": {"employers": employersid}})

    return redirect(f"/employeemain/{resultsemployee['token']}")
