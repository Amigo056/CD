import serial
import time
# 
# =====================================================================
# IMPORTAR AS TUAS FUNÇÕES DOS OUTROS FICHEIROS .PY
# =====================================================================
# O Python vai procurar os ficheiros na mesma pasta e importar as funções
from single_bit_error import single_bit_error       # Ajusta o nome da função se for diferente
from burst_errors import burst_bit_error            # Ajusta o nome da função se for diferente
from hamming import hamming_decode                  # Ajusta o nome da função se for diferente

# Controlo do guião (parâmetro de entrada)
USAR_HAMMING = True
USE_SINGLE_BIT_ERROR = False
USE_BURST_BIT_ERROR = False

# Configuração da Porta Série (Usa a porta do teu ADAPTADOR de jumpers!)
PORTA_ADAPTADOR = 'COM3'  
BAUDRATE = 115200
PROB = 0.01
BURST = 5

try:
    ser = serial.Serial(PORTA_ADAPTADOR, BAUDRATE, timeout=3)
    print(f"[SISTEMA] Ligado à porta {PORTA_ADAPTADOR}. A aguardar dados do Pico 2 W...")
except Exception as e:
    print(f"[ERRO] Falha ao abrir a porta: {e}")
    exit()

# =====================================================================
# FLUXO PRINCIPAL DE PROCESSAMENTO
# =====================================================================
try:
    # Ler a linha enviada pelo Pico 2 W
    dados_bytes = ser.readline()
    
    if dados_bytes:
        texto_recebido = dados_bytes.decode('utf-8').strip()
        print(f"\n[RECEBIDO] Texto puro do Pico: \"{texto_recebido}\"")
        
        # Guardar no ficheiro .txt conforme exigido no guião
        with open("dados_recebidos.txt", "w", encoding="utf-8") as f:
            f.write(texto_recebido + "\n")
        print("[FICHEIRO] Dados guardados com sucesso em 'dados_recebidos.txt'.")
        
        # =================================================================
        # 3. CONTEXTO DA ALÍNEA (b): Injeção e Análise de Erros pós-receção
        # =================================================================
        print("\n==============================================")
        print("          TESTES DE ERRO PÓS-RECEÇÃO          ")
        print("==============================================")
        
        # O ficheiro que acabámos de criar com o texto limpo serve de entrada
        ficheiro_entrada = "dados_recebidos.txt"

        # CENÁRIO 1: Sem Hamming -> Aplicar funções de erro normais
        if not USAR_HAMMING:
            print(f"[MODO] Parâmetro: USAR_HAMMING = {USAR_HAMMING}")

            if USE_SINGLE_BIT_ERROR: 
                # 1. Testar o Erro Isolado (Single Bit Error)
                print("\nExecuting: Single Bit Error...")
                ficheiro_saida_single = "dados_com_erro_single.txt"
            
                # Chamada da tua função com os teus parâmetros exatos:
                single_bit_error(
                    input_file=ficheiro_entrada, 
                    output_file=ficheiro_saida_single, 
                    p=PROB
                )
                print(f"[OK] Ficheiro gerado com erro isolado: '{ficheiro_saida_single}'")
            
            if USE_BURST_BIT_ERROR:
                # 2. Testar o Erro em Rajada (Burst Bit Error)
                print("\nExecuting: Burst Bit Error...")
                ficheiro_saida_burst = "dados_com_erro_burst.txt"
            
                # Chamada da tua função com os teus parâmetros exatos:
                burst_bit_error(
                    input_file=ficheiro_entrada, 
                    output_file=ficheiro_saida_burst, 
                    B=BURST
                )
                print(f"[OK] Ficheiro gerado com erro em rajada: '{ficheiro_saida_burst}'")
            
        # CENÁRIO 2: Com Hamming -> Ativar descodificação/correção
        else:
            print(f"[MODO] Parâmetro: USAR_HAMMING = {USAR_HAMMING} (Deteção ATIVA)")
            
            # Aqui chamas a tua função de Hamming passando o texto ou o ficheiro
            # (conforme a tenhas estruturado)
            hamming_decode(texto_recebido)
    else:
        print("[AVISO] Timeout! Nenhum dado recebido do Pico 2 W.")

except KeyboardInterrupt:
    print("\n[SISTEMA] Interrompido pelo utilizador.")
finally:
    ser.close()
    print("[SISTEMA] Porta série fechada com segurança.")

