# Exercício 1 — Codificação e Compressão de Dados com Perda (Lossy)

**Unidade Curricular:** Codificação de Dados (CD) — LEIC, ISEL  
**Módulo:** A — Parte 3  
**Data:** Abril de 2026

---

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

- Script de processamento: [`Parte 3 - ex1`](./ModuloA/Exercicio3/ex1.py)
- Gráficos individuais: [`Gráfico Bird`](./ModuloA/Exercicio3/resultados_jpeg_ex1/grafico_bird.png), [`Gráfico Bubbles`](./ModuloA/Exercicio3/resultados_jpeg_ex1/grafico_bubbles.png)
- Gráfico comparativo global: [`grafico_comparativo_global.png`](./ModuloA/Exercicio3/resultados_jpeg_ex1/grafico_comparativo_global.png)
- Mosaicos visuais: [`visual_bird.png`](./ModuloA/Exercicio3/resultados_jpeg_ex1/visual_bird.png), [`visual_bubbles.png`](./ModuloA/Exercicio3/resultados_jpeg_ex1/visual_bubbles.png)
