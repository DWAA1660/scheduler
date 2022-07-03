from quart import Blueprint, render_template
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main


employer_routes = Blueprint("employer_routes", __name__)

@employer_routes.route("/manageemployee/<employer_token_sent>/<employee_id_sent>", methods=['GET'])
async def manage_employee(employer_token_sent, employee_id_sent):
    employer_results = await db.main.employer.find_one({"token": employer_token_sent})
    if employer_results is None:
        return 'Invalid credentials'
    employee_results = await db.main.employee.find_one({"id": employee_id_sent, "employers": employer_results['id']})
    if employee_results is None:
        return 'Not valid employee'
    return await render_template("/employers/manage_employee.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

@employer_routes.route("/employermain/<token>", methods=['GET'])
async def employermain(token):
    results = await db.main.employer.find_one({"token": token})
    return await render_template("/employers//employerportal.html", your_token=token, name=results["name"], your_id=results["id"], employees=results["employees"], db=db)


@employer_routes.route("/employersignup", methods=['GET'])
async def employersignup():
    return await render_template('/employers/employer_signup.html')

@employer_routes.route("/employerlogin", methods=['GET'])
async def employerlogin():
    return await render_template('/employers/employerlogin.html')
