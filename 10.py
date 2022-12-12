with open("10.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
testcase = testcase.split("\n")[:-1]
#data = testcase

def run_instructions(data):
    register_values = [1]
    next_value = 1

    for inst in data:
        if "noop" in inst:
            register_values.append(next_value)
            continue
        else:
            parsed_inst = inst.split(" ")
            value_to_add = int(parsed_inst[-1])
            register_values.extend([next_value]*2)
            next_value = register_values[-1] + value_to_add 

    return register_values

ind_to_check = [20, 60, 100, 140, 180, 220]

history = run_instructions(data)
answer = [i * history[i] for i in ind_to_check]
print(sum(answer))

screen = [["0"]*40 for _ in range(6)]

def print_screen(screen):
    for i in screen:
        print("".join(i))

for i, sprite_pos in enumerate(history):
    if i == 0:
        continue
    register_value = sprite_pos
    horizontal_ind = (i-1) % 40
    vertical_ind = (i-1) // 40 

    # determine if the register value is within 3 of the current horizontal position
    if horizontal_ind in {sprite_pos-1, sprite_pos, sprite_pos+1}:
        screen[vertical_ind][horizontal_ind] = "#"
    else:
        screen[vertical_ind][horizontal_ind] = "."
    
print_screen(screen)








