import serial


from single_bit_error import single_bit_error       
from burst_errors import burst_bit_error           
from hamming import hamming_decode_file             

# Controlo do guião (parâmetro de entrada)
USAR_HAMMING = True
USE_SINGLE_BIT_ERROR = True
USE_BURST_BIT_ERROR = True

# Configuração da Porta Série 
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
        
       
        with open("dados_recebidos.txt", "w", encoding="utf-8") as f:
            f.write(texto_recebido + "\n")
        print("[FICHEIRO] Dados guardados com sucesso em 'dados_recebidos.txt'.")
        

        print("\n==============================================")
        print("          TESTES DE ERRO PÓS-RECEÇÃO          ")
        print("==============================================")
        
        
        ficheiro_entrada = "dados_recebidos.txt"

        if USE_SINGLE_BIT_ERROR:
            single_bit_error(
            input_file="dados_recebidos.txt",
            output_file="dados_com_erro_single.txt",
            p=PROB
            )
            print("[OK] Gerado: dados_com_erro_single.txt")

            if USAR_HAMMING:
                hamming_decode_file("dados_com_erro_single.txt")

        if USE_BURST_BIT_ERROR:
            burst_bit_error(
            input_file="dados_recebidos.txt",
            output_file="dados_com_erro_burst.txt",
            B=BURST
            )
            print("[OK] Gerado: dados_com_erro_burst.txt")

            if USAR_HAMMING:
                hamming_decode_file("dados_com_erro_burst.txt")
    else:
        print("[AVISO] Timeout! Nenhum dado recebido do Pico 2 W.")

except KeyboardInterrupt:
    print("\n[SISTEMA] Interrompido pelo utilizador.")
finally:
    ser.close()
    print("[SISTEMA] Porta série fechada com segurança.")

