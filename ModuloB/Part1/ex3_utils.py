from collections import Counter
import math
import os
import tempfile
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys
import shutil
import subprocess

def processar_imagem(caminho_png, qualidades, pasta_saida):
    """
    Processa uma imagem PNG: converte para JPEG com várias qualidades,
    calcula MAE e taxa de compressão, e retorna os dados para o gráfico.
    """
    nome_base = os.path.splitext(os.path.basename(caminho_png))[0]
    img_original = Image.open(caminho_png)

    # Garantir que está em RGB
    img_original = img_original.convert('RGB')

    tamanho_original = os.path.getsize(caminho_png)



    for q in qualidades:
        # Guardar JPEG com qualidade q
        caminho_jpeg = os.path.join(pasta_saida, f"{nome_base}_q{q}.jpg")
        img_original.save(caminho_jpeg, "JPEG", quality=q)


def descomprimir_imagem(caminho_jpeg, pasta_saida, formato_saida="PNG"):

    os.makedirs(pasta_saida, exist_ok=True)

    nome_base = os.path.splitext(os.path.basename(caminho_jpeg))[0]
    img = Image.open(caminho_jpeg)

    # Garantir modo compatível
    if img.mode != "RGB":
        img = img.convert("RGB")

    extensao = formato_saida.lower()
    caminho_saida = os.path.join(pasta_saida, f"{nome_base}_descomprimida.{extensao}")

    img.save(caminho_saida, formato_saida)
    return caminho_saida

def find_7zip():
    """Tenta localizar o executável do 7-Zip automaticamente"""
    try:
        subprocess.run(['7z'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return '7z'
    except FileNotFoundError:
        pass
    
    possible_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

SEVEN_ZIP_PATH = find_7zip()

if SEVEN_ZIP_PATH is None:
    print("ERRO: 7-Zip não encontrado!")
    sys.exit(1)
else:
    print(f"7-Zip encontrado em: {SEVEN_ZIP_PATH}")
    


def compress(input_file, output_dir):
    """Compressão usando 7-Zip - guarda diretamente na pasta output"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Ficheiro não encontrado: {input_file}")
    
    # Guardar o .7z diretamente na pasta de resultados, não na data/
    base_name = os.path.basename(input_file)
    compressed_file = os.path.join(output_dir, base_name + '.7z')
    
 
    result = subprocess.run([SEVEN_ZIP_PATH, 'a', '-y', '-mx=5', compressed_file, input_file], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise RuntimeError(f"Erro na compressão: {result.stderr.decode('utf-8', errors='ignore')}")
    
  
    return compressed_file

def descompress(compressed_file, original_file, pasta_saida):
    """Descompressão usando 7-Zip para uma pasta definida pelo utilizador"""
    
    os.makedirs(pasta_saida, exist_ok=True)

    result = subprocess.run(
        [SEVEN_ZIP_PATH, 'x', '-y', compressed_file, f'-o{pasta_saida}'],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError(
            f"Erro na descompressão: {result.stderr.decode('utf-8', errors='ignore')}"
        )

    original_name = os.path.basename(original_file)
    descompressed_file = os.path.join(pasta_saida, original_name)

    if not os.path.exists(descompressed_file):
        raise FileNotFoundError("Ficheiro descomprimido não encontrado")

    return descompressed_file  


def cifra_vernam(plain_bytes, key_bytes):
    resultado = bytearray()
    for p, k in zip(plain_bytes, key_bytes):
        resultado.append(p ^ k)
    return bytes(resultado)


def decifra_vernam(cipher_bytes, key_bytes):
    resultado = bytearray()
    for c, k in zip(cipher_bytes, key_bytes):
        resultado.append(c ^ k)
    return bytes(resultado)

def filesToTest(path):
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, path)
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]


def ficheiros_iguais(ficheiro1, ficheiro2, tamanho_bloco=8192):
    if not os.path.exists(ficheiro1) or not os.path.exists(ficheiro2):
        raise FileNotFoundError("Um dos ficheiros não existe.")

    if os.path.getsize(ficheiro1) != os.path.getsize(ficheiro2):
        return False

    with open(ficheiro1, "rb") as f1, open(ficheiro2, "rb") as f2:
        while True:
            bloco1 = f1.read(tamanho_bloco)
            bloco2 = f2.read(tamanho_bloco)

            if bloco1 != bloco2:
                return False

            if not bloco1:
                return True
            
            
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


def dimensao_bytes(dados):
    return len(dados)

def calcular_taxa_compressao(tamanho_original, tamanho_comprimido):
    """
    Taxa de compressão = tamanho_original / tamanho_comprimido
    (quanto maior, melhor a compressão)
    """
    return tamanho_original / tamanho_comprimido            


def calcular_frequencias(conteudo):
    return Counter(conteudo)

def desenhar_histograma_matplotlib(frequencias, titulo="Histograma de Símbolos", caminho_saida=None):
    """
    Gera histograma usando matplotlib e, se for fornecido, guarda-o em disco.
    """
    simbolos = list(frequencias.keys())
    contagens = list(frequencias.values())
    plt.figure(figsize=(10, 6))
    plt.bar(simbolos, contagens, color='skyblue', edgecolor='black')
    plt.xlabel('Símbolos')
    plt.ylabel('Frequência')
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if caminho_saida:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        plt.savefig(caminho_saida, dpi=150)

    plt.show()
    plt.close()

