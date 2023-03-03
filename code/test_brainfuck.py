from universal_search import BrainfuckExecution


def main():
    # "Hello World!", wikipedia
    program_helloworld = BrainfuckExecution(
        "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
        "",
    )
    assert program_helloworld.run() == "Hello World!\n"

    # number of steps until n terminates in the collatz procedure; Daniel B Cristofani (cristofdathevanetdotcom) http://www.hevanet.com/cristofd/brainfuck/]
    program_collatz = BrainfuckExecution(
        ">,[[----------[>>>[>>>>]+[[-]+<[->>>>++>>>>+[>>>>]++[->+<<<<<]]<<<]++++++[>------<-]>--[>>[->>>>]+>+[<<<<]>-],<]>]>>>++>+>>[<<[>>>>[-]+++++++++<[>-<-]+++++++++>[-[<->-]+[<<<<]]<[>+<-]>]>[>[>>>>]+[[-]<[+[->>>>]>+<]>[<+>[<<<<]]+<<<<]>>>[->>>>]+>+[<<<<]]>[[>+>>[<<<<+>>>>-]>]<<<<[-]>[-<<<<]]>>>>>>>]>>+[[-]++++++>>>>]<<<<[[<++++++++>-]<.[-]<[-]<[-]<]<,]",
        "27\n",
    )
    assert program_collatz.run() == "111\n"

    print("OK")


if __name__ == "__main__":
    main()
