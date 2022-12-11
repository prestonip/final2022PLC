'''
S --> 'START' <stmt_list> 'STOP'
<stmt_list> --> <stmt>
<stmt> --> <var_stmt> | <select_stmt> | <loop_stmt> | <block> | <function_definition>
<var_stmt> --> ident { '=' { '-' } <expr> }
<select_stmt> -->  'if' '(' <bool_inc> ')' <block> [ 'else' <block> ]
<loop_stmt> -->  'loop' '(' <bool_inc> ')' <block> 
<func_def> --> function_call { param_dec }
<block> --> '{' { <stmt> } '}'

<expr> --> <term> { ('+'|'-') <term> }
<term> --> <factor> { ('*'|'/'|'%') <factor> }
<factor> --> ident | natural_lit | real_lit | bool_lit | char_lit | string_lit | '(' <expr> ')'

<bool_inc> --> <bool_eval> { ('&'|'?'|'!') <bool_eval> }
<bool_eval> --> <bool_expr> { ('>'|'<'|'>o='|'<o='|'=='|'!==') <bool_expr>}
<bool_expr> --> <bool_term> { ('*'|'/'|'%') <bool_term> }
<bool_term> --> <bool_factor> { ('+'|'-') <bool_factor> }
<bool_factor> --> ident | real_lit | natural_lit | bool_lit | char_lit | string_lit | function_call
'''