from enum import Enum
from enum import auto
####################### TOKENS #######################


real_literal = 'real_literal' #fractional number
natural_literal = 'natural_literal'     #whole numbers and 0
bool_literal = 'bool_literal'
char_literal = 'char_literal' #single ascii character including escape character (java rules)
string_literal = 'string_literal' # any number of ascii characters including escape characters

# tab = 10
# backspace = 11
# newline = 12
# c_return = 13
# form_feed = 14
# single_quote = 15
# double_quote = 16
# backslash = 17

assign_op           = 'assign_op'
add_op              = 'add_op'
sub_op              = 'sub_op'
mult_op             = 'mult_op'
div_op              = 'div_op'
exp_op              = 'exp_op'
left_paren          = 'left_paren'
right_paren         = 'right_paren'
mod_op              = 'mod_op'
semicolon           = 'semicolon'
left_brack          = 'left_brack'
right_brack         = 'right_brack'
less_than           = 'less_than'
greater_than        = 'greater_than'
less_than_equal     = 'less_than_equal'
greater_than_equal  = 'greater_than_equal'
equal_to            = 'equal_to'
not_equal_to        = 'not_equal_to'
logical_and         = 'logical_and'
logical_or          = 'logical_or'
logical_not         = 'logical_not'
u_neg_op            = 'u_neg_op'
comma               = 'comma'
left_brace          = 'left_brace'
right_brace         = 'right_brace'
param_dec           = 'param_dec'

string_keyword = 'string_keyword' #string keyword
natural_keyword = 'natural_keyword' #natural keyword
char_keyword = 'char_keyword' # char keyword
real_keyword = 'real_keyword' #real keyword
boolean_keyword = 'boolean_keyword' #boolean keyword
function_call = 'function_call'
ident = 'ident'

if_ = 'if_'
else_ = 'else_'
loop = 'loop'

nocap = 'nocap'
cap = 'cap'

START = 'START'
STOP = 'STOP'




####################### LEXER #######################


class Token():
    def __init__(self, type_, code, value):
        self.type = type_
        self.code = code
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'


    
    # real_literal = 0 #fractional number
    # natural_literal = 1     #whole numbers and 0
    # bool_literal_t = 2
    # bool_literal_f = 3
    # char_literal = 4 #single ascii character including escape character (java rules)
    # string_literal = 5 # any number of ascii characters including escape characters

    # # tab = 10
    # # backspace = 11
    # # newline = 12
    # # c_return = 13
    # # form_feed = 14
    # # single_quote = 15
    # # double_quote = 16
    # # backslash = 17

    # assign_op           = 20
    # add_op              = 21
    # sub_op              = 22
    # mult_op             = 23
    # div_op              = 24
    # exp_op              = 25
    # left_paren          = 26
    # right_paren         = 27
    # mod_op              = 28
    # semicolon           = 29
    # left_brack          = 30
    # right_brack         = 31
    # less_than           = 32
    # greater_than        = 33
    # less_than_equal     = 34
    # greater_than_equal  = 35
    # equal_to            = 36
    # not_equal_to        = 37
    # logical_and         = 38
    # logical_or          = 39
    # logical_not         = 40
    # u_neg_op            = 41
    # comma               = 42
    # left_brace          = 43
    # right_brace         = 44
    # param_dec           = 45

    # string_keyword = 50 #string keyword
    # natural_keyword = 51 #natural keyword
    # char_keyword = 52 # char keyword
    # real_keyword = 53 #real keyword
    # boolean_keyword = 54 #boolean keyword
    # function_call = 55
    # ident = 56

    # if_ = 60
    # else_ = 61
    # loop = 62

    # nocap = 70
    # cap = 71

    # START = 100
    # STOP = 99
        


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
                    tokens.append(Token(real_literal, real_literal, num))
                else:
                    tokens.append(Token(natural_literal, natural_literal, num))

            # char literals
            elif self.curr_char == "\'" :
                char_char = ''
                self.advance()
                if self.curr_char == "\'":
                    tokens.append(Token(char_literal, char_literal, char_char))
                    self.advance()
                elif self.curr_char.isascii() and self.curr_char != '\\' and self.curr_char != '\'':
                    char_char += self.curr_char
                    self.advance()
                    if self.curr_char == "\'":
                        tokens.append(Token(char_literal, char_literal, char_char))
                        self.advance()
                    else:   return self.lexError('Invalid character literal format')
                elif self.curr_char == '\\':
                    char_char += self.curr_char
                    self.advance()
                    if self.curr_char == 't' or self.curr_char == 'b' or self.curr_char == 'n' or self.curr_char == 'r' or self.curr_char == 'f' or self.curr_char == '\'' or self.curr_char == '\"':
                            char_char += self.curr_char
                            self.advance()
                            if self.curr_char == '\'':
                                tokens.append(Token(char_literal, char_literal, char_char))
                                self.advance()
                    elif self.curr_char == '\\':
                        self.advance()
                        if self.curr_char == '\'':
                            tokens.append(Token(char_literal, char_literal, char_char))
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
                    tokens.append(Token(string_literal, string_literal, str_str))
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
                                tokens.append(Token(function_call, function_call, None))
                                tokens.append(Token(param_dec, param_dec, None))
                                self.advance()
                            else: return self.lexError("invalid function call")
                        else: return self.lexError("invalid function call")
                    elif self.curr_char == ")":
                        tokens.append(Token(function_call, function_call, None))
                        self.advance()
                    else: return self.lexError("invalid function call")
                elif str_str == "try":        tokens.append(Token(if_, if_, None)) # selection
                elif str_str == "catch":    tokens.append(Token(else_, else_, None)) # selection
                elif str_str == "loop":     tokens.append(Token(loop, loop, None)) # loop
                elif str_str == "word":     tokens.append(Token(string_keyword)) # strings
                elif str_str == "num":      tokens.append(Token(natural_keyword, natural_keyword, None)) # naturals
                elif str_str == "char":     tokens.append(Token(char_keyword, char_keyword, None)) # chars
                elif str_str == "frac":     tokens.append(Token(real_keyword, real_keyword, None)) # reals
                elif str_str == "bool":     tokens.append(Token(boolean_keyword, boolean_keyword, None))
                elif str_str == "nocap":    tokens.append(Token(bool_literal, bool_literal, 'true')) # bool_lit true
                elif str_str == "cap":      tokens.append(Token(bool_literal, bool_literal, 'false')) # bool_lit false
                elif str_str == "START":    tokens.append(Token(START, START, None))
                elif str_str == "STOP":    tokens.append(Token(STOP, STOP, None))
                else:                       
                    tokens.append(Token(ident, ident, None))

            # all other tokens conditions
            else:    
                match self.curr_char:
                    case '#':
                        while self.curr_char != '\n' and self.curr_char != None:
                            self.advance()
                    case '+': tokens.append(Token(add_op, add_op, None)), self.advance()
                    case '-': tokens.append(Token(sub_op, sub_op, None)), self.advance()
                    case '*': tokens.append(Token(mult_op, mult_op, None)), self.advance()
                    case '/': tokens.append(Token(div_op, div_op, None)), self.advance()
                    case '^': tokens.append(Token(exp_op, exp_op, None)), self.advance()
                    case '(': tokens.append(Token(left_paren, left_paren, None)), self.advance()
                    case ')': tokens.append(Token(right_paren, right_paren, None)), self.advance()
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token(greater_than_equal, greater_than_equal, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(greater_than, greater_than, None))
                    case '<':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token(less_than_equal, less_than_equal, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(less_than, less_than, None))
                    case '=':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(equal_to, equal_to, None))
                            self.advance()
                        else:
                            tokens.append(Token(assign_op, assign_op, None))
                    case '!':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == "=":
                                tokens.append(Token(not_equal_to, sub_op, None))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(logical_not, logical_not, None))
                    case '&': tokens.append(Token(logical_and,logical_and, None)), self.advance()
                    case '?': tokens.append(Token(logical_or,logical_or, None)), self.advance()
                    case '~': tokens.append(Token(u_neg_op, u_neg_op, None)), self.advance()
                    case ';': tokens.append(Token(semicolon, semicolon, None)), self.advance()
                    case '{': tokens.append(Token(left_brack, left_brack, None)), self.advance()
                    case '}': tokens.append(Token(right_brack, right_brack, None)), self.advance()
                    case ',': tokens.append(Token(comma, comma, None)), self.advance()
                    case '[': tokens.append(Token(left_brace, left_brace, None)), self.advance()
                    case ']': tokens.append(Token(right_brace, right_brace, None)), self.advance()
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