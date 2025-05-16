from apscheduler.schedulers.background import BackgroundScheduler

from utilities.collateral_data_utility import CollateralDataPusher

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(CollateralDataPusher.push_latest_collateral_data, "cron", hour="0,8,16", minute=30)
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()
