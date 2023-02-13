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
    
    """
    Returns whether the program has finished executing.
    """
    def is_finished(self):
        return self.instruction_pointer >= len(self.program)
    
    """
    Executes a single step of the program. There is some unspecified behavior in the language
    specificiation or that are technically syntax errors, but we try to define these
    in some reasonable way by slightly modifying the language specification only so that we
    do not need to handle these errors.
    """
    def step(self):
        if self.is_finished():
            return
        command = self.program[self.instruction_pointer]
        if command == '>':
            self.data_pointer += 1
        elif command == '<':
            self.data_pointer -= 1
        elif command == '+':
            self.data[self.data_pointer] = self.data.get(self.data_pointer, 0) + 1
            if self.data[self.data_pointer] == 256:
                self.data[self.data_pointer] = 0
        elif command == '-':
            self.data[self.data_pointer] = self.data.get(self.data_pointer, 0) - 1
            if self.data[self.data_pointer] == -1:
                self.data[self.data_pointer] = 255
        elif command == '.':
            self.output.append(chr(self.data.get(self.data_pointer, 0)))
        elif command == ',':
            # This is technically not according to the language spec, but it's
            # pretty convenient so that the program doesn't just crash when it runs
            # out of input.
            if self.input_pointer >= len(self.input):
                self.data[self.data_pointer] = 0
            else:
                self.data[self.data_pointer] = ord(self.input[self.input_pointer])
                self.input_pointer += 1
        elif command == '[':
            if self.data.get(self.data_pointer, 0) == 0:
                # Jump it forward to the matching ] command.
                # Keep track of how many nested loops we are in.
                counter = 0
                while self.instruction_pointer < len(self.program):
                    if self.program[self.instruction_pointer] == '[':
                        counter += 1
                    elif self.program[self.instruction_pointer] == ']':
                        counter -= 1
                        if counter == 0:
                            break
                    self.instruction_pointer += 1
        elif command == ']':
            if self.data.get(self.data_pointer, 0) != 0:
                # Jump it back to the matching [ command.
                # Keep track of how many nested loops we are in.
                counter = 0
                while self.instruction_pointer > 0:
                    if self.program[self.instruction_pointer] == ']':
                        counter += 1
                    elif self.program[self.instruction_pointer] == '[':
                        counter -= 1
                        if counter == 0:
                            break
                    self.instruction_pointer -= 1
        self.instruction_pointer += 1

    """
    Executes the program until it is finished and returns the output.
    """
    def run(self):
        while not self.is_finished():
            self.step()
        return ''.join(self.output)

def main():
    # Prints "Hello World!".
    program = BrainfuckExecution('++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.', '')
    print(program.run())

if __name__ == '__main__':
    main()