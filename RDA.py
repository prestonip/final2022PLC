'''
S --> 'START' <stmt_list> 'STOP'
<stmt_list> --> <stmt>
<stmt> --> <var_stmt> | <select_stmt> | <loop_stmt> | <block> | <function_definition>
<var_stmt> --> ident { '=' { '-' } <expr> }
<select_stmt> -->  'if' '(' <bool_inc> ')' <block> [ 'else' <block> ]
<loop_stmt> -->  'loop' '(' <bool_inc> ')' <block> 
<func_def> --> ident '(' { param_dec } ')' <block>
<block> --> '{' { <stmt> } '}'

<expr> --> <term> { ('+'|'-') <term> }
<term> --> <factor> { ('*'|'/'|'%'|'^') <factor> }
<factor> --> ident | natural_lit | real_lit | bool_lit | char_lit | string_lit | '(' <expr> ')'

<bool_inc> --> <bool_eval> { ('&'|'?'|'!') <bool_eval> }
<bool_eval> --> <bool_expr> { ('>'|'<'|'>o='|'<o='|'=='|'!==') <bool_expr>}
<bool_expr> --> <bool_term> { ('*'|'/'|'%'|'^') <bool_term> }
<bool_term> --> <bool_factor> { ('+'|'-') <bool_factor> }
<bool_factor> --> ident | real_lit | natural_lit | bool_lit | char_lit | string_lit
'''




####################### PARSER #######################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.curr_token = tokens[self.pos]
    
    def advance(self):
        self.pos += 1 
        self.curr_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        return self.curr_token

    # S --> 'START' <stmt_list> 'STOP'
    def start(self):
        if self.curr_token.type == 'START':
            self.advance()
            self.stmt_list()
            self.end()
        else:
            self.syntaxError('start')


    # <stmt_list> --> <stmt>
    def stmt_list(self):
        while self.curr_token.type == 'ident' or self.curr_token.type == 'string_keyword' or self.curr_token.type == 'natural_keyword' or self.curr_token.type == 'boolean_keyword' or self.curr_token.type == 'char_keyword' or self.curr_token.type == 'real_keyword' or self.curr_token.type == 'if_' or self.curr_token.type == 'loop' or self.curr_token.type == 'left_brack':
            self.stmt()


    # <stmt> --> <var_stmt> | <select_stmt> | <loop_stmt> | <block> | <function_definition>
    def stmt(self):
        match self.curr_token.type:
            case 'ident':               self.var_stmt()
            case 'string_keyword':      self.var_stmt()
            case 'natural_keyword':     self.var_stmt()
            case 'char_keyword':        self.var_stmt()
            case 'real_keyword':        self.var_stmt()
            case 'boolean_keyword':     self.var_stmt()
            case 'if_':                 self.select_stmt()
            case 'loop':                self.loop_stmt()
            case 'left_brack':          self.block()
            case _:             pass

    # <func_def> --> ident '(' { param_dec } ')' <block>
    def func_def(self):
        if self.curr_token.type == 'left_paren':
            self.advance()
            while self.curr_token.type == 'param_dec':
                self.advance()
                if self.curr_token.type == 'comma':
                    self.advance()
            if self.curr_token.type == 'right_paren':
                self.advance()
                if self.curr_token.type == 'left_brack':
                    self.block()

    # <var_stmt> --> ident { '=' { '-' } <expr> } | { <func_def> } ';'
    def var_stmt(self):
        if self.curr_token.type == 'string_keyword' or self.curr_token.type == 'natural_keyword' or self.curr_token.type == 'char_keyword' or self.curr_token.type == 'real_keyword' or self.curr_token.type == 'boolean_keyword':
            self.advance()
            if self.curr_token.type != 'ident':
                self.syntaxError('no ident after keyword')
        while self.curr_token.type == 'ident':
            self.advance()
            if self.curr_token.type == 'assign_op': 
                self.advance()
                if self.curr_token.type == 'sub_op':
                    self.advance()
                    self.expr()
                    if self.curr_token.type == 'semicolon':
                        self.advance()
                    else:
                        self.syntaxError('stmt')
                else:
                    self.expr()
                    if self.curr_token.type == 'semicolon':
                        self.advance()
                    else: 
                        self.syntaxError('stmt')
            elif self.curr_token.type == 'left_paren':
                self.func_def()
            else:
                self.syntaxError('stmt')


    # <expr> --> <term> { ('+'|'-') <term> }
    def expr(self):
        self.term()
        while self.curr_token.type == 'add_op' or self.curr_token.type == 'sub_op':
            self.advance()
            self.term()

    # <term> --> <factor> { ('*'|'/'|'%'|'^') <factor> }
    def term(self):
        self.factor()
        while self.curr_token.type == 'mult_op' or self.curr_token.type == 'div_op' or self.curr_token.type == 'mod_op' or self.curr_token.type == 'exp_op':
            self.advance()
            self.factor()

    # <factor> --> ident | natural_lit | real_lit | bool_lit | char_lit | string_lit | '(' <expr> ')'
    def factor(self):
        if self.curr_token.type == 'ident' or self.curr_token.type == 'natural_literal' or self.curr_token.type == 'real_literal' or self.curr_token.type == 'bool_literal' or self.curr_token.type == 'char_literal' or self.curr_token.type == 'string_literal':
            self.advance()
        elif self.curr_token.type == 'left_paren':
            self.advance()
            if self.curr_token.type == 'sub_op':
                self.advance()
                self.expr()
            else:
                self.expr()
            if self.curr_token.type == 'right_paren':
                self.advance()
            else: 
                self.syntaxError('factor')
        else: 
            self.syntaxError('factor')

    # <select_stmt> -->  'if' '(' <bool_inc> ')' <block> [ 'else' <block> ]
    def select_stmt(self):
        if self.curr_token.type == 'if_':
            self.advance()
            if self.curr_token.type == 'left_paren':
                self.advance()
                self.bool_inc()
                if self.curr_token.type == 'right_paren':
                    self.advance()
                    self.block()
                    while self.curr_token.type == 'else_':
                        self.advance()
                        self.block()
                else:
                    self.syntaxError('select')
            else:
                self.syntaxError('select')
        else: 
            self.syntaxError('select')

    # <loop_stmt> -->  'loop' '(' <bool_inc> ')' <block> 
    def loop_stmt(self):
        if self.curr_token.type == 'loop':
            self.advance()
            if self.curr_token.type == 'left_paren':
                self.advance()
                self.bool_inc()
                if self.curr_token.type == 'right_paren':
                    self.advance()
                    self.block()
                else:
                    self.syntaxError('loop')
            else:
                self.syntaxError('loop')
        else:
            self.syntaxError('loop')


    # <bool_inc> --> <bool_eval> { ('&'|'?'|'!') <bool_eval> }
    def bool_inc(self):
        self.bool_eval()
        while self.curr_token.type == 'logical_and' or self.curr_token.type == 'logical_or' or self.curr_token.type == 'logical_not':
            self.advance()
            self.bool_eval()

    # <bool_eval> --> <bool_expr> { ('>'|'<'|'>o='|'<o='|'=='|'!==') <bool_expr>}
    def bool_eval(self):
        self.bool_expr()
        while self.curr_token.type == 'greater_than' or self.curr_token.type == 'less_than' or self.curr_token.type == 'greater_than_equal' or self.curr_token.type == 'less_than_equal' or self.curr_token.type == 'equal_to' or self.curr_token.type == 'not_equal_to':
            self.advance()
            self.bool_expr()

    # <bool_expr> --> <bool_term> { ('*'|'/'|'%'|'^') <bool_term> }
    def bool_expr(self):
        self.bool_term()
        while self.curr_token.type == 'add_op' or self.curr_token.type == 'sub_op':
            self.advance()
            self.bool_term()

    # <bool_term> --> <bool_factor> { ('+'|'-') <bool_factor> }
    def bool_term(self):
        self.bool_factor()
        while self.curr_token.type == 'mutl_op' or self.curr_token.type == 'div_op' or self.curr_token.type == 'mod_op' or self.curr_token.type == 'exp_op':
            self.advance()
            self.bool_factor()

    # <bool_factor> --> ident | real_lit | natural_lit | bool_lit | char_lit | string_lit 
    def bool_factor(self):
        if self.curr_token.type == 'ident' or self.curr_token.type == 'natural_literal' or self.curr_token.type == 'real_literal' or self.curr_token.type == 'boolean_lit':
            self.advance()
        else:
            self.syntaxError('bool factor')

    
    # <block> --> '{' { <stmt> } '}'
    def block(self):
        if self.curr_token.type == 'left_brack':
            self.advance()
            while self.curr_token.type == 'if_' or self.curr_token.type == 'loop' or self.curr_token.type == 'ident' or self.curr_token.type == 'left_brack':
                self.stmt_list()
            if self.curr_token.type == 'right_brack':
                self.advance()
            else:
                self.syntaxError('block')
        else:
            self.syntaxError('block')    

    # end statement
    def end(self):
        if self.curr_token.type == 'STOP':
            print('BASED CODE')
        else:
            self.syntaxError('end') 

    def syntaxError(self, type):
        print(type + ' error')
    