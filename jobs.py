from crypt import methods
from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/")
db = client.main


jobs = Blueprint("jobs", __name__, template_folder="templates/jobs")

@jobs.route("/jobmainemployer/<job_id_sent>/<employer>", methods=['GET'])
def jobmain(job_id_sent, employer):
    results = db.main.jobs.find_one({"id": job_id_sent})
    if results is None:
        return 'Not a valid job'

    employer_results = db.main.employer.find_one({"token": employer})
    employees = results["employees"]
    if employer_results is None:
        return 'Not a valid employer of this job'

    return render_template("job_main.html", job_employees=employees, results=results, db=db, owner_id=employer_results["id"], owner_token=employer_results["token"], owner=employer_results["name"], employer_employees=employer_results["employees"], job_id = results["id"])