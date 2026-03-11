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
    plt.savefig('histograma'+str(counter)+'.png', dpi=150)
    plt.show()
    counter += 1

def prepare_test_files():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, 'Data')
    with open(os.path.join(data_dir, 'input_j1.txt'), 'w') as f:
        f.write('aaaabbcd')
    with open(os.path.join(data_dir, 'input_j2.txt'), 'w') as f:
        f.write('awqsedrftgyhujikolpçzxcvbnmeeeeeeeeeeeeeeeoooooooaaaaaaaaaaaaaaaaaaaauusssssfffffiqiqunxz')
    with open(os.path.join(data_dir, 'input_j3.txt'), 'w') as f:
        f.write('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaao')

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
    
        frequencias = utils.calcular_frequencias(conteudo)
        print('------------------------')
        print(f'Entropia de {os.path.basename(input_file)}: {utils.entropia(conteudo):.4f}\n')
        desenhar_histograma_matplotlib(frequencias, titulo=f"Histograma de Símbolos - {os.path.basename(input_file)}")

if __name__ == "__main__":
    main()