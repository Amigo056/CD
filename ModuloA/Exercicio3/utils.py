import math
from collections import Counter
import os
import matplotlib.pyplot as plt
from PIL import Image

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

def filesToTest(path):
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, path)
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]


def ler_pixels_imagem(file_path, modo="L"):
    img = Image.open(file_path).convert(modo)
    conteudo = list(img.getdata())
    return conteudo, img


def histograma_pixels(file_path, modo="L"):
    conteudo, _ = ler_pixels_imagem(file_path, modo)
    return calcular_frequencias(conteudo)


def image_entropia(file_path, modo="L"):
    conteudo, _ = ler_pixels_imagem(file_path, modo)
    return entropia(conteudo)


            
def draw_histogram_matplotlib(frequencias, titulo, output_path="ex1Results"):
    hist = [frequencias.get(i, 0) for i in range(256)]

    plt.figure(figsize=(12, 6))
    plt.bar(range(256), hist, color='skyblue', edgecolor='black', width=1.0)
    plt.xlabel('Intensidade do pixel (0-255)')
    plt.ylabel('Frequência Absoluta')
    plt.title(titulo)

    plt.xticks(range(0, 256, 16))
    plt.tight_layout()

    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, output_path)

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    file_name = os.path.splitext(titulo)[0]
    caminho_completo = os.path.join(pasta_saida, f"{file_name}.png")

    plt.savefig(caminho_completo, dpi=150)
    plt.show()
    plt.close()

def file_scanner(file,output_path = "ex1Results"):
    
   
    conteudo, img = ler_pixels_imagem(file, modo="L")
    

    file_name = os.path.basename(file)

    frequencias = calcular_frequencias(conteudo)
    total = len(conteudo)
    simbolo_max, freq_max = simbolo_mais_frequente(conteudo)


    entropia_valor = entropia(conteudo)

    print(f'\n{"="*50}')
    print(f'FICHEIRO: {file_name})')
    print(f'{"="*50}')
    print(f'Total de símbolos: {total}')
    print(f'\n>>> ENTROPIA DA FONTE <<<')
    print(f'  H = {entropia_valor:.4f} bits/símbolo')
    print(f'{"="*50}\n')
    
    
    draw_histogram_matplotlib(frequencias, titulo=f"Histogram_{file_name}", output_path=output_path)
    
    return {
        'entropia': entropia_valor,

    }            
    
    