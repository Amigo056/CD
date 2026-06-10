def hamming_encode_nibble(d1, d2, d3, d4):
    """Codifica 4 bits de dados em 7 bits (Hamming 7,4)"""
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    return [d1, d2, d3, d4, p1, p2, p3]

def hamming_decode_7bits(bloco):
    """
    Recebe uma lista de 7 bits [d1, d2, d3, d4, p1, p2, p3].
    Deteta se há erro, corrige se for erro de 1 bit, e devolve os 4 bits originais.
    """
    d1, d2, d3, d4, p1, p2, p3 = bloco

    # Calcular os síndromas de erro (XOR entre o que devia ser e o que veio)
    s1 = p1 ^ (d1 ^ d2 ^ d4)
    s2 = p2 ^ (d1 ^ d3 ^ d4)
    s3 = p3 ^ (d2 ^ d3 ^ d4)

    # O valor do síndroma indica a posição do erro (em binário: s3 s2 s1)
    # Convertendo para decimal para saber qual bit falhou:
    posicao_erro = (s3 << 2) | (s2 << 1) | s1

    if posicao_erro != 0:
        print(f"  [HAMMING] Erro detetado no bit posição (s3s2s1 binário): {posicao_erro}")
        
        # Mapeamento padrão da posição do erro para o bit correspondente na nossa lista:
        # Se alteraste a ordem dos bits na tua aula, ajusta este dicionário!
        mapeamento_posicao = {
            1: 4,  # p1 falhou (índice 4 na lista)
            2: 5,  # p2 falhou (índice 5 na lista)
            4: 6,  # p3 falhou (índice 6 na lista)
            3: 0,  # d1 falhou (índice 0 na lista)
            5: 1,  # d2 falhou (índice 1 na lista)
            6: 2,  # d3 falhou (índice 2 na lista)
            7: 3   # d4 falhou (índice 3 na lista)
        }
        
        if posicao_erro in mapeamento_posicao:
            idx = mapeamento_posicao[posicao_erro]
            bloco[idx] ^= 1  # Faz o 'flip' do bit para o corrigir!
            print(f"  [HAMMING] Bit corrigido com sucesso!")
    else:
        print("  [HAMMING] Bloco verificado. Sem erros.")

    # Devolve apenas os 4 bits de dados originais [d1, d2, d3, d4]
    return bloco[0:4]

def byte_to_bits(valor):
    return [(valor >> i) & 1 for i in range(7, -1, -1)]

def hamming_decode_file(nome_ficheiro):
    with open(nome_ficheiro, "rb") as f:
        dados = f.read()

    total_blocos = 0
    erros_detetados = 0

    for byte in dados:
        bits = byte_to_bits(byte)

        nibble1 = bits[:4]
        nibble2 = bits[4:]

        bloco1 = hamming_encode_nibble(*nibble1)
        bloco2 = hamming_encode_nibble(*nibble2)

        _, erro1 = hamming_decode_7bits(bloco1)
        _, erro2 = hamming_decode_7bits(bloco2)

        total_blocos += 2
        erros_detetados += int(erro1) + int(erro2)

    print(f"[HAMMING] Ficheiro analisado: {nome_ficheiro}")
    print(f"[HAMMING] Total de blocos: {total_blocos}")
    print(f"[HAMMING] Erros detetados/corrigidos: {erros_detetados}")