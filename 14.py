with open("14.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "498,4 -> 498,6 -> 496,6",
    "503,4 -> 502,4 -> 502,9 -> 494,9",
]
#data = testcase

split_data = [d.split(" -> ") for d in data]

pairs = [[tuple(int(i) for i in s.split(",")) for s in d] for d in split_data]

def path_between_points(p1, p2):
    """
    Create a path between two points and return all indices
    Both points must be in the same row or column
    """
    assert p1[0] == p2[0] or p1[1] == p2[1], f"{p1} and {p2} don't share a coordinate"
    
    if p1[0] == p2[0]:
        if p1[1] > p2[1]:
            step = -1
        else:
            step = 1
        return [
            (p1[0], i) for i in range(p1[1], p2[1]+step, step)
        ]

    else:
        if p1[0] > p2[0]:
            step = -1
        else:
            step = 1
        return [
            (i, p1[1]) for i in range(p1[0], p2[0]+step, step)
        ]

rocks = set()
# add all indices containg rocks to rocks
for l in pairs:
    for i in range(len(l)-1):
        path = path_between_points(l[i], l[i+1])
        rocks |= set(path)

import copy
rocks_orig = copy.copy(rocks)

def simulate_sand(rocks):
    """
    Given the coordinates of the current rocks,
    simulate the path of a single grain of sand.
    """
    sand = (500, 0)
    sand_is_stuck = False
    sand_in_freefall = False

    lowest_rock = max(rocks, key=lambda x: x[1])[1]

    while not sand_is_stuck and not sand_in_freefall:
        starting_sand = sand
        # try to move the sand down
        if (sand[0], sand[1]+1) not in rocks:
            sand = (sand[0], sand[1]+1)
        # try to move the sand down and to the left
        elif (sand[0]-1, sand[1]+1) not in rocks:
            sand = (sand[0]-1, sand[1]+1)
        # try to move the sand down and to the right
        elif (sand[0]+1, sand[1]+1) not in rocks:
            sand = (sand[0]+1, sand[1]+1)
        # the sand is blocked, return the index of its resting place
        if starting_sand == sand:
            sand_is_stuck = True
        # the sand is lower than the lowest rock, so it must be falling forever
        if sand[1] > lowest_rock:
            sand_in_freefall = True

    if sand_is_stuck:
        return sand

# simulate sand, add the resting spot to rocks and stop when there are no more stuck grains of sand
sand_counter = 0
while sand := simulate_sand(rocks):
    rocks |= {sand}   
    sand_counter += 1
print(sand_counter)

# now there is a floor
rocks = rocks_orig

lowest_rock = max(rocks, key=lambda x: x[1])[1]
floor = lowest_rock + 2

def simulate_sand_v2(rocks):
    """
    Given the coordinates of the current rocks,
    simulate the path of a single grain of sand.
    """
    sand = (500, 0)
    sand_is_stuck = False

    sand_is_hitting_floor = lambda sand: sand[1]+1 == floor

    while not sand_is_stuck: 
        #print(sand)
        starting_sand = sand
        # try to move the sand down
        if (sand[0], sand[1]+1) not in rocks and not sand_is_hitting_floor(sand):
            sand = (sand[0], sand[1]+1)
        # try to move the sand down and to the left
        elif (sand[0]-1, sand[1]+1) not in rocks and not sand_is_hitting_floor(sand):
            sand = (sand[0]-1, sand[1]+1)
        # try to move the sand down and to the right
        elif (sand[0]+1, sand[1]+1) not in rocks and not sand_is_hitting_floor(sand):
            sand = (sand[0]+1, sand[1]+1)

        # the sand is blocked, return the index of its resting place
        if starting_sand == sand:
            sand_is_stuck = True

    return sand

sand_counter = 0
while (sand := simulate_sand_v2(rocks)) != (500, 0):
    rocks |= {sand}
    sand_counter += 1

# we have to print +1 because the final grain is not counted
print(sand_counter+1)




