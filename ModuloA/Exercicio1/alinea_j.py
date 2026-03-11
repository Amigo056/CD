# (j) Recebe o nome de um ficheiro de entrada e apresenta o histograma dos símbolos do ficheiro e a respetiva entropia.
from alinea_h import entropia
import matplotlib.pyplot as plt
from collections import Counter
import os

def desenhar_histograma_matplotlib(frequencias, titulo="Histograma de Símbolos"):
    """
    Gera histograma usando matplotlib - salva como imagem.
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
    plt.savefig('histograma.png', dpi=150)
    plt.show()

def calcular_frequencias(conteudo):
    return Counter(conteudo)

def prepare_test_files():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, 'Data')
    with open(os.path.join(data_dir, 'input_j1.txt'), 'w') as f:
        f.write('ABCD1234surhhfuiweifowej')
    with open(os.path.join(data_dir, 'input_j2.txt'), 'w') as f:
        f.write('EFGH5678diueioewjxpkxqp')
    with open(os.path.join(data_dir, 'input_j3.txt'), 'w') as f:
        f.write('IJKL9012928874238hduweeeee')

def files_path():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    
    input1 = os.path.join(dir_atual, 'Data', 'input_j1.txt')

    input2 = os.path.join(dir_atual, 'Data', 'input_j2.txt')
    
    input3 = os.path.join(dir_atual, 'Data', 'input_j3.txt')
    
    return input1, input2, input3

def main():
    prepare_test_files()

    input1, input2, input3 = files_path()

    for input_file in [input1, input2, input3]:
        with open(input_file, 'r') as f:
            conteudo = f.read()
    
        frequencias = calcular_frequencias(conteudo)
        desenhar_histograma_matplotlib(frequencias, titulo=f"Histograma de Símbolos - {os.path.basename(input_file)}")

if __name__ == "__main__":
    main()