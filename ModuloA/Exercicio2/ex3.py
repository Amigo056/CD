# 3. Codificação e compressão de dados sem perda - análise de resultados.
#   Escolha uma ferramenta de compressão de uso comum (por exemplo, WinZip, WinRar ou 7-Zip).
#   (a) Escreva uma função que, sobre um ficheiro de entrada, determina e apresenta o valor da entropia; realiza a compressão
#       e a descompressão com a ferramenta escolhida; determine a razão de compressão, o tempo de compressão e o tempo
#       de descompressão; verifique que o ficheiro original e o ficheiro descodificado são iguais. Apresente os resultados para
#       alguns ficheiros do conjunto TestFilesCD.zip e para outros ficheiro gerados no exercício 2.
#   (b) Sobre os resultados da alínea anterior, apresente o gráfico que relaciona a entropia do ficheiro (eixo dos xx) e a compressão obtida em bit por byte (eixo dos yy). 
#       Comente sobre o formato do gráfico.

import subprocess
import time
import os
import utils

def compress(input_file, compressType):
    if compressType == '7z':
        compressed_file = input_file + '.7z'
        start_time = time.time()
        subprocess.run(['7z', 'a', compressed_file, input_file], stdout=subprocess.DEVNULL)
        tempo_compressao = time.time() - start_time
        return compressed_file, tempo_compressao
    else:
        raise ValueError("Tipo de compressão não suportado")
    
def descompress(compressed_file, compressType):
    if compressType == '7z':
        descompressed_file = compressed_file.replace('.7z', '_descompressed' + os.path.splitext(compressed_file)[1])
        start_time = time.time()
        subprocess.run(['7z', 'x', compressed_file, '-so'], stdout=subprocess.DEVNULL)
        tempo_descompressao = time.time() - start_time
        return descompressed_file, tempo_descompressao
    else:
        raise ValueError("Tipo de compressão não suportado")
    
def compress_ratio(input_file, compressed_file):
    tamanho_original = os.path.getsize(input_file)
    tamanho_comprimido = os.path.getsize(compressed_file)
    return tamanho_comprimido / tamanho_original


def compress_descompress(input_file):
    # Compressão usando 7-Zip
    compressed_file, tempo_compressao = compress(input_file, '7z')

    # Descompressão
    descompressed_file, tempo_descompressao = descompress(compressed_file, '7z')

    # Verificar integridade dos ficheiros
    with open(input_file, 'rb') as f:
        original_data = f.read()
    
    with open(descompressed_file, 'rb') as f:
        descompressed_data = f.read()

    assert original_data == descompressed_data, "Ficheiros não são iguais após descompressão!"

    # Calcular razão de compressão
    razao_compressao = compress_ratio(input_file, compressed_file)

    return {
        'tempo_compressao': tempo_compressao,
        'tempo_descompressao': tempo_descompressao,
        'razao_compressao': razao_compressao
    }

def main():
    files = utils.filesToTest()
    resultados = []
    for file in files:
    
        resultado = compress_descompress(file)
        resultados.append((os.path.basename(file), resultado))

        print(f"Ficheiro: {os.path.basename(file)}")
        print(f"Entropia: {utils.file_entropia(file):.4f}")
        print(f"Tempo de Compressão: {resultado['tempo_compressao']:.4f} segundos")
        print(f"Tempo de Descompressão: {resultado['tempo_descompressao']:.4f} segundos")
        print(f"Razão de Compressão: {resultado['razao_compressao']:.4f}\n")

if __name__ == "__main__":
    main()