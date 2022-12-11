####################### TOKENS #######################

# token structure
class Token():
    def __init__(self, type_, code, value):
        self.type = type_
        self.code = code
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

# token chart w/ corresponding codes

real_literal = 0 
natural_literal = 1
bool_literal = 2
char_literal = 3 
string_literal = 4 


assign_op           = 10
add_op              = 11
sub_op              = 12
mult_op             = 13
div_op              = 14
exp_op              = 15
left_paren          = 16
right_paren         = 17
mod_op              = 18
semicolon           = 19
left_brack          = 20
right_brack         = 21
less_than           = 22
greater_than        = 23
less_than_equal     = 24
greater_than_equal  = 25
equal_to            = 26
not_equal_to        = 27
logical_and         = 28
logical_or          = 29
logical_not         = 30
u_neg_op            = 31
comma               = 32
left_brace          = 33
right_brace         = 34
param_dec           = 35

string_keyword = 40 #string keyword
natural_keyword = 41 #natural keyword
char_keyword = 42 # char keyword
real_keyword = 43 #real keyword
boolean_keyword = 44 #boolean keyword
function_call = 45
ident = 46

if_ = 50
else_ = 51
loop = 52

nocap = 60
cap = 61

START = 100
STOP = 99
        


####################### LEXER #######################

# lexer with all the lex functions
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []
        while self.curr_char != None:

            # look for numbers
            if self.curr_char.isnumeric(): 
                num = ""
                # get more numbers
                while self.curr_char.isnumeric():
                    num += self.curr_char
                    self.advance()
                    # if you get a division operator, add it to the current number
                    if self.curr_char == "/":
                        num += self.curr_char
                        self.advance()
                # if our number has a division op, its a real
                if '/' in num:
                    tokens.append(Token('real_literal', real_literal, num))
                # if it doesn't, its a natural
                else:
                    tokens.append(Token('natural_literal', natural_literal, num))

            # look for single quote
            elif self.curr_char == "\'" :
                char_char = ''
                self.advance()
                # if no ascii char has been added, output the empty char
                if self.curr_char == "\'":
                    tokens.append(Token('char_literal', char_literal, char_char))
                    self.advance()
                # if we get an ascii char that isn't escape...
                elif self.curr_char.isascii() and self.curr_char != '\\' and self.curr_char != '\'':
                    char_char += self.curr_char
                    self.advance()
                    # look for another single quote, and output the char
                    if self.curr_char == "\'":
                        tokens.append(Token('char_literal', char_literal, char_char))
                        self.advance()
                    else:   return self.lexError('Invalid character literal format')
                # if we get escape char...
                elif self.curr_char == '\\':
                    char_char += self.curr_char
                    self.advance()
                    # and the next character is one of these...
                    if self.curr_char == 't' or self.curr_char == 'b' or self.curr_char == 'n' or self.curr_char == 'r' or self.curr_char == 'f' or self.curr_char == '\'' or self.curr_char == '\"':
                            char_char += self.curr_char
                            self.advance()
                            # look for a single quote and output char
                            if self.curr_char == '\'':
                                tokens.append(Token('char_literal', char_literal, char_char))
                                self.advance()
                    # if it's one of these
                    elif self.curr_char == '\\':
                        self.advance()
                        # look for a single quote and output char
                        if self.curr_char == '\'':
                            tokens.append(Token('char_literal', char_literal, char_char))
                            self.advance()
                    else: return self.lexError('Invalid escape sequence format')
                else:   return self.lexError('Invalid character literal format')

            # look for double quote
            elif self.curr_char == "\"" :
                str_str = ""
                self.advance()
                # while we're reading ascii chars...
                while self.curr_char.isascii() and self.curr_char != "\"":
                    # if we get escape char...
                    if self.curr_char == "\\":
                        self.advance()
                        # look for one of these
                        if self.curr_char == 't' or self.curr_char == 'b' or self.curr_char == 'n' or self.curr_char == 'r' or self.curr_char == 'f' or self.curr_char == '\'' or self.curr_char == '\"' or self.curr_char == '\\':
                                self.advance()
                        else: return self.lexError('Invalid escape sequence format')
                    # if not, just keep adding ascii to the string
                    else: 
                        str_str += self.curr_char
                        self.advance() 
                # if we get double quote, output the whole string
                if self.curr_char == "\"":
                    tokens.append(Token('string_literal', string_literal, str_str))
                    self.advance()
                else:   return self.lexError('Invalid string literal format')

            # keywords can be letters and underscores
            elif self.curr_char.isalpha() or self.curr_char == "_":
                str_str = ""
                # so while we're reading those, add them to the keyword...
                while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                    str_str += self.curr_char 
                    self.advance()


                # (very janky function calling recognition ahead. please forgive the crusty nature of the following code. thank you.) 
                # if we get a left paren after out chars...



                # if self.curr_char == "(":
                #     self.advance()
                #     # and the next char is a '$'...
                #     if self.curr_char == "$":
                #         self.advance()
                #         # look for param name
                #         if self.curr_char.isalpha() or self.curr_char == "_":
                #             str_str = ""
                #             while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                #                 str_str += self.curr_char 
                #                 self.advance()
                #             # once param name is typed, if we get right paren, and the param we just found isn't a keyword, output the function call, and the parameter...
                #             if self.curr_char == ')' and str_str != "try" and str_str != "catch" and str_str != "loop" and str_str != "word" and str_str != "num" and str_str != "char" and str_str != "frac" and str_str != "bool" and str_str != "true" and str_str != "cap" and str_str != "START" and str_str != "STOP":
                #                 tokens.append(Token('function_call', function_call, None))
                #                 tokens.append(Token('param_dec', param_dec, None))
                #                 self.advance()
                #             else: return self.lexError("invalid function call")
                #         else: return self.lexError("invalid function call")
                #     # and if we get a right paren with no parameters inside, return just the function call
                #     elif self.curr_char == ")":
                #         tokens.append(Token('function_call', function_call, None))
                #         self.advance()
                #     else: return self.lexError("invalid function call")



                # keywords for various stuff:


                
                if str_str == "try":        tokens.append(Token('if_', if_, None)) # selection
                elif str_str == "catch":    tokens.append(Token('else_', else_, None)) # selection
                elif str_str == "loop":     tokens.append(Token('loop', loop, None)) # loop
                elif str_str == "word":     tokens.append(Token('string_keyword', string_keyword, None)) # strings
                elif str_str == "num":      tokens.append(Token('natural_keyword', natural_keyword, None)) # naturals
                elif str_str == "char":     tokens.append(Token('char_keyword', char_keyword, None)) # chars
                elif str_str == "frac":     tokens.append(Token('real_keyword', real_keyword, None)) # reals
                elif str_str == "bool":     tokens.append(Token('boolean_keyword', boolean_keyword, None))
                elif str_str == "nocap":    tokens.append(Token('bool_literal', bool_literal, 'true')) # bool_lit true
                elif str_str == "cap":      tokens.append(Token('bool_literal', bool_literal, 'false')) # bool_lit false
                elif str_str == "START":    tokens.append(Token('START', START, None))
                elif str_str == "STOP":    tokens.append(Token('STOP', STOP, None))
                # if it's none of any of that, its an variable identifier
                else:
                    tokens.append(Token('ident', ident, None))


            # not keywords or idents, not literals, so special characters.
            else:
                # all special characters and character patterns
                match self.curr_char:
                    case '#':
                        while self.curr_char != '\n' and self.curr_char != None:
                            self.advance()
                    case '+': tokens.append(Token('add_op', add_op, None)), self.advance()
                    case '-': tokens.append(Token('sub_op', sub_op, None)), self.advance()
                    case '*': tokens.append(Token('mult_op', mult_op, None)), self.advance()
                    case '/': tokens.append(Token('div_op', div_op, None)), self.advance()
                    case '^': tokens.append(Token('exp_op', exp_op, None)), self.advance()
                    case '(': tokens.append(Token('left_paren', left_paren, None)), self.advance()
                    case ')': tokens.append(Token('right_paren', right_paren, None)), self.advance()
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token('greater_than_equal', greater_than_equal, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token('greater_than', greater_than, None))
                    case '<':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token('less_than_equal', less_than_equal, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token('less_than', less_than, None))
                    case '=':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token('equal_to', equal_to, None))
                            self.advance()
                        else:
                            tokens.append(Token('assign_op', assign_op, None))
                    case '!':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == "=":
                                tokens.append(Token('not_equal_to', not_equal_to, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token('logical_not', logical_not, None))
                    case '&': tokens.append(Token('logical_and',logical_and, None)), self.advance()
                    case '?': tokens.append(Token('logical_or',logical_or, None)), self.advance()
                    case ';': tokens.append(Token('semicolon', semicolon, None)), self.advance()
                    case '{': tokens.append(Token('left_brack', left_brack, None)), self.advance()
                    case '}': tokens.append(Token('right_brack', right_brack, None)), self.advance()
                    case ',': tokens.append(Token('comma', comma, None)), self.advance()
                    case '[': tokens.append(Token('left_brace', left_brace, None)), self.advance()
                    case ']': tokens.append(Token('right_brace', right_brace, None)), self.advance()
                    case '$': 
                        str_str += self.curr_char 
                        self.advance()
                        while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                            str_str += self.curr_char 
                            self.advance()
                        tokens.append(Token('param_dec', param_dec, None))

                    case ' ': self.advance()
                    case '\t': self.advance()
                    case '\n': self.advance()
                    case _: return self.lexError("ion know, its one of these")
        return tokens
        
    # error function that takes a hand-typed message from yours truly :)
    def lexError(self, invalid_char):
        self.invalid_char = invalid_char
        return f'Lexical Error: {invalid_char}'



####################### RUNNER #######################
# run this bih
def run(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    return tokens