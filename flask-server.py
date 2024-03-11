from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

def job():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"This is a scheduled job at {current_time}.")

# 設定APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(job, trigger='interval', seconds=10)
scheduler.start()

# 定義路由
@app.route('/')
def index():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run()
