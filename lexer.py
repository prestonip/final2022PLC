####################### TOKENS #######################


class Token():
    def __init__(self, type_, code, value):
        self.type = type_
        self.code = code
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

real_literal = 0 #fractional number
natural_literal = 1     #whole numbers and 0
bool_literal = 2
char_literal = 3 #single ascii character including escape character (java rules)
string_literal = 4 # any number of ascii characters including escape characters


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

            # real and natural literals
            if self.curr_char.isnumeric(): 
                num = ""
                while self.curr_char.isnumeric():
                    num += self.curr_char
                    self.advance()
                    if self.curr_char == "/":
                        num += self.curr_char
                        self.advance()
                if '/' in num:
                    tokens.append(Token('real_literal', real_literal, num))
                else:
                    tokens.append(Token('natural_literal', natural_literal, num))

            # char literals
            elif self.curr_char == "\'" :
                char_char = ''
                self.advance()
                if self.curr_char == "\'":
                    tokens.append(Token('char_literal', char_literal, char_char))
                    self.advance()
                elif self.curr_char.isascii() and self.curr_char != '\\' and self.curr_char != '\'':
                    char_char += self.curr_char
                    self.advance()
                    if self.curr_char == "\'":
                        tokens.append(Token('char_literal', char_literal, char_char))
                        self.advance()
                    else:   return self.lexError('Invalid character literal format')
                elif self.curr_char == '\\':
                    char_char += self.curr_char
                    self.advance()
                    if self.curr_char == 't' or self.curr_char == 'b' or self.curr_char == 'n' or self.curr_char == 'r' or self.curr_char == 'f' or self.curr_char == '\'' or self.curr_char == '\"':
                            char_char += self.curr_char
                            self.advance()
                            if self.curr_char == '\'':
                                tokens.append(Token('char_literal', char_literal, char_char))
                                self.advance()
                    elif self.curr_char == '\\':
                        self.advance()
                        if self.curr_char == '\'':
                            tokens.append(Token('char_literal', char_literal, char_char))
                            self.advance()
                    else: return self.lexError('Invalid escape sequence format')
                else:   return self.lexError('Invalid character literal format')

            # string literals
            elif self.curr_char == "\"" :
                str_str = ""
                self.advance()
                while self.curr_char.isascii() and self.curr_char != "\"":
                    if self.curr_char == "\\":
                        self.advance()
                        if self.curr_char == 't' or self.curr_char == 'b' or self.curr_char == 'n' or self.curr_char == 'r' or self.curr_char == 'f' or self.curr_char == '\'' or self.curr_char == '\"' or self.curr_char == '\\':
                                self.advance()
                        else: return self.lexError('Invalid escape sequence format')
                    else: 
                        str_str += self.curr_char
                        self.advance() 
                if self.curr_char == "\"":
                    tokens.append(Token('string_literal', string_literal, str_str))
                    self.advance()
                else:   return self.lexError('Invalid string literal format')

            # keywords
            elif self.curr_char.isalpha() or self.curr_char == "_":
                str_str = ""
                while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                    str_str += self.curr_char 
                    self.advance()
                if self.curr_char == "(":
                    self.advance()
                    if self.curr_char == "$":
                        self.advance()
                        if self.curr_char.isalpha() or self.curr_char == "_":
                            str_str = ""
                            while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                                str_str += self.curr_char 
                                self.advance()
                            if self.curr_char == ')' and str_str != "try" and str_str != "catch" and str_str != "loop" and str_str != "word" and str_str != "num" and str_str != "char" and str_str != "frac" and str_str != "bool" and str_str != "true" and str_str != "cap" and str_str != "START" and str_str != "STOP":
                                tokens.append(Token('function_call', function_call, None))
                                tokens.append(Token('param_dec', param_dec, None))
                                self.advance()
                            else: return self.lexError("invalid function call")
                        else: return self.lexError("invalid function call")
                    elif self.curr_char == ")":
                        tokens.append(Token('function_call', function_call, None))
                        self.advance()
                    else: return self.lexError("invalid function call")
                elif str_str == "try":        tokens.append(Token('if_', if_, None)) # selection
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
                else:                       
                    tokens.append(Token('ident', ident, None))

            # all other tokens conditions
            else:    
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
                    # case '$': tokens.append(Token(param_dec), self.advance()
                    case ' ': self.advance()
                    case '\t': self.advance()
                    case '\n': self.advance()
                    case _: return self.lexError(self.curr_char)
        return tokens
        
    def lexError(self, invalid_char):
        self.invalid_char = invalid_char
        return f'Lexical Error: {invalid_char}'



####################### RUNNER #######################

def run(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    return tokens