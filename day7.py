from helpers import download
import re


class task:
    def __init__(self, name):
        self.name = name
        self.blocks = set()
        self.blockedby = set()

    # Required to allow sorting
    def __lt__(self, other):
        return self.name < other.name


def getData():
    r = download('https://adventofcode.com/2018/day/7/input')
    regex = re.compile(r'^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$')
    data = {}
    available = []
    for line in r.iter_lines():
        blocker, blockee = regex.match(line.decode()).groups()
        if blocker not in data:
            data[blocker] = task(blocker)
            available.append(data[blocker])
        if blockee not in data:
            data[blockee] = task(blockee)

        data[blocker].blocks.add(data[blockee])
        data[blockee].blockedby.add(data[blocker])

        if data[blockee] in available:
            available.remove(data[blockee])

    # Sort the available tasks, by their name, backwards so that .pop() gets the next one
    available.sort(reverse=True)

    return data, available


def puzzle1(data, available):
    output = ''
    while len(available) > 0:
        current = available.pop()
        output += current.name
        for v in current.blocks:
            v.blockedby.remove(data[current.name])
            if len(v.blockedby) == 0:
                available.append(v)
        available.sort(reverse=True)

    print('Answer: {}'.format(output))


def assignJob(worker_jobs, worker_timers, available):
    newjob = available.pop()
    worker_jobs.append(newjob)
    # The time each job takes is 60 + name, where A=1 .. Z=26
    worker_timers.append(newjob.name.encode()[0] - 'A'.encode()[0] + 61)


def puzzle2(data, available):
    time = 0
    worker_jobs = []
    worker_timers = []

    # Assign intial jobs
    while len(worker_jobs) < 5 and len(available) > 0:
        assignJob(worker_jobs, worker_timers, available)

    while len(available) > 0 or len(worker_jobs) > 0:
        # Tick all timers
        i = 0
        while i < len(worker_timers):
            worker_timers[i] -= 1
            # Expire finished jobs and unblock remaining jobs
            if worker_timers[i] == 0:
                for v in worker_jobs[i].blocks:
                    v.blockedby.remove(data[worker_jobs[i].name])
                    if len(v.blockedby) == 0:
                        available.append(v)

                del worker_timers[i]
                del worker_jobs[i]
            else:
                i += 1

        available.sort(reverse=True)

        # Assign new jobs
        while len(worker_jobs) < 5 and len(available) > 0:
            assignJob(worker_jobs, worker_timers, available)

        # Increment time
        time += 1

    # Print the time after incrementing, since the puzzle wants the time of the first empty step
    print('Answer: {}'.format(time))


if __name__ == '__main__':
    # Since this solution involves removing pointers from lists, it requires processing the input twice to reset the data structures
    puzzle1(*getData())
    puzzle2(*getData())
