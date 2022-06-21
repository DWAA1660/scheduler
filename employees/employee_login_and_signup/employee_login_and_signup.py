from flask import Blueprint, redirect, request, flash
import pymongo
import random
client = pymongo.MongoClient("mongodb://localhost:27017/scheduler")
db = client.main
characters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

employee_login_and_signup = Blueprint("employee_login_and_signup", __name__)


@employee_login_and_signup.route("/employeesignupdata", methods=['POST'])
def employeesignupdata():
    name = request.form['name']
    phone = int(request.form['phone'])
    email = request.form['email'].lower()
    password = request.form['password']
    namesplit = name.split(" ")
    token = random.sample(characters, 20)
    token_done = "".join(token)
    id = random.sample(characters, 10)
    id_done = "".join(id)


    db.main.employee.insert_one({"name": name, "phone": phone, "email": email, "password": password, "id": id_done, "token": token_done, "employers": []})

    return redirect (f"/employeemain/{token_done}")
    
@employee_login_and_signup.route("/employeelogindata", methods=['POST'])
def employeelogindata():
    email = request.form['email'].lower()
    password = request.form['password']

    results = db.main.employee.find_one({"email": email, "password": password})
    if results is None:
        return "<h1> Credentials are invalid please try again <a href='/employeelogin'>back to login</a>"
    

    return redirect(f"/employeemain/{results['token']}")
