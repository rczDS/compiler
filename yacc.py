import re
import ply.yacc as yacc
from compiler.lex import tokens, identifier
from compiler.AST import ASTInternalNode
from compiler.AST import ASTExternalNode

reserved_1 = ['true', 'false']


def p_start_unit(p):
    """ start_unit : all_declaration
                   | start_unit all_declaration """
    p[0] = ASTInternalNode('start_unit', p[1:])


def p_all_declaration(p):
    """ all_declaration : func_declaration 
                        | var_declaration """
    p[0] = ASTInternalNode('all_declaration', p[1:])


def p_var_declaration(p):
    """ var_declaration : declaration_specifiers ';'
                        | declaration_specifiers init_declarator_list ';' """
    p[0] = ASTInternalNode('var_declaration', p[1:])


def p_init_declarator_list(p):
    """ init_declarator_list : init_declarator
                             | init_declarator_list ',' init_declarator """
    p[0] = ASTInternalNode('init_declarator_list', p[1:])


def p_init_declarator(p):
    """ init_declarator : declarator
                        | declarator '=' init """
    p[0] = ASTInternalNode('init_declarator', p[1:])


def p_declaration_specifiers(p):
    """ declaration_specifiers : type_specifier
                              | type_specifier declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers
                              | func_specifier
                              | func_specifier declaration_specifiers """
    p[0] = ASTInternalNode('declaration_specifiers', p[1:])


def p_type_specifier(p):
    """ type_specifier : VOID
                       | CHAR
                       | INT
                       | DOUBLE
                       | BOOL """
    p[0] = ASTInternalNode('type_specifier', p[1:])


def p_type_qualifier(p):
    """ type_qualifier : CONST
                       | RESTRICT
                       | VOLATILE """
    p[0] = ASTInternalNode('type_qualifier', p[1:])


def p_type_qualifier_list(p):
    """ type_qualifier_list : type_qualifier
                            | type_qualifier type_qualifier_list """
    p[0] = ASTInternalNode('type_qualifier_list', p[1:])


def p_func_specifier(p):
    """ func_specifier : INLINE """
    p[0] = ASTInternalNode('func_specifier', p[1:])


def p_specifier_qualifier_list(p):
    """ specifier_qualifier_list : type_specifier specifier_qualifier_list
                                 | type_specifier
                                 | type_qualifier specifier_qualifier_list
                                 | type_qualifier  """
    p[0] = ASTInternalNode('specifier_qualifier_list', p[1:])


def p_declarator(p):
    """ declarator : pointer direct_declarator
                   | direct_declarator """
    p[0] = ASTInternalNode('declarator', p[1:])


def p_pointer(p):
    """ pointer : '*'
                | '*' type_qualifier_list
                | '*' pointer
                | '*' type_qualifier_list pointer """
    p[0] = ASTInternalNode('pointer', p[1:])


def p_direct_declarator(p):
    """ direct_declarator : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' type_qualifier_list assignment_expr ']'
                        | direct_declarator '[' type_qualifier_list ']'
                        | direct_declarator '[' assignment_expr ']'
                        | direct_declarator '[' STATIC type_qualifier_list assignment_expr ']'
                        | direct_declarator '[' type_qualifier_list STATIC assignment_expr ']'
                        | direct_declarator '[' type_qualifier_list '*' ']'
                        | direct_declarator '[' '*' ']'
                        | direct_declarator '[' ']'
                        | direct_declarator '(' parameter_list ')'
                        | direct_declarator '(' identifier_list ')'
                        | direct_declarator '(' ')' """
    if len(p) == 2 and not p[1] in reserved_1:
        p[1] = ASTExternalNode('IDENTIFIER', p[1])
    p[0] = ASTInternalNode('direct_declarator', p[1:])


def p_identifier_list(p):
    """ identifier_list : IDENTIFIER
                        | identifier_list ',' IDENTIFIER """
    if len(p) == 2 and not p[1] in reserved_1:
        p[1] = ASTExternalNode('IDENTIFIER', p[1])
    elif len(p) == 4 and not p[3] in reserved_1:
        p[3] = ASTExternalNode('IDENTIFIER', p[3])
    p[0] = ASTInternalNode('identifier_list', p[1:])


def p_assignment_expr(p):
    """ assignment_expr : conditional_expr
                        | unary_expr assignment_op assignment_expr """
    p[0] = ASTInternalNode('assignment_expr', p[1:])


def p_assignment_op(p):
    """ assignment_op : '='
                      | MUL_ASSIGN
                      | DIV_ASSIGN
                      | MOD_ASSIGN
                      | ADD_ASSIGN
                      | SUB_ASSIGN
                      | LEFT_ASSIGN
                      | RIGHT_ASSIGN
                      | AND_ASSIGN
                      | XOR_ASSIGN
                      | OR_ASSIGN """
    p[0] = ASTInternalNode('assignment_op', p[1:])


def p_constant_expr(p):
    """ constant_expr : conditional_expr """
    p[0] = ASTInternalNode('constant_expr', p[1:])


def p_conditional_expr(p):
    """ conditional_expr : logical_or_expr
                         | logical_or_expr '?' expr ':' conditional_expr """
    p[0] = ASTInternalNode('conditional_expr', p[1:])


# 逻辑 or 表达式
def p_logical_or_expr(p):
    """ logical_or_expr : logical_and_expr
                        | logical_or_expr OR_OP logical_and_expr """
    p[0] = ASTInternalNode('logical_or_expr', p[1:])


# 逻辑 and 表达式
def p_logical_and_expr(p):
    """ logical_and_expr : inclusive_or_expr
                         | logical_and_expr AND_OP inclusive_or_expr """
    p[0] = ASTInternalNode('logical_and_expr', p[1:])


# 或运算表达式（或运算）
def p_inclusive_or_expr(p):
    """ inclusive_or_expr : exclusive_or_expr
                          | inclusive_or_expr '|' exclusive_or_expr """
    p[0] = ASTInternalNode('inclusive_or_expr', p[1:])


# 异或运算表达式（异或运算）
def p_exclusive_or_expr(p):
    """ exclusive_or_expr : and_expr
                          | exclusive_or_expr '^' and_expr """
    p[0] = ASTInternalNode('exclusive_or_expr', p[1:])


# 与运算表达式（与运算）
def p_and_expr(p):
    """ and_expr : equality_expr
                 | and_expr '&' equality_expr """
    p[0] = ASTInternalNode('and_expr', p[1:])


# 等值判断表达式（相等、不等）
def p_equality_expr(p):
    """ equality_expr : relation_expr
                      | equality_expr EQ_OP relation_expr
                      | equality_expr NE_OP relation_expr """
    p[0] = ASTInternalNode('equality_expr', p[1:])


# 关系表达式（大于、小于、大于等于、小于等于）
def p_relation_expr(p):
    """ relation_expr : shift_expr
                      | relation_expr '<' shift_expr
                      | relation_expr '>' shift_expr
                      | relation_expr LE_OP shift_expr
                      | relation_expr GE_OP shift_expr """
    p[0] = ASTInternalNode('relation_expr', p[1:])


# 位移表达式（左移、右移）
def p_shift_expr(p):
    """ shift_expr : add_expr
                   | shift_expr LEFT_OP add_expr
                   | shift_expr RIGHT_OP add_expr """
    p[0] = ASTInternalNode('shift_expr', p[1:])


# 加法表达式（加减）
def p_add_expr(p):
    """ add_expr : mul_expr
                 | add_expr '+' mul_expr
                 | add_expr '-' mul_expr """
    p[0] = ASTInternalNode('add_expr', p[1:])


# 乘法表达式（乘除模）
def p_mul_expr(p):
    """ mul_expr : unary_expr
                 | mul_expr '*' unary_expr
                 | mul_expr '/' unary_expr
                 | mul_expr '%' unary_expr """
    p[0] = ASTInternalNode('mul_expr', p[1:])


def p_unary_expr(p):
    """ unary_expr : postfix_expr
                   | unary_op unary_expr
                   | INC_OP unary_expr
                   | DEC_OP unary_expr
                   | SIZEOF unary_expr
                   | SIZEOF '(' type_name ')' """
    p[0] = ASTInternalNode('unary_expr', p[1:])


def p_unary_op(p):
    """ unary_op : '&'
                 | '*'
                 | '+'
                 | '-'
                 | '~'
                 | '!' """
    p[0] = ASTInternalNode('unary_op', p[1:])


def p_postfix_expr(p):
    """ postfix_expr : primary_expr
                     | postfix_expr '[' expr ']'
                     | postfix_expr '(' ')'
                     | postfix_expr '(' argument_expr_list ')'
                     | postfix_expr '.' IDENTIFIER
                     | postfix_expr PTR_OP IDENTIFIER
                     | postfix_expr INC_OP
                     | postfix_expr DEC_OP
                     | '(' type_name ')' '{' init_list '}'
                     | '(' type_name ')' '{' init_list ',' '}' """
    if len(p) == 4 and not p[2] == '(' and not p[3] in reserved_1:
        p[3] = ASTExternalNode('IDENTIFIER', p[3])
    p[0] = ASTInternalNode('postfix_expr', p[1:])


def p_primary_expr(p):
    """ primary_expr : IDENTIFIER
                     | CONSTANT
                     | STRING_LITERAL
                     | '(' expr ')' """
    if re.match(r'(([_a-zA-Z])([0-9]|([_a-zA-Z]))*)', p[1]) and not p[1] in reserved_1:
        p[1] = ASTExternalNode('IDENTIFIER', str(p[1]))
    p[0] = ASTInternalNode('primary_expr', p[1:])


def p_expr(p):
    """ expr : assignment_expr
             | expr ',' assignment_expr """
    p[0] = ASTInternalNode('expr', p[1:])


def p_type_name(p):
    """ type_name : specifier_qualifier_list """
    p[0] = ASTInternalNode('type_name', p[1:])


def p_parameter_list(p):
    """ parameter_list : parameter_declaration
                       | parameter_list ',' parameter_declaration """
    p[0] = ASTInternalNode('parameter_list', p[1:])


def p_parameter_declaration(p):
    """ parameter_declaration : declaration_specifiers declarator
                              | declaration_specifiers """
    p[0] = ASTInternalNode('parameter_declaration', p[1:])


def p_argument_expr_list(p):
    """ argument_expr_list : assignment_expr
                           | argument_expr_list ',' assignment_expr """
    p[0] = ASTInternalNode('argument_expr_list', p[1:])


def p_init_list(p):
    """ init_list : init
                  | init_list ',' init
                  | designation init
                  | init_list ',' designation init """
    p[0] = ASTInternalNode('init_list', p[1:])


def p_init(p):
    """ init : assignment_expr
             | '{' init_list '}'
             | '{' init_list ',' '}' """
    p[0] = ASTInternalNode('init', p[1:])


def p_designation(p):
    """ designation : designator_list '=' """
    p[0] = ASTInternalNode('deignation', p[1:])


def p_designator_list(p):
    """ designator_list : designator
                        | designator_list designator """
    p[0] = ASTInternalNode('designator_list', p[1:])


def p_designator(p):
    """ designator : '[' constant_expr ']'
                   | '.' IDENTIFIER """
    p[0] = ASTInternalNode('designator', p[1:])


def p_func_declaration(p):
    """ func_declaration : declaration_specifiers declarator declaration_list compound_stat
                         | declaration_specifiers declarator compound_stat """
    p[0] = ASTInternalNode('func_declaration', p[1:])


def p_declaration_list(p):
    """ declaration_list : var_declaration
                         | declaration_list var_declaration """
    p[0] = ASTInternalNode('declaration_list', p[1:])


# 复合语句（代码块）
def p_compound_stat(p):
    """ compound_stat : '{' '}'
                      | '{' block_item_list '}' """
    p[0] = ASTInternalNode('compound_stat', p[1:])


# 代码块元素 列表
def p_block_item_list(p):
    """ block_item_list : block_item
                        | block_item_list block_item """
    p[0] = ASTInternalNode('block_item_list', p[1:])


# 代码块元素
def p_block_item(p):
    """ block_item : var_declaration
                   | stat """
    p[0] = ASTInternalNode('block_item', p[1:])


# 语句
# 推导 -> 标记语句（labeled_statement）|
def p_stat(p):
    """ stat : labeled_stat
                  | compound_stat
                  | expr_stat
                  | selection_stat
                  | iteration_stat
                  | jump_stat """
    p[0] = ASTInternalNode('stat', p[1:])


# 标记语句
def p_labeled_stat(p):
    """ labeled_stat : IDENTIFIER ':' stat
                     | CASE constant_expr ':' stat
                     | DEFAULT ':' stat """
    if len(p) == 4 and not p[1] == 'default' and not p[1] in reserved_1:
        p[1] = ASTExternalNode('IDENTIFIER', p[1])
    p[0] = ASTInternalNode('labeled_stat', p[1:])


# 表达式语句
def p_expr_stat(p):
    """ expr_stat : ';'
                  | expr ';' """
    p[0] = ASTInternalNode('expr_stat', p[1:])


# 选择语句
def p_selection_stat(p):
    """ selection_stat : IF '(' expr ')' stat ELSE stat
                       | IF '(' expr ')' stat
                       | SWITCH '(' expr ')' stat """
    p[0] = ASTInternalNode('selection_stat', p[1:])


# 循环语句
def p_iteration_stat(p):
    """ iteration_stat : WHILE '(' expr ')' stat
                       | DO stat WHILE '(' expr ')' ';'
                       | FOR '(' expr_stat expr_stat ')' stat
                       | FOR '(' expr_stat expr_stat expr ')' stat
                       | FOR '(' var_declaration expr_stat ')' stat
                       | FOR '(' var_declaration expr_stat expr ')' stat """
    p[0] = ASTInternalNode('iteration_stat', p[1:])


# 跳转语句
def p_jump_stat(p):
    """ jump_stat : GOTO IDENTIFIER ';'
                  | CONTINUE ';'
                  | BREAK ';'
                  | RETURN ';'
                  | RETURN expr ';' """
    if len(p) == 4 and p[1] == 'goto' and not p[2] in reserved_1:
        p[2] = ASTExternalNode('IDENTIFIER', p[2])
    p[0] = ASTInternalNode('jump_stat', p[1:])


def p_error(p):
    print('[Error]: type - %s, value - %s, lineno - %d, lexpos - %d' % (p.type, p.value, p.lineno, p.lexpos))


parser = yacc.yacc()

while True:
    try:
        filename = input("input filename: ")
        with open(filename, 'r') as file:
            result = parser.parse(file.read())
            print(result)
    except EOFError:
        break
