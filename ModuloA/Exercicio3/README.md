# Exercício 1 — Codificação e Compressão de Dados com Perda (Lossy)


## 1. Objetivo

O presente exercício tem como finalidade analisar o comportamento de um codec de compressão com perda (*lossy*), nomeadamente o formato **JPEG**, aplicado a imagens originais em formato PNG (sem perda). Pretende-se:

- (a) Converter imagens PNG para JPEG com diferentes níveis de qualidade e observar as versões resultantes;
- (b) Relacionar quantitativamente a **taxa de compressão** com o **erro absoluto médio (MAE)** e comentar o formato do gráfico obtido.

---

## 2. Fundamentação Teórica

### 2.1 Compressão Lossy vs. Lossless

- **PNG** (Portable Network Graphics) utiliza compressão **sem perda** (*lossless*), baseada no algoritmo DEFLATE. Garante reprodução fiel dos dados originais, mas com limites de compressão.
- **JPEG** (Joint Photographic Experts Group) utiliza compressão **com perda** (*lossy*), baseada na **Transformada Discreta do Cosseno (DCT)** aplicada a blocos de 8×8 pixeis, seguida de quantização dos coeficientes de frequência. A quantização é controlada pelo parâmetro de *qualidade* (0–100), sendo irreversível.

### 2.2 Métricas Utilizadas

**Taxa de Compressão (TC):**

$$
TC = \frac{\text{Tamanho}_{original}}{\text{Tamanho}_{comprimido}}
$$

Quanto maior o valor, mais reduzido ficou o ficheiro.

**Erro Absoluto Médio (MAE):**

Dadas duas imagens $I_1$ e $I_2$ de dimensão $M \times N$:

$$
MAE(I_1, I_2) = \frac{1}{M \cdot N} \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} |I_1[m,n] - I_2[m,n]|
$$

O MAE mede a diferença média absoluta entre pixeis da imagem original e da comprimida, numa escala de 0 a 255 (por canal).

---

## 3. Metodologia

### 3.1 Ferramentas

- **Linguagem:** Python 3
- **Bibliotecas:** Pillow (PIL) para manipulação de imagens, NumPy para cálculo vetorizado do MAE, Matplotlib para geração de gráficos.

### 3.2 Procedimento

1. **Leitura** das imagens originais em formato PNG a partir da pasta `Test_Images`.
2. **Conversão** para o formato JPEG iterando sobre os seguintes níveis de qualidade: **95, 85, 75, 50, 25, 10, 5**.
3. **Cálculo** da taxa de compressão comparando o tamanho em bytes do ficheiro original com o comprimido.
4. **Cálculo** do MAE entre a imagem original (em memória, convertida para RGB) e a versão JPEG recém-gerada (reaberta para garantir comparação justa).
5. **Visualização:** geração de gráficos *Taxa de Compressão (xx) vs. MAE (yy)* por imagem, mosaicos comparativos e gráfico global agregado.

---

## 4. Resultados

### 4.1 Imagens Processadas

Foram processadas 2 imagens do conjunto de teste:

| Imagem | Dimensões | Tamanho Original (PNG) |
|--------|-----------|------------------------|
| `bird.png` | 256 × 256 | 32.493 bytes |
| `bubbles.png` | 714 × 682 | 187.450 bytes |

### 4.2 Tabela de Resultados — `bird.png`

| Qualidade JPEG | Tamanho (bytes) | Taxa de Compressão | MAE |
|:--------------:|:---------------:|:------------------:|:---:|
| 95 | 17.659 | **1,84×** | 0,9340 |
| 85 | 8.939 | **3,63×** | 1,4352 |
| 75 | 6.357 | **5,11×** | 1,7131 |
| 50 | 4.189 | **7,76×** | 2,1564 |
| 25 | 2.890 | **11,24×** | 2,7891 |
| 10 | 1.944 | **16,71×** | 4,4068 |
| 5 | 1.527 | **21,28×** | 6,7396 |

### 4.3 Tabela de Resultados — `bubbles.png`

| Qualidade JPEG | Tamanho (bytes) | Taxa de Compressão | MAE |
|:--------------:|:---------------:|:------------------:|:---:|
| 95 | 93.787 | **2,00×** | 0,4708 |
| 85 | 51.700 | **3,63×** | 0,8556 |
| 75 | 36.961 | **5,07×** | 1,1430 |
| 50 | 21.801 | **8,60×** | 1,6030 |
| 25 | 13.849 | **13,54×** | 2,1837 |
| 10 | 9.699 | **19,33×** | 3,5131 |
| 5 | 7.992 | **23,45×** | 6,3617 |

---

## 5. Análise e Discussão

### 5.1 Formato do Gráfico

O gráfico que relaciona a **taxa de compressão (eixo xx)** com o **MAE (eixo yy)** apresenta uma **curva crescente e não-linear**, com as seguintes características:

1. **Crescimento monótono:** à medida que a taxa de compressão aumenta (ficheiros mais pequenos), o erro médio também aumenta. Isto reflete diretamente o *trade-off* fundamental da compressão com perda: **maior redução de dados implica maior degradação da informação.**

2. **Comportamento não-linear / côncavo:** a curva não é uma reta. Existe uma zona inicial (qualidades elevadas, Q95 → Q50) onde o ganho em compressão é significativo com um aumento moderado do MAE. A partir de certo ponto (aproximadamente Q25 para baixo), o MAE começa a crescer de forma mais acelerada em relação ao ganho adicional de compressão. Este fenómeno é visível no "joelho" da curva.

3. **Zona de eficiência:** entre Q85 e Q75, observa-se um bom compromisso — taxas de compressão na ordem de 3× a 5× com erros médios inferiores a 2 (numa escala de 255), correspondentes a diferenças praticamente imperceptíveis ao olho humano.

4. **Zona de degradação acentuada:** para Q ≤ 10, o MAE dispara (superior a 3,5), traduzindo artefactos típicos do JPEG como **blocagem** (*blocking*, devido à quantização agressiva dos blocos 8×8 da DCT), **ringing** e perda de detalhe de alta frequência.

### 5.2 Comparação entre Imagens

Apesar de ambas as curvas seguirem a mesma tendência global, verificam-se diferenças notáveis:

| Aspeto | `bird.png` | `bubbles.png` |
|--------|-----------|---------------|
| **MAE para taxa similar** | Superior | Inferior |
| **Compressibilidade** | Menor eficiência relativa | Maior eficiência relativa |
| **Explicação** | Provavelmente contém detalhes finos (penas, contornos nítidos) que são destruídos pela quantização da DCT. | Provavelmente contém gradientes suaves e áreas homogéneas, que o JPEG comprime eficientemente com pouco erro. |

Isto demonstra que **a eficiência da compressão JPEG é fortemente dependente do conteúdo da imagem**, não sendo possível estabelecer uma relação universal fixa entre qualidade e erro.

### 5.3 Interpretação dos Valores de MAE

- **MAE < 1,0:** Diferença média inferior a 1 nível de cor (escala 0–255). Praticamente imperceptível.
- **MAE ≈ 1,5–2,5:** Degradação ligeira. Aceitável para aplicações web ou pré-visualização.
- **MAE > 4,0:** Artefactos visíveis a olho nu. Só justificável quando o tamanho do ficheiro é critico.
- **MAE > 6,0:** Qualidade muito baixa. Imagem apresenta blocagem evidente e perda de informação significativa.

---

## 6. Conclusão

O exercício permitiu verificar experimentalmente o comportamento da compressão JPEG como caso de estudo de codificação com perda. Os resultados confirmam que:

- Existe um **compromisso inelutável** entre taxa de compressão e fidelidade da imagem.
- A relação entre estas duas grandezas é **não-linear**, apresentando uma zona de eficiência (Q75–Q85) e uma zona de degradação acelerada (Q < 25).
- O desempenho do codec depende das **características do conteúdo visual**, sendo as imagens com gradientes suaves mais favoráveis à compressão JPEG do que as imagens com detalhes de alta frequência.

Para aplicações práticas, recomenda-se o uso de qualidades entre **75 e 90**, que oferecem reduções de tamanho significativas (3× a 5×) com erros médios baixos e degradação visual mínima.

---

## Anexos

- Script de processamento: [`Parte 3 - ex1`](./ex1.py)
- Gráficos individuais: [`Gráfico Bird`](./resultados_jpeg_ex1/grafico_bird.png), [`Gráfico Bubbles`](./resultados_jpeg_ex1/grafico_bubbles.png)
- Gráfico comparativo global: [`grafico_comparativo_global.png`](./resultados_jpeg_ex1/grafico_comparativo_global.png)
- Mosaicos visuais: [`visual_bird.png`](./resultados_jpeg_ex1/visual_bird.png), [`visual_bubbles.png`](./resultados_jpeg_ex1/visual_bubbles.png)



# Exercício 2 — Cifra e Decifra de Imagens com a Cifra de Vernam

## 1. Objetivo

O presente exercício tem como finalidade implementar e avaliar um sistema de **cifra e decifra de imagens** com base na **cifra de Vernam**, aplicável a imagens monocromáticas e coloridas.

Pretende-se:

- (a) Implementar uma aplicação que permita cifrar e decifrar uma imagem, na sua totalidade ou apenas numa **área retangular definida pelo utilizador**;
- (b) Apresentar resultados experimentais que comprovem o funcionamento do conjunto cifrador/decifrador, através da análise da **entropia**, dos **histogramas** das imagens original, cifrada e decifrada, e do cálculo do **erro absoluto médio (MAE)** entre a imagem original e a imagem decifrada.

---

## 2. Fundamentação Teórica

### 2.1 Cifra de Vernam

A cifra de Vernam é uma cifra simétrica em que cada símbolo da mensagem é combinado com um símbolo correspondente da chave. Em dados binários, essa combinação pode ser implementada através da operação **XOR**, sendo a mesma operação usada tanto na cifra como na decifra.

Sejam $P$ os dados originais, $K$ a chave e $C$ os dados cifrados. A operação utilizada é:

$$
C = P \oplus K
$$

e a decifra é obtida por:

$$
P = C \oplus K
$$

Assim, desde que seja usada a mesma chave, a aplicação repetida de XOR permite recuperar os dados originais.

### 2.2 Representação da imagem

Na implementação realizada, as imagens são abertas com a biblioteca **Pillow** e convertidas para o modo `RGB`, garantindo uma representação uniforme com três canais por píxel. Esta conversão é importante porque permite trabalhar sempre com uma sequência previsível de bytes, independentemente do formato original do ficheiro.

Para efeitos de análise estatística posterior, nomeadamente cálculo de entropia e histogramas, as imagens são convertidas para o modo `L` (tons de cinzento), passando cada píxel a ser representado por um único valor inteiro entre 0 e 255.

### 2.3 Métricas utilizadas

**Entropia:**

A entropia mede o grau de imprevisibilidade ou aleatoriedade dos símbolos observados. No contexto da imagem, foi calculada a partir da distribuição das intensidades dos píxeis.

$$
H = - \sum_i p_i \log_2(p_i)
$$

em que $p_i$ representa a probabilidade de ocorrência do símbolo $i$.

**Erro Absoluto Médio (MAE):**

O MAE foi utilizado para medir a diferença média entre os píxeis da imagem original e da imagem decifrada.

$$
MAE(I_1, I_2) = \frac{1}{M \cdot N} \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} |I_1[m,n] - I_2[m,n]|
$$

Se a decifra recuperar corretamente a imagem original, o valor esperado do MAE é nulo ou muito próximo de zero.

---

## 3. Metodologia

### 3.1 Ferramentas

- **Linguagem:** Python 3
- **Bibliotecas:** Pillow para manipulação de imagens, `secrets` para geração da chave aleatória, `matplotlib` para desenho dos histogramas, `collections.Counter` para cálculo de frequências.

### 3.2 Procedimento

1. **Leitura** das imagens de teste a partir da pasta `Test Images`.
2. **Conversão** de cada imagem para `RGB`, garantindo uma estrutura uniforme dos dados em memória.
3. **Seleção** da região a cifrar: imagem inteira ou uma área retangular definida pelo utilizador através das coordenadas `(x, y, w, h)`.
4. **Extração** da região com `crop()` e conversão da mesma para bytes com `tobytes()`.
5. **Geração** de uma chave aleatória com o mesmo tamanho da região a processar, usando `secrets.token_bytes(len(dados))`.
6. **Cifra** dos bytes através de XOR entre os bytes da imagem e os bytes da chave.
7. **Gravação** da chave num ficheiro binário, de modo a poder ser reutilizada na decifra.
8. **Reconstrução** da região processada com `Image.frombytes(...)`, seguida de reinserção na imagem original com `paste()`.
9. **Decifra** da imagem cifrada usando a mesma chave e a mesma região retangular.
10. **Análise experimental** das imagens original, cifrada e decifrada, com cálculo de histogramas, entropia e MAE.

---

## 4. Implementação

### 4.1 Cifra e Decifra

Foram definidas duas funções principais: `cifra_vernam()` e `decifra_vernam()`. Ambas percorrem os bytes dos dados e da chave em paralelo, usando `zip(...)`, e aplicam a operação XOR a cada par de bytes. O resultado é acumulado num `bytearray`, que no final é convertido para `bytes`.

### 4.2 Seleção da região

A função `selecionar_retangulo()` permite definir a zona da imagem a processar. Se o utilizador não indicar um retângulo, a função devolve as coordenadas correspondentes à imagem inteira. Caso contrário, recebe um tuplo `(x, y, w, h)` e converte-o para o formato `(left, upper, right, lower)`, que é o formato usado pela biblioteca Pillow.

### 4.3 Processamento da imagem

A função `processar_imagem(...)` centraliza o funcionamento do programa.

Numa primeira fase, a imagem é aberta e convertida para `RGB`; de seguida é selecionada a região a processar e essa região é extraída com `crop()`.

Os dados da região são convertidos para bytes através de `tobytes()`. No modo de cifra, é gerada uma chave aleatória do mesmo tamanho e os dados são cifrados por XOR. No modo de decifra, a chave é lida do ficheiro binário e reutilizada para recuperar os dados originais.

Depois disso, os novos bytes são transformados novamente em imagem com `Image.frombytes("RGB", regiao.size, novos_dados)` e a região resultante é recolocada na imagem com `paste()`. Finalmente, a imagem processada é guardada no disco.

### 4.4 Processamento automático do conjunto de imagens

Na função `main()`, foi definido um conjunto de imagens de teste composto por ficheiros `PNG` e `TIF`, bem como um conjunto de retângulos para cifrar em cada imagem. Para cada ficheiro, o programa gera uma imagem cifrada, a respetiva chave e, em seguida, a imagem decifrada correspondente.

---

## 5. Resultados

### 5.1 Imagens processadas

Foram processadas 9 imagens do conjunto de teste:

| Imagem |
|--------|
| `barb.tif` |
| `bird.png` |
| `bubbles.png` |
| `goldhill.tif` |
| `lena1.tif` |
| `lena3.tif` |
| `mandrill.tif` |
| `monarch.tif` |
| `tulips.tif` |

### 5.2 Análise estatística

Para cada imagem original, cifrada e decifrada, foi calculada a **entropia da imagem** e gerado o respetivo **histograma**, recorrendo às funções auxiliares implementadas.

As imagens foram convertidas para modo `L`, os valores dos píxeis foram obtidos com `getdata()`, e as frequências foram calculadas com `Counter`. Os histogramas foram desenhados com **Matplotlib**, usando 256 bins, correspondentes aos níveis de intensidade entre 0 e 255.

### 5.3 MAE

O MAE foi calculado entre a imagem original e a imagem decifrada, de forma a verificar se a operação de decifra recupera corretamente a imagem inicial. Esta comparação foi feita a partir das imagens abertas em memória, em formato RGB.



| Imagem | Entropia Original | Entropia Cifrada | Entropia Decifrada | MAE (Original vs Decifrada) |
|--------|-------------------|------------------|--------------------|-----------------------------|
| `barb.tif` | 7.4664 bits/símbolo | 7.4651 bits/símbolo | 7.4664 bits/símbolo | 0.0000 |
| `bird.png` | 6.7744 bits/símbolo | 7.1577 bits/símbolo | 6.7744 bits/símbolo | 0.0000 |
| `bubbles.png` | 5.8765 bits/símbolo | 5.9706 bits/símbolo | 5.8765 bits/símbolo | 0.0000 |
| `goldhill.tif` | 7.4778 bits/símbolo | 7.5779 bits/símbolo | 7.4778 bits/símbolo | 0.0000 |
| `lena1.tif` | 7.5683 bits/símbolo | 7.5823 bits/símbolo | 7.5683 bits/símbolo | 0.0000 |
| `lena3.tif` | 7.4451 bits/símbolo | 7.5109 bits/símbolo | 7.4451 bits/símbolo | 0.0000 |
| `mandrill.tif` | 7.3579 bits/símbolo | 7.4470 bits/símbolo | 7.3579 bits/símbolo | 0.0000 |
| `monarch.tif` | 7.1842 bits/símbolo | 7.3600 bits/símbolo | 7.1842 bits/símbolo | 0.0000 |
| `tulips.tif` | 7.6991 bits/símbolo | 7.7279 bits/símbolo | 7.6991 bits/símbolo | 0.0000 |
---


## 6. Análise e Discussão

### 6.1 Funcionamento do cifrador/decifrador

Os resultados experimentais confirmam o funcionamento correto do conjunto cifrador/decifrador. Em todas as imagens testadas, a entropia da imagem decifrada coincide exatamente com a entropia da imagem original, e o valor de MAE entre ambas é igual a 0.0000.

Este resultado mostra que o processo de decifra recupera integralmente os dados originais da imagem, sem introdução de erro. Tal comportamento é consistente com a utilização da operação XOR na cifra de Vernam, uma vez que a aplicação da mesma chave sobre os dados cifrados permite restaurar exatamente os dados iniciais.

### 6.2 Entropia

A análise da entropia mostra que, na maioria dos casos, a imagem cifrada apresenta um valor de entropia superior ao da imagem original. Esse comportamento é visível, por exemplo, em `bird.png` (de 6.7744 para 7.1577 bits/símbolo), `goldhill.tif` (de 7.4778 para 7.5779 bits/símbolo) e `monarch.tif` (de 7.1842 para 7.3600 bits/símbolo).

Este aumento indica que a cifra reduz a estrutura estatística visível da imagem, tornando a distribuição dos níveis de intensidade mais próxima de uma distribuição uniforme. Ainda assim, observa-se que este comportamento não é absolutamente universal, uma vez que em `barb.tif` a entropia da imagem cifrada ficou ligeiramente abaixo da original (7.4651 face a 7.4664 bits/símbolo), embora a diferença seja muito pequena e não altere a conclusão global.

Por sua vez, a imagem decifrada apresenta sempre exatamente o mesmo valor de entropia da imagem original. Isto comprova que a estrutura estatística da imagem é totalmente restaurada após a decifra.

### 6.3 Histogramas

Os histogramas das imagens originais apresentam distribuições características do conteúdo visual de cada imagem, com concentrações em determinadas zonas da escala de cinzentos e com perfis não uniformes.

Após a cifra, os histogramas tornam-se, em geral, mais dispersos e menos estruturados, refletindo a alteração estatística introduzida pela aplicação da chave. Embora nem sempre se obtenha uma distribuição perfeitamente uniforme, verifica-se uma perda clara dos padrões associados ao conteúdo visual original.

Já os histogramas das imagens decifradas reproduzem o mesmo perfil observado nas imagens originais. Este resultado reforça a conclusão de que a operação de decifra recupera corretamente a imagem inicial.

### 6.4 MAE

O erro absoluto médio entre a imagem original e a imagem decifrada foi igual a 0.0000 em todas as imagens analisadas.

Este resultado significa que, píxel a píxel, não existe qualquer diferença entre a imagem original e a imagem decifrada. Assim, pode concluir-se que a implementação realizada permite uma recuperação exata da informação original, validando experimentalmente o correto funcionamento do sistema de cifra e decifra.

---

## 7. Conclusão

O exercício permitiu implementar e validar experimentalmente uma aplicação de cifra e decifra de imagens com base na cifra de Vernam. A solução desenvolvida suporta o processamento da imagem completa ou apenas de uma região retangular definida pelo utilizador, recorrendo a uma chave aleatória do mesmo tamanho da área cifrada.

A análise dos resultados mostrou que a imagem cifrada apresenta maior aleatoriedade estatística, refletida no aumento da entropia e na alteração do histograma, enquanto a imagem decifrada recupera as características da imagem original. O cálculo do MAE entre a imagem original e a imagem decifrada confirmou quantitativamente o correto funcionamento do sistema.

---

## Anexos

### Código-fonte

- Script principal de cifra e decifra: [`ex2.py`](./ex2.py)
- Script utilitário para cálculo de entropia e geração de histogramas: [`utils-3.py`](./utils-3.py)
- Script de testes experimentais: [`ex2b-2.py`](./ex2b-2.py)

### Imagens originais

- [`barb.tif`](./Test_Images/barb.tif)
- [`bird.png`](./Test_Images/bird.png)
- [`bubbles.png`](./Test_Images/bubbles.png)
- [`goldhill.tif`](./Test_Images/goldhill.tif)
- [`lena1.tif`](./Test_Images/lena1.tif)
- [`lena3.tif`](./Test_Images/lena3.tif)
- [`mandrill.tif`](./Test_Images/mandrill.tif)
- [`monarch.tif`](./Test_Images/monarch.tif)
- [`tulips.tif`](./Test_Images/tulips.tif)

### Imagens cifradas

- [`cifrado_barb.tif`](./imagens_cifradas/cifrado_barb.tif)
- [`cifrado_bird.png`](./imagens_cifradas/cifrado_bird.png)
- [`cifrado_bubbles.png`](./imagens_cifradas/cifrado_bubbles.png)
- [`cifrado_goldhill.tif`](./imagens_cifradas/cifrado_goldhill.tif)
- [`cifrado_lena1.tif`](./imagens_cifradas/cifrado_lena1.tif)
- [`cifrado_lena3.tif`](./imagens_cifradas/cifrado_lena3.tif)
- [`cifrado_mandrill.tif`](./imagens_cifradas/cifrado_mandrill.tif)
- [`cifrado_monarch.tif`](./imagens_cifradas/cifrado_monarch.tif)
- [`cifrado_tulips.tif`](./imagens_cifradas/cifrado_tulips.tif)

### Imagens decifradas

- [`decifrado_barb.tif`](./imagens_decifradas/decifrado_barb.tif)
- [`decifrado_bird.png`](./imagens_decifradas/decifrado_bird.png)
- [`decifrado_bubbles.png`](./imagens_decifradas/decifrado_bubbles.png)
- [`decifrado_goldhill.tif`](./imagens_decifradas/decifrado_goldhill.tif)
- [`decifrado_lena1.tif`](./imagens_decifradas/decifrado_lena1.tif)
- [`decifrado_lena3.tif`](./imagens_decifradas/decifrado_lena3.tif)
- [`decifrado_mandrill.tif`](./imagens_decifradas/decifrado_mandrill.tif)
- [`decifrado_monarch.tif`](./imagens_decifradas/decifrado_monarch.tif)
- [`decifrado_tulips.tif`](./imagens_decifradas/decifrado_tulips.tif)

### Histogramas das imagens originais

- [`Histogram_barb.png`](./ex2bResults/original_histogramas/Histogram_barb.png)
- [`Histogram_bird.png`](./ex2bResults/original_histogramas/Histogram_bird.png)
- [`Histogram_bubbles.png`](./ex2bResults/original_histogramas/Histogram_bubbles.png)
- [`Histogram_goldhill.png`](./ex2bResults/original_histogramas/Histogram_goldhill.png)
- [`Histogram_lena1.png`](./ex2bResults/original_histogramas/Histogram_lena1.png)
- [`Histogram_lena3.png`](./ex2bResults/original_histogramas/Histogram_lena3.png)
- [`Histogram_mandrill.png`](./ex2bResults/original_histogramas/Histogram_mandrill.png)
- [`Histogram_monarch.png`](./ex2bResults/original_histogramas/Histogram_monarch.png)
- [`Histogram_tulips.png`](./ex2bResults/original_histogramas/Histogram_tulips.png)

### Histogramas das imagens cifradas

- [`Histogram_cifrado_barb.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_barb.png)
- [`Histogram_cifrado_bird.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_bird.png)
- [`Histogram_cifrado_bubbles.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_bubbles.png)
- [`Histogram_cifrado_goldhill.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_goldhill.png)
- [`Histogram_cifrado_lena1.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_lena1.png)
- [`Histogram_cifrado_lena3.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_lena3.png)
- [`Histogram_cifrado_mandrill.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_mandrill.png)
- [`Histogram_cifrado_monarch.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_monarch.png)
- [`Histogram_cifrado_tulips.png`](./ex2bResults/cifra_histogramas/Histogram_cifrado_tulips.png)

### Histogramas das imagens decifradas

- [`Histogram_decifrado_barb.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_barb.png)
- [`Histogram_decifrado_bird.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_bird.png)
- [`Histogram_decifrado_bubbles.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_bubbles.png)
- [`Histogram_decifrado_goldhill.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_goldhill.png)
- [`Histogram_decifrado_lena1.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_lena1.png)
- [`Histogram_decifrado_lena3.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_lena3.png)
- [`Histogram_decifrado_mandrill.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_mandrill.png)
- [`Histogram_decifrado_monarch.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_monarch.png)
- [`Histogram_decifrado_tulips.png`](./ex2bResults/decifra_histogramas/Histogram_decifrado_tulips.png)
