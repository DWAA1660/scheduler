from quart import Blueprint, redirect, request, flash
import motor
import random
import motor.motor_asyncio
import hashlib
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/scheduler")
db = client.main

characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employer_signup_and_login = Blueprint("employer_signup_and_login", __name__)



@employer_signup_and_login.route("/employersignupdata", methods=['POST'])
async def employersignupdata():
    name = (await request.form)['name']
    phone = (await request.form)['phone']
    email = (await request.form) ['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()
    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)
    

    results = await db.main.employer.find_one({"email": email})
    print(results)
    if results is not None:
        return 'That email is already registered'
    
    await db.main.employer.insert_one({"name": name, "phone": phone, "email": email, "password": password_hashed, "token": token_done, "id": id_done, "employees": []})

    return redirect (f"/employermain/{token_done}")
    

@employer_signup_and_login.route("/employerlogindata", methods=['POST'])
async def employerlogindata():
    email = (await request.form)['email'].lower()
    password = (await request.form) ['password'].encode('utf-8')
    password_hashed = hashlib.sha256(password).hexdigest()

    results = await db.main.employer.find_one({"email": email, "password": password_hashed})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employerlogin'>back to login</a>"
    

    return redirect(f"/employermain/{results['token']}")