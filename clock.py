from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from taskawareness import trello

sched = BlockingScheduler(timezone='utc')

def scheduled_job():
    now = datetime.now() - timedelta(hours=5)
    today = now.strftime('%Y-%m-%d')
    actions = trello.fetch_actions()
    trello.store_archived_cards(actions, today)

sched.add_job(scheduled_job, 'cron', day_of_week='mon-sun', hour=4, minute=40)

sched.start()
