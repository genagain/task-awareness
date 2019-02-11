from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from taskawareness import trello

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=22, minute=30)
def scheduled_job():
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    actions = trello.fetch_actions()
    trello.store_archived_cards(actions, today)

