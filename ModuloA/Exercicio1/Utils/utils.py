import math
import os
from collections import Counter

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

    total_simbolos = len(conteudo)
    entropia = 0
    
    for freq in frequencia.values():
        probabilidade = freq / total_simbolos
        entropia -= probabilidade * math.log2(probabilidade)
    return entropia

def calcular_frequencias(conteudo):
    return Counter(conteudo)


def prepare_test_files():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, '..', 'Data')
    with open(os.path.join(data_dir, 'input1.txt'), 'w') as f:
        f.write('aaaabbcd')
    with open(os.path.join(data_dir, 'input2.txt'), 'w') as f:
        f.write('awqsedrftgyhujikolpçzxcvbnmeeeeeeeeeeeeeeeoooooooaaaaaaaaaaaaaaaaaaaauusssssfffffiqiqunxz')
    with open(os.path.join(data_dir, 'input3.txt'), 'w') as f:
        f.write('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaao')

def files_path():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    
    input1 = os.path.join(dir_atual, '..', 'Data', 'input1.txt')
    output1 = os.path.join(dir_atual, '..', 'Data', 'output1.txt')

    input2 = os.path.join(dir_atual, '..', 'Data', 'input2.txt')
    output2 = os.path.join(dir_atual, '..', 'Data', 'output2.txt')
    
    input3 = os.path.join(dir_atual, '..', 'Data', 'input3.txt')
    output3 = os.path.join(dir_atual, '..', 'Data', 'output3.txt')
    
    return input1, output1, input2, output2, input3, output3   