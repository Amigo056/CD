
import math
import os
import sys
from PIL import Image
import subprocess
import ex3_utils
import ex3a
import ex1b
import math
import secrets
import tempfile
from PIL import Image, UnidentifiedImageError

def cod_de_fonte(input_file, output_dir, modo='lossless', qualidade=90):
    os.makedirs(output_dir, exist_ok=True)

    if modo == 'lossless':
        ficheiro_gerado = ex3_utils.compress(input_file, output_dir)
    elif modo == 'loss':
        qualidades = [qualidade]
        ex3_utils.processar_imagem(input_file, qualidades, output_dir)
        nome_base = os.path.splitext(os.path.basename(input_file))[0]
        ficheiro_gerado = os.path.join(output_dir, f"{nome_base}_q{qualidade}.jpg")
    else:
        raise ValueError("Modo invalido. Usa 'lossless' ou 'loss'.")

    with open(ficheiro_gerado, 'rb') as f:
        data = f.read()

    return data
        
def cifra(data,ficheiro_chave):
    chave = secrets.token_bytes(len(data))
    novos_dados = ex3_utils.cifra_vernam(data, chave)
    with open(ficheiro_chave, "wb") as f:
            f.write(chave)
    return novos_dados

def cod_de_canal(dados):
   return ex3a.encode_crc32(dados)

def canal(dados):
    return ex1b.burst_bit_error_bytes(dados, 0)

def decod_de_canal(dados):
    return ex3a.check_crc32(dados)


def decifrar(dados_cifrados, ficheiro_chave):
    with open(ficheiro_chave, 'rb') as f:
        chave = f.read()
    dados_decifrados = ex3_utils.cifra_vernam(dados_cifrados, chave)
    return dados_decifrados

def decod_de_fonte(dados, output_dir, modo='lossless', nome_original=None):
    os.makedirs(output_dir, exist_ok=True)

    if nome_original is None:
        raise ValueError("É preciso indicar o nome_original.")

    nome_base = os.path.splitext(os.path.basename(nome_original))[0]
    if modo == 'lossless':
        with tempfile.TemporaryDirectory(prefix="descompressao_") as pasta_tmp:
            caminho_7z = os.path.join(pasta_tmp, f"{nome_base}_temp.7z")

            with open(caminho_7z, "wb") as f:
                f.write(dados)

            ficheiro_extraido = ex3_utils.descompress(caminho_7z, nome_original, output_dir)
            return ficheiro_extraido

    elif modo == 'loss':
        with tempfile.TemporaryDirectory(prefix="imagem_") as pasta_tmp:
            caminho_jpg = os.path.join(pasta_tmp, f"{nome_base}_recebida.jpg")

            with open(caminho_jpg, "wb") as f:
                f.write(dados)

            ficheiro_saida = ex3_utils.descomprimir_imagem(caminho_jpg, output_dir, formato_saida="PNG")
            return ficheiro_saida

    else:
        raise ValueError("Modo invalido. Usa 'lossless' ou 'loss'.")
    
    
def test_files(files, modo, qualidade=90):
    input_files = ex3_utils.filesToTest(files)
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_chaves = os.path.join(dir_script, "chaves")
    pasta_resultados_cod = os.path.join(dir_script, "Resultados_Codificados")
    pasta_resultados_decod = os.path.join(dir_script, "Resultados_Decodificados")
    for input_file in input_files:
        nome_base = os.path.splitext(os.path.basename(input_file))[0]
        file_chave = os.path.join(pasta_chaves,f"{nome_base}_key.key")
        cod_fonte_data = cod_de_fonte(input_file, pasta_resultados_cod, modo=modo, qualidade=qualidade)
        cifra_data = cifra(cod_fonte_data, file_chave)
        cod_canal_data = cod_de_canal(cifra_data)
        canal_data = canal(cod_canal_data)
        decod_canal_data, check_crc = decod_de_canal(canal_data)

        if not check_crc:
            print(f"Erro detectado no canal para o ficheiro {input_file}")
        else:
            print(f"Sem erros detectados no canal para o ficheiro {input_file}")
            dados_decifrados = decifrar(decod_canal_data, file_chave)
            ficheiro_decodificado = decod_de_fonte(
                dados_decifrados,
                pasta_resultados_decod,
                modo=modo,
                nome_original=input_file,
            )
            print(f"Ficheiro decodificado guardado em: {ficheiro_decodificado}")

    
def main():
    test_files("Ex3TestFilesLossless", modo='lossless')
    #test_files("Ex3TestFilesLoss", modo='loss', qualidade=70)

    print("-" * 50)
    original_files = ex3_utils.filesToTest("Ex3TestFilesLossless")
    decod_files = ex3_utils.filesToTest("Resultados_Decodificados")
    for orig, decod in zip(original_files, decod_files):
        if ex3_utils.ficheiros_iguais(orig, decod):
            print(f"Os ficheiros {orig} e {decod} são idênticos.")
        else:
            print(f"Os ficheiros {orig} e {decod} são diferentes.")

if __name__ == "__main__":
    main()    
              
               
     