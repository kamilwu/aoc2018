import re
from collections import defaultdict

def process(instr, base_estimate, workers):
    return get_pipeline(instr), calc_total_time(instr, base_estimate, workers)

def get_pipeline(instr):
    pipeline = ''
    instructions = instr.copy()
    while instructions:
        for task in instructions:
            if all(map(lambda x: x in pipeline, instructions[task])):  # all conditions satisfied
                pipeline += task
                del instructions[task]
                break
    return pipeline

def calc_total_time(instr, base_estimate, workers):
    def estimate(task):
        return ord(task) - ord('A') + 1 + base_estimate
    time_spent = 0
    satisfied = set()
    already_taken = set()
    possible = [x for x in instr if all(map(lambda y: y in satisfied, instr[x])) and x not in already_taken]
    workload = {}

    while possible or workload:
        while possible:
            if len(workload) == workers:
                minimum = min(workload.values())
                time_spent += minimum
                completed_tasks = [k for k, v in workload.items() if v == minimum]
                for task in completed_tasks:
                    satisfied.add(task)
                    workload.pop(task, None)
                workload = {x: workload[x] - minimum for x in workload}
            task = possible.pop()
            already_taken.add(task)
            workload[task] = estimate(task)
        minimum = min(workload.values())
        time_spent += minimum
        completed_tasks = [k for k, v in workload.items() if v == minimum]
        for task in completed_tasks:
            satisfied.add(task)
            workload.pop(task, None)
        workload = {x: workload[x] - minimum for x in workload}
        possible = [x for x in instr if all(map(lambda y: y in satisfied, instr[x])) and x not in already_taken]
    return time_spent

def build_instructions(puzzle):
    with open(puzzle) as file:
        instr = defaultdict(list)
        for line in file:
            prereq, step = re.findall(r' ([A-Z]) ', line)
            instr[step].append(prereq)

        for x in get_non_dependent_tasks(instr):
            instr[x] = []

        return dict(sorted(instr.items()))

def get_non_dependent_tasks(instr):
    prereqs = []
    for x in instr.values():
        prereqs += x
    return set(prereqs).difference(set(instr.keys()))

if __name__ == '__main__':
    print(process(build_instructions('data/7-test.txt'), base_estimate=0, workers=2))
    print(process(build_instructions('data/7.txt'), base_estimate=60, workers=5))
