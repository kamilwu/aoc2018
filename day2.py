from collections import defaultdict

def checksum(boxes):
    two, three = 0, 0
    for box in boxes:
        histogram = defaultdict(int)
        for ch in box:
            histogram[ch] += 1
        if 2 in histogram.values():
            two += 1
        if 3 in histogram.values():
            three += 1
    return two * three

def common_letters(boxes):
    def match(s1, s2):
        pos = -1
        for i, (c1, c2) in enumerate(zip(s1, s2)):
            if c1 != c2:
                if pos != -1:
                    return -1
                pos = i
        return pos

    for i, box in enumerate(boxes):
        for other_box in boxes[i:]:
            differ_at = match(box, other_box)
            if differ_at != -1:
                return box[:differ_at] + box[differ_at + 1:]

if __name__ == '__main__':
    with open('data/2.txt') as f:
        data = f.readlines()
        print(checksum(data))
        print(common_letters(data))
