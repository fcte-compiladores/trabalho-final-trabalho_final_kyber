from lexer import lex
from parser import Parser
from codegen import CodeGenerator

def run_kyber_pipeline(code):
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodeGenerator()
    return codegen.generate(ast)

def test_full_blink_program():
    kyber_code = """
        var delay_time: int = 100
        setup { pin 13 is output }
        loop {
            set pin 13 to high
            delay delay_time
            set pin 13 to low
            delay 200
        }
    """
    
    expected_ino_code = """
        int delay_time = 100;

        void setup() {
          pinMode(13, OUTPUT);
        }

        void loop() {
          digitalWrite(13, HIGH);
          delay(delay_time);
          digitalWrite(13, LOW);
          delay(200);
        }
    """.replace(" ", "").replace("\n", "")

    actual_ino_code = run_kyber_pipeline(kyber_code).replace(" ", "").replace("\n", "")
    
    assert actual_ino_code == expected_ino_code