from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

job_datahandlers = Blueprint("job_datahandlers", __name__)

# jobs
@job_datahandlers.route("/job_add_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
def job_add_employee(job_id_sent, owner_sent):
    id=request.form["Employee"]
    employee_id = db.main.employee.find_one({"id": id})

    db.main.jobs.update_one({"id": job_id_sent}, {"$push": {"employees": employee_id["id"]}})
    return redirect(f"/jobmainemployer/{job_id_sent}/{owner_sent}")

@job_datahandlers.route("/jobcreate/<token_sent>", methods=['POST'])
def jobcreate(token_sent):
    job_name = request.form["job_name"]
    id = random.sample(characters, 10)
    job_id = "".join(id)
    db.main.jobs.insert_one({"owner": token_sent, "name": job_name, "id": job_id, "employees": []})

    return redirect(f"/jobmainemployer/{job_id}/{token_sent}")
    #employers
