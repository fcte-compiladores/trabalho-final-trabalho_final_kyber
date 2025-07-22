from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "  " * self.indent_level

    def generate(self, program_node: ProgramNode):
        global_code = "".join(self.visit(var_decl) for var_decl in program_node.global_vars)
        setup_code = self.visit(program_node.setup, "setup")
        loop_code = self.visit(program_node.loop, "loop")
        return f"{global_code}\n{setup_code}\n{loop_code}"

    def visit(self, node, block_name=None):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        if block_name: return visitor(node, block_name)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Nenhum método visit_{type(node).__name__} encontrado')

    def visit_BlockNode(self, node, block_name):
        self.indent_level += 1
        statements_code = "".join(f"{self.indent()}{self.visit(stmt)}\n" for stmt in node.statements)
        self.indent_level -= 1
        return f"void {block_name}() {{\n{statements_code}}}\n"

    def visit_IfNode(self, node):
        condition_code = self.visit(node.condition)
        
        self.indent_level += 1
        then_statements = "".join(f"{self.indent()}{self.visit(stmt)}\n" for stmt in node.then_block.statements)
        self.indent_level -= 1
        
        code = f"if ({condition_code}) {{\n{then_statements}{self.indent()}}}"
        
        if node.else_block:
            self.indent_level += 1
            else_statements = "".join(f"{self.indent()}{self.visit(stmt)}\n" for stmt in node.else_block.statements)
            self.indent_level -= 1
            code += f" else {{\n{else_statements}{self.indent()}}}"
        return code

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"{left} {node.op} {right}"

    def visit_VarDeclNode(self, node):
        type_mapping = {'int': 'int', 'String': 'String'}
        cpp_type = type_mapping[node.var_type]
        value_code = self.visit(node.value)
        return f"{cpp_type} {node.name} = {value_code};"

    def visit_PinModeNode(self, node): return f"pinMode({self.visit(node.pin)}, OUTPUT);"
    def visit_SetPinNode(self, node): return f"digitalWrite({self.visit(node.pin)}, {node.state.upper()});"
    def visit_DelayNode(self, node): return f"delay({self.visit(node.duration)});"
    def visit_SerialBeginNode(self, node): return f"Serial.begin({self.visit(node.speed)});"
    def visit_SerialPrintlnNode(self, node): return f"Serial.println({self.visit(node.value)});"
    
    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value
    def visit_IdentifierNode(self, node): return node.name