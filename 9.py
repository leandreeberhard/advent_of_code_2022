with open("9.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
]
testcase2 = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20",
]
#data = testcase2

split_data = [x.split(" ") for x in data]
split_data = [(x[0], int(x[1])) for x in split_data]

#sh = state of head
#st = state of tail
sh = [0, 0]
st = [0, 0]

def update_tail(sh, st):
    # the tail can make at most one move in each coordinate per step
    # a move will be carried out by the tail if it decreases the distance
    # between it and the head
    distance = lambda t1, t2: (
        (t1[0]-t2[0])**2 + (t1[1]-t2[1])**2
    )
    
    # consider all possible moves
    possible_moves = {
        (x, y) for x in [-1,0,1] for y in [-1,0,1]
    } - {(0, 0)}

    # carry out the move that minimized the distance between the head and
    # tail
    add_tuples = lambda t1, t2: [sum(i) for i in zip(t1, t2)]
    distances = {
        move: distance(add_tuples(st, move), sh)
        for move in possible_moves
    }

    # find the move that ends with the smallest possible distance
    best_move = min(distances, key=distances.get)
   
    #print(f"Before: {sh=}, {st=}")
    # if the distance between the head and tails is above the maxumum,
    # update the state of the tail
    if distance(st, sh) > 2:
        st = add_tuples(st, best_move)
    # otherwise, the tail stays put
    #print(f"After: {sh=}, {st=}")
    return st

states_visited_by_tail = {(0, 0)}

def execute_instruction(inst, sh, st):
    global states_visited_by_tail

    direction, n_steps = inst

    # carry out each move one at a time
    for _ in range(n_steps):
        if direction == "R":
            sh[0] += 1
        elif direction == "L":
            sh[0] -= 1
        elif direction == "U":
            sh[1] += 1
        elif direction == "D":
            sh[1] -= 1
        else:
            raise ValueError(f"Invalid direction: {direction}")
        
        #update tail only depends on how the head moved
        st = update_tail(sh, st)
        states_visited_by_tail |= {tuple(st)}

    return sh, st

for step in split_data:
    sh, st = execute_instruction(step, sh, st)

print(len(states_visited_by_tail))


# now, instead of a head and tail, we have a head and 10 tails
# we only care about the positions visited by the final tail
states = [[0, 0] for _ in range(10)]

states_visited_by_tail2 = {(0, 0)}

def execute_instruction2(inst, states):
    global states_visited_by_tail2

    direction, n_steps = inst

    for _ in range(n_steps):
        if direction == "R":
            states[0][0] += 1
        elif direction == "L":
            states[0][0] -= 1
        elif direction == "U":
            states[0][1] += 1
        elif direction == "D":
            states[0][1] -= 1
        else:
            raise ValueError(f"Invalid direction: {direction}")
        
        # now we just need to update each tail in order
        for i in range(1, 10):
            states[i] = update_tail(states[i-1], states[i])
        
        # record the position of the tail
        states_visited_by_tail2 |= {tuple(states[-1])}

    return states

for step in split_data:
    states = execute_instruction2(step, states)

print(len(states_visited_by_tail2))
