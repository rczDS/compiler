import ply.lex as lex
from ply.lex import TOKEN


tokens = (
    'CONSTANT',
    'STRING_LITERAL',
    'IDENTIFIER',
    'ADD_ASSIGN',
    'SUB_ASSIGN',
    'MUL_ASSIGN',
    'DIV_ASSIGN',
    'MOD_ASSIGN',
    'AND_ASSIGN',
    'XOR_ASSIGN',
    'OR_ASSIGN',
    'RIGHT_OP',
    'LEFT_OP',
    'INC_OP',
    'DEC_OP',
    'PTR_OP',
    'AND_OP',
    'OR_OP',
    'LE_OP',
    'GE_OP',
    'EQ_OP',
    'NE_OP',
)

reserved = {
    'break': 'BREAK',
    'bool': 'BOOL',
    'case': 'CASE',
    'char': 'CHAR',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do': 'DO',
    'double': 'DOUBLE',
    'else': 'ELSE',
    'for': 'FOR',
    'if': 'IF',
    'inline': 'INLINE',
    'int': 'INT',
    'return': 'RETURN',
    'sizeof': 'SIZEOF',
    'switch': 'SWITCH',
    'void': 'VOID',
    'while': 'WHILE',
}
tokens = tokens + tuple(reserved.values())

literals = ';,:=.&![]{}~()+-*/%><^|?'

t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_XOR_ASSIGN = r'\^='
t_OR_ASSIGN = r'\|='
t_RIGHT_OP = r'>>'
t_LEFT_OP = r'<<'
t_INC_OP = r'\+\+'
t_DEC_OP = r'--'
t_PTR_OP = r'->'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='

number = r'[0-9]'
letter = r'([_a-zA-Z])'

boolean = r'(true|false)'
integer = r'(0?%s+)' % number
char = r'(\'(\\.|[^\\\'])+\')'
constant = r'(%s|%s|%s)' % (integer, char, boolean)
string_literal = r'"(\\.|[^\\"])*"'
identifier = r'(%s(%s|%s)*)' % (letter, number, letter)


@TOKEN(constant)
def t_CONSTANT(t):
    return t


@TOKEN(string_literal)
def t_STRING_LITERAL(t):
    return t


@TOKEN(identifier)
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


t_ignore = ' \t\v\f'


def t_COMMENT(t):
    r"""//[^\n]*"""
    pass


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


if __name__ == '__main__':
    while True:
        try:
            filename = input('filename(lex): ')
            with open(filename, 'r') as file:
                data = file.read()
                lexer.input(data)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok)
        except EOFError:
            break
