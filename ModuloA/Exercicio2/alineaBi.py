import random
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
from ex2alineaA import symbol_source

X = [1, 2, 3,4,5,6]
P = [1/6] * 6  

def lançarDado():
    dado1 = symbol_source(X, P, 1,)
    dado2 = symbol_source(X, P, 1,)
    return dado1, dado2

def jogarTurno(jogador, turno, nome_jogador, ficheiro):
    dado1, dado2 = lançarDado()
    soma = dado1[0] + dado2[0]
    jogador.append(soma)

    total = sum(jogador)
    ficheiro.write(
        f"Turno {turno} | {nome_jogador} | dado1={dado1[0]} | dado2={dado2[0]} | soma={soma} | total={total}\n"
    )
    ficheiro.flush()

    print(f"{nome_jogador} lançou: {dado1} e {dado2} (Soma: {soma})")

    if dado1[0] == dado2[0]:
        print("Duplo! Quer jogar novamente? S/N")
        while True:
            resposta = input().upper()
            if resposta == "S":
                jogarTurno(jogador, turno, nome_jogador, ficheiro)
                break
            if resposta == "N":
                break
    
    
def main():
    jogador1 = []
    jogador2 =  []
    turn = 1

    while True:
        print(f"Numero de jogadas?")
        try:
            num_jogadas = int(input())
        except ValueError:
            print("Entrada inválida. Introduza um número inteiro.")
            continue

        if num_jogadas > 0:
            break
        print("Número de jogadas deve ser maior que zero. Tente novamente.")
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, "ex2Results")
    caminho_log = os.path.join(pasta_saida,"jogo_dado3.txt")
    
    with open(caminho_log, "w", encoding="utf-8") as log_file:
        while turn <= num_jogadas:
            print(f"Turno {turn}: Jogador 1")
            jogarTurno(jogador1, turn, "Jogador 1", log_file)

            print(f"Turno {turn}: Jogador 2")
            jogarTurno(jogador2, turn, "Jogador 2", log_file)

            turn += 1

    print("Fim do jogo!")
    print(f"Pontuação final do Jogador 1: {sum(jogador1)}")
    print(f"Pontuação final do Jogador 2: {sum(jogador2)}")
    if(sum(jogador1) > sum(jogador2)):
        print("Jogador 1 é o vencedor!")
    elif(sum(jogador2) > sum(jogador1)):
        print("Jogador 2 é o vencedor!")
    else:
        print("O jogo terminou empatado!")

if __name__ == "__main__":
    main()