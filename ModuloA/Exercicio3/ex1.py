"""
1. Codificação e compressão de dados com perda (lossy) - análise de resultados.
Escolha uma ferramenta de conversão de imagens entre diferentes formatos (por exemplo de formato PNG para JPEG). Em
alternativa, também poderá usar funcionalidades da linguagem Python para a conversão de imagens para o formato JPEG.
    (a) Utilize a aplicação ou escreva uma função que, sobre um ficheiro de imagem de entrada, realize a conversão para o
formato JPEG, com diferentes níveis de qualidade (perda). Apresente a imagem original (PNG) e as diferentes versões
JPEG, com vários níveis de qualidade, para alguns ficheiros do conjunto TestImages.zip.
    (b) Sobre os resultados da alínea anterior, para cada imagem e para diferentes níveis de qualidade, apresente o gráfico que
relaciona a taxa de compressão (eixo dos xx) e o erro absoluto médio (eixo dos yy). O erro absoluto médio, Mean
Absolute Error (MAE), entre duas imagens I1 e I2, de resolução espacial M x N, é definido como:
   (ver fórmula no enunciado - ModuloA/Docs/Parte3/CD_ver_25_26_Modulo_A_3.pdf)
Comente sobre o formato do gráfico.
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
PASTA_ENTRADA = "ModuloA/Exercicio3/Test_Images"      # Pasta com as imagens PNG originais
PASTA_SAIDA = "ModuloA/Exercicio3/resultados_jpeg_ex1"   # Pasta onde guardar os JPEGs e gráficos
QUALIDADES = [95, 85, 75, 50, 25, 10, 5]  # Níveis de qualidade JPEG a testar

os.makedirs(PASTA_SAIDA, exist_ok=True)

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def calcular_mae(img_original, img_comprimida):
    """
    Calcula o Mean Absolute Error (MAE) entre duas imagens.
    As imagens devem ter as mesmas dimensões.
    """
    # Converter para arrays numpy (valores 0-255)
    arr1 = np.array(img_original).astype(np.float64)
    arr2 = np.array(img_comprimida).astype(np.float64)

    # Se forem RGB, calcular MAE sobre todos os canais
    mae = np.mean(np.abs(arr1 - arr2))
    return mae


def calcular_taxa_compressao(tamanho_original, tamanho_comprimido):
    """
    Taxa de compressão = tamanho_original / tamanho_comprimido
    (quanto maior, melhor a compressão)
    """
    return tamanho_original / tamanho_comprimido


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

    resultados = {
        'qualidade': [],
        'taxa_compressao': [],
        'mae': [],
        'tamanho_bytes': [],
        'caminhos_jpeg': []
    }

    print(f"\n{'='*60}")
    print(f"Imagem: {nome_base}.png | Dimensões: {img_original.size}")
    print(f"Tamanho original: {tamanho_original:,} bytes")
    print(f"{'Qualidade':>10} | {'Tamanho (B)':>12} | {'Taxa Comp.':>10} | {'MAE':>10}")
    print("-" * 60)

    for q in qualidades:
        # Guardar JPEG com qualidade q
        caminho_jpeg = os.path.join(pasta_saida, f"{nome_base}_q{q}.jpg")
        img_original.save(caminho_jpeg, "JPEG", quality=q)

        # Reabrir para calcular MAE
        img_jpeg = Image.open(caminho_jpeg)

        tamanho_jpeg = os.path.getsize(caminho_jpeg)
        taxa = calcular_taxa_compressao(tamanho_original, tamanho_jpeg)
        mae = calcular_mae(img_original, img_jpeg)

        resultados['qualidade'].append(q)
        resultados['taxa_compressao'].append(taxa)
        resultados['mae'].append(mae)
        resultados['tamanho_bytes'].append(tamanho_jpeg)
        resultados['caminhos_jpeg'].append(caminho_jpeg)

        print(f"{q:>10} | {tamanho_jpeg:>12,} | {taxa:>10.2f}x | {mae:>10.4f}")

    return resultados, img_original


def criar_grafico(resultados, nome_imagem, pasta_saida):
    """
    Cria o gráfico Taxa de Compressão (xx) vs MAE (yy).
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    x = resultados['taxa_compressao']
    y = resultados['mae']
    qualidades = resultados['qualidade']

    ax.plot(x, y, 'b-o', linewidth=2, markersize=8, label='JPEG')

    # Anotar cada ponto com a qualidade correspondente
    for i, q in enumerate(qualidades):
        ax.annotate(f'Q={q}', (x[i], y[i]), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontsize=9)

    ax.set_xlabel('Taxa de Compressão (tamanho original / tamanho comprimido)', fontsize=12)
    ax.set_ylabel('Erro Absoluto Médio (MAE)', fontsize=12)
    ax.set_title(f'Compressão JPEG - {nome_imagem}', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    caminho_grafico = os.path.join(pasta_saida, f"grafico_{nome_imagem}.png")
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()
    print(f"Gráfico guardado: {caminho_grafico}")


def criar_mosaico_visual(nome_imagem, img_original, resultados, pasta_saida, max_amostras=4):
    """
    Cria uma figura com a imagem original e algumas versões JPEG para comparação visual.
    Útil para incluir no relatório.
    """
    n = min(max_amostras, len(resultados['qualidade']))
    indices = np.linspace(0, len(resultados['qualidade'])-1, n, dtype=int)

    fig, axes = plt.subplots(1, n + 1, figsize=(3*(n+1), 3))

    # Original
    axes[0].imshow(img_original)
    axes[0].set_title('Original (PNG)', fontsize=10)
    axes[0].axis('off')

    # Versões JPEG
    for i, idx in enumerate(indices, 1):
        q = resultados['qualidade'][idx]
        img_jpeg = Image.open(resultados['caminhos_jpeg'][idx])
        axes[i].imshow(img_jpeg)
        axes[i].set_title(f'JPEG Q={q}\nMAE={resultados["mae"][idx]:.2f}', fontsize=9)
        axes[i].axis('off')

    plt.suptitle(f'Comparação Visual - {nome_imagem}', fontsize=12)
    plt.tight_layout()
    caminho = os.path.join(pasta_saida, f"visual_{nome_imagem}.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"Mosaico visual guardado: {caminho}")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

def main():
    # Procurar todas as imagens PNG na pasta de entrada
    ficheiros_png = sorted([
        os.path.join(PASTA_ENTRADA, f) 
        for f in os.listdir(PASTA_ENTRADA) 
        if f.lower().endswith('.png')
    ])

    if not ficheiros_png:
        print(f"ERRO: Nenhum ficheiro PNG encontrado em '{PASTA_ENTRADA}'")
        print("Certifica-te de que descomprimiste o TestImages.zip para essa pasta.")
        return

    print(f"Encontradas {len(ficheiros_png)} imagem(ns) PNG para processar.")

    todos_resultados = {}

    for caminho in ficheiros_png:
        nome = os.path.splitext(os.path.basename(caminho))[0]
        resultados, img_original = processar_imagem(caminho, QUALIDADES, PASTA_SAIDA)
        criar_grafico(resultados, nome, PASTA_SAIDA)
        criar_mosaico_visual(nome, img_original, resultados, PASTA_SAIDA)
        todos_resultados[nome] = resultados

    # Gráfico comparativo global (todas as imagens no mesmo gráfico)
    fig, ax = plt.subplots(figsize=(10, 7))
    for nome, res in todos_resultados.items():
        ax.plot(res['taxa_compressao'], res['mae'], '-o', label=nome, linewidth=2)

    ax.set_xlabel('Taxa de Compressão', fontsize=12)
    ax.set_ylabel('Erro Absoluto Médio (MAE)', fontsize=12)
    ax.set_title('Comparação Global: Taxa de Compressão vs MAE', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_SAIDA, "grafico_comparativo_global.png"), dpi=150)
    plt.close()
    print(f"\nGráfico comparativo global guardado.")

    print(f"\n{'='*60}")
    print("PROCESSAMENTO CONCLUÍDO!")
    print(f"Resultados guardados em: {os.path.abspath(PASTA_SAIDA)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()