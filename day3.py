from collections import defaultdict
import re

def find_overlapping(claims):
    fabric = defaultdict(int)
    for _, start_x, start_y, w, h in claims:
        for i in range(start_x, start_x + w):
            for j in range(start_y, start_y + h):
                fabric[(i, j)] += 1
    return len(list(filter(lambda x: x > 1, fabric.values()))), \
        get_id_of_intact_claim(claims, fabric)

def get_id_of_intact_claim(claims, fabric):
    for claim_id, start_x, start_y, w, h in claims:
        intact = True
        for i in range(start_x, start_x + w):
            for j in range(start_y, start_y + h):
                if fabric[(i, j)] != 1:
                    intact = False
                    break
            if not intact:
                break
        if intact:
            return claim_id

if __name__ == '__main__':
    with open('data/3.txt') as f:
        claims = [tuple(map(int, re.findall(r'\d+', x))) for x in f.readlines()]
        print(find_overlapping(claims))
