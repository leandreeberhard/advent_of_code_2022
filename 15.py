with open("15.txt", "r") as f:
    data = f.read().split("\n")[:-1]

def parse_line(l):
    split_l = l.split(": ")
    coordinates = []
    for s in split_l:
        rem, y = s.split("y=")
        y = int(y)
        rem, _ = rem.split(", ")
        rem, x = rem.split("x=")
        x = int(x)
        coordinates.append((x, y))
    return coordinates

testcase = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
]

#data = testcase

parsed_data = [parse_line(l) for l in data]

# a sensor reports the location of the closest beacon in terms of the manhattan distance
def manhattan_dist(p1, p2):
    # compute the manhattan distance
    x_diff = abs(p1[0] - p2[0])
    y_diff = abs(p1[1] - p2[1])

    return x_diff + y_diff

# get the distance between any sensor and the closest beacon
distances_from_beacon = [
    (sen, manhattan_dist(sen, beac)) for sen, beac in parsed_data
]

# now find all points in a given row that are at least as close to each sensor
# as the closest beacon
def eliminate_points(sen, dist, row):
    """
    sen: coordinate of sensor
    dist: distance to closest beacon
    row: y coordinate of row
    """
    # notice that the closest point in a row is where the x coordinate matches
    closest_point = (sen[0], row)
    dist_to_closest_point = manhattan_dist(sen, closest_point)
    
    # instead of returing tuples, return the lowest and highest x coord
    # that can be eliminated
    lowest_point = sen[0] - dist + dist_to_closest_point
    highest_point = sen[0] + dist - dist_to_closest_point
    
    return lowest_point, highest_point

search_row = 2000000
#search_row = 10

def find_all_eliminated_x_coords(distances_from_beacon, row, remove_beacons=True):
    eliminated_ranges = [
        eliminate_points(sen, dist, row)
        for sen, dist in distances_from_beacon
    ]
    eliminated_ranges = [
        r for r in eliminated_ranges
        if r[0] <= r[1]
    ]

    # find the overlap
    eliminated_x_coords = set()
    for rl, rh in eliminated_ranges:
        x_coords = set(range(rl, rh+1))
        eliminated_x_coords |= x_coords

    if remove_beacons:
        # subtract the number of known beacons in the row
        all_beacons_x_coords = {
            t[1][0] for t in parsed_data if t[1][1] == row
        }
        eliminated_x_coords -= all_beacons_x_coords

    return eliminated_x_coords
print(len(find_all_eliminated_x_coords(distances_from_beacon, search_row)))



coord_min = 0
coord_max = 4000000
#coord_max = 20

def reduce_range(elim_range, possible_ranges):
    """
    elim_range: tuple of coordinates to be eliminated
    possible_ranges: list of disjoint segments given by their start and end
    """
    low, high = elim_range
    seg_new = []

    for seg in possible_ranges:
        # four cases
        # case 1: seg completely contains elim_range
        if seg[0] <= low and seg[1] >= high:
            # split up seg into two ranges
            seg1 = (seg[0], low-1)
            seg2 = (high+1, seg[1])
            
            for s in [seg1, seg2]:
                if s[0] < s[1]:
                    seg_new.append(s)

        # case 2: seg is completely contained by elim_range
        elif seg[0] >= low and seg[1] <= high:
            pass            

        # case 3: seg overlaps, but one endpoint is different
        # in this case, either low or high must be contained in seg
        elif not(seg[1] <= low or seg[0] >= high):
            # segment contains low
            if seg[0] < low and seg[1] > low:
                s = (seg[0], low-1)
            # segment contains high
            elif seg[0] < high and seg[1] > high:
                s = (high+1, seg[1])

            seg_new.append(s)

        # case 4: segments are disjoint
        else:
            seg_new.append(seg)

    return seg_new
    
def sort_ranges(ranges):
    return sorted(ranges, key=lambda x: x[0])

def find_all_eliminated_x_coords_fast(distances_from_beacon, row):
    # instead of finding all intermediate elements, eliminate the entire range at once
    possible_ranges = [(coord_min, coord_max)]
    
    eliminated_ranges = [
        eliminate_points(sen, dist, row)
        for sen, dist in distances_from_beacon
    ]
    eliminated_ranges = [
        r for r in eliminated_ranges
        if r[0] <= r[1]
    ]

    for elim_range in eliminated_ranges:
        possible_ranges = reduce_range(elim_range, possible_ranges)
        possible_ranges = sort_ranges(possible_ranges)

    return possible_ranges


# now find the only position that could contain a beacon in the search area

for y in range(coord_min, coord_max+1):
    possible_ranges = find_all_eliminated_x_coords_fast(distances_from_beacon, y)
    if len(possible_ranges) > 0:
        xy_answer = (possible_ranges[0][0], y)

print(4000000 * xy_answer[0] + xy_answer[1])


