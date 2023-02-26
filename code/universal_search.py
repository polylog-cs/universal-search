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

import itertools
import sys


class BrainfuckExecution:
    """
    This class represents a single execution of a brainfuck program. It is initialized with the
    program and the input. It can be stepped through one command at a time, or it can be run
    until it is finished.
    """

    # Initializes the execution with the program and the input.
    def __init__(self, program: str, input: str):
        self.program = program
        self.program_pointer = 0
        self.data = {}
        self.data_pointer = 0
        self.input = input
        self.input_pointer = 0
        self.output = []

    # Returns whether the program has finished executing.
    def is_finished(self) -> bool:
        return self.program_pointer >= len(self.program)

    # Executes a single step of the program. There is some unspecified behavior in the language
    # specificiation or that are technically syntax errors, but we try to define these
    # in some reasonable way by slightly modifying the language specification only so that we
    # do not need to handle these errors. Treat this implementation as the specification of
    # a new slightly modified language invented for this purpose.
    def step(self) -> None:
        if self.is_finished():
            return
        command = self.program[self.program_pointer]
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
                while self.program_pointer < len(self.program):
                    if self.program[self.program_pointer] == "[":
                        counter += 1
                    elif self.program[self.program_pointer] == "]":
                        counter -= 1
                        if counter == 0:
                            break
                    self.program_pointer += 1
        elif command == "]":
            if self.data.get(self.data_pointer, 0) != 0:
                # Jump it back to the matching [ command.
                # Keep track of how many nested loops we are in.
                counter = 0
                while self.program_pointer >= 0:
                    if self.program[self.program_pointer] == "]":
                        counter += 1
                    elif self.program[self.program_pointer] == "[":
                        counter -= 1
                        if counter == 0:
                            break
                    self.program_pointer -= 1
        self.program_pointer += 1

    # Executes the program until it is finished and returns the output.
    def run(self) -> str:
        while not self.is_finished():
            self.step()
        return "".join(self.output)


# This class represents a universal search algorithm that can be used to find a program
# that takes the input and finds the output. It generates the programs in a breadth-first
# search manner, and it executes them in parallel. When it starts executing the n-th program,
# it performs 2 steps of the (n - 1)-th program, 4 steps of the (n - 2)-th program, 8 steps
# of the (n - 3)-th program, etc. When a program finishes, it validates its output and if
# it is correct, it stops the search.
class UniversalSearch:
    def __init__(self, input: str):
        self.input = input
        # Initiate the executions with an empty program
        self.executions = [BrainfuckExecution("", input)]
        self.n = 0

    @staticmethod
    def all_brainfuck_programs():
        alphabet = "><+-.,[]"
        k = 1
        while True:
            # Generates all possible tuples of length k made up from characters
            # from alphabet. Returns a generator, so the programs are only
            # generated when they are needed.
            all_k_character_programs = itertools.combinations_with_replacement(
                alphabet, k
            )
            for program in all_k_character_programs:
                yield program
            k += 1

    # Function to be implemented by the user that returns True if the output is correct.
    def validate(self, output: str) -> bool:
        pass

    # Systematically generates the programs and executes them.
    def search(self) -> str:
        for program in self.all_brainfuck_programs():
            self.executions.append(BrainfuckExecution(program, str(self.input)))
            for i in range(self.n + 1):
                # If the program has already finished, skip it.
                if self.executions[i].is_finished():
                    print("X", end="")
                    continue
                else:
                    print(".", end="")

                # Execute the i-th program for 2^(n-i) steps.
                for _ in range(2 ** (self.n - i)):
                    self.executions[i].step()

                # If the program has finished, validate the output.
                if self.executions[i].is_finished():
                    output = "".join(self.executions[i].output)
                    if self.validate(output):
                        return output, self.executions[i].program
            print()

            self.n += 1


class FactorizationSearch(UniversalSearch):
    """This class uses the universal search to find factors of a given integer."""

    # Checks that the output can be splitted into more than one comma-separated
    # integers greater than 1 whose product is the input.
    def validate(self, output: str) -> bool:
        factors_str = output.split(",")
        # We immediately return in situations where the resulting product is
        # definitely larger than self.input so that we don't end up multiplying
        # very large numbers and mess up our time complexity.
        if sum(len(factor_str) - 1 for factor_str in factors_str) > len(self.input) - 1:
            return False
        try:
            factors = [int(factor) for factor in factors_str]
        except ValueError:
            return False
        if len(factors) <= 1:
            return False
        product = 1
        for factor in factors:
            if factor <= 1:
                return False
            product *= factor
        return product == int(self.input)


def main():
    # Debugging
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

    try:
        input = sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} [number-to-factorise]")
        exit(1)

    print("Output: {}, Program: {}".format(FactorizationSearch(input).search()))


if __name__ == "__main__":
    main()
