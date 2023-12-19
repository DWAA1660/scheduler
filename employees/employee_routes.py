from quart import Blueprint, render_template, request, redirect, session
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main


employee_routes = Blueprint("employee_routes", __name__)

@employee_routes.route("/manageemployer/<employer_id_sent>", methods=['GET'])
async def manage_employee(employer_id_sent):
    try:
        employee_token_sent = session['employee_token']
    except KeyError:
        return redirect('/employee/login')
    if (employee_results := await db.main.employee.find_one({"token": employee_token_sent})) is None:
        return 'Invalid credentials'
    if (employer_results := await db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results['id']})) is None:
        return 'Your not an employee'
    return await render_template("/employees/manage_employer.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

@employee_routes.route("/employee/signup/", methods=['GET'])
async def employeesignup():
    return await render_template("/employees/employee_signup.html")

@employee_routes.route("/employee/login/", methods=['GET'])
async def employeelogin():
    return await render_template('/employees/employeelogin.html')

@employee_routes.route("/employee/portal/", methods=['GET'])
async def employeemain():
    #cookie stuff
    try:
        token_cookie = session['employee_token']
    except KeyError:
        return redirect('/employee/login')
    if (cookie_results := await db.main.employee.find_one({"token": token_cookie})) is None:
        return redirect("/employee/login")

    # rest of stuff
    employers = db.main.employer.find({"employees": cookie_results['id']})
    results = await db.main.employee.find_one({"token": token_cookie})
    job_results = db.main.jobs.find({"employees": results['id']})
    return await render_template("/employees/employeeportal.html",
    name=results["name"],
    employers=employers,
    your_id=results["id"],
    db=db,
    your_token=token_cookie,
    jobs=job_results
    )

@employee_routes.route("/employee_job_portal/<job_id>/", methods=['GET'])
async def employee_job_portal(job_id):
    try:
        employee_token = session['employee_token']
    except KeyError:
        return redirect('/employee/login')
    if (employee_results := await db.main.employee.find_one({"token": employee_token})) is None:
        return redirect("/employeelogin")
    if (job_results := await db.main.jobs.find_one({"id": job_id, "employees": employee_results['id']})) is None:
        return 'Not a valid job'
    return await render_template("/employees/employee_job_portal.html",
    job_name=job_results['name'],
    employees=job_results['employees'],
    db=db,
    my_token=employee_token,
    job_id=job_id,
    )
