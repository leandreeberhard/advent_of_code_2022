with open("2.txt", "r") as f:
    strategy = f.readlines()

testcase = [
    "A Y\n",
    "B X\n",
    "C Z\n",
]

value_map = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

conversion_map = {
    "A": "X",
    "B": "Y",
    "C": "Z",
}

outcome_map = {
    "win": 6,
    "tie": 3,
    "loss": 0,
}

rps_tuples = (
    ("X", "Y", "Z"),
    ("Z", "X", "Y"),
    ("Y", "Z", "X"),
)

def determine_win(opp, you):
    get_middle = lambda t: t[1]
    t = next(x for x in rps_tuples if get_middle(x) == you)
    if opp == t[0]:
        return "win"
    elif opp == t[1]:
        return "tie"
    else:
        return "loss"

def get_points(opponent, you):    
    points = value_map[you]
    opp_conv = conversion_map[opponent]
    win_status = determine_win(opp_conv, you)
    points += outcome_map[win_status]
    return points
    
new_mapping = {
    "X": "loss",
    "Y": "tie",
    "Z": "win",
}
def get_move(opp, you):
    t = next(t for t in rps_tuples if t[1] == opp)
    if you == "X":
        return t[0]
    elif you == "Y":
        return t[1]
    else:
        return t[2]

def get_points2(opponent, you):
    # modify you so that it matches the instructions
    opp_conv = conversion_map[opponent]
    you_mapped = get_move(opp_conv, you)
    points = value_map[you_mapped]
    
    # now you know the win status immediately
    win_status = new_mapping[you]
    points += outcome_map[win_status]
    return points

total_points = 0
total_points2 = 0
for i in strategy:
    conv = i[:-1].split(" ")
    total_points += get_points(*conv)
    total_points2 += get_points2(*conv)
    
    
print(total_points, total_points2)
    
    
