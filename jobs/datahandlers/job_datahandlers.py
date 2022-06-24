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
