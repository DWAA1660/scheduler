from quart import Blueprint, render_template, request, redirect
import motor
import motor.motor_asyncio
from CONFIG import *
import time
client = CLIENT
db = client.main


employer_routes = Blueprint("employer_routes", __name__)


@employer_routes.route("/manageemployee/<employee_id_sent>", methods=['GET'])
async def manage_employee(employee_id_sent):
    # cookie stuff
    token_cookie = request.cookies.get('employer_token')
    cookie_results = await db.main.employer.find_one({'token': token_cookie})

    if cookie_results is None:
        return redirect('/employerlogin')
    # done with cookies
    employee_results = await db.main.employee.find_one({"id": employee_id_sent, "employers": cookie_results['id']})
    if employee_results is None:
        return 'Not valid employee'
    return await render_template("/employers/manage_employee.html", employee_results_sent=employee_results, employer_results_sent=cookie_results)


@employer_routes.route("/employer/main/", methods=['GET'])
async def employermain():
    # cookie stuff
    cookie_token = request.cookies.get('employer_token')
    results = await db.main.employer.find_one({"token": cookie_token})
    if cookie_token is None or results is None:
        return redirect('/employerlogin')
    return await render_template("/employers//employerportal.html", your_token=cookie_token, name=results["name"], your_id=results["id"], employees=results["employees"], db=db)


@employer_routes.route("/employer/signup", methods=['GET'])
async def employersignup():
    return await render_template('/employers/employer_signup.html')


@employer_routes.route("/employerlogin", methods=['GET'])
async def employerlogin():
    return await render_template('/employers/employerlogin.html')
