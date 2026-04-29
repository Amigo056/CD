import os

from ModuloA.Exercicio2.utils import simbolo_mais_frequente, entropia, calcular_frequencias, prob_max, info_propria, max_entropia, entropia_redundancia, ler_ficheiro
import matplotlib.pyplot as plt
import ex2 

    
def filesToTest(path):
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir_atual, path)
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]


    
def main():
    test_files = filesToTest("Test Images")

    try:
        for file in test_files:
            print(f"Processando ficheiro: {file}")
    except Exception as e:
        print(f"Erro ao processar ficheiro {file}: {e}")        
        
if __name__ == "__main__":
    main()               


            
            

