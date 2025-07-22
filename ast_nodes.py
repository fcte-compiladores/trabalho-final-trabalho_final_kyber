
# Definiçãao da estrutura de dados da nossa Árvore Sintática Abstrata.

from dataclasses import dataclass
from typing import List, Union

# valores literais ou nomes
@dataclass
class NumberNode:
    value: str

@dataclass
class StringNode:
    value: str

@dataclass
class IdentifierNode:
    name: str

ValueNode = Union[NumberNode, StringNode, IdentifierNode]

# comandos (Statements)
@dataclass
class VarDeclNode:
    name: str
    var_type: str
    value: ValueNode

@dataclass
class PinModeNode:
    pin: ValueNode
    direction: str # 'output'

@dataclass
class SetPinNode:
    pin: ValueNode
    state: str # 'high' ou 'low'

@dataclass
class DelayNode:
    duration: ValueNode

@dataclass
class SerialBeginNode:
    speed: ValueNode

@dataclass
class SerialPrintlnNode:
    value: ValueNode

StatementNode = Union[VarDeclNode, PinModeNode, SetPinNode, DelayNode, SerialBeginNode, SerialPrintlnNode]

@dataclass
class BlockNode:
    statements: List[StatementNode]

@dataclass
class ProgramNode:
    global_vars: List[VarDeclNode]
    setup: BlockNode
    loop: BlockNode


@dataclass
class BinaryOpNode:
    left: ValueNode
    op: str # O operador, ex: '>'
    right: ValueNode

# if/else
@dataclass
class IfNode:
    condition: BinaryOpNode
    then_block: 'BlockNode'
    else_block: 'BlockNode' = None # o 'else' é opcional

StatementNode = Union[VarDeclNode, PinModeNode, SetPinNode, DelayNode, SerialBeginNode, SerialPrintlnNode, IfNode]
ExpressionNode = Union[ValueNode, BinaryOpNode]