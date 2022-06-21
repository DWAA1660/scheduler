from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employer_signup_and_login = Blueprint("employer_signup_and_login", __name__)



@employer_signup_and_login.route("/employersignupdata", methods=['POST'])
def employersignupdata():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email'].lower()
    password = request.form['password']

    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)
        
    db.main.employer.insert_one({"name": name, "phone": phone, "email": email, "password": password, "token": token_done, "id": id_done, "employees": []})

    return redirect (f"/employermain/{token_done}")
    

@employer_signup_and_login.route("/employerlogindata", methods=['POST'])
def employerlogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employer.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employerlogin'>back to login</a>"
    

    return redirect(f"/employermain/{results['token']}")