from quart import Blueprint, render_template, request, redirect, session
import motor
import motor.motor_asyncio
from CONFIG import *
client = CLIENT
db = client.main


job_routes = Blueprint("job_routes", __name__)

@job_routes.route("/jobmainemployer/<job_id_sent>/", methods=['GET'])
async def jobmain(job_id_sent):
    try:
        employer_token = session['employer_token']
    except KeyError:
        return redirect('/employer/login')
    if (results := await db.main.jobs.find_one({"id": job_id_sent})) is None:
        return 'Not a valid job'

    employer_results = await db.main.employer.find_one({"token": employer_token})
    employees = results["employees"]
    if employer_results is None:
        return 'Not a valid employer of this job'
    try:
        shared_url=results['calendar']
    except KeyError:
        shared_url=None
    return await render_template("/jobs/job_main.html",
                        job_employees=employees, 
                        results=results,
                        db=db,
                        owner_id=employer_results["id"],
                        owner_token=employer_results["token"],
                        owner=employer_results["name"],
                        employer_employees=employer_results["employees"],
                        job_id = results["id"],
                        price_per_hour=results["price_per_hour"],
                        shared_url=shared_url,
                        )
