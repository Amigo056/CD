import math
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

def max_entropia(frequencias):
    return math.log2(len(frequencias))

def entropia_redundancia(entropia, frequencias):
    return max_entropia(frequencias) - entropia

def calcular_frequencias(conteudo):
    return Counter(conteudo)

def prob_max(freq_max, total):
    return freq_max / total

def info_propria(prob):
    return -math.log2(prob)
