with open("18.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "2,2,2",
    "1,2,2",
    "3,2,2",
    "2,1,2",
    "2,3,2",
    "2,2,1",
    "2,2,3",
    "2,2,4",
    "2,2,6",
    "1,2,5",
    "3,2,5",
    "2,1,5",
    "2,3,5",
]
#data = testcase

def parse_tuple(tup_string):
    split_tup = tup_string.split(",")
    tup = tuple(int(x) for x in split_tup)
    return tup

parsed_data = [parse_tuple(t)for t in data]

def tup_dist(tup1, tup2):
    assert len(tup1) == len(tup2)
    return sum(abs(tup1[i] - tup2[i]) for i in range(len(tup1)))

def find_neighbors(tup, all_tups):
    return len(tuple(t for t in all_tups if tup_dist(t, tup) == 1))

def count_surface_area(all_tups):
    neighbors_per_tup = [find_neighbors(t, all_tups) for t in all_tups]
    s = 0
    for x in neighbors_per_tup:
        s += (6 - x)

    return s

surface_area_of_shape = count_surface_area(parsed_data)
print(f"{surface_area_of_shape=}")

# now find the cubes of air trapped in droplets
# 1. find points completely enclosed in the shape
# 2. calculate the surface area of these shapes
# 3. subtract the surface area of the enclosed shape from that of the original shape

def find_min_max_coord(parsed_data, coord):
    key = lambda x: x[coord]
    max_coord = max(parsed_data, key=key)[coord]
    min_coord = min(parsed_data, key=key)[coord]

    return min_coord, max_coord


# find the boundaries of the data
def find_boundaries_square(parsed_data):
    # find the min and max of each coordinate
    max_dict = {}
    min_dict = {}

    for i in range(3):
        min_coord, max_coord = find_min_max_coord(parsed_data, i)

        # pad the boundaries of the square so that no points on the boundary
        # are in the shape
        max_dict[i] = max_coord + 1
        min_dict[i] = min_coord - 1

    return min_dict, max_dict

def area_of_enclosing_square(parsed_data):
    min_dict, max_dict = find_boundaries_square(parsed_data)

    area = 1
    for i in range(3):
        area *= (max_dict[i]- min_dict[i])

    return area


def increment_point(point, coordinate, positive):
    factor = 1 if positive else -1
    output = []
    for i in range(3):
        if i == coordinate:
            output.append(point[i] + factor)
        else:
            output.append(point[i])
    return tuple(output)   

min_dict, max_dict = find_boundaries_square(parsed_data)

def point_is_empty_space(point, parsed_data):
    """
    Decide if the current point is on the outside of the shape
    AND inside of the enclosing square.
    """
    point_not_in_shape = point not in parsed_data
    point_on_inside_of_shape = all(
        min_dict[i] <= point[i] <= max_dict[i]
        for i in range(3)
    )

    return point_not_in_shape and point_on_inside_of_shape

outside_points = []
visited = []
# implement the flood fill algorithm
def flood_fill(point):
    q = [point]
    while len(q) > 0:
        current_point = q.pop(0)

        visited.append(current_point)

        if point_is_empty_space(current_point, parsed_data):
            outside_points.append(current_point)

            for i in range(3):
                for positive in [True, False]:
                    to_append = increment_point(current_point, i, positive)
                    if to_append not in visited and to_append not in q:
                        q.append(to_append)

starting_point = (
    min_dict[0],
    min_dict[1],
    min_dict[2]
)

flood_fill(starting_point)

# to find the interior, get all points inside the containing square, subtract the
# outside points and then subtract the points in the shape
points_in_square = {
    (x, y, z)
    for x in range(min_dict[0], max_dict[0]+1)
    for y in range(min_dict[1], max_dict[1]+1)
    for z in range(min_dict[2], max_dict[2]+1)
}

enclosed_empty_points = points_in_square - set(outside_points) - set(parsed_data)

# calculate the surface area of the enclosed empty space
empty_points_surface_area = count_surface_area(enclosed_empty_points)

print(f"{empty_points_surface_area=}")
print(f"Area of outside facing surfaces: {surface_area_of_shape-empty_points_surface_area}")




