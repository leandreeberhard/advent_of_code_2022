with open("17.txt", "r") as f:
    data = f.read().split("\n")[0]

testcase = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
#data = testcase

# 1. rock appears 3 units above the highest point of the last rock and 2 units from the left edge
# 2. rock is pushed left or right according to the gas
# 3. rock is moves down
# 4. When rock comes to a rest (no more downward movemenet possible), the process begins again

EDGE_L = 0
EDGE_R = 6

class Rock:
    def __init__(self, starting_coord):
        # if the shape is enclosed in a box, then this is the
        # bottom left corner
        self.position = starting_coord
        self.is_blocked = False

    @property
    def vertices(self):
        """
        To be implemented in child clases
        """
        pass

    @property
    def left_edge(self):
        # return the lowest y coordinate of the shape
        return min(v[0] for v in self.vertices)

    @property
    def right_edge(self):
        return max(v[0] for v in self.vertices)

    @property
    def bottom_edge(self):
        return min(v[1] for v in self.vertices)

    @property
    def top_edge(self):
        return max(v[1] for v in self.vertices)

    def other_blocks_rock(self, other, direction):
        if direction == "left":
            new_vert = {(x-1, y) for x, y in self.vertices}
        elif direction == "right":
            new_vert = {(x+1, y) for x, y in self.vertices}
        elif direction == "down":
            new_vert = {(x, y-1) for x, y in self.vertices} 
        else:
            raise ValueError(f"Invalid direction: {direction}")
        return len(
            new_vert & set(other.vertices)
        ) > 0

    def edge_blocks_rock(self, direction):
        if direction == "left":
            return self.left_edge - 1 < EDGE_L
        elif direction == "right":
            return self.right_edge + 1 > EDGE_R
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def move(self, direction, stack):
        # first try moving in direction, then down. If the rock is
        # blocked in both directions, then mark it as blocked
        x, y = self.position

        is_blocked_lateral = (
            any(self.other_blocks_rock(other, direction) for other in stack)
            or self.edge_blocks_rock(direction)
        )

        if direction == "left":
            if not is_blocked_lateral:
                self.position = (x-1, y)
        elif direction == "right":
            if not is_blocked_lateral:
                self.position = (x+1, y)
        else:
            raise ValueError(f"Invalid direction: {direction}")
        
        x, y = self.position

        is_blocked_vertical = (
            any(self.other_blocks_rock(other, "down") for other in stack)
        )

        #print(direction, is_blocked_lateral, self.right_edge, is_blocked_vertical, self.bottom_edge)

        if not is_blocked_vertical:
            self.position = (x, y-1)
        else:
            self.is_blocked = True


class Horiz(Rock):
    @property
    def vertices(self):
        x, y = self.position
        vert = [
            self.position,
            (x+1, y),
            (x+2, y),
            (x+3, y),
        ]
        return vert

class Plus(Rock):
    @property
    def vertices(self):
        x, y = self.position
        vert = [
            (x+1, y),
            (x, y+1),
            (x+1, y+1),
            (x+1, y+2),
            (x+2, y+1),
        ]
        return vert

class RevL(Rock):
    @property
    def vertices(self):
        x, y = self.position
        vert = [
            self.position,
            (x+1, y),
            (x+2, y),
            (x+2, y+1),
            (x+2, y+2),
        ]
        return vert

class Vert(Rock):
    @property
    def vertices(self):
        x, y = self.position
        vert = [
            self.position,
            (x, y+1),
            (x, y+2),
            (x, y+3),
        ]
        return vert

class Square(Rock):
    @property
    def vertices(self):
        x, y = self.position
        vert = [
            self.position,
            (x+1, y),
            (x, y+1),
            (x+1, y+1),
        ]
        return vert

class Base:
    def __init__(self):
        self.vertices = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
        ]

def get_highest_point_in_stack(stack):
    max_y = 0
    for rock in stack:
        max_rock = max(rock.vertices, key=lambda x: x[1])
        if max_rock[1] > max_y:
            max_y = max_rock[1]
    return max_y

def lateral_generator(data):
    i = -1
    while True:
        i += 1
        char =  data[i % len(data)]
        direction = "right" if char == ">" else "left"
        yield direction

def rock_generator():
    rock_order = [
        Horiz, Plus, RevL, Vert, Square,
    ]
    i = -1
    while True:
        i += 1
        RockClass = rock_order[i % len(rock_order)]

        stack_height = get_highest_point_in_stack(stack)
        #print(f"Generating {RockClass}, {stack_height=}")
        yield RockClass(
            (2, stack_height+4)
        )


stack = [Base()]
direction_gen = lateral_generator(data)
rock_gen = rock_generator()


N_BLOCKS = 2022
while len(stack) < N_BLOCKS+1:
    next_rock = next(rock_gen)
    print(f"Block {len(stack)} is falling.", end="\r")
    #print(next_rock.position)
    while not next_rock.is_blocked:
        next_dir = next(direction_gen)
        next_rock.move(next_dir, stack)
        #print(next_rock.position)
    else:
        stack.append(next_rock)

print("\n", get_highest_point_in_stack(stack))











