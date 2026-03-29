# Generadores de Números Pseudoaleatorios

Proyecto en Python para generar números pseudoaleatorios mediante distintos algoritmos, incluyendo generadores base, distribuciones uniformes y distribución normal. También incluye pruebas estadísticas para verificar la calidad de las secuencias generadas.

---

## Requisitos

- Python 3.10 o superior
- Dependencias: `scipy`, `matplotlib`

Para ejecutar la interfaz gráfica:

```bash
python app.py
```

La lógica de generación y pruebas está desacoplada de la interfaz. Para usar los generadores o pruebas directamente desde código, importar desde `generators.py` o desde los archivos de prueba correspondientes.

---

## Archivos del proyecto

```
proyecto/
├── archivos/
│   ├── mid_square.csv              # Ejemplo de semillas para Cuadrados Medios
│   ├── congruence.csv              # Ejemplo de parámetros para el método Congruencial
│   ├── uniform_mid_square.csv      # Ejemplo de parámetros para Uniforme – Cuadrados Medios
│   ├── uniform_congruence.csv      # Ejemplo de parámetros para Uniforme – Congruencial
│   ├── normal_mid_square.csv       # Ejemplo de parámetros para Normal – Cuadrados Medios
│   └── normal_congruence.csv       # Ejemplo de parámetros para Normal – Congruencial
├── generators.py                   # Algoritmos de generación de números pseudoaleatorios
├── prueba_medias.py                # Prueba estadística de medias
├── prueba_varianza.py              # Prueba estadística de varianza
├── prueba_chi_cuadrado.py          # Prueba Chi-Cuadrado
├── prueba_ks.py                    # Prueba de Kolmogorov-Smirnov
├── prueba_poker.py                 # Prueba de Póker
├── prueba_rachas.py                # Prueba de Rachas
├── app.py                          # Interfaz gráfica
└── import_seeds.py                 # Lectura de semillas desde archivos CSV
```

---

## Generadores (`generators.py`)

### 1. Cuadrados Medios — `mid_square(seed, number_ri)`

Eleva la semilla al cuadrado, extrae los dígitos centrales y usa ese resultado como siguiente semilla.

**Parámetros:**

| Parámetro   | Tipo  | Descripción                                     |
|-------------|-------|-------------------------------------------------|
| `seed`      | `int` | Semilla inicial. Debe tener al menos 3 dígitos. |
| `number_ri` | `int` | Cantidad de números a generar.                  |

**Retorna:** `list[float]` — lista de valores entre 0 y 1.

**Ejemplo:**

```python
from generators import mid_square

resultados = mid_square(1234, 5)
print(resultados)  # [0.5227, 0.3215, ...]
```

> IMPORTANTE: La semilla debe tener mínimo 3 dígitos. De lo contrario se lanza una excepción.

---

### 2. Congruencial Mixto — `congruence(xo, k, c, g, number_ri)`

Método congruencial general. Aplica la fórmula:

```
Xi = (Xi-1 * a + c) mod m
```

Donde `a = 1 + 2k` y `m = 2^g`.

**Parámetros:**

| Parámetro   | Tipo  | Descripción                                       |
|-------------|-------|---------------------------------------------------|
| `xo`        | `int` | Semilla inicial.                                  |
| `k`         | `int` | Multiplicador (se usa como `a = 1 + 2k`).         |
| `c`         | `int` | Incremento (constante aditiva).                   |
| `g`         | `int` | Módulo en potencia de 2 (`m = 2^g`).              |
| `number_ri` | `int` | Cantidad de números a generar.                    |

**Retorna:** `list[float]` — valores normalizados entre 0 y 1.

**Ejemplo:**

```python
from generators import congruence

resultados = congruence(xo=7, k=100, c=21, g=12, number_ri=10)
```

---

### 3. Congruencial Aditivo — `congruence_additive(xo, c, g, number_ri)`

Variante del método congruencial donde el multiplicador es 0 (`k=0`).

**Parámetros:**

| Parámetro   | Tipo  | Descripción                          |
|-------------|-------|--------------------------------------|
| `xo`        | `int` | Semilla inicial.                     |
| `c`         | `int` | Incremento.                          |
| `g`         | `int` | Módulo en potencia de 2 (`m = 2^g`). |
| `number_ri` | `int` | Cantidad de números a generar.       |

**Ejemplo:**

```python
from generators import congruence_additive

resultados = congruence_additive(xo=5, c=15, g=10, number_ri=10)
```

---

### 4. Congruencial Multiplicativo — `congruence_multiplicative(xo, k, g, number_ri)`

Variante del método congruencial donde el incremento es 0 (`c=0`).

**Parámetros:**

| Parámetro   | Tipo  | Descripción                          |
|-------------|-------|--------------------------------------|
| `xo`        | `int` | Semilla inicial.                     |
| `k`         | `int` | Multiplicador.                       |
| `g`         | `int` | Módulo en potencia de 2 (`m = 2^g`). |
| `number_ri` | `int` | Cantidad de números a generar.       |

**Ejemplo:**

```python
from generators import congruence_multiplicative

resultados = congruence_multiplicative(xo=3, k=200, g=14, number_ri=10)
```

---

### 5. Distribución Uniforme (general) — `general_uniform(list_ri, range_min, range_max)`

Transforma una lista de valores Ri (entre 0 y 1) a un rango `[range_min, range_max]` usando la fórmula:

```
Ni = range_min + (range_max - range_min) * Ri
```

**Parámetros:**

| Parámetro   | Tipo          | Descripción                              |
|-------------|---------------|------------------------------------------|
| `list_ri`   | `list[float]` | Lista de valores Ri entre 0 y 1.         |
| `range_min` | `float`       | Límite inferior del rango de salida.     |
| `range_max` | `float`       | Límite superior del rango de salida.     |

**Retorna:** `list[float]` — valores distribuidos en el rango especificado.

---

### 6. Uniforme – Cuadrados Medios — `uniform_mid_square(seed, range_min, range_max, number_ri)`

Genera números con distribución uniforme en `[range_min, range_max]` usando el método de Cuadrados Medios para producir los Ri.

**Parámetros:**

| Parámetro   | Tipo    | Descripción                                     |
|-------------|---------|-----------------------------------------------|
| `seed`      | `int`   | Semilla inicial. Debe tener al menos 3 dígitos. |
| `range_min` | `float` | Límite inferior del rango de salida.            |
| `range_max` | `float` | Límite superior del rango de salida.            |
| `number_ri` | `int`   | Cantidad de números a generar.                  |

**Retorna:** `list[float]` — valores en `[range_min, range_max]`.

**Ejemplo:**

```python
from generators import uniform_mid_square

resultados = uniform_mid_square(seed=1234, range_min=4, range_max=100, number_ri=10)
```

---

### 7. Uniforme – Congruencial — `uniform_distribution_congruence(xo, k, c, g, range_min, range_max, number_ni)`

Genera números con distribución uniforme en `[range_min, range_max]` usando el método Congruencial Mixto para producir los Ri.

**Parámetros:**

| Parámetro    | Tipo    | Descripción                                  |
|--------------|---------|----------------------------------------------|
| `xo`         | `int`   | Semilla inicial.                             |
| `k`          | `int`   | Multiplicador (se usa como `a = 1 + 2k`).    |
| `c`          | `int`   | Incremento (constante aditiva).              |
| `g`          | `int`   | Módulo en potencia de 2 (`m = 2^g`).         |
| `range_min`  | `float` | Límite inferior del rango de salida.         |
| `range_max`  | `float` | Límite superior del rango de salida.         |
| `number_ni`  | `int`   | Cantidad de números a generar.               |

**Retorna:** `list[float]` — valores en `[range_min, range_max]`.

**Ejemplo:**

```python
from generators import uniform_distribution_congruence

resultados = uniform_distribution_congruence(xo=7, k=100, c=21, g=12, range_min=4, range_max=100, number_ni=10)
```

---

### 8. Uniforme – Congruencial Aditivo — `uniform_distribution_additive(xo, c, g, range_min, range_max, number_ni)`

Variante del uniforme congruencial donde el multiplicador es 0 (`k=0`).

**Parámetros:**

| Parámetro   | Tipo    | Descripción                          |
|-------------|---------|--------------------------------------|
| `xo`        | `int`   | Semilla inicial.                     |
| `c`         | `int`   | Incremento.                          |
| `g`         | `int`   | Módulo en potencia de 2 (`m = 2^g`). |
| `range_min` | `float` | Límite inferior del rango de salida. |
| `range_max` | `float` | Límite superior del rango de salida. |
| `number_ni` | `int`   | Cantidad de números a generar.       |

**Ejemplo:**

```python
from generators import uniform_distribution_additive

resultados = uniform_distribution_additive(xo=5, c=15, g=10, range_min=10, range_max=20, number_ni=10)
```

---

### 9. Uniforme – Congruencial Multiplicativo — `uniform_distribution_multiplicative(xo, k, g, range_min, range_max, number_ni)`

Variante del uniforme congruencial donde el incremento es 0 (`c=0`).

**Parámetros:**

| Parámetro   | Tipo    | Descripción                          |
|-------------|---------|--------------------------------------|
| `xo`        | `int`   | Semilla inicial.                     |
| `k`         | `int`   | Multiplicador.                       |
| `g`         | `int`   | Módulo en potencia de 2 (`m = 2^g`). |
| `range_min` | `float` | Límite inferior del rango de salida. |
| `range_max` | `float` | Límite superior del rango de salida. |
| `number_ni` | `int`   | Cantidad de números a generar.       |

**Ejemplo:**

```python
from generators import uniform_distribution_multiplicative

resultados = uniform_distribution_multiplicative(xo=3, k=200, g=14, range_min=100, range_max=200, number_ni=10)
```

---

### 10. Box-Muller — `box_muller(list_ri)`

Transforma una lista de números pseudoaleatorios uniformes en pares de valores con distribución normal estándar N(0, 1) usando la transformación de Box-Muller:

```
z0 = sqrt(-2 * ln(r_i))   * cos(2π * r_{i+1})
z1 = sqrt(-2 * ln(r_i))   * sin(2π * r_{i+1})
```

**Parámetros:**

| Parámetro  | Tipo          | Descripción                                                         |
|------------|---------------|---------------------------------------------------------------------|
| `list_ri`  | `list[float]` | Lista de Ri en el rango (0, 1]. Su longitud debe ser par.           |

**Retorna:** `list[list[float]]` — lista de pares `[z0, z1]` con distribución N(0, 1).

> IMPORTANTE: La lista debe tener longitud par y todos sus valores deben estar en el intervalo (0, 1]. Se lanza una excepción si algún valor es ≤ 0 o > 1.

---

### 11. Distribución Normal — `normal_distribution(list_ri, mean, std_dev)`

Genera valores con distribución normal N(mean, std_dev²) a partir de números pseudoaleatorios uniformes, aplicando la transformación de Box-Muller y escalando cada valor zi mediante:

```
Ni = mean + zi * std_dev
```

**Parámetros:**

| Parámetro   | Tipo          | Descripción                                               |
|-------------|---------------|-----------------------------------------------------------|
| `list_ri`   | `list[float]` | Lista de Ri en el rango (0, 1]. Su longitud debe ser par. |
| `mean`      | `float`       | Media (μ) de la distribución normal deseada.              |
| `std_dev`   | `float`       | Desviación estándar (σ). Debe ser mayor que 0.            |

**Retorna:** `list[float]` — valores con distribución normal N(mean, std_dev²).

---

### 12. Normal – Congruencial — `normal_distribution_congruence(xo, k, c, g, mean, std_dev, number_ni)`

Genera valores con distribución normal usando el método de Congruencia Lineal Mixta como generador base de Ri, seguido de la transformación de Box-Muller.

**Parámetros:**

| Parámetro   | Tipo    | Descripción                                                    |
|-------------|---------|----------------------------------------------------------------|
| `xo`        | `int`   | Semilla inicial. Debe estar en el rango [0, m].               |
| `k`         | `int`   | Parámetro para el multiplicador `a = 1 + 2k`.                 |
| `c`         | `int`   | Incremento constante. Debe estar en el rango (0, m].          |
| `g`         | `int`   | Exponente para el módulo `m = 2^g`. Debe ser mayor que 0.     |
| `mean`      | `float` | Media (μ) de la distribución normal deseada.                  |
| `std_dev`   | `float` | Desviación estándar (σ). Debe ser mayor que 0.                |
| `number_ni` | `int`   | Cantidad de valores a generar. Debe ser un número par.        |

**Retorna:** `list[float]` — valores con distribución normal N(mean, std_dev²).

**Ejemplo:**

```python
from generators import normal_distribution_congruence

resultados = normal_distribution_congruence(xo=7, k=100, c=21, g=12, mean=3.5, std_dev=0.4, number_ni=10)
```

---

### 13. Normal – Cuadrados Medios — `normal_distribution_mid_square(seed, mean, std_dev, number_ni)`

Genera valores con distribución normal usando el método de Cuadrados Medios como generador base de Ri, seguido de la transformación de Box-Muller.

**Parámetros:**

| Parámetro   | Tipo    | Descripción                                             |
|-------------|---------|---------------------------------------------------------|
| `seed`      | `int`   | Semilla inicial. Debe tener al menos 3 dígitos.         |
| `mean`      | `float` | Media (μ) de la distribución normal deseada.            |
| `std_dev`   | `float` | Desviación estándar (σ). Debe ser mayor que 0.          |
| `number_ni` | `int`   | Cantidad de valores a generar. Debe ser un número par.  |

**Retorna:** `list[float]` — valores con distribución normal N(mean, std_dev²).

**Ejemplo:**

```python
from generators import normal_distribution_mid_square

resultados = normal_distribution_mid_square(seed=5678, mean=3.5, std_dev=0.4, number_ni=10)
```

---

## Pruebas estadísticas

Todas las pruebas reciben una `secuencia` (lista de números pseudoaleatorios entre 0 y 1) y un `nivel_confianza` (por defecto 0.95). Cada función retorna un diccionario con los valores calculados e incluye un campo `aprueba` (`True`/`False`). Cada archivo también expone una función de gráfico correspondiente que guarda la imagen como PNG y la muestra en pantalla.

---

### 1. Prueba de Medias — `prueba_medias.py`

Verifica que la media muestral de la secuencia sea estadísticamente cercana a 0.5, valor esperado de una distribución uniforme U(0,1). Construye un intervalo de confianza usando el estadístico Z y comprueba si la media muestral cae dentro de ese rango.

```python
from prueba_medias import prueba_medias

resultado = prueba_medias(secuencia, nivel_confianza=0.95)
```

**Retorna:** `N`, `media_muestral`, `media_teorica`, `valor_z`, `margen`, `limite_inferior`, `limite_superior`, `aprueba`.

El archivo también expone `grafico_distribucion_medias(lista_medias)` para visualizar la distribución de medias cuando se ejecutan múltiples simulaciones.

---

### 2. Prueba de Varianza — `prueba_varianza.py`

Verifica que la varianza muestral sea estadísticamente cercana a 1/12 ≈ 0.0833, valor esperado de una U(0,1). Utiliza los cuantiles de la distribución Chi-cuadrado para construir el intervalo de confianza de la varianza.

```python
from prueba_varianza import prueba_varianza

resultado = prueba_varianza(secuencia, nivel_confianza=0.95)
```

**Retorna:** `N`, `varianza_muestral`, `varianza_teorica`, `alpha`, `grados_libertad`, `chi2_inferior`, `chi2_superior`, `limite_inferior`, `limite_superior`, `aprueba`.

---

### 3. Prueba Chi-Cuadrado — `prueba_chi_cuadrado.py`

Divide el intervalo [0,1] en `k` subintervalos (calculado automáticamente como `max(10, √N)`) y compara las frecuencias observadas en cada uno contra la frecuencia esperada teórica. El estadístico resultante se compara contra el valor crítico Chi-cuadrado con `k-1` grados de libertad.

```python
from prueba_chi_cuadrado import prueba_chi_cuadrado

resultado = prueba_chi_cuadrado(secuencia, nivel_confianza=0.95)
```

**Retorna:** `N`, `k`, `frecuencias_observadas`, `frecuencia_esperada`, `chi2_calculado`, `chi2_critico`, `grados_libertad`, `aprueba`.

---

### 4. Prueba de Kolmogorov-Smirnov — `prueba_ks.py`

Compara la función de distribución acumulada empírica de la secuencia contra la distribución uniforme teórica U(0,1). Calcula la máxima diferencia absoluta entre ambas (DMAX) y la compara contra el valor crítico `DMAXP = 1.36 / √N`.

```python
from prueba_ks import prueba_ks

resultado = prueba_ks(secuencia, k=10, nivel_confianza=0.95)
```

**Retorna:** `N`, `k`, `tabla` (lista de intervalos con frecuencias y diferencias acumuladas), `dmax`, `dmaxp`, `aprueba`.

---

### 5. Prueba de Póker — `prueba_poker.py`

Verifica la independencia de los números analizando los patrones formados por sus 5 dígitos decimales significativos. Clasifica cada número en una de 7 categorías (todos diferentes, un par, dos pares, tercia, full house, póker, quintilla) y compara las frecuencias observadas contra las esperadas mediante un estadístico Chi-cuadrado con 6 grados de libertad.

```python
from prueba_poker import prueba_poker

resultado = prueba_poker(secuencia, nivel_confianza=0.95)
```

**Retorna:** `N`, `tabla` (categoría, frecuencia observada, probabilidad teórica, frecuencia esperada, contribución al Chi-cuadrado), `chi2_calculado`, `chi2_critico`, `grados_libertad`, `aprueba`.

---

### 6. Prueba de Rachas — `prueba_rachas.py`

Verifica la aleatoriedad detectando patrones de agrupamiento. Clasifica cada número como `+` si es mayor o igual a la mediana de la secuencia y `-` si es menor, luego cuenta las rachas (grupos consecutivos del mismo signo) y compara el total observado contra el esperado teórico mediante un estadístico Z.

```python
from prueba_rachas import prueba_rachas

resultado = prueba_rachas(secuencia, nivel_confianza=0.95)
```

**Retorna:** `N`, `mediana`, `mediana_teorica`, `n1_positivos`, `n2_negativos`, `rachas_observadas`, `rachas_esperadas`, `varianza_esperada`, `z_calculado`, `z_critico`, `rango_minimo`, `rango_maximo`, `aprueba`.

---

## Estructura de los archivos CSV

Los archivos CSV permiten cargar múltiples conjuntos de parámetros para ejecutar varias simulaciones en una sola ejecución.

### `mid_square.csv` — Semillas para Cuadrados Medios

Una semilla por línea, sin encabezado:

```
5678
1234
9101
```

Cada valor debe ser un entero con al menos 3 dígitos.

---

### `congruence.csv` — Parámetros para el método Congruencial

Formato CSV con encabezado. Columnas requeridas: `xo`, `k`, `c`, `g`:

```csv
xo,k,c,g
7,100,21,12
5,50,15,10
3,200,31,14
```

Cada fila representa una simulación independiente.

---

### `uniform_mid_square.csv` — Parámetros para Uniforme – Cuadrados Medios

Formato CSV con encabezado. Columnas requeridas: `seed`, `min`, `max`:

```csv
seed,min,max
5678,4,100
1234,10,20
9101,100,200
```

---

### `uniform_congruence.csv` — Parámetros para Uniforme – Congruencial

Formato CSV con encabezado. Columnas requeridas: `xo`, `k`, `c`, `g`, `min`, `max`:

```csv
xo,k,c,g,min,max
7,100,21,12,4,100
5,50,15,10,10,20
3,200,31,14,100,200
```

---

### `normal_mid_square.csv` — Parámetros para Normal – Cuadrados Medios

Formato CSV con encabezado. Columnas requeridas: `seed`, `mean`, `std_dev`:

```csv
seed,mean,std_dev
5678,3.5,0.4
1234,5.1,0.2
9101,20,0.5
```

---

### `normal_congruence.csv` — Parámetros para Normal – Congruencial

Formato CSV con encabezado. Columnas requeridas: `xo`, `k`, `c`, `g`, `mean`, `std_dev`:

```csv
xo,k,c,g,mean,std_dev
7,100,21,12,3.5,0.4
5,50,15,10,5.1,0.2
3,200,31,14,20,0.5
```

La cantidad de números a generar debe ser par en todos los métodos de distribución normal.

---

## Interfaz gráfica (`app.py`)

La interfaz permite seleccionar el algoritmo, ingresar los parámetros manualmente o cargar un archivo CSV con múltiples semillas, y visualizar los resultados. Los métodos están organizados en tres grupos: **Generadores base**, **Distribución uniforme** y **Distribución normal**.

- Los métodos **Aditivo** y **Multiplicativo** no admiten carga de CSV y solo se pueden ingresar manualmente, ya que son casos particulares del Congruencial Mixto.
- Los métodos **Cuadrados Medios** y **Congruencial** soportan carga de archivos CSV.
- Los métodos de **Distribución normal** requieren que la cantidad de números a generar sea par, dado que Box-Muller produce los valores en pares.