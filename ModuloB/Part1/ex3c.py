import ex3_utils
import ex3a
import ex3b
import os

def analisar_bloco(nome_bloco, dados, nome_base, pasta_hist):
    tamanho = ex3_utils.dimensao_bytes(dados)
    h = ex3_utils.entropia(dados)
    frequencias = ex3_utils.calcular_frequencias(dados)

    caminho_hist = os.path.join(pasta_hist, f"{nome_base}_{nome_bloco}.png")
    ex3_utils.desenhar_histograma_matplotlib(
        frequencias,
        titulo=f"Histograma {nome_bloco} - {nome_base}",
        caminho_saida=caminho_hist
    )


    print(f'\n{"="*50}')
    print(f'FICHEIRO: {nome_base} - BLOCO: {nome_bloco}')
    print(f'Tamanho (bytes): {tamanho}')
    print(f'Entropia (bits/símbolo): {h:.4f}')
    print(f'{"="*50}')
    return {
        "dimensao": tamanho,
        "entropia": h,
        "histograma": caminho_hist
    }
    
def test_file(input_file, modo, qualidade=90):
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_chaves = os.path.join(dir_script, "chaves")
    pasta_resultados_cod = os.path.join(dir_script, "Resultados_Codificados")
    pasta_resultados_decod = os.path.join(dir_script, "Resultados_Decodificados")
    pasta_histogramas = os.path.join(dir_script, "Histogramas")
    nome_base = os.path.splitext(os.path.basename(input_file))[0]
    file_chave = os.path.join(pasta_chaves, f"{nome_base}_key.key")

    with open(input_file, 'rb') as f:
        data_A = f.read()
        analisar_bloco("A", data_A, nome_base, pasta_histogramas)

    cod_fonte_data = ex3b.cod_de_fonte(input_file, pasta_resultados_cod, modo=modo, qualidade=qualidade)
    analisar_bloco("B", cod_fonte_data, nome_base, pasta_histogramas)

    taxa_compressao = ex3_utils.calcular_taxa_compressao(
        ex3_utils.dimensao_bytes(data_A),
        ex3_utils.dimensao_bytes(cod_fonte_data)
    )
    print(f'Taxa de Compressão: {taxa_compressao:.4f}')

    cifra_data = ex3b.cifra(cod_fonte_data, file_chave)
    analisar_bloco("C", cifra_data, nome_base, pasta_histogramas)

    cod_canal_data = ex3b.cod_de_canal(cifra_data)
    analisar_bloco("D", cod_canal_data, nome_base, pasta_histogramas)
    canal_data = ex3b.canal(cod_canal_data)
    decod_canal_data, check_crc = ex3b.decod_de_canal(canal_data)

    if not check_crc:
        print(f"Erro detectado no canal para o ficheiro {input_file}")
    else:
        dados_decifrados = ex3b.decifrar(decod_canal_data, file_chave)
        ficheiro_decodificado = ex3b.decod_de_fonte(
            dados_decifrados,
            pasta_resultados_decod,
            modo=modo,
            nome_original=input_file,
        )
        print(f"Ficheiro decodificado guardado em: {ficheiro_decodificado}")
        with open(ficheiro_decodificado, 'rb') as f:
            data_E = f.read()
        analisar_bloco("E", data_E, nome_base, pasta_histogramas)


def main():
    dir_script = os.path.dirname(os.path.abspath(__file__))
    test1 = os.path.join(dir_script, "Ex3TestFilesLossless/alice29.txt")
    test2 = os.path.join(dir_script, "Ex3TestFilesLoss/bird.png")
    test_file(test1, modo='lossless')
    test_file(test2, modo='loss', qualidade=70)


if __name__ == "__main__":
    main()  
    
                