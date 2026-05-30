# Projeto B

## Estado do relatório

Este documento é uma versão provisória do relatório do Projeto B. A secção B.1 já inclui os resultados disponíveis dos exercícios 1 e 2. A secção do exercício 3 e a secção B.2 ficam preparadas para receber os resultados finais quando a implementação estiver concluída.

Enunciados: [Projeto B.1](./Docs/CD_ver_25_26_Modulo_B_1.pdf) e [Projeto B.2](./Docs/CD_ver_25_26_Modulo_B_2.pdf).

## Secção 1 - Projeto B.1

### 1.1 Exercício 1 - Simulação de erros no canal

O primeiro exercício implementa dois modelos de erro sobre ficheiros binários: erros isolados de bit e erros em rajada. A implementação trabalha sempre em modo binário, pelo que a mesma função pode ser aplicada a texto, código-fonte, imagens e outros formatos.

Artefactos principais:

| Funcionalidade | Implementação | Resultados |
| --- | --- | --- |
| Erro isolado com probabilidade `p` | [ex1a.py](./Part1/ex1a.py) | [ficheiros](./Part1/SingleBitErrorResults/), [ficheiros com semente](./Part1/SingleBitErrorResultsSeeded/), [imagens](./Part1/SingleBitErrorImages/), [imagens com semente](./Part1/SingleBitErrorImagesSeeded/) |
| Rajada de `B` bits consecutivos | [ex1b.py](./Part1/ex1b.py) | [ficheiros](./Part1/BurstFilesResults/), [imagens](./Part1/BurstImagesResults/) |
| Métricas BER e SER | [ex1c.py](./Part1/ex1c.py) | cálculo aplicado a exemplos de texto e imagem |

Opções de implementação:

- No erro isolado, cada bit do ficheiro é percorrido individualmente e invertido com probabilidade `p`.
- Foi usada a opção de semente fixa (`seed(42)`) para permitir experiências reprodutíveis.
- Na rajada, é escolhida uma posição inicial aleatória e são invertidos `B` bits consecutivos.
- As métricas foram calculadas por comparação binária entre o ficheiro original e o ficheiro corrompido: BER ao nível do bit e SER ao nível do byte/símbolo.

Resultados experimentais já obtidos:

| Entrada | Resultado | Parâmetro | Bits alterados | BER | Bytes alterados | SER |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| [alice29.txt](./TestFiles/alice29.txt) | [alice29.txt corrompido](./Part1/SingleBitErrorResults/alice29.txt) | `p = 0.01` | 11931 | 0.009806 | 11509 | 0.075672 |
| [bird.png](./TestImages/bird.png) | [bird.png corrompido](./Part1/SingleBitErrorImages/bird.png) | `p = 0.01` | 2669 | 0.010268 | 2569 | 0.079063 |
| [18 ficheiros de teste](./TestFiles/) | [resultados com rajada](./Part1/BurstFilesResults/) | `B = 10` | 10 por ficheiro | - | - | - |
| [9 imagens de teste](./TestImages/) | [resultados com rajada](./Part1/BurstImagesResults/) | `B = 10` | 10 por imagem | - | - | - |

Comentários aos resultados:

- Os valores de BER obtidos para o canal de erro isolado ficam próximos de `p = 0.01`, como esperado num processo probabilístico independente.
- A SER é bastante superior à BER porque basta um único bit alterado para que o byte seja considerado errado. Para `p = 0.01`, o valor esperado por byte é aproximadamente `1 - (1 - p)^8`, ou seja, cerca de 0.077.
- Nos testes de rajada, todos os ficheiros e imagens analisados apresentam exatamente 10 bits alterados, confirmando o comportamento esperado para `B = 10`.

### 1.2 Exercício 2 - Correção de erros isolados com códigos de repetição

O segundo exercício compara três configurações: transmissão sem código de controlo de erros, código de repetição `(3,1)` e código de repetição `(5,1)`. O ficheiro é convertido para bits, cada bit é repetido `n` vezes e a descodificação é feita por maioria.

Artefactos principais:

| Artefacto | Ligação |
| --- | --- |
| Script principal | [ex2.py](./Part1/ex2.py) |
| Código de repetição | [repetition_code.py](./Part1/repetition_code.py) |
| Utilitários de bits | [bit_utils.py](./Part1/bit_utils.py) |
| Métricas | [metrics.py](./Part1/metrics.py) |
| Resultados gerados | [Ex2Results](./Part1/Ex2Results/) |
| Tabela completa da alínea 2.b | [tabela_ex2b.md](./Part1/Ex2Results/tabela_ex2b.md) e [tabela_ex2b.csv](./Part1/Ex2Results/tabela_ex2b.csv) |
| Tabela completa da alínea 2.c | [tabela_ex2c.md](./Part1/Ex2Results/tabela_ex2c.md) e [tabela_ex2c.csv](./Part1/Ex2Results/tabela_ex2c.csv) |

Opções de implementação:

- A simulação usa os ficheiros [a.txt](./TestFiles/a.txt) e [fibonacci.kt](./TestFiles/fibonacci.kt).
- Foram testadas as probabilidades `p = 0.001`, `p = 0.01`, `p = 0.05` e `p = 0.1`.
- A comparação experimental mede o BER no canal e o BER depois da descodificação.
- Os ficheiros codificados e transmitidos pelo canal são temporários; os resultados finais descodificados ficam em [Ex2Results](./Part1/Ex2Results/).

Resumo dos resultados da alínea 2.b, usando o BER depois da correção:

| Ficheiro | `p` | Sem código | Repetição `(3,1)` | Repetição `(5,1)` |
| --- | ---: | ---: | ---: | ---: |
| `a.txt` | 0.001 | 0.001543 | 0.000000 | 0.000000 |
| `a.txt` | 0.010 | 0.011574 | 0.000000 | 0.000000 |
| `a.txt` | 0.050 | 0.042438 | 0.002315 | 0.000000 |
| `a.txt` | 0.100 | 0.097994 | 0.021605 | 0.005401 |
| `fibonacci.kt` | 0.001 | 0.001164 | 0.000000 | 0.000000 |
| `fibonacci.kt` | 0.010 | 0.010584 | 0.000212 | 0.000000 |
| `fibonacci.kt` | 0.050 | 0.045830 | 0.005715 | 0.001164 |
| `fibonacci.kt` | 0.100 | 0.097798 | 0.026672 | 0.009526 |

Resumo dos resultados da alínea 2.c:

| Código | Maior `p` com `BER' = 0` nos dois ficheiros testados | Primeiro valor testado onde falha em pelo menos um ficheiro |
| --- | ---: | ---: |
| Repetição `(3,1)` | 0.005 | 0.010 |
| Repetição `(5,1)` | 0.020 | 0.030 |

Comentários aos resultados:

- Sem código de controlo, o BER depois da transmissão coincide com o BER do canal, porque não existe mecanismo de deteção ou correção.
- O código `(3,1)` corrige todos os casos em que, dentro de um grupo de 3 bits repetidos, no máximo 1 bit é alterado. Quando a probabilidade de erro aumenta, cresce a probabilidade de dois ou mais bits do mesmo grupo serem alterados, o que explica os erros residuais.
- O código `(5,1)` apresenta melhor desempenho porque tolera até 2 erros em cada grupo de 5 bits. Essa melhoria tem custo direto: são transmitidos 5 bits por cada bit de informação, contra 3 no código `(3,1)` e 1 na transmissão sem código.
- Nos valores testados, `(5,1)` manteve BER nulo até uma probabilidade mais elevada do que `(3,1)`, confirmando o compromisso entre redundância e capacidade de correção.

### 1.3 Exercício 3 - Secção provisória

Esta subsecção deve ser completada quando a implementação final do exercício 3 estiver fechada. Como ainda não existe um `ex3.py` nem uma pasta de resultados própria no repositório, ficam já definidos os elementos que devem entrar na versão final.

Estrutura proposta para a versão final:

| Elemento a preencher | Conteúdo esperado | Ligação prevista |
| --- | --- | --- |
| Implementação | Descrição da técnica usada no exercício 3, incluindo parâmetros e formato de entrada/saída | `./Part1/ex3.py` |
| Resultados experimentais | Tabelas com BER antes/depois da técnica implementada, para vários valores de `p` ou `B` | `./Part1/Ex3Results/` |
| Ficheiros de saída | Exemplos de ficheiros recuperados ou corrompidos, conforme pedido no enunciado | `./Part1/Ex3Results/` |
| Comparação com os exercícios anteriores | Comentário sobre melhoria, limitações e custo em redundância | este relatório |

Se o exercício 3 continuar a usar erros em rajada, a análise deve partir dos resultados já obtidos no exercício 1: [ficheiros com rajada](./Part1/BurstFilesResults/) e [imagens com rajada](./Part1/BurstImagesResults/). Nesse caso, o comentário principal deve comparar a vulnerabilidade dos códigos de repetição simples a erros consecutivos com a técnica escolhida para dispersar, detetar ou corrigir esses erros.

## Secção 2 - Projeto B.2

Esta secção ainda não tem resultados experimentais disponíveis no repositório. A pasta [Part2](./Part2/) existe, mas [ex1.py](./Part2/ex1.py) está vazio nesta versão.

Estrutura proposta para completar depois da implementação:

| Funcionalidade | Resultados a apresentar | Comentários esperados |
| --- | --- | --- |
| Funcionalidade 1 | Tabela de parâmetros, ficheiros de entrada, ficheiros de saída e métricas relevantes | Explicar se o resultado confirma o comportamento esperado |
| Funcionalidade 2 | Resultados experimentais equivalentes, se existir | Comparar com a funcionalidade anterior e justificar diferenças |
| Funcionalidade 3 | Resultados adicionais pedidos no enunciado | Identificar limitações, casos de erro e custo computacional |

Na versão final, cada linha deve apontar para os ficheiros concretos gerados na pasta `Part2`, seguindo o mesmo estilo usado em B.1: script, tabela de resultados, ficheiros de saída e comentário curto sobre o comportamento observado.

## Checklist antes da entrega final

- Regenerar os resultados da B.1 no fim, para garantir que todos os ficheiros de saída correspondem à versão final dos ficheiros de teste.
- Acrescentar a implementação e os resultados do exercício 3 de B.1.
- Preencher a secção B.2 com uma subsecção por funcionalidade implementada.
- Confirmar que todas as ligações para resultados apontam para ficheiros existentes.
- Rever os comentários experimentais depois de fixar os parâmetros definitivos.
