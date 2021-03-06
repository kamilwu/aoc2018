from datetime import datetime
from collections import defaultdict
import re

def choose_guard(history, strategy):
    total_asleep = defaultdict(int)
    minutes = {}
    for tm, what in history:
        if 'begins shift' in what:
            guard = re.findall(r'\d+', what)[0]
        elif 'falls asleep' in what:
            begin = tm.minute
        else:
            end = tm.minute
            took = end - begin - 1
            total_asleep[guard] += took
            if guard not in minutes:
                minutes[guard] = [0] * 60
            for minute in range(begin, end):
                minutes[guard][minute] += 1

    if strategy == 1:
        best_guard = max(total_asleep, key=total_asleep.get)
        best_minute = minutes[best_guard].index(max(minutes[best_guard]))
        return int(best_guard) * best_minute
    elif strategy == 2:
        best = 0, 0, 0
        for guard, his_minutes in minutes.items():
            the_most = max(his_minutes)
            if the_most > best[2]:
                best = int(guard), his_minutes.index(the_most), the_most
        return best[0] * best[1]

if __name__ == '__main__':
    history = []
    with open('data/4.txt') as f:
        for line in f:
            tm, what = line.rstrip().split('] ')
            tm = datetime.strptime(tm, '[%Y-%m-%d %H:%M')
            history.append((tm, what))

    history = sorted(history, key=lambda x: x[0])
    print(choose_guard(history, strategy=1))
    print(choose_guard(history, strategy=2))
