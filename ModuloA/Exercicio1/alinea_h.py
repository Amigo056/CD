# (h) Realiza a inversão de ordem do conteúdo de um ficheiro, recebendo como parâmetros os nomes do ficheiro de entrada
# e de saída. Por exemplo, se o ficheiro de entrada for ABCD1234, o ficheiro de saída será 4321DCBA. A função deverá
# apresentar o símbolo mais frequente de cada ficheiro e a respetiva entropia
import os
from Utils import utils
def inverter_ficheiro(inputFile, outputFile):
    with open (inputFile, 'r') as f:
        conteudo = f.read()    

    conteudo_invertido = conteudo[::-1]

    with open (outputFile, 'w') as f:
        f.write(conteudo_invertido)

def prepare_test_files():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, 'Data')
    with open(os.path.join(data_dir, 'input1.txt'), 'w') as f:
        f.write('ABCD1234')
    with open(os.path.join(data_dir, 'input2.txt'), 'w') as f:
        f.write('EFGH5678')
    with open(os.path.join(data_dir, 'input3.txt'), 'w') as f:
        f.write('IJKL9012')

def files_path():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    
    input1 = os.path.join(dir_atual, 'Data', 'input1.txt')
    output1 = os.path.join(dir_atual, 'Data', 'output1.txt')

    input2 = os.path.join(dir_atual, 'Data', 'input2.txt')
    output2 = os.path.join(dir_atual, 'Data', 'output2.txt')
    
    input3 = os.path.join(dir_atual, 'Data', 'input3.txt')
    output3 = os.path.join(dir_atual, 'Data', 'output3.txt')
    
    return input1, output1, input2, output2, input3, output3

def main():
    prepare_test_files()

    input1, output1, input2, output2, input3, output3 = files_path()
   
    inverter_ficheiro(input1, output1)
    inverter_ficheiro(input2, output2)
    inverter_ficheiro(input3, output3)

    for read_file in [input1, output1, input2, output2, input3, output3]:
        with open(read_file, 'r') as f:
            conteudo = f.read()
        simbolo, freq = utils.simbolo_mais_frequente(conteudo)
        entropia_valor = utils.entropia(conteudo)
        print('------------------------')
        print(f'Ficheiro: {os.path.basename(read_file)}')
        print(f'Símbolo mais frequente: {simbolo} (frequência: {freq})')
        print(f'Entropia: {entropia_valor:.4f}\n')

if __name__ == "__main__":
    main()