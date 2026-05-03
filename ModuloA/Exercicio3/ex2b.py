import os

import matplotlib.pyplot as plt
import utils
from PIL import Image
import ex1



def test_files():
    original_files = utils.filesToTest("Test_Images")
    cifra_files = utils.filesToTest("imagens_cifradas")
    decifra_files = utils.filesToTest("imagens_decifradas")
    
    try:
        for original_file, cifra_file, decifra_file in zip(original_files, cifra_files, decifra_files):
            
            utils.file_scanner(original_file, output_path="ex2bResults/original_histogramas")
            utils.file_scanner(cifra_file, output_path="ex2bResults/cifra_histogramas")
            utils.file_scanner(decifra_file, output_path="ex2bResults/decifra_histogramas")
            img_original = Image.open(original_file).convert("RGB")
            img_decifra = Image.open(decifra_file)
            mae = ex1.calcular_mae(img_original, img_decifra)
            print(f"Valor de MAE entre {original_file} e {decifra_file}: {mae:.4f}")            
            
    except Exception as e:
        print(f"Erro ao processar ficheiros {cifra_file} e {decifra_file}: {e}")
            
def main():

    test_files()      
        
if __name__ == "__main__":
    main()               


            
            

