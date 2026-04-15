import math
from collections import Counter
import os

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

def file_entropia(file_path):
    conteudo, _ = ler_ficheiro(file_path)
    return entropia(conteudo)

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

def filesToTest():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, 'data')
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

def ler_ficheiro(file_path):
    """
    Lê ficheiro de forma adequada ao tipo (texto ou binário).
    Retorna: (conteudo, modo)
    """
    extensao = os.path.splitext(file_path)[1].lower()
    
    # Extensões de ficheiros binários comuns
    binarios = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.pdf', 
                '.zip', '.rar', '.exe', '.dll', '.bin', '.dat', '.mp3', 
                '.mp4', '.avi', '.mov', '.wav', '.tif', '.ttf', '.woff'}
    
    if extensao in binarios:
        # Ler como binário - cada byte é um símbolo (0-255)
        with open(file_path, 'rb') as f:
            bytes_data = f.read()
            # Converter bytes para lista de inteiros (0-255)
            conteudo = list(bytes_data)
            return conteudo, 'binario'
    else:
        # Ler como texto com encoding UTF-8
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), 'texto'
        except UnicodeDecodeError:
            # Se falhar UTF-8, tenta latin-1 (funciona para qualquer byte)
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read(), 'texto'