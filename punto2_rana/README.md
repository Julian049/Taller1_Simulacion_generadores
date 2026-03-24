# Punto 2 — La rana estadística en mundos paralelos

Simulación y análisis multidimensional de caminatas aleatorias simétricas en 1D, 2D y 3D.

---

## Estructura del módulo

```
punto2_rana/
├── main.py                      # Script principal de ejecución
├── simulacion_caminata.py       # Lógica de simulación en 1D, 2D y 3D
├── generador_congruencial.py    # Adaptador del generador congruencial de generators.py
├── visualizacion.py             # Generación de todos los gráficos
├── analisis_probabilistico.py   # Cálculo teórico de probabilidades de retorno
├── figuras/                     # Carpeta de salida de figuras (se crea automáticamente)
│   ├── histograma_1d.png
│   ├── trayectoria_1d.png
│   ├── scatter_2d.png
│   ├── heatmap_2d.png
│   ├── scatter_3d.png
│   ├── proyecciones_3d.png
│   └── comparativo_dimensiones.png
└── README.md
```

---

## Dependencias

- Python 3.10 o superior
- `matplotlib` (única dependencia externa, para gráficos)
- `generators.py` del proyecto raíz (generador congruencial — sin librerías de aleatoriedad)

Instalar matplotlib:
```bash
pip install matplotlib
```

---

## Ejecución

### Modo completo (100 simulaciones × 1 000 000 pasos — puede tardar varios minutos)
```bash
cd punto2_rana
python main.py
```

### Modo rápido (para prueba rápida: 10 sims × 10 000 pasos)
```bash
python main.py --modo rapido
```

### Parámetros configurables
```bash
python main.py --semilla 42 --simulaciones 200 --pasos 500000
```

| Parámetro        | Default     | Descripción                                |
|------------------|-------------|--------------------------------------------|
| `--semilla`      | `12345`     | Semilla base del generador congruencial    |
| `--simulaciones` | `100`       | Número de simulaciones independientes      |
| `--pasos`        | `1000000`   | Pasos por simulación                       |
| `--modo`         | `completo`  | `rapido` para pruebas de 10 sims × 10 000  |

---

## Generador pseudoaleatorio utilizado

Se reutiliza directamente la función `congruence()` de `generators.py`. El método es **Congruencial Lineal Mixto**:

```
Xᵢ₊₁ = (Xᵢ · a + c) mod m
donde: a = 1 + 2k,  m = 2^g
```

Parámetros por defecto elegidos para período máximo (m = 2³²):
- `k = 1 664 525`  → `a = 3 329 051`
- `c = 1 013 904 223`
- `g = 32`  → `m = 4 294 967 296`

Cada simulación usa una semilla diferente (`semilla_base + i × 1_000_003`) para garantizar la independencia estadística entre simulaciones.

---

## Módulos

### `generador_congruencial.py`
Adaptador que importa `congruence()` de `generators.py` y provee la clase `GeneradorCongruencial` con métodos `generar(n)` y `generar_pasos(n, dims)`.

### `simulacion_caminata.py`
- `simular_1d(semilla, n_pasos, n_sims, pasos_retorno)` → `ResultadoSimulacion`
- `simular_2d(semilla, n_pasos, n_sims, pasos_retorno)` → `ResultadoSimulacion`
- `simular_3d(semilla, n_pasos, n_sims, pasos_retorno)` → `ResultadoSimulacion`
- `analizar_resultado(resultado)` → estadísticas descriptivas

### `analisis_probabilistico.py`
- `prob_retorno_1d(n_saltos)` → probabilidad exacta
- `prob_retorno_2d(n_saltos)` → probabilidad exacta
- `prob_retorno_3d_aproximada(n_saltos)` → aproximación asintótica
- `tabla_probabilidades_retorno(pasos_lista)` → tabla comparativa

### `visualizacion.py`
- `graficar_histograma_1d()` → `figuras/histograma_1d.png`
- `graficar_trayectoria_1d()` → `figuras/trayectoria_1d.png`
- `graficar_scatter_2d()` → `figuras/scatter_2d.png`
- `graficar_heatmap_2d()` → `figuras/heatmap_2d.png`
- `graficar_scatter_3d()` → `figuras/scatter_3d.png`
- `graficar_proyecciones_3d()` → `figuras/proyecciones_3d.png`
- `graficar_comparativo()` → `figuras/comparativo_dimensiones.png`

---

## Fundamento teórico

**Teorema Central del Límite (TCL):** tras N pasos de una caminata simétrica en 1D, la posición final converge en distribución a N(0, N). El histograma de posiciones finales tiene forma gaussiana con σ = √N.

**Teorema de Pólya:** las caminatas aleatorias simétricas son *recurrentes* en 1D y 2D (la rana vuelve al origen con probabilidad 1), pero *transientes* en 3D (P(retorno eventual) ≈ 0.3405).

**Referencias:**
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*, Vol. 1. Wiley.
- Spitzer, F. (1976). *Principles of Random Walk*, 2nd ed. Springer.
