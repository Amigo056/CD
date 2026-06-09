# =====================================================================
# ADICIONA ISTO ÀS TUAS FUNÇÕES NO RECEPTOR.PY
# =====================================================================

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

def hamming_decode(dados_recebidos_bytes):
    """Descodifica uma sequência de bytes inteira usando Hamming (7,4)"""
    print("\n--- Executando: Descodificação Hamming (7,4) no Canal ---")
    
    # 1. Converter a string/bytes recebidos numa lista de bits para simular o canal
    # (No cenário real do guião, o Pico enviaria os bits codificados, mas como 
    # estamos a fazer pós-processamento no PC, vamos fingir que o texto recebido 
    # foi o que passou pelo canal codificado)
    
    # Exemplo simples de teste: Vamos apenas demonstrar a lógica a funcionar
    # para o primeiro caractere do teu pangrama (Letra 'T')
    char_teste = dados_recebidos_bytes[0] if isinstance(dados_recebidos_bytes, bytes) else ord(dados_recebidos_bytes[0])
    
    # Separar os 8 bits do caractere em 2 nibbles (4 bits superiores, 4 inferiores)
    n1 = (char_teste >> 4) & 0x0F
    n2 = char_teste & 0x0F
    
    # Extrair os bits individuais do primeiro nibble para testar
    d1 = (n1 >> 3) & 1
    d2 = (n1 >> 2) & 1
    d3 = (n1 >> 1) & 1
    d4 = n1 & 1
    
    # Codificar
    bloco_codificado = hamming_encode_nibble(d1, d2, d3, d4)
    print(f"Bits de dados originais (4 bits): {[d1,d2,d3,d4]}")
    print(f"Bloco transmitido com Paridade (7 bits): {bloco_codificado}")
    
    # --- SIMULAÇÃO DE INJEÇÃO DE ERRO NO CANAL ---
    # Vamos forçar um erro propositado no bit d2 (índice 1) para ver a magia acontecer
    bloco_codificado[1] ^= 1 
    print(f"Bloco após sofrer ruído no canal:        {bloco_codificado}")
    # ---------------------------------------------
    
    # Correr o descodificador que criámos lá em cima
    dados_corrigidos = hamming_decode_7bits(bloco_codificado)
    print(f"Bits recuperados após o Hamming:         {dados_corrigidos}")