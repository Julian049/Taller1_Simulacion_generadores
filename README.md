# Generadores de Números Pseudoaleatorios

Proyecto en Python para generar números pseudoaleatorios mediante distintos algoritmos, incluyendo generadores base y distribuciones uniformes.

---

## Requisitos

- Python 3.10 o superior
- No se necesitan dependencias externas

Para ejecutar la interfaz gráfica:

```bash
python ui.py
```

Para usar los generadores directamente desde código, importar desde `generators.py`.

---

## Archivos del proyecto

```
├── generators.py               # Algoritmos de generación de números pseudoaleatorios
├── ui.py                       # Interfaz gráfica (Tkinter)
├── import_seeds.py             # Lectura de semillas desde archivos CSV
├── mid_square.csv              # Ejemplo de semillas para Cuadrados Medios
├── congruence.csv              # Ejemplo de parámetros para el método Congruencial
├── uniform_mid_square.csv      # Ejemplo de parámetros para Uniforme – Cuadrados Medios
└── uniform_congruence.csv      # Ejemplo de parámetros para Uniforme – Congruencial
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

| Parámetro   | Tipo         | Descripción                              |
|-------------|--------------|------------------------------------------|
| `list_ri`   | `list[float]`| Lista de valores Ri entre 0 y 1.         |
| `range_min` | `float`      | Límite inferior del rango de salida.     |
| `range_max` | `float`      | Límite superior del rango de salida.     |

**Retorna:** `list[float]` — valores distribuidos en el rango especificado.

---

### 6. Uniforme – Cuadrados Medios — `uniform_mid_square(seed, range_min, range_max, number_ri)`

Genera números con distribución uniforme en `[range_min, range_max]` usando el método de Cuadrados Medios para producir los Ri.

**Parámetros:**

| Parámetro   | Tipo  | Descripción                                     |
|-------------|-------|-------------------------------------------------|
| `seed`      | `int` | Semilla inicial. Debe tener al menos 3 dígitos. |
| `range_min` | `float` | Límite inferior del rango de salida.          |
| `range_max` | `float` | Límite superior del rango de salida.          |
| `number_ri` | `int` | Cantidad de números a generar.                  |

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

| Parámetro    | Tipo  | Descripción                                  |
|--------------|-------|----------------------------------------------|
| `xo`         | `int` | Semilla inicial.                             |
| `k`          | `int` | Multiplicador (se usa como `a = 1 + 2k`).    |
| `c`          | `int` | Incremento (constante aditiva).              |
| `g`          | `int` | Módulo en potencia de 2 (`m = 2^g`).         |
| `range_min`  | `float` | Límite inferior del rango de salida.       |
| `range_max`  | `float` | Límite superior del rango de salida.       |
| `number_ni`  | `int` | Cantidad de números a generar.               |

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

Cada fila representa una simulación independiente. El valor de `seed` debe ser un entero con al menos 3 dígitos.

---

### `uniform_congruence.csv` — Parámetros para Uniforme – Congruencial

Formato CSV con encabezado. Columnas requeridas: `xo`, `k`, `c`, `g`, `min`, `max`:

```csv
xo,k,c,g,min,max
7,100,21,12,4,100
5,50,15,10,10,20
3,200,31,14,100,200
```

Cada fila representa una simulación independiente.

---

## Interfaz gráfica (`ui.py`)

La interfaz permite seleccionar el algoritmo, ingresar los parámetros manualmente o cargar un archivo CSV con múltiples semillas, y visualizar los resultados en una ventana separada con scroll. Los métodos están organizados en dos grupos: **Generadores base** y **Distribución uniforme**.

- Los métodos **Aditivo** y **Multiplicativo** (en ambos grupos) no admiten carga de CSV y solo se pueden ingresar manualmente. Esto es intencional: ambos son casos particulares del Congruencial Mixto — el aditivo fija `k=0` y el multiplicativo fija `c=0`. Si se quisieran ejecutar desde un archivo CSV, bastaría con usar el método **Congruencial** con esos valores en cero directamente en el archivo, sin necesidad de duplicar lógica ni agregar pasos extra al código.
- Los métodos **Cuadrados Medios** y **Congruencial** (en ambos grupos) soportan carga de archivos CSV.
- Los resultados se muestran agrupados por simulación, indicando los parámetros usados en cada una.