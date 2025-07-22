from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.symbol_table = {}
    def get_current_token(self):
        if self.current_token_index < len(self.tokens): return self.tokens[self.current_token_index]
        return ('EOF', '', -1, -1)
    def advance(self): self.current_token_index += 1
    def expect(self, kind, value=None):
        token_kind, token_value, line, col = self.get_current_token()
        if token_kind != kind: raise SyntaxError(f"Erro na linha {line}:{col}: Esperava '{kind}', mas recebi '{token_kind}'")
        if value and token_value != value: raise SyntaxError(f"Erro na linha {line}:{col}: Esperava '{value}', mas recebi '{token_value}'")
        self.advance()
        return token_kind, token_value
    def get_var_type(self, var_name):
        if var_name not in self.symbol_table: raise SyntaxError(f"Erro: Variável '{var_name}' não foi declarada.")
        return self.symbol_table[var_name]

    def parse(self):
        global_vars = []
        setup_block = None
        loop_block = None
        while self.get_current_token()[0] != 'EOF':
            kind, value, _, _ = self.get_current_token()
            if kind == 'KEYWORD' and value == 'var':
                global_vars.append(self.parse_variable_declaration())
            elif kind == 'KEYWORD' and value == 'setup':
                self.advance() # Consome 'setup'
                setup_block = self.parse_statement_block()
            elif kind == 'KEYWORD' and value == 'loop':
                self.advance() # Consome 'loop'
                loop_block = self.parse_statement_block()
            else:
                _, token_value, line, col = self.get_current_token()
                raise SyntaxError(f"Erro na linha {line}:{col}: Comando inesperado '{token_value}'")
        if not setup_block or not loop_block: raise SyntaxError("Erro: O programa precisa de um bloco 'setup' e um 'loop'.")
        return ProgramNode(global_vars=global_vars, setup=setup_block, loop=loop_block)

    def parse_statement_block(self):
        self.expect('LBRACE')
        statements = []
        while self.get_current_token()[1] != '}':
            statements.append(self.parse_statement())
        self.expect('RBRACE')
        return BlockNode(statements=statements)

    def parse_statement(self):
        _, value, _, _ = self.get_current_token()
        if value == 'if': return self.parse_if_statement()
        if value == 'pin': return self.parse_pin_mode()
        if value == 'set': return self.parse_set_pin()
        if value == 'delay': return self.parse_delay()
        if value == 'serialBegin': return self.parse_serial_begin()
        if value == 'serialPrintln': return self.parse_serial_println()
        _, token_value, line, col = self.get_current_token()
        raise SyntaxError(f"Erro na linha {line}:{col}: Comando desconhecido '{token_value}'")

    def parse_if_statement(self):
        self.expect('KEYWORD', 'if')
        condition_node = self.parse_expression()
        then_block = self.parse_statement_block()
        else_block = None
        if self.get_current_token()[1] == 'else':
            self.advance()
            else_block = self.parse_statement_block()
        return IfNode(condition=condition_node, then_block=then_block, else_block=else_block)

    def parse_expression(self):
        left_node = self.parse_value()
        op_kind, op_value, _, _ = self.get_current_token()
        if op_kind not in ['EQUALS_EQUALS', 'BANG_EQUALS', 'GREATER', 'LESS', 'GREATER_EQUALS', 'LESS_EQUALS']:
            raise SyntaxError(f"Esperava um operador de comparação (==, >, <, etc), mas recebi '{op_value}'")
        self.advance()
        right_node = self.parse_value()
        return BinaryOpNode(left=left_node, op=op_value, right=right_node)

    def parse_value(self):
        kind, value, line, col = self.get_current_token()
        if kind == 'NUMBER': self.advance(); return NumberNode(value=value)
        if kind == 'STRING': self.advance(); return StringNode(value=value)
        if kind == 'IDENTIFIER':
            self.advance()
            if value not in self.symbol_table: raise SyntaxError(f"Erro na linha {line}:{col}: Variável '{value}' não declarada.")
            return IdentifierNode(name=value)
        raise SyntaxError(f"Erro na linha {line}:{col}: Esperava um valor, mas recebi '{kind}'.")
    
    def parse_variable_declaration(self):
        self.expect('KEYWORD', 'var')
        _, var_name = self.expect('IDENTIFIER')
        if var_name in self.symbol_table: raise SyntaxError(f"Variável '{var_name}' já declarada.")
        self.expect('COLON'); _, var_type = self.expect('KEYWORD')
        if var_type not in ['int', 'String']: raise SyntaxError(f"Tipo desconhecido '{var_type}'.")
        self.expect('EQUALS')
        initial_value_node = self.parse_value()
        if var_type == 'int' and not isinstance(initial_value_node, NumberNode): raise SyntaxError(f"Tipo incompatível para '{var_name}'.")
        if var_type == 'String' and not isinstance(initial_value_node, StringNode): raise SyntaxError(f"Tipo incompatível para '{var_name}'.")
        self.symbol_table[var_name] = var_type
        return VarDeclNode(name=var_name, var_type=var_type, value=initial_value_node)
    
    def parse_pin_mode(self):
        self.expect('KEYWORD', 'pin')
        pin_node = self.parse_value()
        if isinstance(pin_node, IdentifierNode) and self.get_var_type(pin_node.name) != 'int': raise SyntaxError("Número do pino deve ser do tipo 'int'.")
        self.expect('KEYWORD', 'is'); self.expect('KEYWORD', 'output')
        return PinModeNode(pin=pin_node, direction='output')
    
    def parse_set_pin(self):
        self.expect('KEYWORD', 'set'); self.expect('KEYWORD', 'pin')
        pin_node = self.parse_value()
        if isinstance(pin_node, IdentifierNode) and self.get_var_type(pin_node.name) != 'int': raise SyntaxError("Número do pino para 'set' deve ser do tipo 'int'.")
        self.expect('KEYWORD', 'to'); _, state = self.expect('KEYWORD')
        if state not in ['high', 'low']: raise SyntaxError("Estado do pino deve ser 'high' ou 'low'.")
        return SetPinNode(pin=pin_node, state=state)
   
    def parse_delay(self):
        self.expect('KEYWORD', 'delay')
        duration_node = self.parse_value()
        if isinstance(duration_node, IdentifierNode) and self.get_var_type(duration_node.name) != 'int': raise SyntaxError("'delay' espera um 'int'.")
        return DelayNode(duration=duration_node)
   
    def parse_serial_begin(self):
        self.expect('KEYWORD', 'serialBegin')
        speed_node = self.parse_value()
        if isinstance(speed_node, IdentifierNode) and self.get_var_type(speed_node.name) != 'int': raise SyntaxError("'serialBegin' espera um 'int'.")
        return SerialBeginNode(speed=speed_node)
   
    def parse_serial_println(self):
        self.expect('KEYWORD', 'serialPrintln')
        value_node = self.parse_value()
        if isinstance(value_node, IdentifierNode):
            var_type = self.get_var_type(value_node.name)
            if var_type not in ['int', 'String']: raise SyntaxError(f"Não é possível imprimir uma variável do tipo '{var_type}'.")
        return SerialPrintlnNode(value=value_node)