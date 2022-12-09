####################### TOKENS #######################

DIGITS              = '0123456789'
ALPHAS              = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
INT_LIT               = 'INT_LIT'
INT_LIT_1             = 'INT_LIT_1'
INT_LIT_2             = 'INT_LIT_2'
INT_LIT_4             = 'INT_LIT_4'
INT_LIT_8             = 'INT_LIT_8'

# FLOAT_LIT           = 'FLOAT_LIT'
IDENT               = 'IDENT'



YOINKY              = 'YOINKY' # start of program
SPLOINKY            = 'SPLOINKY' #end of program

NOCAP               = 'NOCAP' # true boolean keyword
CAP                 = 'CAP' # false keyword
AND                 = 'AND'
OR                  = 'OR'

MAYBE               = 'MAYBE' # if keyword
ACTUALLY            = 'ACTUALLY'  # else keyword
LOOP                = 'LOOP' # loop keyword


real_literal = 0 #fractional number
natural_literal = 1     #whole numbers and 0
bool_literal = 2
char_literal = 3 #single ascii character including escape character (java rules)
string_literal = 4 # any number of ascii characters including escape characters

# tab = 10
# backspace = 11
# newline = 12
# c_return = 13
# form_feed = 14
# single_quote = 15
# double_quote = 16
# backslash = 17

assign_op           = 20
add_op              = 21
sub_op              = 22
mult_op             = 23
div_op              = 24
exp_op              = 25
left_paren          = 26
right_paren         = 27
mod_op              = 28
semicolon           = 29
left_brack          = 30
right_brack         = 31
# DOT                 3 '.'
less_than           = 32
greater_than        = 33
less_than_equal     = 34
greater_than_equal  = 35
equal_to            = 36
not_equal_to        = 37
logical_and         = 38
logical_or          = 39
logical_not         = 40
u_neg_op            = 41
comma               = 42
left_brace          = 43
right_brace         = 44

string = 50 #string keyword
natural = 51 #natural keyword
char = 52 # char keyword
real = 53 #real keyword
boolean = 54 #boolean keyword
ident = 55

if_ = 60
else_ = 61
loop = 62

nocap = 70
cap = 71




####################### LEXER #######################


class Token:
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return f'{self.code}'
        


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
                    while self.curr_char.isnumeric():
                        num += self.curr_char
                        self.advance()
                    if self.curr_char == " ":
                        tokens.append(Token(natural_literal)) # returns 0
                else:
                    tokens.append(Token(real_literal))

            # char literals
            elif self.curr_char == "\'" :
                self.advance()
                if self.curr_char == "\'":
                    tokens.append(Token(char_literal))
                    self.advance()
                elif self.curr_char.isascii() and self.curr_char != '\\' and self.curr_char != '\'':
                    self.advance()
                    if self.curr_char == "\'":
                        tokens.append(Token(char_literal))
                        self.advance()
                    else:   return self.lexError('Invalid character literal format')
                if self.curr_char == '\\':
                    self.advance()
                    match self.curr_char:
                        case 't', 'b', 'n', 'r', 'f', '\'', '\"', '\\':
                            self.advance()
                            if self.curr_char == '\'':
                                tokens.append(Token(char_literal))
                                self.advance()
                        case _:
                            return self.lexError('Invalid escape sequence format')
                else:   return self.lexError('Invalid character literal format')

            # string literals
            elif self.curr_char == "\"" :
                self.advance()
                while self.curr_char.isascii() and self.curr_char != "\"":
                    if self.curr_char == '\\':
                        self.advance()
                        match self.curr_char:
                            case 't', 'b', 'n', 'r', 'f', '\'', '\"', '\\':
                                self.advance()
                                if self.curr_char == '\'':
                                    self.advance()
                            case _:
                                return self.lexError('Invalid escape sequence format')
                    else: self.advance() 
                if self.curr_char == "\"":
                    tokens.append(Token(string_literal))
                    self.advance()
                else:   return self.lexError('Invalid string literal format')

            # keywords
            elif self.curr_char.isalpha() or self.curr_char == "_":
                str_str = ""
                while self.curr_char != None and (self.curr_char.isalpha() or self.curr_char == "_"):
                    str_str += self.curr_char 
                    self.advance()
                if str_str == "try":        tokens.append(Token(if_)) # selection
                elif str_str == "catch":    tokens.append(Token(else_)) # selection
                elif str_str == "loop":     tokens.append(Token(loop)) # loop
                elif str_str == "word":     tokens.append(Token(string)) # strings
                elif str_str == "num":      tokens.append(Token(natural)) # naturals
                elif str_str == "char":     tokens.append(Token(char)) # chars
                elif str_str == "frac":     tokens.append(Token(real)) # reals
                elif str_str == "nocap":    tokens.append(Token(nocap)) # bool_lit true
                elif str_str == "cap":      tokens.append(Token(cap)) # bool_lit false
                else:                       tokens.append(ident)

            # all other tokens conditions
            else:    
                match self.curr_char:
                    case '#':
                        while self.curr_char != '\n' and self.curr_char != None:
                            self.advance()
                    case '+': tokens.append(Token(add_op)), self.advance()
                    case '-': tokens.append(Token(sub_op)), self.advance()
                    case '*': tokens.append(Token(mult_op)), self.advance()
                    case '/': tokens.append(Token(div_op)), self.advance()
                    case '^': tokens.append(Token(exp_op)), self.advance()
                    case '(': tokens.append(Token(left_paren)), self.advance()
                    case ')': tokens.append(Token(right_paren)), self.advance()
                    case '>':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token(greater_than_equal))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(greater_than))
                    case '<':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == '=':
                                tokens.append(Token(less_than_equal))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(less_than))
                    case '=':
                        self.advance()
                        if self.curr_char == '=':
                            tokens.append(Token(equal_to))
                            self.advance()
                        else:
                            tokens.append(Token(assign_op))
                    case '!':
                        self.advance()
                        if self.curr_char == '=':
                            self.advance()
                            if self.curr_char == "=":
                                tokens.append(Token(not_equal_to))
                                self.advance()
                            else:
                                return self.lexError("Invalid char " + self.curr_char)
                        else:
                            tokens.append(Token(logical_not))
                    case '~': tokens.append(Token(u_neg_op))
                    case ';': tokens.append(Token(semicolon)), self.advance()
                    case '{': tokens.append(Token(left_brack)), self.advance()
                    case '}': tokens.append(Token(right_brack)), self.advance()
                    case ',': tokens.append(Token(comma)), self.advance()
                    case '[': tokens.append(Token(left_brace)), self.advance()
                    case ']': tokens.append(Token(right_brace)), self.advance()
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