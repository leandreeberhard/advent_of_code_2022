with open("4.txt", "r") as f:
    data = [x[:-1] for x in f.readlines()]

testcase = [
    "2-4,6-8",
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8",
]
#data = testcase

def process_string(string):
    split_string = string.split(",")
    split_ranges = [s.split("-") for s in split_string]
    convert_tuple = lambda t: tuple(int(e) for e in t)
    split_ranges = [convert_tuple(t) for t in split_ranges]

    return split_ranges

processed_data = [process_string(s) for s in data]

# range r1 contains range r2 iff r1[0]<=r2[0] and r1[1]>=r2[0]
def test_superset(r1, r2):
    """
    r1, r2 are both tuples of length 2
    """
    is_superset = lambda r1, r2: r1[0]<=r2[0] and r1[1]>=r2[1]
    return is_superset(r1, r2) or is_superset(r2, r1)

# r1 and r2 do not overlap iff r1[0] > r2[1] or r2[0] > r1[1]
# <=> r1 and r2 overlap if r1[0]<=r2[1] and r2[0]<=r1[1]
def test_overlap(r1, r2):
    do_overlap = lambda r1, r2: r1[0]<=r2[1] and r2[0]<=r1[1]
    return do_overlap(r1, r2)

supersets = [test_superset(*t) for t in processed_data]
overlaps = [test_overlap(*t) for t in processed_data]

print(sum(supersets))
print(sum(overlaps))
