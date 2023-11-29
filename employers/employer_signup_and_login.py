from quart import Blueprint, redirect, request, make_response, session
import motor
import motor.motor_asyncio
import hashlib
from CONFIG import *
import secrets

client = CLIENT
db = client.main


employer_signup_and_login = Blueprint("employer_signup_and_login", __name__)



@employer_signup_and_login.route("/employersignupdata", methods=['POST'])
async def employersignupdata():
    name = (await request.form)['name']
    phone = (await request.form)['phone']
    email = (await request.form) ['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()
    token = secrets.SystemRandom().sample(characters, 20)
    token_done = "".join(token)
    id = secrets.SystemRandom().sample(characters, 10)
    id_done = "".join(id)
    

    results = await db.main.employer.find_one({"email": email})
    if results is not None:
        return 'That email is already registered'
    
    await db.main.employer.insert_one({"name": name, "phone": phone, "email": email, "password": password_hashed, "token": token_done, "id": id_done, "employees": []})

    session['employer_token'] = token_done
    resp = await make_response(redirect ("/employer/portal/"))
    return resp

    

@employer_signup_and_login.route("/employerlogindata", methods=['POST'])
async def employerlogindata():
    email = (await request.form)['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()

    results = await db.main.employer.find_one({"email": email, "password": password_hashed})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employer/login'>back to login</a>"
    
    session['employer_token'] = results['token']
    resp = await make_response(redirect("/employer/portal/"))
    return resp
