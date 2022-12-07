with open("7.txt", "r") as f:
    data = f.read().split("\n")

testcase = [
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
]
#data = testcase

# get rid of empty lines
data = [l for l in data if l != ""]

# build a filesystem tree using a dictionary
fs_tree = {}
cwd = []

for l in data:
    if "$" in l:
        # in this case we need to process the command
        if "cd" in l:
            target = l.split("cd ")[-1]
            if target == "..":
                cwd.pop() 
            else:
                cwd += [target]
        elif "ls" in l:
            # we don't need to handle this command
            pass

    else:
        # add the contents of the file to fs tree
        split_l = l.split(" ")

        current_d = fs_tree
        for k in cwd:
             if k not in current_d:
                 current_d[k] = {}
             current_d = current_d[k]

        if split_l[0] == "dir":
            # add a sub dict at the cwd
            current_d[split_l[1]] = {}
        else:
            # in this case we are dealing with a file
            current_d[split_l[1]] = int(split_l[0])


dir_size_dict = {}

def get_size_of_dir(d, cwd=[]):
    """
    Get the size of the directory and all subfolders
    """
    global dir_size_dict

    total_size = 0
    for k, v in d.items():
        if isinstance(v, int):
            total_size += v
        else:
            size_of_dir = get_size_of_dir(v, cwd=cwd+[k])
            # save the size in the global dict
            dir_size_dict["/".join(cwd+[k])] = size_of_dir
            total_size += size_of_dir
    return total_size

print(fs_tree)
get_size_of_dir(fs_tree)

# filter to all directories above certain size
max_size = 100000
filtered_d = {k: v for k, v in dir_size_dict.items() if v <= max_size}
print(f"Total sum of sized of directories with size no greater than {max_size}: {sum(filtered_d.values())}")


# part 2 of the problem
total_size_of_disk = 70000000
min_free_space_needed = 30000000
available_space = total_size_of_disk - dir_size_dict["/"]
print(f"{total_size_of_disk=}, {available_space=}")

# find the smallest directory st available_space + size_of_directory >= min_free_space_needed
filtered_d = {k: v for k, v in dir_size_dict.items() if available_space + v >= min_free_space_needed}
print(min(filtered_d.items(), key=lambda x: x[1]))

