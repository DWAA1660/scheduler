from quart import Blueprint, redirect, request, make_response, session
import motor
import random
import motor.motor_asyncio
import hashlib
from CONFIG import *
client = CLIENT
db = client.main

employee_login_and_signup = Blueprint("employee_login_and_signup", __name__)


@employee_login_and_signup.route("/employeesignupdata", methods=['POST'])
async def employeesignupdata():
    name = (await request.form) ['name']
    phone = (await request.form) ['phone']
    email = (await request.form)['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()
    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)

    results = await db.main.employee.find_one({"email": email})
    if results is not None:
        return 'That email is already registered'

    await db.main.employee.insert_one({"name": name, "phone": phone, "email": email, "password": password_hashed, "id": id_done, "token": token_done, "employers": []})
    session['employee_token'] = token_done
    resp = await make_response(redirect (f"/employee/portal/"))
    return resp
    
@employee_login_and_signup.route("/employeelogindata", methods=['POST'])
async def employeelogindata():
    email = (await request.form) ['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()


    results = await db.main.employee.find_one({"email": email, "password": password_hashed})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employee/login'>back to login</a>"
    session['employee_token'] = results['token']
    resp = await make_response(redirect(f"/employee/portal/"))
    return resp
