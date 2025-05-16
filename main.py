from fastapi import FastAPI

from workers.cron_scheduler import start_scheduler, shutdown_scheduler

app = FastAPI()

start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    shutdown_scheduler()