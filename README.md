# Kyber: Transpiladorpara Arduino

## Integrantes

* **Nome:** Murilo Perazzo Barbosa Souto
* **Matrícula:** 190129221
* **Turma:** 18h

## Introdução

Este projeto consiste no desenvolvimento do Kyber (cristal kyber), um transpilador que converte uma linguagem de programação de alto nível, para código C++ compatível com a plataforma Arduino. A linguagem foi projetada com uma sintaxe simples, visando facilitar o desenvolvimento para sistemas embarcados.

As principais estratégias e algoritmos utilizados foram:
* **Análise Léxica:** Implementada através de um lexer baseado em Expressões Regulares (Regex) para tokenizar o código fonte.
* **Análise Sintática:** Utilizando um parser Recursivo Descendente, responsável por validar a sintaxe e construir uma **Árvore Sintática Abstrata (AST)** que representa a estrutura do código.
* **Análise Semântica:** Realizada durante a fase de parsing, com o uso de uma **Tabela de Símbolos** para armazenar informações sobre variáveis e realizar a verificação de tipos em comandos e expressões.
* **Geração de Código:** Percorre a AST e gera o código C++ final de forma limpa e desacoplada do parser.

### Exemplo

Aqui podemos ver um exemplo simples. Esse programa faz um led piscar e informa através da comunicação serial o seu estado.

```kyber
// Arquivo: examples/if_test.ky
var temperatura: int = 35
var limite: int = 30

setup {
    serialBegin 9600
}

loop {
    if temperatura > limite {
        serialPrintln "ALERTA: Temperatura muito alta!"
    } else {
        serialPrintln "Temperatura sob controle."
    }
    delay 2000 
}
```

## Instalação e Execução

Para executar o transpilador e os testes, é necessário ter o **Python 3.8+** instalado.

1.  **Clone o repositório:**
    ```sh
    git clone https://github.com/fcte-compiladores/trabalho-final-trabalho_final_kyber
    cd trabalho-final-trabalho_final_kyber
    ```

2.  **Crie e configure o ambiente virtual com `uv`:**
    ```sh
    # Cria o ambiente virtual na pasta .venv
    uv venv

    # Instala o pytest
    uv pip install pytest
    ```

3.  **Para transpilar um arquivo:**
    ```sh
    # O arquivo .ino será gerado na pasta 'output/'
    python3 main.py examples/if.ky
    ```

4.  **Para rodar a suíte de testes:**
    ```sh
    # Executa todos os testes na pasta tests/
    uv run pytest -v
    ```

## Exemplos

A pasta `examples/` contém diversos arquivos `.ky` que demonstram as funcionalidades da linguagem:

* `blink.ky`: Programa mais básico para sistemas embarcados, faz um LED piscar.
* `blink2leds.ky`: Faz dois LEDs piscarem.
* `blink_variaveis.ky`:Controla o delay com variáveis.
* `serial_teste.ky`: Demonstra o uso da comunicação serial para depuração.
* `tipos_primitivos.ky`: Mostra a declaração de variáveis com tipos `int` e `String`.
* `if.ky`: Demonstra o uso de estruturas de controle `if/else`.
* `error.ky`: Não deve gerar nada, apenas uma mensagem de erro no terminal.

## Referências

* https://www.arduino.cc/reference/en/ : Todas as decisões de geração de código (como traduzir delay 1000 para delay(1000); ou var x: String para String x;) foram baseadas nas regras e funções definidas nesta referência

* https://ruslanspivak.com/lsbasi-part1/ : Usado para entender melhor todas as partes gerenciáveis (lexer, parser)

* https://github.com/jamiebuilds/the-super-tiny-compiler : Explica cada passo da criação de um transpilador

## Estrutura do Código

O projeto é dividido da seguinte forma:

* `main.py`: Ponto de entrada da aplicação. lê o arquivo de entrada, chama o lexer, o parser e o gerador de código, e salva o resultado.
* `lexer.py`: Responsável pela **Análise Léxica**. Transforma o código fonte em uma lista de tokens.
* `ast_nodes.py`: Define a estrutura de dados da **Árvore Sintática Abstrata (AST)**.
* `parser.py`: Responsável pela **Análise Sintática e Semântica**. Consome os tokens e constrói a AST, validando a sintaxe e os tipos com o auxílio de uma Tabela de Símbolos.
* `codegen.py`: Responsável pela **Geração de Código**. Percorre a AST e gera o código C++ final.
* `tests/`: Contém os testes unitários e de integração, garantindo a corretude de cada componente.

## Bugs/Limitações/Melhorias Futuras

* **Limitações Atuais:**
    * O sistema de tipos suporta apenas `int` e `String`.
    * Não há suporte para expressões aritméticas complexas (ex: `5 * (x + 2)`).
    * As variáveis possuem apenas escopo global.
    * Não há laços de repetição customizados (for ou while), apenas o `loop()` principal do Arduino.

* **Melhorias Futuras:**
    * Implementar um parser de expressões completo para permitir operações aritméticas.
    * Adicionar suporte para mais tipos de dados, como `float` e `bool`.
    * Introduzir o conceito de escopo local para variáveis declaradas dentro de blocos.
    * Criar laços de repetição for e while.