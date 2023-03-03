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

    program_loop = BrainfuckExecution("+]", "")
    num_steps = 0
    while not program_loop.is_finished():
        num_steps += 1
        program_loop.step()
    # 2 steps (increment + conditional jump) per one iteration
    assert num_steps == 512

    print("OK")


if __name__ == "__main__":
    main()
