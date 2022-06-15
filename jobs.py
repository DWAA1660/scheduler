from crypt import methods
from flask import Blueprint, render_template
import pymongo
client = pymongo.MongoClient("mongodb+srv://DWAA:Pinta123@kimshomecarec.el8me5e.mongodb.net/")
db = client.main


jobs = Blueprint("jobs", __name__, template_folder="templates/jobs")

@jobs.route("/jobmainemployer/<job_id>/<employer>", methods=['GET'])
def jobmain(job_id, employer):
    results = db.main.jobs.find_one({"id": job_id})
    employer_results = db.main.employers.find_one({"token": employer})
    employees = results["employees"]

    if results is None:
        return 'Not a valid job'
    if employer_results is None:
        return 'Not a valid employer of this job'

    return render_template("job_main.html", results=results, employees=employees, db=db, )