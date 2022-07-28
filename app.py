#employees
from employees.datahandlers.employee_datahandlers import employee_datahandlers
from employees.employee_routes import employee_routes
from employees.employee_login_and_signup import employee_login_and_signup
#employers
from employers.datahandlers.employer_datahandlers import employer_datahandlers
from employers.employer_signup_and_login import employer_signup_and_login
from employers.employer_routes import employer_routes
#jobs
from jobs.datahandlers.job_datahandlers import job_datahandlers
from jobs.job_routes import job_routes
#global imports
from quart import Quart, render_template
import motor
from CONFIG import *
client = CLIENT
db = client.main

app = Quart(__name__)
#employees
app.register_blueprint(employee_routes)
app.register_blueprint(employee_datahandlers)
app.register_blueprint(employee_login_and_signup)
#employers
app.register_blueprint(employer_datahandlers)
app.register_blueprint(employer_signup_and_login)
app.register_blueprint(employer_routes)
#jobs
app.register_blueprint(job_datahandlers)
app.register_blueprint(job_routes)

#configs
app.secret_key = 'super secret key'
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=['GET'])
async def index():
    return await render_template('index.html')


@app.route("/getstarted", methods=['GET'])
async def getstarted():
    return await render_template('getstarted.html')

# If the file is run directly,start the app.
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)

