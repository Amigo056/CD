import machine
import time
from hamming import codificar_texto_hamming 

modoHamming = True  
# Configura a UART0 na velocidade de 115200 baud
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# O pangrama exigido no enunciado [cite: 22]
pangrama = "The quick brown fox jumps over the lazy dog"

print("Pico 2 W: A iniciar a transmissão simplex...")

while True:
    if modoHamming:
        print("[PICO] A iniciar envio codificado caractere a caractere...")
        
        # Percorre o pangrama letra a letra
        for letra in pangrama:
            # Codifica apenas uma letra de cada vez (gera 14 bytes de '0's e '1's)
            bloco_letra = codificar_texto_hamming(letra)
            
            # Garante formato bytes e envia de imediato
            if isinstance(bloco_letra, str):
                uart.write(bloco_letra.encode('utf-8'))
            else:
                uart.write(bloco_letra)
                
            # Pequena pausa de 2 milissegundos para o buffer da UART esvaziar
            time.sleep_ms(2)
            
        # Quando acabar a frase toda, envia o fim de linha para destravar o PC
        uart.write(b"\r\n")
        print("[PICO] Frase completa enviada.")
        
    else:
        # Modo normal sem Hamming
        uart.write((pangrama + "\r\n").encode("utf-8"))
        
    time.sleep(2)
