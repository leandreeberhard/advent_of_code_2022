with open("6.txt", "r") as f:
    data = f.read().rstrip("\n")

testcase = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
testcase2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
testcase3 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
#data = testcase3

first_index = None
for i in range(4, len(data)):
    if len(set(data[i-4:i])) == 4:
        first_index = i
        break
print(first_index)

first_index_message = None
for i in range(14, len(data)):
    if len(set(data[i-14:i])) == 14:
        first_index_message = i
        break
print(first_index_message)



