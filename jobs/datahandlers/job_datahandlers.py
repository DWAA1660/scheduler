import re
from tracemalloc import start
from unittest import result
from quart import Blueprint, redirect, request, flash
import motor
import random
import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

job_datahandlers = Blueprint("job_datahandlers", __name__)

# jobs
@job_datahandlers.route("/job_add_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
async def job_add_employee(job_id_sent, owner_sent):
    id=(await request.form)["Employee"]
    employee_id = await db.main.employee.find_one({"id": id})
    if employee_id is None:
        return 'Not valid employee'
    job_results = await db.main.jobs.find_one({"id": job_id_sent, "employees": employee_id["id"]})
    if job_results is None:
        await db.main.jobs.update_one({"id": job_id_sent}, {"$push": {"employees": employee_id["id"]}})
        return redirect(f"/jobmainemployer/{job_id_sent}/{owner_sent}")
    
    return 'That person is already an employer'

@job_datahandlers.route("/job_remove_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
async def job_remove_employee(job_id_sent, owner_sent):
    id=(await request.form)["Employee"]
    employee_id = await db.main.employee.find_one({"id": id})
    if employee_id is None:
        return 'Not valid employee'
    job_results = await db.main.jobs.find_one({"id": job_id_sent, "employees": employee_id["id"]})
    if job_results is not None:
        await db.main.jobs.update_one({"id": job_id_sent}, {"$pull": {"employees": employee_id["id"]}})
        return redirect(f"/jobmainemployer/{job_id_sent}/{owner_sent}")
    
    return 'That person is not an employer'

@job_datahandlers.route("/jobcreate/<token_sent>", methods=['POST'])
async def jobcreate(token_sent):
    job_name = (await request.form) ["job_name"]
    id = random.sample(characters, 10)
    job_id = "".join(id)
    await db.main.jobs.insert_one({"owner": token_sent, "name": job_name, "id": job_id, "employees": []})

    return redirect(f"/jobmainemployer/{job_id}/{token_sent}")

@job_datahandlers.route("/employee_shift_log/<employee_id_sent>/<job_id>", methods=['POST'])
async def employee_shift_log(employee_id_sent, job_id):
    data = (await request.form)
    start_time = data['start_time']
    start_date = data['start_date']
    result = await db.main.employee.find_one({"id": employee_id_sent})
    if result is None:
        return 'Incorrect employee'
    end_time = data['end_time']
    end_date = data['end_date']
    end_time_hour = data['end_time'].split(':')[0]
    end_time_minute = data['end_time'].split(':')[1]
    start_time_hour = data['start_time'].split(':')[0]
    start_time_minute = data['start_time'].split(':')[1]
        
    if data['end_date'].split('-')[2] > data['start_date'].split('-')[2] or data['end_date'].split('-')[1] > data['start_date'].split('-')[1]:
        end_time_hour = int(end_time_hour) + 24

    total_hours = int(end_time_hour) - int(start_time_hour)

    total_minutes = int(end_time_minute) - int(start_time_minute)


    db.main.shifts.insert_one({"employee": employee_id_sent, "start_date": start_date, "end_date": end_date, "start_time": start_time, "end_time": end_time, "job_id": job_id, "total_hours": total_hours, "total_minutes": total_minutes})
    return redirect(f"/employee_job_portal/{job_id}/{result['token']}")

