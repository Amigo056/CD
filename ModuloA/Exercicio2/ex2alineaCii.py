
import os
from pathlib import Path
from ex2alineaA import symbol_source


def ler_linhas(nome_ficheiro):
    with open(nome_ficheiro, "r",encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]
    

def criar_cartoes(n_cartoes, ficheiro_saida):
    X = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    P = [0.30103, 0.17609, 0.12494, 0.09691, 0.07918, 0.06695, 0.05799, 0.05115, 0.04576]
    n_symbols = 8

    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_data = os.path.join(dir_script, "data")
    nomes = ler_linhas(os.path.join(pasta_data, "Nomes.txt"))
    apelidos = ler_linhas(os.path.join(pasta_data, "Apelidos.txt"))
    localidades = ler_linhas(os.path.join(pasta_data, "Localidades.txt"))
    profissoes = ler_linhas(os.path.join(pasta_data, "Profissoes.txt"))
    
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, "ex2Results")
    caminho_saida = os.path.join(pasta_saida,ficheiro_saida)
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        for _ in range(n_cartoes):
            id_cartao = "".join(map(str, symbol_source(X, P, n_symbols)))
            nome = symbol_source(nomes, [1 / len(nomes)] * len(nomes), 1)[0]
            apelido = symbol_source(apelidos, [1 / len(apelidos)] * len(apelidos), 1)[0]
            localidade = symbol_source(localidades, [1 / len(localidades)] * len(localidades), 1)[0]
            profissao = symbol_source(profissoes, [1 / len(profissoes)] * len(profissoes), 1)[0]

            sql = (
                f"INSERT INTO Pessoas (ID, Nome, Apelido, Localidade, Profissao) VALUES "
                f"({id_cartao}, '{nome}', '{apelido}', '{localidade}', '{profissao}');\n"
            )
            f.write(sql)
            

    print(f"Foram criados {n_cartoes} cartoes em: {caminho_saida}")



    
def main():
    criar_cartoes(5000, "cartoes2.txt")

if __name__ == "__main__":
    main()    
    
    

