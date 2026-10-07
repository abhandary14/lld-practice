"""
Design a thread-safe Task Scheduler that accepts tasks and executes them concurrently using a fixed number of worker threads.

The scheduler should support submitting tasks, starting execution, and shutting down cleanly. Each task should execute exactly once. The scheduler must not create a new thread for every task, must avoid busy waiting, and must ensure that worker threads do not remain blocked indefinitely during shutdown.

Tasks may be submitted before or while the scheduler is running. When shutdown begins, the scheduler should finish all tasks that were already accepted before terminating its workers.

Your design should clearly separate the responsibilities of a task from those of the scheduler and should use appropriate concurrency primitives where needed.
"""

# class Task:
    # owns task details:
    # task id, payload, created_time (time.now), schedule_time (time.now)
    # status enum: TaskStatus.ADDED, TaskStatus.SCHEDULED, TaskStatus.EXECUTED

    # def execute():
        # print executing task

    # ...

# class TaskScheduler:
    # tasks -> min-heap 
    # use a lock
    # scheduler status: running, not running
    # worker threads = [ Thread ] # we will only use one thread for now,
    
    # start() -> starts the scheduler, schedules task by popping from heap
    # schedule_task() -> status to SCHEDULED, calculate schedule_time, push to heap
    # stop() -> status to not running, thread.join()

from enum import Enum
from threading import Thread, Lock, Event
import datetime
import heapq

class TaskStatus(Enum):
    CREATED = 1
    SCHEDULED = 2
    EXECUTED = 3

class SchedulerStatus(Enum):
    RUNNING = 0
    STOPPED = 1

class Task:
    def __init__(self, task_id, payload):
        self.task_id = task_id
        self.payload = payload
        self.task_status = TaskStatus.CREATED
        self.created_time = datetime.datetime.now()
        self.scheduled_time = None

    def execute_task(self):
        if self.task_status == TaskStatus.SCHEDULED:
            self.task_status = TaskStatus.EXECUTED
            print(f"Executed task {self.task_id}: {self.payload}")

    # makes the object comparable in the min-heap
    def __lt__(self, other):
        return self.scheduled_time < other.scheduled_time

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.lock = Lock()
        self.event = Event()
        self.scheduler_status = SchedulerStatus.RUNNING
        
        self.worker = Thread(target=self._start)
        self.worker.start()

    def schedule_task(self, task: Task, delay: int):
        scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        task.scheduled_time = scheduled_time

        with self.lock:
            heapq.heappush(self.tasks, task)
            task.task_status = TaskStatus.SCHEDULED
            print(f"Scheduled Task {task.task_id} to run at {scheduled_time}")

        self.event.set()

    def _start(self):
        # the scheduler should execute all tasks before stopping
        while self.scheduler_status == SchedulerStatus.RUNNING or self.tasks:
            current_task = None
            timeout = None
            with self.lock:
                if not self.tasks:
                    timeout = None
                else:
                    next_task = self.tasks[0]
                    delay = (next_task.scheduled_time - datetime.datetime.now()).total_seconds()

                    if self.scheduler_status == SchedulerStatus.STOPPED or delay <= 0:
                        current_task = heapq.heappop(self.tasks)
                    else:
                        timeout = delay

            if current_task:
                current_task.execute_task()
            else:
                self.event.wait(timeout=timeout)
                self.event.clear()

    def stop(self):
        self.scheduler_status = SchedulerStatus.STOPPED
        self.event.set()
        self.worker.join()
        print("Scheduler stopped.")


import time
def main():
    scheduler = TaskScheduler()

    task1 = Task(1, "Send email")
    task2 = Task(2, "Generate report")
    task3 = Task(3, "Run startup app")

    scheduler.schedule_task(task1, delay=3)
    scheduler.schedule_task(task2, delay=1)
    scheduler.schedule_task(task3, delay=5)

    time.sleep(4)

    scheduler.stop()

if __name__ == "__main__":
    main()