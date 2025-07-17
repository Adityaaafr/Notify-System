from apscheduler.schedulers.background import BackgroundScheduler
from typing import List,Optional
from pydantic import BaseModel, Field, field_validator
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import time

class Employee(BaseModel):
    name: str
    balance: float
    email: Optional[str]=None
    active: bool = True 

    @field_validator('balance')
    def validate_balance(cls,v):
        if v>10000:
            raise ValueError("Balance cannot be more than 10,000 /-")
        return v
raw_data=[
    {"name": "Aditya", "balance":1200,"email":"aditya501@gmail.com"},
    {"name": "Ekta", "balance":900},
    {"name": "Jitendra", "balance":-1100,"active": False},

]

try:
    employee_list: List[Employee]=[Employee(**data) for data in raw_data]
except Exception as e:
    print(" Validation error while parsing the employee data:")
    print(e)
    exit()

Warning_limit = 1000
Block_limit = -1000

def check_balances():
    print("\n Checking employee balances...")
    for emp in employee_list:
        if  emp.balance <= Block_limit:
           print(f"{emp.name}'s service is being disabled ! Balance: {emp.balance}")
        elif emp.balance <= Warning_limit:
            print(f"reminder to {emp.name} to recharge! Balance: {emp.balance}")
        else:
            print(f"{emp.name}'s balance is sufficient: Balance {emp.balance}")

def listener(event):
    if event.exception:
        print(f" JOB {event.job_id} failed!")
    else:
        print(f" JOB {event.job_id} ran successfully.")

scheduler = BackgroundScheduler()
scheduler.add_job(check_balances,'interval',seconds = 10, id='balance-checker', replace_existing=True)
scheduler.add_listener(listener,EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()

try:
    print("Notify System is Live.....if you want to stop kindly press CTRL + C to stop")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
    print("Scheduler has stopped now.")