"""
This is an (essentially) asymptotically optimal program for factoring in the sense that whenever there is a (brainfuck)
program that solves factoring in time f(n), our algorithm solves factoring in time
O(f(n) + n**1.58). The term n**1.58 is the time complexity of multiplying two long numbers 
with n digits in Python (Python uses Karatsuba's algorithm). 
"""

import sys

"""
The language consists of eight commands, listed below. A brainfuck program is a sequence
of these commands, possibly interspersed with other characters (which are ignored).
The commands are executed sequentially, with some exceptions: an instruction pointer begins
at the first command, and each command it points to is executed, after which it normally moves
forward to the next command. The program terminates when the instruction pointer moves past the
last command.

The brainfuck language uses a simple machine model consisting of the program and instruction
pointer, as well as a one-dimensional array of at least 30,000 byte cells initialized to zero;
a movable data pointer (initialized to point to the leftmost byte of the array);
and two streams of bytes for input and output (most often connected to a keyboard and a monitor
respectively, and using the ASCII character encoding).

>	Increment the data pointer (to point to the next cell to the right).
<	Decrement the data pointer (to point to the next cell to the left).
+	Increment (increase by one) the byte at the data pointer.
-	Decrement (decrease by one) the byte at the data pointer.
.	Output the byte at the data pointer.
,	Accept one byte of input, storing its value in the byte at the data pointer.
[	If the byte at the data pointer is zero, then instead of moving the instruction pointer
    forward to the next command, jump it forward to the command after the matching ] command.
]	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer
    forward to the next command, jump it back to the command after the matching [ command.
"""

"""
This class represents a single execution of a brainfuck program. It is initialized with the
program and the input. It can be stepped through one command at a time, or it can be run
until it is finished.
"""


class BrainfuckExecution:

    """
    Initializes the execution with the program and the input.
    """

    def __init__(self, program, input):
        self.program = program
        self.data = {}
        self.data_pointer = 0
        self.instruction_pointer = 0
        self.input = input
        self.input_pointer = 0
        self.output = []
        self.checked = False

    """
    Returns whether the program has finished executing.
    """

    def is_finished(self):
        return self.instruction_pointer >= len(self.program)

    def is_checked(self):
        return self.checked

    def set_checked(self):
        self.checked = True

    def get_output(self):
        return "".join(self.output)

    """
    Executes a single step of the program. We modify the language specification slightly so that we
    do not need to handle syntax errors.
    """

    def step(self):
        if self.is_finished():
            return
        command = self.program[self.instruction_pointer]
        if command == ">":
            self.data_pointer += 1
        elif command == "<":
            self.data_pointer -= 1
        elif command == "+":
            self.data[self.data_pointer] = self.data.get(self.data_pointer, 0) + 1
            if self.data[self.data_pointer] == 256:
                self.data[self.data_pointer] = 0
        elif command == "-":
            self.data[self.data_pointer] = self.data.get(self.data_pointer, 0) - 1
            if self.data[self.data_pointer] == -1:
                self.data[self.data_pointer] = 255
        elif command == ".":
            self.output.append(chr(self.data.get(self.data_pointer, 0)))
        elif command == ",":
            # This is technically not according to the language spec, but it's
            # pretty convenient so that the program doesn't just crash when it runs
            # out of input.
            if self.input_pointer >= len(self.input):
                self.data[self.data_pointer] = 0
            else:
                self.data[self.data_pointer] = ord(self.input[self.input_pointer])
                self.input_pointer += 1
        elif command == "[":
            if self.data.get(self.data_pointer, 0) == 0:
                # Jump it forward to the matching ] command.
                # Keep track of how many nested loops we are in.
                counter = 0
                while self.instruction_pointer < len(self.program):
                    if self.program[self.instruction_pointer] == "[":
                        counter += 1
                    elif self.program[self.instruction_pointer] == "]":
                        counter -= 1
                        if counter == 0:
                            break
                    self.instruction_pointer += 1
        elif command == "]":
            if self.data.get(self.data_pointer, 0) != 0:
                # Jump it back to the matching [ command.
                # Keep track of how many nested loops we are in.
                counter = 0
                while self.instruction_pointer > 0:
                    if self.program[self.instruction_pointer] == "]":
                        counter += 1
                    elif self.program[self.instruction_pointer] == "[":
                        counter -= 1
                        if counter == 0:
                            break
                    self.instruction_pointer -= 1
        self.instruction_pointer += 1

    def steps(self, num_of_steps=1):
        for _ in range(num_of_steps):
            self.step()
            if self.is_finished():
                break

    """
    Executes the program until it is finished and returns the output.
    """

    def run(self):
        while not self.is_finished():
            self.step()
        # print(self.data)
        return "".join(self.output)


def allBrainfuckPrograms():
    def nextBrainfuckProgram(str):
        alphabet = ["<", ">", "+", "-", ".", ",", "[", "]"]
        i = len(str) - 1
        for i in reversed(range(0, len(str))):
            if str[i] != "]":
                return (
                    str[:i]
                    + alphabet[alphabet.index(str[i]) + 1]
                    + "<" * (len(str) - i - 1)
                )
        return "<" * (len(str) + 1)

    str = ""
    while True:
        yield str
        str = nextBrainfuckProgram(str)


def main():

    # DEBUGGING
    # "Hello World!", wikipedia
    program_helloworld = BrainfuckExecution(
        "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
        "",
    )

    # number of steps until n terminates in the collatz procedure; Daniel B Cristofani (cristofdathevanetdotcom) http://www.hevanet.com/cristofd/brainfuck/]
    program_collatz = BrainfuckExecution(
        ">,[[----------[>>>[>>>>]+[[-]+<[->>>>++>>>>+[>>>>]++[->+<<<<<]]<<<]++++++[>------<-]>--[>>[->>>>]+>+[<<<<]>-],<]>]>>>++>+>>[<<[>>>>[-]+++++++++<[>-<-]+++++++++>[-[<->-]+[<<<<]]<[>+<-]>]>[>[>>>>]+[[-]<[+[->>>>]>+<]>[<+>[<<<<]]+<<<<]>>>[->>>>]+>+[<<<<]]>[[>+>>[<<<<+>>>>-]>]<<<<[-]>[-<<<<]]>>>>>>>]>>+[[-]++++++>>>>]<<<<[[<++++++++>-]<.[-]<[-]<[-]<]<,]",
        chr(48 + 1) + chr(48 + 6) + chr(10),
    )

    # UNIVERSAL SEARCH

    input_number = int(sys.argv[1])

    list_of_programs = []
    for program in allBrainfuckPrograms():
        # append new program to the list
        list_of_programs.append(BrainfuckExecution(program, str(input_number)))
        print(len(list_of_programs))
        # simulate certain number of steps of each program in the list
        num_of_steps = 1
        for program in reversed(list_of_programs):
            program.steps(num_of_steps)
            # check the output of the algorithm, we assume it is two comma separated numbers, terminate if correct
            if program.is_finished() and not program.is_checked():
                try:
                    str_a, str_b = program.get_output().split(",", 1)
                    a, b = int(str_a), int(str_b)
                    # we check that both numbers are <= input_number so that we
                    # don't end up multiplying very large numbers and mess up
                    # our time complexity:
                    if (
                        1 < a <= input_number
                        and 1 < b <= input_number
                        and a * b == input_number
                    ):
                        print(a, b)
                        return
                except:
                    pass
                program.set_checked()
            num_of_steps *= 2


if __name__ == "__main__":
    main()
