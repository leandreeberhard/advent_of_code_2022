with open("11.txt", "r") as f:
    data = f.read()

testcase = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
data = testcase

def process_data(data):
    data = data.split("\n")
    monkeys = []
    # split the data into chunks based on the empty lines
    current_monkey = ""
    for l in data:
        if len(l) != 0:
            current_monkey += "__div__" + l
        else:
            monkeys.append(current_monkey)
            current_monkey = ""
    return monkeys

processed_data = process_data(data)

def apply_operations(operations):
    val = operations[0]
    for op in operations[1:]:
        val = op(val)
    return val

class Monkey:
    def __init__(self, ind, starting_items, operation, test):
        self.ind = ind
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        self.items_inspected = 0

    def __repr__(self):
        if len(self.starting_items) > 0 and isinstance(self.starting_items[0], list):
            #return f"{self.ind=}, {self.items_inspected=}, starting_items={[apply_operations(x) for x in self.starting_items]}" 
            return f"{self.ind=}, {self.items_inspected=}"
        else:
            return f"{self.ind=}, {self.items_inspected=}"

    def turn(self):
        target_monkeys = []

        for i, item in enumerate(self.starting_items):
            # step 1: apply operation to the starting_items
            self.starting_items[i] = self.operation(self.starting_items[i]) 
            # step 2: divide worry level by 3
            self.starting_items[i] //= 3
            # step 3: monkey tests item
            target_monkey = self.test(self.starting_items[i])
            target_monkeys.append((target_monkey, self.starting_items[i]))
            
            # keep track of items inspected
            self.items_inspected += 1

        # the monkey throws all items at the end of the turn
        self.starting_items = []
        return target_monkeys
           
    #def turn_v2(self):
    #    target_monkeys = []
    #    for i, item in enumerate(self.starting_items):
    #        # step 1: apply operation to the starting_items
    #        # now instead of saving the number, save a list of operations
    #        item.append(self.operation)
    #       
    #        # apply all the operations to the starting value 
    #        target_monkey = self.test(apply_operations(item))
    #        target_monkeys.append((target_monkey, item))
    #       
    #        # keep track of items inspected
    #        self.items_inspected += 1

    #    # throw away all items
    #    self.starting_items = []
    #    return target_monkeys
    def turn_v2(self):
        target_monkeys = []
        for i, item in enumerate(self.starting_items):
            self.starting_items[i] = self.operation(self.starting_items[i])
            self.starting_items[i] //= 3
            target_monkey = self.test(self.starting_items[i])
            target_monkeys.append((target_monkey, self.starting_items[i]))
            self.items_inspected += 1

        self.starting_items = []
        return target_monkeys


    def catch_item(self, item):
        # item is just the worry level of the item
        self.starting_items.append(item)

def parse_monkey(string):
    split_string = string.split("__div__")
    for l in split_string:
        if "Monkey" in l:
            ind = int(l.rstrip(":").split(" ")[-1])
        if "Starting" in l:
            items_string = l.split(": ")[-1]
            items = [int(i) for i in items_string.split(", ")]
        if "Operation" in l:
            operation = f"lambda old: {l.split('= ')[-1]}"
            operation = eval(operation)
        if "Test" in l:
            divisor = int(l.split("by ")[-1])
        if "true" in l:
            true_monkey = int(l.split("monkey ")[-1])
        if "false" in l:
            false_monkey = int(l.split("monkey ")[-1])
    
    test = lambda w: true_monkey if w % divisor == 0 else false_monkey

    return Monkey(ind=ind, starting_items=items, operation=operation, test=test)

parsed_monkeys = [parse_monkey(string) for string in processed_data]

def simulate_round(parsed_monkeys):
    for monkey in parsed_monkeys:
        target_monkeys = monkey.turn()
        for target_monkey, worry_level in target_monkeys:
            parsed_monkeys[target_monkey].catch_item(worry_level)

for i in range(20):
    simulate_round(parsed_monkeys)

sorted_monkeys = sorted(parsed_monkeys, key=lambda x: x.items_inspected, reverse=True)
print(parsed_monkeys)
print(sorted_monkeys[0].items_inspected * sorted_monkeys[1].items_inspected)


parsed_monkeys_v2 = [parse_monkey(string) for string in processed_data]
#for m in parsed_monkeys_v2:
#    for i in range(len(m.starting_items)):
#        m.starting_items[i] = [m.starting_items[i]]

def simulate_round_v2(parsed_monkeys):
    for monkey in parsed_monkeys:
        target_monkeys = monkey.turn_v2()

        for target_monkey, worry_level in target_monkeys:
            parsed_monkeys[target_monkey].catch_item(worry_level)

round_to_print = [1, 20, 1000, 2000, 3000, 4000, 5000]
for i in range(5000):
    simulate_round_v2(parsed_monkeys_v2)
    if i+1 in round_to_print:
        print(parsed_monkeys_v2)    








