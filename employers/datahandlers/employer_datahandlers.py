from quart import Blueprint, redirect, request, make_response
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employer_datahandlers = Blueprint("employer_datahandlers", __name__)


@employer_datahandlers.route("/quitemployer/<employer_id_sent>/<employee_token_sent>", methods=['POST'])
async def quit_employer(employer_id_sent, employee_token_sent):
    employee_results = await db.main.employee.find_one({"token": employee_token_sent})
    if (await request.form) ['manage_employee'] == 'Quit':
        if employee_results is None:
            return 'Your not an employee'
        employer_results = await db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results["id"]})
        if employer_results is None:
            return 'employer results are invalid'
        await db.main.employer.update_one({"token": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        #removes employer to employees db
        await db.main.jobs.update_many({"owner": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        await db.main.employee.update_one({"token": employee_token_sent}, {"$pull": {"employers": employer_results['id']}})
        return redirect(f"/employee/portal/")

@employer_datahandlers.route("/fireemployee/<employee_id_sent>/<employer_token_sent>", methods=['POST'])
async def fire_employee(employee_id_sent, employer_token_sent):
    employer_results = await db.main.employer.find_one({"token": employer_token_sent})
    if (await request.form)['manage_employee'] == 'Fire':
        if employer_results is None:
            return 'employer results are invalid'
        employee_results = await db.main.employee.find_one({"id": employee_id_sent, "employers": employer_results["id"]})
        if employee_results is None:
            return 'Not an employee'
        await db.main.employer.update_one({"id": employer_results["id"]}, {"$pull": {"employees": employee_id_sent}})
        await db.main.employee.update_one({"id": employee_id_sent}, {"$pull": {"employers": employer_results['id']}})
        await db.main.jobs.update_many({"owner": employer_results["token"]}, {"$pull": {"employees": employee_results["id"]}})
        return redirect(f"/employer/portal/")
    else: 
        return 'Whoops what'

@employer_datahandlers.route('/employer/logout/', methods=['POST', 'GET'])
async def employerlogout():
    resp = await make_response(redirect (f"/employer/login/"))
    resp.set_cookie('employer_token', '', expires=0)
    return resp