import math
from alinea_h import entropia,simbolo_mais_frequente, prepare_test_files, files_path

def analisa_ficheiro(file):
   
    with open(file, "r") as f:
        dados = f.read()
    if not dados:
        return None, 0.0

    simbolo_mais_freq, freq = simbolo_mais_frequente(dados)    
    entropia_valor = entropia(dados)
    print(f'Símbolo mais frequente: {simbolo_mais_freq} (frequência: {freq})')
    print(f'Entropia: {entropia_valor:.4f}\n')

    return simbolo_mais_freq ,freq ,entropia_valor

def main():
    prepare_test_files()
    input1, output1, input2, output2, input3, output3 = files_path()
    analisa_ficheiro(input1)
    analisa_ficheiro(input2)
    analisa_ficheiro(input3) 

if __name__ == "__main__":
    main()