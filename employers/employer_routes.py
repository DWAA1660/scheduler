from quart import Blueprint, render_template, request, redirect, session
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
    try:  
        token_cookie = session['employer_token']
    except KeyError:
        return redirect('/employer/login')

    if (cookie_results := await db.main.employer.find_one({'token': token_cookie})) is None:
        return redirect('/employer/login/')
    # done with cookies

    if (employee_results := await db.main.employee.find_one(
        {"id": employee_id_sent, "employers": cookie_results['id']}
        )) is None:
        return 'Not valid employee'
    return await render_template(
        "/employers/manage_employee.html",
        employee_results_sent=employee_results,
        employer_results_sent=cookie_results
        )


@employer_routes.route("/employer/portal/", methods=['GET'])
async def employermain():
    # cookie stuff
    try: 
        cookie_token = session['employer_token']
    except KeyError:
        return redirect('/employer/login')
    employer_id = await db.main.employer.find_one({"token": cookie_token})
    employees = db.main.employee.find({"employers": employer_id['id']})
    if cookie_token is None or employer_id is None:
        return redirect('/employer/login')
    return await render_template(
        "/employers//employerportal.html",
        your_token=cookie_token,
        name=employer_id["name"],
        your_id=employer_id["id"],
        employees=employees,
        db=db
        )


@employer_routes.route("/employer/signup/", methods=['GET'])
async def employersignup():
    return await render_template('/employers/employer_signup.html')


@employer_routes.route("/employer/login/", methods=['GET'])
async def employerlogin():
    return await render_template('/employers/employerlogin.html')
