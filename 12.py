with open("12.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "Sabqponm",
    "abcryxxl",
    "accszExk",
    "acctuvwj",
    "abdefghi",
]
#data = testcase

grid = [list([ord(i)-ord("a") if i not in {"S", "E"} else i for i in s]) for s in data]
# replace "E" with 27
for l in grid:
    if "E" in l:
        l[l.index("E")] = 26

def print_grid(grid):
    for l in grid:
        print("\t".join([str(i) for i in l]))

# for each square, create a matrix containing the directions you can move in.
neighbors_grid = [
    [
        [] for j in range(len(grid[0]))
    ] for i in range(len(grid))
]

for i in range(len(grid)):
    for j in  range(len(grid[0])):
        for move in [(0,1), (1,0), (0,-1), (-1,0)]:
            i_add, j_add = move
            if 0 <= i + i_add < len(grid) and 0 <= j + j_add < len(grid[0]):
                if isinstance(grid[i][j], str) or isinstance(grid[i+i_add][j+j_add], str):
                    neighbors_grid[i][j].append((i+i_add, j+j_add))
                else:
                    # test if the target square is higher or lower than the current square
                    start = grid[i][j]
                    end = grid[i+i_add][j+j_add]
                    if start + 1 >= end:
                        neighbors_grid[i][j].append((i+i_add, j+j_add))


def move_is_valid(neighbors_grid, visited, source, target):
    """
    Check if it is possible to move to target from source, or if source has already been visited
    """
    i, j = source
    i_new, j_new = target

    is_neighbor = target in neighbors_grid[i][j]
    has_been_visited = visited[i_new][j_new]

    return is_neighbor and not has_been_visited

def find_index(grid, value):
    """
    Find the starting and ending squares
    """
    row_bool = [value in l for l in grid]
    i = row_bool.index(True)

    j = grid[i].index(value)

    return i, j


start_ind = find_index(grid, "S")
end_ind = find_index(grid, 26)

def find_shortest_path(grid, start_ind, end_ind):
    # keep track of whether each square has been visited or not
    visited = [
        [
            grid[i][j] == "S" for j in range(len(grid[0]))
        ] for i in range(len(grid))
    ]

    # squares to visit
    q = []
    # starting square. Each tuple is (i, j, distance_from_source, path)
    q.append((*start_ind, 0, [start_ind]))
    
    # length of shorted path found
    shortest_distance = 10e1000000
    shortest_path = []

    while len(q) > 0:
        # process node on left of queue
        i, j, distance, path_history = q.pop(0)

        if (i, j) == end_ind:
            shortest_distance = distance
            shortest_path = path_history
            break

        for neighbor in neighbors_grid[i][j]:
            i_new, j_new = neighbor
            if not visited[i_new][j_new]:
                visited[i_new][j_new] = True
                q.append((i_new, j_new, distance+1, path_history+[neighbor]))

    if shortest_path != 10e1000000:
        return shortest_distance, shortest_path
    else:
        raise Exception("Unable to find a solution")


shortest_path = find_shortest_path(grid, start_ind, end_ind)
print(shortest_path)

# find all squares at elevation 0
start_ind_list = []
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 0:
            start_ind_list.append((i, j))


print(start_ind_list)
shortest_paths = [find_shortest_path(grid, i, end_ind) for i in start_ind_list]
print(min(shortest_paths, key=lambda x: x[0]))



