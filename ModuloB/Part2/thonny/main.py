import machine
import time

# Configura a UART0 na velocidade de 115200 baud
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# O pangrama exigido no enunciado [cite: 22]
pangrama = "The quick brown fox jumps over the lazy dog\r\n"

print("Pico 2 W: A iniciar a transmissão simplex...")

while True:
    uart.write(pangrama.encode('utf-8'))
    time.sleep(2)