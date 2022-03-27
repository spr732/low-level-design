import enum


class User(enum.Enum):
    ROOT = 1
    ADMIN = 2
    USER = 3

    def __lt__(self, other):
        return self.value < other.value


class SchedulingAlgorithm(enum.Enum):
    FCFS = 1
    SJF = 2
    FPS = 3
    EDF = 4


class Job:
    __id = 0

    def __init__(self, name: str, duration: int, priority: int, deadline: int, user: User):
        self.id = Job.get_unique_id()
        self.name = name
        self.duration = duration
        self.priority = priority
        self.deadline = deadline
        self.user = user

    @classmethod
    def get_unique_id(cls):
        cls.__id += 1
        return cls.__id

    def __str__(self):
        return self.name


class JobScheduleAlgorithm:
    def __init__(self, threads: int):
        self.threads = threads

    def schedule(self, queue: list, thread_capacity: list, result: list):
        pass

    def process_job(self, thread_capacity: list):
        min_element = min(*thread_capacity)
        for i in range(len(thread_capacity)):
            thread_capacity[i] -= min_element

    def schedule(self, queue: list, thread_capacity: list, result: list):
        while queue:
            for i in range(self.threads):
                if thread_capacity[i] == 0:
                    if queue:
                        job = queue[0]
                        result[i].append(job)
                        thread_capacity[i] += job.duration
                        queue.pop(0)
            self.process_job(thread_capacity)


class FirstComeFirstServe(JobScheduleAlgorithm):
    pass


class ShortestJobFirst(JobScheduleAlgorithm):
    def schedule(self, queue: list, thread_capacity: list, result: list):
        queue = sorted(queue, key=lambda sub: (sub.duration, sub.priority))
        super().schedule(queue, thread_capacity, result)


class FixedPriorityScheduling(JobScheduleAlgorithm):
    def schedule(self, queue: list, thread_capacity: list, result: list):
        queue = sorted(queue, key=lambda sub: (sub.priority, sub.user, sub.duration))
        super().schedule(queue, thread_capacity, result)


class EarliestDeadlineFirst(JobScheduleAlgorithm):
    def schedule(self, queue: list, thread_capacity: list, result: list):
        queue = sorted(queue, key=lambda sub: (sub.deadline, sub.priority, sub.duration))
        total_time_taken = [0]*self.threads
        while queue:
            for i in range(self.threads):
                if thread_capacity[i] == 0:
                    if queue:
                        job = queue[0]
                        total_time_taken[i] += job.duration
                        if total_time_taken[i] <= job.deadline:
                            result[i].append(job)
                        else:
                            total_time_taken[i] -= job.duration
                        thread_capacity[i] += job.duration
                        queue.pop(0)
            self.process_job(thread_capacity)


class Scheduler:
    __algo_q = {
        SchedulingAlgorithm.FCFS: FirstComeFirstServe,
        SchedulingAlgorithm.SJF: ShortestJobFirst
    }

    def __init__(self):
        self.jobs = []
        self.fcfs_queue = []
        self.sjf_queue = []
        self.fps_queue = []
        self.edf_queue = []

    def add_job(self, job: Job):
        self.jobs.append(job)
        self.fcfs_queue.append(job)
        self.sjf_queue.append(job)
        self.fps_queue.append(job)
        self.edf_queue.append(job)

    def get_scheduling_sequence(self, algorithm: SchedulingAlgorithm, threads: int):
        result = [[] for _ in range(threads)]
        thread_capacity = [0] * threads
        if algorithm == SchedulingAlgorithm.FCFS:
            FirstComeFirstServe(threads).schedule(self.fcfs_queue, thread_capacity, result)
        if algorithm == SchedulingAlgorithm.SJF:
            ShortestJobFirst(threads).schedule(self.sjf_queue, thread_capacity, result)
        if algorithm == SchedulingAlgorithm.FPS:
            FixedPriorityScheduling(threads).schedule(self.fps_queue, thread_capacity, result)
        if algorithm == SchedulingAlgorithm.EDF:
            EarliestDeadlineFirst(threads).schedule(self.edf_queue, thread_capacity, result)
        return result


if __name__ == "__main__":
    j1 = Job("J1", 10, 0, 10, User.ROOT)
    j2 = Job("J2", 20, 0, 40, User.ADMIN)
    j3 = Job("J3", 15, 2, 40, User.ROOT)
    j4 = Job("J4", 30, 1, 40, User.USER)
    j5 = Job("J5", 10, 2, 30, User.USER)

    scheduler = Scheduler()
    scheduler.add_job(j1)
    scheduler.add_job(j2)
    scheduler.add_job(j3)
    scheduler.add_job(j4)
    scheduler.add_job(j5)

    res = scheduler.get_scheduling_sequence(SchedulingAlgorithm.FCFS, 2)
    for jobs in res:
        print([i.name for i in jobs])

    res = scheduler.get_scheduling_sequence(SchedulingAlgorithm.SJF, 2)
    for jobs in res:
        print([i.name for i in jobs])

    res = scheduler.get_scheduling_sequence(SchedulingAlgorithm.FPS, 2)
    for jobs in res:
        print([i.name for i in jobs])

    res = scheduler.get_scheduling_sequence(SchedulingAlgorithm.EDF, 2)
    for jobs in res:
        print([i.name for i in jobs])
