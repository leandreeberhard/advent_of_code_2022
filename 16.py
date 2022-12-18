with open("16.txt", "r") as f:
    data = f.read().split("\n")[:-1]

testcase = [
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
    "Valve HH has flow rate=22; tunnel leads to valve GG",
    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
    "Valve JJ has flow rate=21; tunnel leads to valve II",
]
#data = testcase

def parse_line(l):
    split_l = l.split("; ")
    rem, flow_rate = split_l[0].split("=")
    flow_rate = int(flow_rate)
    split_rem = rem.split(" ")
    valve_id = split_rem[1]

    split_children = split_l[1].split(" ")
    children_ids = split_children[4:]
    parsed_children = [s.rstrip(",") for s in children_ids]

    return valve_id, flow_rate, parsed_children

parsed_data = [parse_line(l) for l in data]
valve_dict = {
    i[0]: i[1:] for i in parsed_data
}
#print(valve_dict)

TIME_LIMIT = 30
remaining_time = TIME_LIMIT

# opening valve takes 1 minue
# traveling between any two valves takes 1 minute
def calculate_value_of_valve(flow_rate, remaining_time):
    # if the remaining time is less than zero, the valve should have no value
    remaining_time = max(0, remaining_time)
    return flow_rate * (remaining_time)

def shortest_path(valve_dict, start, destination):
    # do a breadth first search to find the shortest path between any two nodes
    visited = []
    q = [[start]]
    if start == destination:
        return q
    
    while q:
        path = q.pop(0)
        node = path[-1]

        if node not in visited:
            neighbors = valve_dict[node][-1]

            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                q.append(new_path)

                if neighbor == destination:
                    return new_path
            visited.append(node)
    print(f"Unable to find path between {start} and {destination}")

from copy import copy
call_count = 0

def depth_first(valve, remaining_time, max_value, opened, visited):
    """
    Starting at valve, we can either open the valve (if it is not open already)
    at a cost of 1 time unit, or move on directly to a neighbor. Each move takes
    1 time unit regardless of if we opened the valve or not.

    When the remaining time is <= 0, we return the current value.
    """
    global call_count
    call_count += 1

    if call_count % 1000 == 0:
        print(f"call count {call_count}")
    #print(f"exploring {valve=}, {remaining_time=}, {opened=}, {visited=}, {max_value=}")

    if remaining_time <= 0 or sum([valve_dict[v][0] for v in valve_dict if v not in opened]) == 0:
        return max_value, opened, visited

    # calculate the current value of the valve if we open it (starting at the next time)
    current_value = calculate_value_of_valve(valve_dict[valve][0], remaining_time-1)

    max_value_orig = copy(max_value)
    opened_orig = copy(opened)
    visited_orig = copy(visited)
    
    visited += [valve]

    for v in valve_dict[valve][1]:
        if valve not in opened:
            val, op, vis = depth_first(
                v,
                remaining_time-2,
                max_value_orig + current_value,
                opened_orig + [valve],
                visited_orig + [valve],
            )
            if val > max_value:
                max_value = val
                opened = copy(op)
                visited = vis

        val, op, vis = depth_first(
            v,
            remaining_time-1,
            max_value_orig,
            opened_orig,
            visited_orig + [valve],
        )
        if val > max_value:
            max_value = val
            opened = copy(op)
            visited = vis

    return max_value, opened, visited


#print(depth_first("AA", TIME_LIMIT, 0, [], []))

def get_most_valuable_valve(valve, time_remaining, opened):
    valves_to_check = set(valve_dict.keys()) - set(opened)

    distances = {
        v: len(shortest_path(valve_dict, valve, v))-1 for v in valves_to_check 
    }
    values = {
        v: valve_dict[v][0] * (time_remaining - distances[v] - 1) 
        for v in valves_to_check
    }

    best_valve = max(values, key=values.get)
    value = values[best_valve]

    return best_valve, value 


time_remaining = TIME_LIMIT
opened = []
current_valve = "AA"
total_value = 0

while time_remaining > 0 and sum(valve_dict[v][0] for v in valve_dict.keys() if v not in opened) > 0:
    destination, value = get_most_valuable_valve(current_valve, time_remaining, opened)

    distance_to_destination = len(shortest_path(valve_dict, current_valve, destination))-1

    current_valve = destination
    opened += [destination]
    total_value += value
    time_remaining -= (distance_to_destination+1)
    
    print(destination, value)

print(total_value)


def calculate_value_of_path(path):
    """
    Given an order of valves opened, calculate the value of that path
    """
    current_valve = "AA"
    value = 0
    time_remaining = TIME_LIMIT
    for destination in path:
        dist = len(shortest_path(valve_dict, current_valve, destination))-1
        value += valve_dict[destination][0] * (time_remaining - dist - 1)
        time_remaining -= (dist+1)
        current_valve = destination

    return value

from itertools import permutations
def get_all_paths(valve_dict):
    # all keys with non-zero value
    valves = [v for v in valve_dict if valve_dict[v][0] > 0]

    return permutations(valves)

path_dict = {
    p: calculate_value_of_path(p) for p in get_all_paths(valve_dict)
}

max_path = max(path_dict, key=path_dict.get)
print(max_path, path_dict[max_path])

