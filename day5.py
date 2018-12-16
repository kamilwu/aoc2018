import sys

def trigger_reaction(polymer):
    stack = []
    for ch in polymer:
        if stack and abs(ord(ch) - ord(stack[-1])) == 32:
            stack.pop()
        else:
            stack.append(ch)
    return len(stack)

def improve(polymer):
    units_to_check = set(polymer.lower())
    best = sys.maxsize
    for unit in units_to_check:
        best = min(best, trigger_reaction(polymer.replace(unit, '')
                                          .replace(unit.upper(), '')))
    return best

if __name__ == '__main__':
    with open('data/5.txt') as f:
        polymer = f.read().rstrip()
        print(trigger_reaction('dabAcCaCBAcCcaDA'))
        print(trigger_reaction(polymer))
        print(improve(polymer))
