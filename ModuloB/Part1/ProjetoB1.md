# Projeto B.1

## Exercício 1 - Simulação de erros no canal

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

## Exercício 2 - Correção de erros isolados com códigos de repetição

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


## Exercício 3 - Codificação e Compressão de Dados sem Perda

### Introdução

Este exercício tem como objetivo estudar uma cadeia completa de tratamento de dados composta por compressão, cifragem, codificação de canal, simulação de erro e recuperação final da informação. A implementação foi organizada em três módulos principais:

- `ex3a.py`, com a implementação da codificação de canal (CRC32) e verificação de integridade
- `ex3_utils.py`, com funções auxiliares para compressão, descompressão, cálculo de entropia, histogramas e cifragem de Vernam
- `ex3b.py`, com a lógica de codificação e descodificação de fonte e de canal
- `ex3c.py`, com o script de teste e de análise dos blocos intermédios do processo


O fluxo experimental segue a cadeia:

1. Leitura do ficheiro original
2. Codificação de fonte, em modo `lossless` ou `loss`
3. Cifragem com chave aleatória
4. Codificação de canal com CRC32
5. Simulação de erro no canal
6. Verificação do CRC e descodificação final
7. Comparação entre o ficheiro original e o ficheiro recuperado, quando aplicável

---

###  Implementação

#### Codificação de fonte

A função `cod_de_fonte()` implementa a etapa de compressão da fonte. No modo `lossless`, o ficheiro é comprimido com 7-Zip, através da função `compress()` definida em `ex3_utils.py`. No modo `loss`, o ficheiro de imagem é convertido para JPEG com uma qualidade escolhida pelo utilizador, através de `processar_imagem()`.

Na recuperação, `decod_de_fonte()` executa a operação inversa:

- no modo `lossless`, o conteúdo recebido é guardado temporariamente como um `.7z` e depois descomprimido com 7-Zip
- no modo `loss`, os bytes recebidos são gravados como JPEG temporário e convertidos novamente para PNG

Esta separação permite testar dois cenários distintos: compressão sem perdas para texto e dados estruturados, e compressão com perdas para imagem. A codificação com perda segue o esquema descrito no Exercício 1 do Projeto A.3, enquanto a codificação sem perdas corresponde ao Exercício 3 do Projeto A.2.

#### Cifragem de Vernam

A função `cifra()` gera uma chave aleatória com `secrets.token_bytes(len(data))` e aplica XOR byte a byte com `cifra_vernam()`. A chave é guardada em disco para permitir a descifragem posterior. A função `decifrar()` lê essa chave e recupera os dados originais com o mesmo operador XOR.

Este mecanismo corresponde a uma cifra de Vernam simples, em que a segurança depende da aleatoriedade da chave e da sua utilização de um único uso. A implementação da cifra de Vernam segue o enunciado do Exercício 2 do Projeto A.3.

#### Codificação de canal

A proteção contra erros é feita em duas etapas e está implementada no ficheiro `ex3a.py`:

- `crc32_value()` calcula o valor CRC32 de um bloco de bytes com `zlib.crc32()`
- `encode_crc32()` acrescenta o CRC32 ao fim dos dados, criando um frame com redundância de verificação
- `check_crc32()` separa o payload do CRC recebido e compara-o com o CRC calculado novamente

Em `ex3b.py`, estas funções são usadas da seguinte forma:

- `cod_de_canal()` aplica `encode_crc32()`
- `decod_de_canal()` valida a integridade com `check_crc32()`

Depois disso, a função `canal()` simula perturbação no meio de transmissão com `burst_bit_error_bytes()`. 
#### Análise de blocos

O script `ex3c.py` calcula, para cada bloco intermédio do processo, o tamanho em bytes, a entropia e o histograma das frequências. Os blocos analisados são:

- `A`: ficheiro original
- `B`: ficheiro após codificação de fonte
- `C`: ficheiro após cifragem
- `D`: ficheiro após codificação de canal
- `E`: ficheiro final recuperado

A função `analisar_bloco()` usa `entropia()`, `calcular_frequencias()` e `desenhar_histograma_matplotlib()` para produzir a caracterização estatística de cada estágio.

---

###  Resultados e Comentários


#### Resumo dos valores obtidos

| Ficheiro | Bloco A | Bloco B | Bloco C | Bloco D | Bloco E |
| --- | --- | --- | --- | --- | --- |
| `alice29.txt` | 152090 bytes, 4.5677 bits/símbolo | 48615 bytes, 7.9957 bits/símbolo | 48615 bytes, 7.9967 bits/símbolo | 48619 bytes, 7.9967 bits/símbolo | 152090 bytes, 4.5677 bits/símbolo |
| `bird.png` | 32493 bytes, 7.9843 bits/símbolo | 6227 bytes, 7.8620 bits/símbolo | 6227 bytes, 7.9698 bits/símbolo | 6231 bytes, 7.9697 bits/símbolo | 38224 bytes, 7.9835 bits/símbolo |

#### Ficheiro `alice29.txt`

O ficheiro de texto apresenta o comportamento mais esclarecedor do ponto de vista informacional. O bloco `A` tem 152090 bytes e uma entropia de 4.5677 bits/símbolo, o que confirma a redundância típica de texto natural. Depois da codificação de fonte, o bloco `B` desce para 48615 bytes, o que corresponde a uma taxa de compressão de 3.1285, e a entropia sobe para 7.9957 bits/símbolo. Isto mostra que o 7-Zip transforma o texto redundante numa sequência muito mais próxima de uma distribuição uniforme.

A cifragem no bloco `C` mantém exatamente o tamanho do bloco anterior, porque a operação é XOR byte a byte, mas a entropia continua praticamente no máximo, passando para 7.9967 bits/símbolo. Isto é coerente com a função da cifra de Vernam: ocultar qualquer estrutura estatística observável. O bloco `D` acrescenta apenas 4 bytes ao frame, passando para 48619 bytes, devido ao CRC32. A entropia permanece inalterada à escala apresentada, porque a redundância introduzida pelo CRC é pequena face ao tamanho total do ficheiro.

O bloco `E` volta a ter 152090 bytes e 4.5677 bits/símbolo, exatamente como o original. Este resultado confirma que a cadeia completa preserva integralmente o ficheiro quando não ocorre erro no canal: compressão, cifra, CRC, transmissão e recuperação funcionam de forma consistente.

#### Ficheiro `bird.png`

No caso da imagem, o bloco `A` já apresenta uma entropia muito elevada, 7.9843 bits/símbolo, o que é esperado para um ficheiro PNG que já contém compressão interna e distribuição de bytes próxima do máximo. Após a codificação de fonte em modo com perdas, o bloco `B` reduz-se para 6227 bytes e a entropia fica em 7.8620 bits/símbolo. Apesar da forte redução no tamanho, a estrutura interna dos dados continua densa, o que é normal numa imagem convertida para JPEG.

Nos blocos `C` e `D`, a entropia sobe novamente para valores muito próximos de 8 bits/símbolo, respetivamente 7.9698 e 7.9697, devido ao efeito da cifragem e do acréscimo do CRC. Tal como no texto, a etapa de canal acrescenta apenas os 4 bytes do código de verificação, pelo que a variação de tamanho é mínima.

O bloco `E` termina com 38224 bytes e 7.9835 bits/símbolo. Aqui o ficheiro recuperado já não coincide com o original ao nível de tamanho, porque a codificação de fonte usada foi com perda: a imagem foi convertida para JPEG e depois regravada em PNG na descodificação final. O resultado mostra que a cadeia preserva o conteúdo visual de forma aceitável, mas não garante identidade byte a byte com o ficheiro de partida.

#### Interpretação global

Os resultados confirmam três comportamentos principais:

- a compressão sem perdas do texto reduz fortemente o tamanho e concentra os bytes numa distribuição quase uniforme
- a cifragem de Vernam mantém o tamanho, mas elimina a previsibilidade estatística dos dados
- o CRC32 acrescenta apenas uma redundância pequena e controlada, suficiente para verificação de integridade

Além disso, a comparação entre `alice29.txt` e `bird.png` mostra a diferença entre os dois modos do bloco de codificação de fonte. No modo sem perdas, o resultado final coincide com o original. No modo com perdas, a recuperação preserva a informação funcional da imagem, mas não a sua representação exata. Isso torna o exercício útil para distinguir compressão sem perdas, compressão com perdas e proteção de canal como fases com objetivos diferentes dentro da mesma cadeia.

---

### Conclusão

A implementação confirmou que é possível combinar compressão, cifragem e codificação de canal numa sequência coerente de processamento. No modo sem perdas, a cadeia preserva integralmente o ficheiro original. No modo com perdas, a reconstrução mantém a informação visual essencial, mas não a identidade byte a byte do original.

Do ponto de vista informacional, o exercício mostra que cada etapa tem um efeito distinto na estrutura dos dados:

- a compressão reduz redundância
- a cifragem remove padrões estatísticos visíveis
- a codificação de canal acrescenta proteção contra erros
- a descodificação restaura os dados sempre que a integridade for mantida

---

### Anexos

#### Código-fonte

- Script principal de análise: [`ex3c.py`](./ex3c.py)
- Codificação e descodificação: [`ex3b.py`](./ex3b.py)
- Codificação de canal com CRC32: [`ex3a.py`](./ex3a.py)
- Funções utilitárias: [`ex3_utils.py`](./ex3_utils.py)

#### Resultados

- Ficheiros comprimidos: `Resultados_Codificados/`
- Ficheiros recuperados: `Resultados_Decodificados/`
- Histogramas dos blocos: `Histogramas/`
- Chaves geradas: `chaves/`

