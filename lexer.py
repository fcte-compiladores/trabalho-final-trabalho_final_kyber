import re

TOKEN_REGEX = [
    ('COMMENT', r'//.*'),
    ('KEYWORD', r'\b(setup|loop|pin|is|output|set|to|high|low|delay|var|serialBegin|serialPrintln|int|String|if|else)\b'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER',  r'\d+'),
    ('STRING',  r'"[^"]*"'),
    ('EQUALS_EQUALS', r'=='),
    ('BANG_EQUALS',   r'!='),
    ('GREATER_EQUALS',r'>='),
    ('LESS_EQUALS',   r'<='),
    ('GREATER', r'>'),
    ('LESS',    r'<'),
    ('EQUALS',  r'='),
    # --------------------------
    ('COLON',   r':'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('NEWLINE', r'\n'),
    ('SKIP',    r'[ \t]+'),
    ('MISMATCH',r'.'),
]
TOKEN_MASTER_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_REGEX)

def lex(code):
    tokens = []
    line_num = 1
    line_start = 0
    for mo in re.finditer(TOKEN_MASTER_REGEX, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind in ['SKIP', 'COMMENT', 'NEWLINE']: continue
        if kind == 'MISMATCH': raise RuntimeError(f'Erro na linha {line_num}:{column}: Caractere inesperado "{value}"')
        tokens.append((kind, value, line_num, column))
    return tokens