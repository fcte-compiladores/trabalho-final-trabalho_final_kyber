from lexer import lex

def test_variable_declaration():
    code = "var my_var: int = 10"
    tokens = lex(code)
    token_values = [t[1] for t in tokens]
    assert token_values == ["var", "my_var", ":", "int", "=", "10"]

def test_if_statement_with_operators():
    code = "if x >= 100 {}"
    tokens = lex(code)
    token_values = [t[1] for t in tokens]
    assert token_values == ["if", "x", ">=", "100", "{", "}"]

def test_comments_and_whitespace():
    code = """
    // Isso é um comentário
    var x: int = 5 // comentário no final
    """
    tokens = lex(code)
    token_values = [t[1] for t in tokens]
    assert token_values == ["var", "x", ":", "int", "=", "5"]