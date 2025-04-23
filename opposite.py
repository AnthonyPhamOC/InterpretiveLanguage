import sys

program_filepath = sys.argv[1]

# Read file lines
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue
    
    # Label !!! Maybe change it to something else?
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    # Store token
    program.append(opcode)
    token_counter += 1

    # Push 
    if opcode == "POP":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    # Print
    elif opcode == "READ":
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    # Jump Equal to 0
    elif opcode == "CROUCH.DIFF.TO.0":
        label = parts[1]
        program.append(label)
        token_counter += 1
    # Jump greater than 0
    elif opcode == "CROUCH.LESS.THAN.0":
        label = parts[1]
        program.append(label)
        token_counter += 1

class Stack:

    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        return self.buf[self.sp]

    def bottom(self):
        return self.buf[0]

    def set_bottom(self, number):
        self.buf[0] = number

pc = 0
stack = Stack(256)

while program[pc] != "BEGIN":
    opcode = program[pc]
    pc += 1

    # PUSH
    if opcode == "POP":
        number = program[pc]
        pc += 1
        stack.push(number)
    # POP
    elif opcode == "PUSH":
        stack.pop()
    # ADD
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(a + b)
    # SUB
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)
    # PRINT
    elif opcode == "READ":
        string_literal = program[pc]
        pc += 1
        print(string_literal)
    # READ Integer
    elif opcode == "PRNTSTRING":
        number = int(input())
        stack.push(number)
    # READ STRING
    elif opcode == "PRNTINTEGER":
        try:
            character = ord(input("")[0])
            stack.push(character)
        except IndexError:
            stack.push(0)
    # JUMP EQ 0
    elif opcode == "CROUCH.DIFF.TO.0":
        number = stack.top()
        if number == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    # JUMP GT 0
    elif opcode == "CROUCH.LESS.THAN.0":
        number = stack.top()
        if number > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    # Duplicate
    elif opcode == "ORIGINATE":
        a = stack.pop()
        stack.push(a)
        stack.push(a)
    # Print as String
    elif opcode == "RDINTEGER":
        print(chr(stack.pop()), end="", flush=True)
    # Print as Interger
    elif opcode == "RDSTRING":
        print(int(stack.pop()), end="", flush=True)
    # Swap
    elif opcode == "STAY":
        a = stack.pop()
        b = stack.pop()
        stack.push(a)
        stack.push(b)
    # Pop top add to first
    elif opcode == "SUBFROMTOP":
        a = stack.pop()
        number = stack.bottom()
        number += a
        stack.set_bottom(number)

