# (j) Recebe o nome de um ficheiro de entrada e apresenta o histograma dos símbolos do ficheiro e a respetiva entropia.
from Utils import utils
import matplotlib.pyplot as plt
import os

counter = 1

def desenhar_histograma_matplotlib(frequencias, titulo="Histograma de Símbolos"):
    """
    Gera histograma usando matplotlib - salva como imagem.
    """
    simbolos = list(frequencias.keys())
    contagens = list(frequencias.values())
    global counter
    plt.figure(figsize=(10, 6))
    plt.bar(simbolos, contagens, color='skyblue', edgecolor='black')
    plt.xlabel('Símbolos')
    plt.ylabel('Frequência')
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'histograma{counter}.png', dpi=150)
    plt.show()
    counter += 1

def main():
    utils.prepare_test_files()

    input1, _, input2, _, input3, _ = utils.files_path()

    for input_file in [input1, input2, input3]:
        with open(input_file, 'r') as f:
            conteudo = f.read()
    
        frequencias = utils.calcular_frequencias(conteudo)
        print(f'------------{os.path.basename(input_file)}------------')
        print(f'Entropia: {utils.entropia(conteudo):.4f}\n')
        desenhar_histograma_matplotlib(frequencias, titulo=f"Histograma de Símbolos - {os.path.basename(input_file)}")

if __name__ == "__main__":
    main()