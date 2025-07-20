class Transpiler:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.symbol_table = set()
        self.global_code = ""
        self.main_code = ""

    def get_current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return ('EOF', '', -1, -1)

    def advance(self):
        self.current_token_index += 1

    def expect(self, kind, value=None):
        token_kind, token_value, line, col = self.get_current_token()
        if token_kind != kind:
            raise SyntaxError(f"Erro de sintaxe na linha {line}:{col}: Esperava um token do tipo '{kind}', mas recebi '{token_kind}'")
        if value and token_value != value:
            raise SyntaxError(f"Erro de sintaxe na linha {line}:{col}: Esperava o valor '{value}', mas recebi '{token_value}'")
        self.advance()
        return token_kind, token_value
    
    def transpile(self):
        while self.get_current_token()[0] != 'EOF':
            kind, value, _, _ = self.get_current_token()
            if kind == 'KEYWORD' and value == 'var': self.parse_variable_declaration()
            elif kind == 'KEYWORD' and value == 'setup': self.parse_block("setup")
            elif kind == 'KEYWORD' and value == 'loop': self.parse_block("loop")
            else:
                _, token_value, line, col = self.get_current_token()
                raise SyntaxError(f"Erro na linha {line}:{col}: Comando inesperado no topo do arquivo '{token_value}'")
        return self.global_code + "\n" + self.main_code
    
    # --- Handlers ---

    def parse_block(self, block_name):
        self.expect('KEYWORD', block_name)
        self.expect('LBRACE')
        self.main_code += f"void {block_name}() {{\n"
        while self.get_current_token()[1] != '}':
            self.parse_statement()
        self.expect('RBRACE')
        self.main_code += "}\n\n"

    def parse_statement(self):
        _, value, _, _ = self.get_current_token()

        if value == 'pin': self.parse_pin_mode()
        elif value == 'set': self.parse_set_pin()
        elif value == 'delay': self.parse_delay()
        elif value == 'serialBegin': self.parse_serial_begin()
        elif value == 'serialPrintln': self.parse_serial_println()
        else:
            _, token_value, line, col = self.get_current_token()
            raise SyntaxError(f"Erro na linha {line}:{col}: Comando desconhecido '{token_value}'")

    def parse_variable_declaration(self):
        self.expect('KEYWORD', 'var')
        _, var_name = self.expect('IDENTIFIER')
        if var_name in self.symbol_table:
            _, _, line, col = self.get_current_token()
            raise SyntaxError(f"Erro na linha {line}:{col}: Variável '{var_name}' já foi declarada.")
        self.symbol_table.add(var_name)
        self.expect('EQUALS')
        _, var_value = self.expect('NUMBER')
        self.global_code += f"int {var_name} = {var_value};\n"
    
    def parse_pin_mode(self):
        self.expect('KEYWORD', 'pin')
        _, pin_number = self.expect('NUMBER')
        self.expect('KEYWORD', 'is')
        self.expect('KEYWORD', 'output')
        self.main_code += f"  pinMode({pin_number}, OUTPUT);\n"

    def parse_set_pin(self):
        self.expect('KEYWORD', 'set')
        self.expect('KEYWORD', 'pin')
        _, pin_number = self.expect('NUMBER')
        self.expect('KEYWORD', 'to')
        _, state = self.expect('KEYWORD')
        if state not in ['high', 'low']: raise SyntaxError(f"...")
        self.main_code += f"  digitalWrite({pin_number}, {state.upper()});\n"

    def parse_delay(self):
        self.expect('KEYWORD', 'delay')
        kind, value, line, col = self.get_current_token()
        if kind == 'NUMBER':
            self.advance()
            self.main_code += f"  delay({value});\n"
        elif kind == 'IDENTIFIER':
            self.advance()
            if value not in self.symbol_table: raise SyntaxError(f"...")
            self.main_code += f"  delay({value});\n"
        else:
            raise SyntaxError(f"Erro na linha {line}:{col}: 'delay' espera um número ou uma variável.")

    def parse_serial_begin(self):
        self.expect('KEYWORD', 'serialBegin')
        _, speed = self.expect('NUMBER')
        self.main_code += f"  Serial.begin({speed});\n"

    def parse_serial_println(self):
        self.expect('KEYWORD', 'serialPrintln')
        kind, value, line, col = self.get_current_token()

        if kind == 'STRING':
            self.advance()
            self.main_code += f"  Serial.println({value});\n"
        elif kind == 'IDENTIFIER':
            self.advance()
            if value not in self.symbol_table:
                raise SyntaxError(f"Erro na linha {line}:{col}: Variável '{value}' não foi declarada.")
            self.main_code += f"  Serial.println({value});\n"
        else:
            raise SyntaxError(f"Erro na linha {line}:{col}: 'serialPrintln' espera uma string ou uma variável.")