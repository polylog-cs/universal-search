import itertools
import sys


class BrainfuckExecution:
    """
    This class represents a single execution of a Brainfuck program. It is initialized
    with the program and the input. It can be stepped through one command at a time.
    """

    def __init__(self, program: str, input: str):
        self.program = program
        self.program_pointer = 0
        self.data = {}
        self.data_pointer = 0
        self.input = input
        self.input_pointer = 0
        self.output = []

    def is_finished(self) -> bool:
        return self.program_pointer >= len(self.program)

    # Executes a single step of the program.
    # We extend the language specification a bit so that it never crashes.
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
            if self.input_pointer >= len(self.input):
                self.data[self.data_pointer] = 0
            else:
                self.data[self.data_pointer] = ord(self.input[self.input_pointer])
                self.input_pointer += 1
        elif command == "[":
            if self.data.get(self.data_pointer, 0) == 0:
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


class UniversalSearch:
    """
    This class represents a universal search algorithm that is used to find a program
    that takes the input and computes the correct output. We generate all programs in an
    exhaustive manner, and execute them in parallel. When we start
    executing the n-th program, we simulate 1 step of the n-th program, 2 steps
    of the (n - 1)-th program, 4 steps of the (n - 2)-th program, 8 steps
    of the (n - 3)-th program, etc. When a program finishes, we check its output
    and if it is correct, we stop the search.
    """

    def __init__(self, input: str):
        self.input = input
        # Initiate the executions with an empty program
        self.executions = [BrainfuckExecution("", input)]
        self.n = 0

    # Systematically generates all possible Brainfuck programs, starting from the
    # shortest ones.
    @staticmethod
    def all_brainfuck_programs():
        alphabet = "><+-.,[]"
        k = 1
        while True:
            # Generates all possible tuples of length k made up from characters of the
            # brainfuck alphabet. Returns a generator, so the next program is always
            # generated only once it is needed.
            all_k_character_programs = itertools.product(
                alphabet, repeat=k
            )
            for program in all_k_character_programs:
                yield "".join(program)
            k += 1

    # Function to be implemented by the user; returns True if the output is correct.
    def check(self, output: str) -> bool:
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

                # If the program has finished, check the output.
                if self.executions[i].is_finished():
                    output = "".join(self.executions[i].output)
                    if self.check(output):
                        return output, self.executions[i].program
            print()

            self.n += 1


class UniversalFactorization(UniversalSearch):
    """This class uses the universal search to find factors of a given integer."""

    # Checks that the output can be split into two comma-separated integers greater than
    # 1 whose product is the input.
    def check(self, output: str) -> bool:
        try:
            a_str, b_str = output.split(",")
            a, b = int(a_str), int(b_str)
        except ValueError:
            return False
        if a <= 1 or b <= 1:
            return False
        return a * b == int(self.input)


class UniversalSort(UniversalSearch):
    # Checks that the output contains the same numbers as the input
    # but in the sorted order
    def check(self, output: str) -> bool:
        def split_to_ints(string):
            return [int(x) for x in string.split(",")]

        in_list = split_to_ints(self.input)
        try:
            out_list = split_to_ints(output)
        except ValueError:
            return False
        # We assume the input doesn't contain the same number twice
        if set(out_list) != set(in_list):
            return False
        for i in range(len(out_list) - 1):
            if out_list[i] > out_list[i + 1]:
                return False
        return True


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} [number-to-factorise]")
        exit(1)

    output, program = UniversalFactorization(input).search()
    print()
    print(f"Output: {output}")
    print(f"Program: {program}")


if __name__ == "__main__":
    main()
