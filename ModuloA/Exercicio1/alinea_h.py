#(h) Realiza a inversão de ordem do conteúdo de um ficheiro, recebendo como parâmetros os nomes do ficheiro de entrada
#e de saída. Por exemplo, se o ficheiro de entrada for ABCD1234, o ficheiro de saída será 4321DCBA. A função deverá
#apresentar o símbolo mais frequente de cada ficheiro e a respetiva entropia

import math
from test import test
import os

def inverter_ficheiro(inputFile, outputFile):
    with open (inputFile, 'r') as f:
        conteudo = f.read()    

    conteudo_invertido = conteudo[::-1]

    with open (outputFile, 'w') as f:
        f.write(conteudo_invertido)

    
def simbolo_mais_frequente(conteudo):
    frequencia = {}
    for simbolo in conteudo:
        if simbolo in frequencia:
            frequencia[simbolo] += 1
        else:
            frequencia[simbolo] = 1
    
    simbolo_mais_frequente = max(frequencia, key=frequencia.get)
    return simbolo_mais_frequente, frequencia[simbolo_mais_frequente]

def entropia(conteudo):
    frequencia = {}
    for simbolo in conteudo:
        frequencia[simbolo] = frequencia.get(simbolo, 0) + 1
    print(f'Frequência do símbolo mais frequente: {frequencia}')

    total_simbolos = len(conteudo)
    print(f'Total de símbolos: {total_simbolos}')
    entropia = 0
    
    for freq in frequencia.values():
        probabilidade = freq / total_simbolos
        entropia -= probabilidade * math.log2(probabilidade)
    print(f'Entropia calculada: {entropia}')
    return entropia

def prepare_test_files():
    '''
    Cria os ficheiros de teste necessários para a função inverter_ficheiro.
    '''
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, 'Data')
    with open(os.path.join(data_dir, 'input1.txt'), 'w') as f:
        f.write('ABCD1234')
    with open(os.path.join(data_dir, 'input2.txt'), 'w') as f:
        f.write('EFGH5678')
    with open(os.path.join(data_dir, 'input3.txt'), 'w') as f:
        f.write('IJKL9012')

def files_path():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    
    input1 = os.path.join(dir_atual, 'Data', 'input1.txt')
    output1 = os.path.join(dir_atual, 'Data', 'output1.txt')
    input2 = os.path.join(dir_atual, 'Data', 'input2.txt')
    output2 = os.path.join(dir_atual, 'Data', 'output2.txt')
    input3 = os.path.join(dir_atual, 'Data', 'input3.txt')
    output3 = os.path.join(dir_atual, 'Data', 'output3.txt')
    return input1, output1, input2, output2, input3, output3

def main():

    input1, output1, input2, output2, input3, output3 = files_path()
   
    inverter_ficheiro(input1, output1)
    inverter_ficheiro(input2, output2)
    inverter_ficheiro(input3, output3)

    for input_file, output_file in [(input1, output1), (input2, output2), (input3, output3)]:
        with open(input_file, 'r') as f:
            conteudo = f.read()
        simbolo, freq = simbolo_mais_frequente(conteudo)
        entropia_valor = entropia(conteudo)
        print(f'Símbolo mais frequente: {simbolo} (frequência: {freq})')
        print(f'Entropia: {entropia_valor:.4f}')

if __name__ == "__main__":
    main()