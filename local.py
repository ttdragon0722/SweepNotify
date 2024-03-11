from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime,timezone,timedelta
import json
from requests import post

checkWeekDay = "sun"
hour = 12
minute = None

def getTime()->str:
    source = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=1)
    dt2 = source.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    return dt2.strftime(format="%y-%m-%d")

def getTimeRange():
    wd1 = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=1)
    wd2 = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=5)
    return wd1.astimezone(timezone(timedelta(hours=8))).strftime(format="%m-%d")+" ~ "+ wd2.astimezone(timezone(timedelta(hours=8))).strftime(format="%m-%d")

def sendMsg(msg:str):
    url = 'https://notify-api.line.me/api/notify'
    token = '5rItJvIYCjGKoB32xEOXuh5PfLibyvFYlegskDmRw8n'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message':msg}
    data = post(url, headers=headers, data=data) 

def job():
    with open('source.json',encoding="utf-8") as f:
        source = json.load(f)
    
    msg = "\n請\n"
    try:
        if len(source[getTime()]) == 0 :
            return
        for i,name in enumerate(source[getTime()]):
            msg += name +" "
    except:
        return
    msg += f"同學\n在 {getTimeRange()}期間 記得去早掃^^"
    sendMsg(msg=msg)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # scheduler.add_job(job, trigger='interval', seconds=10)
    scheduler.add_job(job, trigger=CronTrigger(day_of_week=checkWeekDay, hour=hour,minute=minute))
    try:
        print("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


