with open("3.txt", "r") as f:
    data = f.readlines()

testcase = [
    "vJrwpWtwJgWrhcsFMMfFFhFp\n",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\n",
    "PmmdzqPrVvPwwTWBwg\n",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\n",
    "ttgJtRGJQctTZtZT\n",
    "CrZsJsPPZsGzwwsLwLmpwMDw\n",
]
#data = testcase

values_dict = {}
current_n_lower = ord("a")
current_n_upper = ord("A")
current_val_lower = 1
current_val_upper = 27

for _ in range(26):
    current_lower = chr(current_n_lower)
    current_upper = chr(current_n_upper)
    values_dict[current_lower] = current_val_lower
    values_dict[current_upper] = current_val_upper

    current_n_lower += 1
    current_n_upper += 1
    current_val_lower += 1
    current_val_upper += 1


def get_value_of_common_element(line):
    line = line[:-1]
    compartment1 = set(line[: len(line) // 2])
    compartment2 = set(line[len(line) // 2 :])

    common_element = compartment1 & compartment2
    # assume there is only a single common element
    common_element = next(s for s in common_element)

    value = values_dict[common_element]
    return value


def get_common_element_group_of_three(list_of_three):
    list_of_three = [l[:-1] for l in list_of_three]
    assert len(list_of_three) == 3, "list_of_three doesn't have 3 elements"

    # find element common to all three lines
    line1, line2, line3 = (set(l) for l in list_of_three)

    common_element = next(s for s in line1 & line2 & line3)

    value = values_dict[common_element]
    return value


values1 = [get_value_of_common_element(l) for l in data]
values2 = [
    get_common_element_group_of_three(data[i : i + 3])
    for i in range(0, len(data), 3)
]

print(sum(values1), sum(values2))
