#  Projeto B.2

## 1. Objetivo

O presente exercício teve como finalidade implementar um sistema de comunicação de dados entre uma Raspberry Pi e um PC, recorrendo a uma ligação série via USB, em modo **simplex**. Pretendeu-se que a Raspberry Pi funcionasse como emissor e o PC como recetor, utilizando a biblioteca **pyserial** em Python para receber a informação transmitida.

Além disso, pretendeu-se analisar o comportamento do sistema em dois cenários distintos:

- (a) transmissão normal, sem deteção de erros;
- (b) análise de erros introduzidos posteriormente no PC, usando padrões de erro isolado (*single bit error*) e em rajada (*burst bit error*), com apoio do código **Hamming (7,4)**.



---


## 2. Fundamentação Teórica


### 2.1 Comunicação Simplex

Numa comunicação **simplex**, a informação circula apenas num único sentido. Neste trabalho, a Raspberry Pi desempenha o papel de emissor, transmitindo continuamente mensagens para o PC, que funciona apenas como recetor.

A ligação entre os dois dispositivos é feita através de comunicação série, com transmissão de dados a uma determinada velocidade de baudrate. Esta abordagem é simples, robusta e muito utilizada em sistemas embebidos e experiências laboratoriais de comunicação digital.


### 2.2 Deteção de Erros com Hamming (7,4)

O código **Hamming (7,4)** é uma técnica de deteção e correção de erros que transforma 4 bits de dados em 7 bits, acrescentando 3 bits de paridade. Estes bits adicionais permitem identificar a existência de erros e, no caso de um erro simples, determinar a sua posição exata e corrigi-lo.

Neste exercício, o Hamming foi usado para analisar os dados após a receção, permitindo verificar o comportamento do sistema perante erros introduzidos artificialmente no PC.


### 2.3 Tipos de Erro

Foram considerados dois tipos de erro:

- **Single Bit Error:** alteração de um único bit na sequência recebida;
- **Burst Bit Error:** alteração de vários bits consecutivos, simulando uma rajada de erro no canal.

Estes testes permitem avaliar a robustez do sistema e a eficácia do código Hamming em diferentes condições.



---


## 3. Metodologia


### 3.1 Ferramentas Utilizadas

Foram utilizados os seguintes recursos:

- **Raspberry Pi Pico 2 W** como emissor;
- **PC** como recetor;
- **Python 3** para o programa de receção;
- **pyserial** para comunicação série;
- ficheiros auxiliares para introdução de erros e análise com Hamming.


### 3.2 Procedimento Experimental

O procedimento seguido foi o seguinte:

1. Configuração da Raspberry Pi para enviar repetidamente uma string em modo série.
2. Ligação da Raspberry Pi ao PC através da porta série.
3. Leitura dos dados recebidos no PC usando a biblioteca `pyserial`.
4. Escrita da informação recebida na consola e em ficheiro.
5. Introdução opcional de erros no ficheiro recebido.
6. Análise dos dados alterados com o código Hamming (7,4), quando ativado.



---


## 4. Implementação


### 4.1 Emissor

No emissor foi desenvolvido um programa em MicroPython para a Raspberry Pi Pico 2 W. Esse programa configura a interface UART e transmite repetidamente um pangrama, com intervalo de tempo entre envios.

A mensagem enviada corresponde a uma das frases especificadas no enunciado, sendo convertida para bytes antes da transmissão.


### 4.2 Recetor

No recetor foi desenvolvido um programa em Python com a biblioteca `pyserial`. O programa abre a porta série associada à Raspberry Pi, aguarda a receção de dados e lê a mensagem enviada.
Após a leitura, a mensagem é guardada num ficheiro de texto e utilizada como base para testes de erros posteriores.


### 4.3 Módulo Hamming

Foi implementado um módulo de Hamming (7,4) com funções de codificação e descodificação. O módulo calcula bits de paridade, gera o síndroma de erro e identifica a posição de um bit errado dentro do bloco de 7 bits.

Quando é detetado um erro simples, o sistema pode corrigir automaticamente esse bit e recuperar os dados originais. Este mecanismo foi usado para analisar os efeitos dos erros introduzidos sobre os dados recebidos.



---


## 5. Resultados


### 5.1 Funcionamento sem Deteção de Erros

Na primeira fase, o sistema foi testado sem qualquer mecanismo de deteção de erros. Verificou-se que o PC recebeu corretamente as mensagens enviadas pela Raspberry Pi, confirmando o funcionamento da ligação simplex.

A informação recebida foi apresentada na consola e gravada com sucesso num ficheiro, demonstrando que o sistema de comunicação base estava operacional.


### 5.2 Testes com Erro Isolado e em Rajada

Na segunda fase, os dados recebidos foram alterados através de funções de erro isolado e erro em rajada. Estas modificações foram feitas no PC após a receção, tal como definido no enunciado.

Os testes permitiram observar que:

- o erro isolado afeta apenas um bit, sendo mais facilmente detetável;
- o erro em rajada afeta vários bits consecutivos, provocando maior degradação da sequência recebida.


### 5.3 Análise com Hamming

Quando o modo Hamming foi ativado, os dados alterados puderam ser analisados através dos bits de paridade. O sistema conseguiu identificar erros simples e determinar a posição do bit incorreto.

Desta forma, foi possível verificar experimentalmente que o código Hamming (7,4) é adequado para deteção e correção de erros isolados, embora apresente limitações perante erros em rajada.



---


## 6. Análise e Discussão

Os resultados obtidos mostraram que a comunicação entre a Raspberry Pi e o PC foi realizada com sucesso, cumprindo o objetivo de transmissão simplex. A receção com `pyserial` revelou-se adequada para este tipo de ligação, permitindo uma implementação simples e funcional.

A análise de erros demonstrou que o comportamento do sistema varia consoante o padrão de erro introduzido. Enquanto o código Hamming responde eficazmente a erros simples, os erros em rajada são mais difíceis de tratar, uma vez que podem comprometer vários bits do mesmo bloco ou de blocos consecutivos.

Assim, o exercício permitiu não só validar a comunicação entre dispositivos, mas também estudar de forma prática mecanismos básicos de deteção e correção de erros em canais digitais.



---


## 7. Conclusão

Este exercício permitiu implementar um sistema de comunicação simplex entre uma Raspberry Pi e um PC, usando transmissão série via USB e receção com `pyserial`.

Verificou-se que:

- a comunicação base funcionou corretamente;
- os dados recebidos puderam ser armazenados e analisados;
- os testes de erro permitiram estudar o comportamento do sistema em diferentes situações;
- o código Hamming (7,4) mostrou-se eficaz na deteção e correção de erros simples.

De forma global, o trabalho permitiu consolidar conceitos de comunicação digital, transmissão série e controlo de erros, através de uma implementação prática e experimental.



---


## Anexos

- Script do emissor: `main-3.py`
- Script do recetor: `receptor.py`
- Módulo de Hamming: `hamming.py`
- Função de erro isolado: `single_bit_error.py`
- Função de erro em rajada: `burst_errors.py`
- Ficheiro com dados recebidos: `dados_recebidos.txt`