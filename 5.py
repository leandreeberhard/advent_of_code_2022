with open("5.txt", "r") as f:
    data = f.read()
    
testcase = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

#data = testcase

split_data = data.split("\n")
# parse the split data to extract the crates
# each crate is three characters, whether it's empty or not
# there is a single space between crates
crates = []

ind = 0
while split_data[ind] != "":
    # save the current line
    line = split_data[ind] 
    crate_count = 0
    # final line with the crate numbers
    if "[" not in line:
        break
    else:
        # iterate through all characters in the line 4 at a time
        for j in range(0, len(line), 4):
            current_char = line[j:j+4]
            current_char = current_char.rstrip(" ")

            # add a new list to the crate count if the current index doesn't exist
            if len(crates) < crate_count+1:
                crates.append([])

            if "[" in current_char:
                # extract the character from the brackets
                crate_letter = current_char[1]

                crates[crate_count] = crates[crate_count] + [crate_letter]

            crate_count += 1
    ind += 1

# delete the lines we just processed
split_data = split_data[ind+2:]

# function to parse an instruction
# move 1 from 2 to 1
def parse_instruction(inst):
    inst, dest = inst.split(" to ")
    inst, source = inst.split(" from ")
    inst, n_moves = inst.split("move ")

    return int(n_moves), int(source), int(dest)

# parse the instructions
parsed_instructions = []
for line in split_data:
    try:
        parsed_instructions.append(parse_instruction(line))
    except:
        print(f"Unable to format line {line}")

def execute_instruction(crates, inst):
    n_moves, source, dest = inst
    for _ in range(n_moves):
        source_ind = source - 1
        dest_ind = dest - 1
        to_move = crates[source_ind].pop(0)
        crates[dest_ind] = [to_move] + crates[dest_ind]

def execute_instruction_v2(crates, inst):
    # now crates are moved all at the same time
    n_moves, source, dest = inst
    source_ind = source-1
    dest_ind = dest-1

    # select the first n_moves items from the source
    to_move = crates[source_ind][:n_moves]

    # carry out the move
    crates[source_ind] = crates[source_ind][n_moves:]
    crates[dest_ind] = to_move + crates[dest_ind]

import copy
crates_orig = copy.deepcopy(crates)

# execute all the instructions
for inst in parsed_instructions:
   execute_instruction(crates, inst)
   execute_instruction_v2(crates_orig, inst)

def get_answer(crates):
    answer = ""
    for crate in crates:
        answer += crate[0]
    return answer

print(crates)
print(get_answer(crates))


print(crates_orig)
print(get_answer(crates_orig))
