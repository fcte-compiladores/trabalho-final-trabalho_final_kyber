import sys
from lexer import lex
from transpiler import Transpiler

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada.ky>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    
    output_filename = input_filepath.split('/')[-1].replace('.ky', '.ino')
    output_filepath = f"output/{output_filename}"

    print(f"Lendo o arquivo de entrada: {input_filepath}")
    try:
        with open(input_filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_filepath}' não encontrado.")
        sys.exit(1)

    try:
        print("Analisando tokens...")
        tokens = lex(source_code)
        
        print("Transpilando código...")
        transpiler = Transpiler(tokens)
        output_code = transpiler.transpile()

        with open(output_filepath, 'w') as f:
            f.write(output_code)
        
        print("-" * 20)
        print(f"Sucesso! Código transpilado salvo em: {output_filepath}")
        print("Código Gerado:")
        print("-" * 20)
        print(output_code)

    except (RuntimeError, SyntaxError) as e:
        print(f"\nERRO: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()