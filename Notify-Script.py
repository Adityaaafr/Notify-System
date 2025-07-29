from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import time
from db.Main_db import SessionLocal, Employee

WARNING_LIMIT = 1000
BLOCK_LIMIT = -1000

def check_balances():
    print("\nChecking employee Balances")
    db = SessionLocal()
    employees = db.query(Employee).all()
    for emp in employees:
        if not emp.active:
            continue
        if emp.balance <= BLOCK_LIMIT:
            print(f"{emp.name}'s service is being disabled! Balance: {emp.balance}")
        elif emp.balance <= WARNING_LIMIT:
            print(f"Reminder to {emp.name} to recharge! Balance: {emp.balance}")
        else:
            print(f"{emp.name}'s balance is sufficient: Balance {emp.balance}")
    db.close()

def listener(event):
    if event.exception:
        print(f"JOB {event.job_id} failed!")
    else:
        print(f"JOB {event.job_id} ran successfully.")

def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_balances, 'interval', seconds=10, id='balance-checker', replace_existing=True)
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    try:
        print("Notify System is Live... Press CTRL + C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler has stopped now.")

if __name__ == "__main__":
    main()
