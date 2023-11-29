from calendar import calendar
from quart import Blueprint, redirect, request, send_file, render_template, session
from invoice import invoice
import motor
import motor.motor_asyncio
from CONFIG import *
import secrets

client = CLIENT
from datetime import timedelta
from datetime import datetime
db = client.main
from invoice import invoice

job_datahandlers = Blueprint("job_datahandlers", __name__)

# jobs
@job_datahandlers.route('/job_add_calendar/<job_id>', methods=['POST'])
async def add_calendar(job_id):
    calendarlink = (await request.form)['calendarlink']
    await db.main.jobs.update_one({"id": job_id}, {"$set": {"calendar": calendarlink}}) 
    return redirect(f'/jobmainemployer/{job_id}')

@job_datahandlers.route("/jobeditprice/<job_id>", methods=['POST'])
async def jobeditprice(job_id):
    try:
        employer_token = session['employer_token']
    except KeyError:
        return redirect('/employer/login/')
    if employer_token is None:
        return redirect("/employer/login")

    new_price = (await request.form)['newprice']
    job_results = await db.main.jobs.find_one({"id": job_id, "owner": employer_token})
    if job_results is None:
        return 'Not valid job'
    
    await db.main.jobs.update_one({"id": job_id, "owner": employer_token}, {"$set": {"price_per_hour": float(new_price)}})
    return redirect(f"/jobmainemployer/{job_id}")    

@job_datahandlers.route("/jobmakeinvoice/<job_id_sent>/<owner_sent>", methods=['POST'])
async def jobmakeinvoice(job_id_sent, owner_sent):
    job_results = await db.main.jobs.find_one({"id": job_id_sent, "owner": owner_sent})
    if job_results is None:
        return 'Not a valid job'
    amount_of_shifts = await db.main.shifts.count_documents({"job_id": job_id_sent})
    shift_results = db.main.shifts.find({"job_id": job_id_sent})

    input_start_date = (await request.form)['start_date']

    input_end_date = (await request.form)['end_date']

    await invoice(
        job_id=job_id_sent,
        job_name=job_results['name'],
        amount_of_shifts=amount_of_shifts,
        shift_results=shift_results,
        price_per_hour=job_results['price_per_hour'],
        input_start_date=input_start_date,
        input_end_date=input_end_date,
    )
    #For windows you need to use drive name [ex: F:/Example.pdf]
    return await send_file(f'static/{job_id_sent}-invoice.docx', as_attachment=True)
    



@job_datahandlers.route("/job_add_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
async def job_add_employee(job_id_sent, owner_sent):
    id=(await request.form)["Employee"]
    employee_id = await db.main.employee.find_one({"id": id})
    if employee_id is None:
        return 'Not valid employee'
    job_results = await db.main.jobs.find_one({"id": job_id_sent, "employees": employee_id["id"]})
    if job_results is None:
        await db.main.jobs.update_one({"id": job_id_sent}, {"$push": {"employees": employee_id["id"]}})
        return redirect(f"/jobmainemployer/{job_id_sent}/")
    
    return 'That person is already an employer'

@job_datahandlers.route("/job_remove_employee/<job_id_sent>/<owner_sent>", methods=['POST'])
async def job_remove_employee(job_id_sent, owner_sent):
    id=(await request.form)["Employee"]
    employee_id = await db.main.employee.find_one({"id": id})
    if employee_id is None:
        return 'Not valid employee'
    job_results = await db.main.jobs.find_one({"id": job_id_sent, "employees": employee_id["id"]})
    if job_results is not None:
        await db.main.jobs.update_one({"id": job_id_sent}, {"$pull": {"employees": employee_id["id"]}})
        return redirect(f"/jobmainemployer/{job_id_sent}/")
    
    return 'That person is not an employer'

@job_datahandlers.route("/jobcreate/", methods=['POST'])
async def jobcreate():
    try:
        employer_token = session['employer_token']
    except KeyError:
        return redirect('/employer/login')
    job_name = (await request.form) ["job_name"]
    price_per_hour = (await request.form) ["price_per_hour"]
    id = secrets.SystemRandom().sample(characters, 10)
    job_id = "".join(id)
    await db.main.jobs.insert_one({"owner": employer_token, "name": job_name, "id": job_id, "employees": [], 'price_per_hour': float(price_per_hour)})

    return redirect(f"/jobmainemployer/{job_id}/")

@job_datahandlers.route("/employee_shift_log/<employee_id_sent>/<job_id>", methods=['POST'])
async def employee_shift_log(employee_id_sent, job_id):
    data = (await request.form)
    start_time = data['start_time']
    start_date = data['start_date']
    
    result = await db.main.employee.find_one({"id": employee_id_sent})
    if result is None:
        return 'Incorrect employee'
    end_time = data['end_time']
    end_date = data['end_date']
    #start times
    start_day_stripped = start_date.split('-')[2]
    start_month_stripped = start_date.split('-')[1]
    start_year_stripped = start_date.split('-')[0]
    start_hour_stripped = start_time.split(':')[0]
    start_minute_stripped = start_time.split(':')[1]

    start_inputted_var = f"{start_year_stripped}-{start_month_stripped}-{start_day_stripped}-{start_hour_stripped}:{start_minute_stripped}"

    start_time_total = datetime.strptime(start_inputted_var, '%Y-%m-%d-%H:%M')


    end_day_stripped = end_date.split('-')[2]
    end_month_stripped = end_date.split('-')[1]
    end_year_stripped = end_date.split('-')[0]
    end_hour_stripped = end_time.split(':')[0]
    end_minute_stripped = end_time.split(':')[1]

    end_inputted_var = f"{end_year_stripped}-{end_month_stripped}-{end_day_stripped}-{end_hour_stripped}:{end_minute_stripped}"

    end_time_total = datetime.strptime(end_inputted_var, '%Y-%m-%d-%H:%M')

    totaltime = end_time_total - start_time_total

    minutes = totaltime.total_seconds() / 60
    hours = minutes // 60
    minutes_remainder = minutes % 60
    if end_time_total < start_time_total:
        return await render_template('errors/incorrect_time.html', job_id=job_id) 
        
    db.main.shifts.insert_one({"employee": employee_id_sent, "start_date": start_date, "end_date": end_date, "start_time": start_time, "end_time": end_time, "job_id": job_id, "total_time": f"{int(hours)}:{int(minutes_remainder)}"})
    return redirect(f"/employee_job_portal/{job_id}")

'''"start_date": "2022-06-28",
  "end_date": "2022-06-28",
  "start_time": "15:12",
  "end_time": "15:44",'''
