from django.shortcuts import render
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta

def run():
    time.sleep(5)
    from .talabat import start_talabat
    from .careem import start_careem
    from .cs_mena import start_csmena
    from .ask_pepper import start_ask_pepper
    from .makane import start_makane
    sched = BackgroundScheduler ({'apscheduler.job_defaults.max_instances': 5})
    date =(datetime.date(datetime.now()))
    from .models import  MainappOrder,MainappChannel


    start_date  = date - timedelta(days=1)
    end_date = date - timedelta(days=0)
    start_timer = datetime.now()
    # channel = MainappChannel.objects.get(name='makane')
    # orders = MainappOrder.objects.filter(channel = channel).delete()
    # print(orders)

    sched.add_job(start_talabat,args=[start_date,end_date,start_timer])
    sched.add_job(start_talabat, 'interval',[start_date,end_date,start_timer], hours=3)


    # sched.add_job(start_careem,args=[start_date,end_date,start_timer])
    # sched.add_job(start_careem, 'interval',[start_date,end_date,start_timer], hours=3)

    # start_date  = date - timedelta(days=2)
    # end_date = date - timedelta(days=0)

    # sched.add_job(start_csmena,args=[start_date,end_date,start_timer])
    # sched.add_job(start_csmena, 'interval',[start_date,end_date,start_timer], hours=3)

    # sched.add_job(start_ask_pepper,args=[start_date,end_date,start_timer])
    # sched.add_job(start_ask_pepper, 'interval',[start_date,end_date,start_timer], hours=3)

    # sched.add_job(start_makane,args=[start_date,end_date,start_timer])
    # sched.add_job(start_makane, 'interval',[start_date,end_date,start_timer], hours=3)

    sched.start()

def run_scraper_code():
    sched = BackgroundScheduler()
    sched.add_job(run)
    sched.start()
   
