from quart import Blueprint, render_template, request, redirect
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main


employee_routes = Blueprint("employee_routes", __name__)

@employee_routes.route("/manageemployer/<employer_id_sent>", methods=['GET'])
async def manage_employee(employer_id_sent):
    employee_token_sent = request.cookies.get('employee_token')

    employee_results = await db.main.employee.find_one({"token": employee_token_sent})
    if employee_results is None:
        return 'Invalid credentials'
    employer_results = await db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results['id']})
    if employer_results is None:
        return 'Your not an employee'
    return await render_template("/employees/manage_employer.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

@employee_routes.route("/employees/signup", methods=['GET'])
async def employeesignup():
    return await render_template("/employees/employee_signup.html")

@employee_routes.route("/employee/login", methods=['GET'])
async def employeelogin():
    return await render_template('/employees/employeelogin.html')

@employee_routes.route("/employee/portal/", methods=['GET'])
async def employeemain():
    #cookie stuff
    token_cookie = request.cookies.get('employee_token')
    cookie_results = await db.main.employee.find_one({"token": token_cookie})
    if cookie_results is None:
        return redirect("/employeelogin")

    # rest of stuff
    results = await db.main.employee.find_one({"token": token_cookie})
    job_results = db.main.jobs.find({"employees": results['id']})
    return await render_template("/employees/employeeportal.html",
    name=results["name"],
    employers=results["employers"],
    your_id=results["id"],
    db=db,
    your_token=token_cookie,
    jobs=job_results
    )

@employee_routes.route("/employee_job_portal/<job_id>/", methods=['GET'])
async def employee_job_portal(job_id):
    employee_token = request.cookies.get("employee_token")
    employee_results = await db.main.employee.find_one({"token": employee_token})
    if employee_results is None:
        return redirect("/employeelogin")
    job_results = await db.main.jobs.find_one({"id": job_id, "employees": employee_results['id']})
    if job_results is None:
        return 'Not a valid job'
    return await render_template("/employees/employee_job_portal.html",
    job_name=job_results['name'],
    employees=job_results['employees'],
    db=db,
    my_token=employee_token,
    job_id=job_id,
    )
