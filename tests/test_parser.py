import pytest
from lexer import lex
from parser import Parser
from ast_nodes import *

def test_valid_program_parsing():
    code = """
    var x: int = 10
    setup { pin 13 is output }
    loop { delay x }
    """
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast, ProgramNode)
    assert len(ast.global_vars) == 1
    assert isinstance(ast.global_vars[0], VarDeclNode)
    assert ast.global_vars[0].name == "x"
    
    assert isinstance(ast.setup, BlockNode)
    assert len(ast.setup.statements) == 1
    assert isinstance(ast.setup.statements[0], PinModeNode)

    assert isinstance(ast.loop, BlockNode)
    assert isinstance(ast.loop.statements[0], DelayNode)

def test_invalid_syntax():
    # Testa se o parser vai dar  inválido
    code = "var x: int = 10 20 30"
    tokens = lex(code)
    parser = Parser(tokens)

    with pytest.raises(SyntaxError):
        parser.parse()