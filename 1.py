with open("1.txt") as f:
    input = f.readlines()


split_inputs = []
current = []
for l in input:
    try:
        current.append(int(l))
    except:
        split_inputs.append(current)
        current = []

sums = [sum(l) for l in split_inputs]
top_maxes = []

for _ in range(3):
    top_maxes.append(max(sums))
    del sums[sums.index(max(sums))]

print(top_maxes, sum(top_maxes))
