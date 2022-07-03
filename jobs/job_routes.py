from quart import Blueprint, render_template
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main


job_routes = Blueprint("job_routes", __name__)

@job_routes.route("/jobmainemployer/<job_id_sent>/<employer_token_sent>", methods=['GET'])
async def jobmain(job_id_sent, employer_token_sent):
    results = await db.main.jobs.find_one({"id": job_id_sent})
    if results is None:
        return 'Not a valid job'

    employer_results = await db.main.employer.find_one({"token": employer_token_sent})
    employees = results["employees"]
    if employer_results is None:
        return 'Not a valid employer of this job'

    return await render_template("/jobs/job_main.html", job_employees=employees, 
                        results=results,
                        db=db, owner_id=employer_results["id"],
                        owner_token=employer_results["token"], owner=employer_results["name"],
                        employer_employees=employer_results["employees"],
                        job_id = results["id"])