import lexer
import RDA

class Compiler:
    f1 = open("test1.txt")
    f2 = open("test2.txt")
    # Change the file name below to test the different files
    text = f3.read()
    lex = lexer.Lexer(text)
    result = lexer.run(text)
    print(result)
    parser = RDA.Parser(result)
    print(parser.start())