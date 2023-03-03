from universal_search import BrainfuckExecution


def main():
    # "Hello World!", wikipedia
    program_helloworld = BrainfuckExecution(
        "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
        "",
    )
    print("".join(program_helloworld.run()), end="")

    # number of steps until n terminates in the collatz procedure; Daniel B Cristofani (cristofdathevanetdotcom) http://www.hevanet.com/cristofd/brainfuck/]
    program_collatz = BrainfuckExecution(
        ">,[[----------[>>>[>>>>]+[[-]+<[->>>>++>>>>+[>>>>]++[->+<<<<<]]<<<]++++++[>------<-]>--[>>[->>>>]+>+[<<<<]>-],<]>]>>>++>+>>[<<[>>>>[-]+++++++++<[>-<-]+++++++++>[-[<->-]+[<<<<]]<[>+<-]>]>[>[>>>>]+[[-]<[+[->>>>]>+<]>[<+>[<<<<]]+<<<<]>>>[->>>>]+>+[<<<<]]>[[>+>>[<<<<+>>>>-]>]<<<<[-]>[-<<<<]]>>>>>>>]>>+[[-]++++++>>>>]<<<<[[<++++++++>-]<.[-]<[-]<[-]<]<,]",
        chr(48 + 1) + chr(48 + 6) + chr(10),
    )
    print("".join(program_collatz.run()), end="")


if __name__ == "__main__":
    main()
