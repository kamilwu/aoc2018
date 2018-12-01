def calc_freq(changes):
    freq = 0
    for n in changes:
        freq += n
    return freq

def calibrate(changes):
    already_seen = set()
    freq = 0
    while True:
        for n in changes:
            freq += n
            if freq not in already_seen:
                already_seen.add(freq)
            else:
                return freq

if __name__ == '__main__':
    with open('data/1.txt') as f:
        changes = [int(x.replace('+', '')) for x in f.readlines()]
        print(calc_freq(changes))
        print(calibrate(changes))
