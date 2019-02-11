from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from taskawareness import trello

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=3, minute=30)
def scheduled_job():
    now = datetime.now() - timedelta(hours=5)
    today = now.strftime('%Y-%m-%d')
    actions = trello.fetch_actions()
    trello.store_archived_cards(actions, today)
