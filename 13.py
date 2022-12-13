with open("13.txt", "r") as f:
    data = f.read()

testcase = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

#data = testcase
split_data = data.split("\n")

pairs = []
current_pair = []
for l in split_data:
    if l != "":
        current_pair.append(eval(l))
    else:
        pairs.append(current_pair)
        current_pair = []
if len(current_pair) > 0:
    pairs.append(current_pair)

print(pairs[-1])

def compare(left, right):
    # right <= left if each value in the list is <= each value in the other
    # or if all elements are equal and right has fewer elements
    # returns 0 if left < right, 1 if left == right and 2 if left > right

    if isinstance(right, list) != isinstance(left, list):
        # convert the integer to a list
        if isinstance(right, list):
            left = [left]
        else:
            right = [right]

    if isinstance(right, list) and isinstance(left, list):
        # compare elements until we find a comparable element
        for l, r in zip(left, right):
            if compare(l, r) == 1:
                continue
            elif compare(l, r) == 0:
                return 0
            else:
                return 2
        
        # handle the case where all comparable elements are equal
        if all(compare(l, r) == 1 for l, r in zip(left, right)):
            if len(left) < len(right):
                return 0
            elif len(left) == len(right):
                return 1
            else:
                return 2

    else:
        # in this case both elements are integers
        if left < right:
            return 0
        elif left == right:
            return 1
        else:
            return 2

correct_ind = []
for i, pair in enumerate(pairs):
    left, right = pair
    comparison = compare(left, right)
    if comparison == 0:
        correct_ind.append(i+1)

print(correct_ind, sum(correct_ind))

# rearrange the pairs into the correct order
sorted_pairs = [
    pair if compare(*pair)==0 else reversed(pair) for pair in pairs
]
concat_pairs = []
for pair in sorted_pairs:
    concat_pairs += pair

# add the packets to the pairs
concat_pairs.append([[2]])
concat_pairs.append([[6]])

# convert the comparison to the correct format
from functools import cmp_to_key
compare_new = lambda x, y: compare(x, y)-1
sorted_concat_pairs = sorted(concat_pairs, key=cmp_to_key(compare_new))

# find the divider packets
ind2 = sorted_concat_pairs.index([[2]])
ind6 = sorted_concat_pairs.index([[6]])

print(ind2, ind6, (ind2+1)*(ind6+1))


