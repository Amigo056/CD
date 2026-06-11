import serial


from single_bit_error import single_bit_error_bits       
from burst_errors import burst_bit_error_bits        
from hamming import descodificar_texto_hamming             

# Controlo do guião (parâmetro de entrada)
USAR_HAMMING = False
USE_SINGLE_BIT_ERROR = True
USE_BURST_BIT_ERROR = False

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
        outFile = "dados_recebidos.txt"
        texto_recebido = dados_bytes.decode('utf-8').strip()
        print(f"\n[RECEBIDO] Texto puro do Pico: \"{texto_recebido}\"")
        
       
        
        if not USAR_HAMMING:
            with open(outFile, "w", encoding="utf-8") as f:
                f.write(texto_recebido + "\n")
            print("[FICHEIRO] Dados guardados com sucesso em 'dados_recebidos.txt'.")
          
        else:        
            dados_ba = bytearray(texto_recebido, "utf-8")
        
            if USE_SINGLE_BIT_ERROR:
                outFile = "dados_com_erro_single.txt"
                dados_ba = single_bit_error_bits(dados_ba, p=PROB)
                print(f"Bits com erro aleatório: {dados_ba}")

            if USE_BURST_BIT_ERROR:
                outFile = "dados_com_erro_burst.txt"
                dados_ba = burst_bit_error_bits(dados_ba, B=BURST)
                print(f"Bits com erro aleatório: {dados_ba}")
           
            texto_descodificado, erros_detetados, erros_corrigidos = descodificar_texto_hamming(dados_ba)
            print(f"Erros detetados: {erros_detetados}")
            print(f"Erros corrigidos: {erros_corrigidos}")

            with open(outFile, "w", encoding="utf-8") as f:
                f.write(texto_descodificado + "\n")
            print(f"[FICHEIRO] Dados guardados com sucesso em {outFile}.")
    else:
        print("[AVISO] Timeout! Nenhum dado recebido do Pico 2 W.")
        
        

except KeyboardInterrupt:
    print("\n[SISTEMA] Interrompido pelo utilizador.")
finally:
    ser.close()
    print("[SISTEMA] Porta série fechada com segurança.")
