# (i) Recebe o nome de um ficheiro como entrada e determina o símbolo mais frequente e a entropia do ficheiro (ver slides 6).

from Utils import utils

def analisa_ficheiro(file):
   
    with open(file, "r") as f:
        dados = f.read()
    if not dados:
        return None, 0.0

    simbolo_mais_freq, freq = utils.simbolo_mais_frequente(dados)    
    entropia_valor = utils.entropia(dados)
    print(f'Símbolo mais frequente: {simbolo_mais_freq} (frequência: {freq})')
    print(f'Entropia: {entropia_valor:.4f}\n')

    return simbolo_mais_freq ,freq ,entropia_valor

def main():
    utils.prepare_test_files()
    input1, _, input2, _, input3, _ = utils.files_path()
    analisa_ficheiro(input1)
    analisa_ficheiro(input2)
    analisa_ficheiro(input3) 

if __name__ == "__main__":
    main()