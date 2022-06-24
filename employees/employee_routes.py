from quart import Blueprint, render_template
import motor
import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")
db = client.main


employee_routes = Blueprint("employee_routes", __name__)

@employee_routes.route("/manageemployer/<employee_token_sent>/<employer_id_sent>", methods=['GET'])
async def manage_employee(employee_token_sent, employer_id_sent):
    employee_results = await db.main.employee.find_one({"token": employee_token_sent})
    if employee_results is None:
        return 'Invalid credentials'
    employer_results = await db.main.employer.find_one({"id": employer_id_sent, "employees": employee_results['id']})
    if employer_results is None:
        return 'Your not an employee'
    return await render_template("/employees/manage_employer.html", employee_results_sent=employee_results, employer_results_sent=employer_results)

@employee_routes.route("/employees/employeesignup", methods=['GET'])
async def employeesignup():
    return await render_template("/employees/employee_signup.html")

@employee_routes.route("/employeelogin", methods=['GET'])
async def employeelogin():
    return await render_template('/employees/employeelogin.html')

@employee_routes.route("/employeemain/<token>", methods=['GET'])
async def employeemain(token):
    results = await db.main.employee.find_one({"token": token})
    return await render_template("/employees/employeeportal.html", name=results["name"], employers=results["employers"], your_id=results["id"], db=db, your_token=token)

