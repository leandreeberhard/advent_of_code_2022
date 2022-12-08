with open("8.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]
#data = testcase

converted_data = [
    [int(i) for i in line]
    for line in data
]

# for every tree in the interior of the array, determine if the tree is visible or not
def is_visible(grid, ind, dir):
    """
    ind is a tuple of length 2
    dir is left, right, top, bottom
    """
    x, y = ind
    current_val = grid[x][y]

    if dir == "left":
        values_to_compare = [grid[x][i] for i in range(0, y)]
    elif dir == "right":
        values_to_compare = [grid[x][i] for i in range(y+1, len(grid[x]))]
    elif dir == "top":
        values_to_compare = [grid[i][y] for i in range(0, x)]
    elif dir == "bottom":
        values_to_compare = [grid[i][y] for i in range(x+1, len(grid))]
    else:
        raise ValueError(f"Got {dir=}")

    return all(current_val > v for v in values_to_compare)

def print_grid(grid):
    for l in grid:
        print(l)

# determine if each tree is visible or not
visible_grid = [
    [2 for i in range(len(data[0]))]
    for _ in range(len(data))
]
# mark the edges as visible (1)
interior_ind = [(x, y) for x in range(1, len(data)-1) for y in range(1, len(data[0])-1)]
all_ind = [(x, y) for x in range(len(data)) for y in range(len(data[0]))]
border_ind = set(all_ind) - set(interior_ind)

for x, y in border_ind:
    visible_grid[x][y] = 1

for ind in interior_ind:
    res = [is_visible(data, ind, dir) for dir in ["left", "right", "top", "bottom"]]
    x, y = ind
    visible_grid[x][y] = int(any(res))

def sum_grid(grid):
    sums = [sum(l) for l in grid]
    return sum(sums)

print(sum_grid(visible_grid))


def get_senic_score(grid, ind):
    """
    ind is a tuple of length 2
    """
    x, y = ind
    current_value = grid[x][y]

    viewing_distances = []
    for dir in ["left", "right", "top", "bottom"]:
        if dir == "left":
            values_to_compare = [current_value > grid[x][i] for i in range(0, y)]
            values_to_compare = reversed(values_to_compare)
        elif dir == "right":
            values_to_compare = [current_value > grid[x][i] for i in range(y+1, len(grid[x]))]
        elif dir == "top":
            values_to_compare = [current_value > grid[i][y] for i in range(0, x)]
            values_to_compare = reversed(values_to_compare)
        elif dir == "bottom":
            values_to_compare = [current_value > grid[i][y] for i in range(x+1, len(grid))]

        # start counting until the first tree that blocks the view
        dist = 0
        for i in values_to_compare:
            if i:
                dist += 1
            else:
                dist += 1
                break
        viewing_distances.append(dist)
        
    return viewing_distances[0]*viewing_distances[1]*viewing_distances[2]*viewing_distances[3]

viewing_grid = [
    [get_senic_score(data, (x, y)) for y in range(len(data[0]))]
    for x in range(len(data))
]

def get_max(grid):
    maxes = [max(l) for l in grid]
    return max(maxes)

print(get_max(viewing_grid))
