import parsefeeds
from flask import Flask, send_from_directory
from flask_apscheduler import APScheduler

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config.from_object(Config())

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)

# interval example
@scheduler.task('interval', id='do_job_1', minutes=30, misfire_grace_time=900)
def job1():
    print('Job 1 executed')
    exec(open('parsefeeds.py').read())

scheduler.start()

#app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
