from datetime import datetime, timedelta
import time
import os
import argparse

from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

from schedule_training.cmd2deploy import cmd2deploy

parser = argparse.ArgumentParser(description='deploy')
parser.add_argument(
    '--server_num',
    type=int,
    default=0)
args = parser.parse_args()

# store total commands to know when to stop scheduler
total = 0

# define counter and counter lock to check how many commands executed
counter_lock = Lock()
counter = [0]

# job definition
def execute(command_list, counter):
    for command in command_list:
        os.system(command)

        # add counter when each commands ends
        counter_lock.acquire()
        counter[0] += 1
        counter_lock.release()

# init scheduler
executors = {
    'default': {'type': 'threadpool', 'max_workers': 50}
}

scheduler = BackgroundScheduler(executors=executors)
scheduler.start()

# get command_lists
cmd2deploy = cmd2deploy(args.server_num)
command_lists = cmd2deploy.make_cmd_list()

# store total commands
for command_list in command_lists:
    total += len(command_list)

# deploy commands
delta = timedelta(seconds=1)
for i, command_list in enumerate(command_lists):
    scheduler.add_job(execute, 'date', run_date=datetime.now()+delta*(i+1), args=[command_list, counter])

# scheduler handling part
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
try:
    # This is here to simulate application activity (which keeps the main thread alive).
    # if every jobs ended, stop
    while counter[0] < total:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
