"""
visualizacion.py
-----------------
Módulo de generación de gráficos para los resultados de la caminata aleatoria.

Funciones principales
---------------------
- graficar_histograma_1d()  : Histograma de posiciones finales en 1D
- graficar_scatter_2d()     : Scatter plot de posiciones finales en 2D
- graficar_heatmap_2d()     : Mapa de calor de densidad en 2D
- graficar_scatter_3d()     : Scatter 3D de posiciones finales
- graficar_proyecciones_3d(): Proyecciones ortogonales XY, XZ, YZ
- graficar_comparativo()    : Resumen comparativo de las tres dimensiones
- graficar_trayectoria_1d() : Traza de una simulación individual en 1D

Justificación de visualizaciones
----------------------------------
1D → Histograma: la distribución de posiciones es unidimensional; el histograma
     revela directamente la forma de campana predicha por el TCL.

2D → Scatter plot: muestra la dispersión espacial y la simetría rotacional.
     Heatmap: visualiza la densidad de llegada, útil para apreciar la distribución
     gaussiana bidimensional subyacente.

3D → Scatter 3D: da intuición espacial del volumen explorado.
     Proyecciones ortogonales: reducen la complejidad visual y permiten comparar
     ejes independientemente, siendo más informativos que el scatter 3D solo.
"""

import os
import math
import matplotlib
matplotlib.use("Agg")  # backend sin pantalla para entornos sin GUI
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Directorio de salida de figuras
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------

def _guardar(fig: plt.Figure, nombre: str) -> str:
    """Guarda la figura en el directorio de salida y retorna la ruta."""
    ruta = os.path.join(OUTPUT_DIR, nombre)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta


def _campana_normal(x_vals: list[float], media: float, desv: float) -> list[float]:
    """
    Evalúa la función de densidad normal N(media, desv²) en x_vals.
    Implementación manual, sin scipy, para coherencia con el enfoque from-scratch.
    """
    factor = 1.0 / (desv * math.sqrt(2 * math.pi))
    return [factor * math.exp(-0.5 * ((x - media) / desv) ** 2) for x in x_vals]


# ---------------------------------------------------------------------------
# 1D
# ---------------------------------------------------------------------------

def graficar_histograma_1d(resultado: dict, estadisticas: dict,
                            n_bins: int = 60) -> str:
    """
    Genera el histograma de posiciones finales en 1D y superpone la curva normal
    teórica predicha por el Teorema Central del Límite.

    El TCL predice que, tras N pasos de una caminata aleatoria simétrica,
    la posición final sigue aproximadamente N(0, √N).

    Parámetros
    ----------
    resultado : dict
        ResultadoSimulacion de simular_1d().
    estadisticas : dict
        Salida de analizar_resultado().
    n_bins : int
        Número de intervalos del histograma.

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    posiciones = [p[0] for p in resultado["posiciones_finales"]]
    n_pasos    = resultado["n_pasos"]
    n_sims     = resultado["n_simulaciones"]
    media      = estadisticas["coords_medias"][0]
    desv       = estadisticas["desv_distancia"]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histograma normalizado (densidad de probabilidad)
    counts, bin_edges, _ = ax.hist(
        posiciones, bins=n_bins, density=True,
        color="#4C72B0", alpha=0.7, edgecolor="white", linewidth=0.5,
        label="Frecuencia relativa simulada"
    )

    # Curva normal teórica N(0, √N)
    desv_teorica = math.sqrt(n_pasos)
    x_min = min(posiciones)
    x_max = max(posiciones)
    paso_x = (x_max - x_min) / 500
    x_teorico = [x_min + i * paso_x for i in range(501)]
    y_teorico  = _campana_normal(x_teorico, 0, desv_teorica)

    ax.plot(x_teorico, y_teorico, color="#C44E52", linewidth=2.0,
            label=f"N(0, √N) teórica  (σ = {desv_teorica:.0f})")

    ax.axvline(0, color="gray", linestyle="--", linewidth=1.2, alpha=0.6,
               label="Origen (μ = 0)")
    ax.axvline(media, color="#DD8452", linestyle=":", linewidth=1.5,
               label=f"Media observada = {media:.1f}")

    ax.set_title(
        f"Histograma de posiciones finales — Caminata aleatoria 1D\n"
        f"({n_sims} simulaciones · {n_pasos:,} pasos c/u)",
        fontsize=13, pad=12
    )
    ax.set_xlabel("Posición final de la rana", fontsize=11)
    ax.set_ylabel("Densidad de probabilidad", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    return _guardar(fig, "histograma_1d.png")


def graficar_trayectoria_1d(semilla: int, n_pasos: int = 5000) -> str:
    """
    Traza la trayectoria de una única simulación en 1D (posición vs. paso).

    Se limita a `n_pasos` primeros pasos para legibilidad visual.

    Parámetros
    ----------
    semilla : int
        Semilla para el generador.
    n_pasos : int
        Número de pasos a graficar.

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from generador_congruencial import GeneradorCongruencial

    gen = GeneradorCongruencial(semilla)
    ri_values = gen.generar(n_pasos)

    trayectoria = [0]
    pos = 0
    for ri in ri_values:
        pos += 1 if ri >= 0.5 else -1
        trayectoria.append(pos)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(range(len(trayectoria)), trayectoria, linewidth=0.6,
            color="#4C72B0", alpha=0.85)
    ax.axhline(0, color="red", linewidth=1.0, linestyle="--", alpha=0.5)
    ax.set_title(f"Trayectoria 1D — semilla {semilla} — {n_pasos:,} pasos",
                 fontsize=12)
    ax.set_xlabel("Número de paso")
    ax.set_ylabel("Posición")
    ax.grid(alpha=0.3)

    return _guardar(fig, "trayectoria_1d.png")


# ---------------------------------------------------------------------------
# 2D
# ---------------------------------------------------------------------------

def graficar_scatter_2d(resultado: dict) -> str:
    """
    Scatter plot de posiciones finales en 2D.

    Justificación: permite observar la distribución espacial isotrópica
    de las posiciones finales, confirmando la simetría rotacional de la
    caminata simétrica bidimensional.

    Parámetros
    ----------
    resultado : dict
        ResultadoSimulacion de simular_2d().

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    posiciones = resultado["posiciones_finales"]
    xs = [p[0] for p in posiciones]
    ys = [p[1] for p in posiciones]
    n_sims  = resultado["n_simulaciones"]
    n_pasos = resultado["n_pasos"]

    fig, ax = plt.subplots(figsize=(8, 8))
    sc = ax.scatter(xs, ys, alpha=0.5, s=20, c=range(n_sims),
                    cmap="viridis", edgecolors="none")
    ax.scatter(0, 0, marker="*", s=250, color="red", zorder=5, label="Origen")
    plt.colorbar(sc, ax=ax, label="Índice de simulación")

    ax.set_title(
        f"Posiciones finales — Caminata aleatoria 2D\n"
        f"({n_sims} simulaciones · {n_pasos:,} pasos c/u)",
        fontsize=12
    )
    ax.set_xlabel("Posición X")
    ax.set_ylabel("Posición Y")
    ax.legend(fontsize=10)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)

    return _guardar(fig, "scatter_2d.png")


def graficar_heatmap_2d(resultado: dict, n_bins: int = 40) -> str:
    """
    Mapa de calor (heatmap) de densidad de posiciones finales en 2D.

    Justificación: el heatmap revela la distribución gaussiana bidimensional
    subyacente con mayor claridad que el scatter plot cuando hay muchos puntos,
    mostrando la concentración de probabilidad cerca del origen.

    Parámetros
    ----------
    resultado : dict
        ResultadoSimulacion de simular_2d().
    n_bins : int
        Número de celdas por eje del heatmap.

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    posiciones = resultado["posiciones_finales"]
    xs = [p[0] for p in posiciones]
    ys = [p[1] for p in posiciones]
    n_sims  = resultado["n_simulaciones"]
    n_pasos = resultado["n_pasos"]

    # Construcción manual del heatmap mediante histograma 2D
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    ancho_x = (x_max - x_min) / n_bins
    ancho_y = (y_max - y_min) / n_bins

    grilla = [[0] * n_bins for _ in range(n_bins)]
    for x, y in zip(xs, ys):
        col = min(int((x - x_min) / ancho_x), n_bins - 1)
        fil = min(int((y - y_min) / ancho_y), n_bins - 1)
        grilla[fil][col] += 1

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(
        grilla, origin="lower", aspect="auto",
        extent=[x_min, x_max, y_min, y_max],
        cmap="hot_r", interpolation="nearest"
    )
    plt.colorbar(im, ax=ax, label="Frecuencia")
    ax.scatter(0, 0, marker="*", s=250, color="cyan", zorder=5, label="Origen")
    ax.set_title(
        f"Heatmap de densidad — Caminata aleatoria 2D\n"
        f"({n_sims} simulaciones · {n_pasos:,} pasos c/u)",
        fontsize=12
    )
    ax.set_xlabel("Posición X")
    ax.set_ylabel("Posición Y")
    ax.legend(fontsize=10)

    return _guardar(fig, "heatmap_2d.png")


# ---------------------------------------------------------------------------
# 3D
# ---------------------------------------------------------------------------

def graficar_scatter_3d(resultado: dict) -> str:
    """
    Scatter 3D de posiciones finales.

    Justificación: proporciona una visión intuitiva del volumen tridimensional
    explorado por la rana, útil para apreciar la dispersión isotrópica en el espacio.

    Parámetros
    ----------
    resultado : dict
        ResultadoSimulacion de simular_3d().

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    posiciones = resultado["posiciones_finales"]
    xs = [p[0] for p in posiciones]
    ys = [p[1] for p in posiciones]
    zs = [p[2] for p in posiciones]
    n_sims  = resultado["n_simulaciones"]
    n_pasos = resultado["n_pasos"]

    fig = plt.figure(figsize=(9, 8))
    ax  = fig.add_subplot(111, projection="3d")

    sc = ax.scatter(xs, ys, zs, alpha=0.5, s=15, c=range(n_sims),
                    cmap="plasma", depthshade=True)
    ax.scatter(0, 0, 0, marker="*", s=300, color="red", zorder=5,
               label="Origen")

    plt.colorbar(sc, ax=ax, label="Índice de simulación", pad=0.1)
    ax.set_title(
        f"Posiciones finales — Caminata aleatoria 3D\n"
        f"({n_sims} simulaciones · {n_pasos:,} pasos c/u)",
        fontsize=11
    )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend(fontsize=9)

    return _guardar(fig, "scatter_3d.png")


def graficar_proyecciones_3d(resultado: dict) -> str:
    """
    Proyecciones ortogonales XY, XZ e YZ de las posiciones finales en 3D.

    Justificación: las proyecciones ortogonales eliminan la oclusión inherente
    al scatter 3D y permiten analizar la distribución marginal en cada par de
    ejes, comprobando la independencia y la simetría en cada plano.

    Parámetros
    ----------
    resultado : dict
        ResultadoSimulacion de simular_3d().

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    posiciones = resultado["posiciones_finales"]
    xs = [p[0] for p in posiciones]
    ys = [p[1] for p in posiciones]
    zs = [p[2] for p in posiciones]
    n_sims  = resultado["n_simulaciones"]
    n_pasos = resultado["n_pasos"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    params_plot = [
        (xs, ys, "X", "Y", "Proyección XY"),
        (xs, zs, "X", "Z", "Proyección XZ"),
        (ys, zs, "Y", "Z", "Proyección YZ"),
    ]

    for ax, (a, b, lx, ly, titulo) in zip(axes, params_plot):
        ax.scatter(a, b, alpha=0.4, s=15, color="#4C72B0", edgecolors="none")
        ax.scatter(0, 0, marker="*", s=200, color="red", zorder=5, label="Origen")
        ax.set_title(titulo, fontsize=11)
        ax.set_xlabel(lx)
        ax.set_ylabel(ly)
        ax.set_aspect("equal")
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

    fig.suptitle(
        f"Proyecciones ortogonales — Caminata aleatoria 3D\n"
        f"({n_sims} simulaciones · {n_pasos:,} pasos c/u)",
        fontsize=12, y=1.02
    )
    fig.tight_layout()

    return _guardar(fig, "proyecciones_3d.png")


# ---------------------------------------------------------------------------
# Comparativo entre dimensiones
# ---------------------------------------------------------------------------

def graficar_comparativo(stats_1d: dict, stats_2d: dict, stats_3d: dict,
                          res_1d: dict, res_2d: dict, res_3d: dict) -> str:
    """
    Panel comparativo de métricas clave entre las tres dimensiones.

    Muestra en cuatro subgráficos:
    1. Probabilidad de retorno al origen (barras).
    2. Distancia media al origen (barras).
    3. Tiempo total de ejecución (barras).
    4. Desviación estándar de la distancia (barras).

    Parámetros
    ----------
    stats_Xd : dict
        Salida de analizar_resultado() para cada dimensión.
    res_Xd : dict
        ResultadoSimulacion para cada dimensión (usado para etiquetas).

    Retorna
    -------
    str
        Ruta de la figura guardada.
    """
    dims   = ["1D", "2D", "3D"]
    colors = ["#4C72B0", "#55A868", "#C44E52"]

    prob_retornos  = [stats_1d["prob_retorno"],    stats_2d["prob_retorno"],    stats_3d["prob_retorno"]]
    dist_medias    = [stats_1d["media_distancia"],  stats_2d["media_distancia"],  stats_3d["media_distancia"]]
    t_totales      = [stats_1d["tiempo_total"],     stats_2d["tiempo_total"],     stats_3d["tiempo_total"]]
    desv_distancias= [stats_1d["desv_distancia"],   stats_2d["desv_distancia"],   stats_3d["desv_distancia"]]

    fig = plt.figure(figsize=(14, 9))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    def _barras(ax, valores, titulo, ylabel, fmt="{:.4f}"):
        barras = ax.bar(dims, valores, color=colors, width=0.5, edgecolor="white")
        ax.set_title(titulo, fontsize=11, pad=8)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_ylim(0, max(valores) * 1.25)
        for bar, val in zip(barras, valores):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(valores) * 0.03,
                    fmt.format(val), ha="center", va="bottom", fontsize=9)
        ax.grid(axis="y", alpha=0.3)

    _barras(fig.add_subplot(gs[0, 0]), prob_retornos,
            "Probabilidad de retorno al origen\n(primeros 1 000 pasos)",
            "Probabilidad estimada")

    _barras(fig.add_subplot(gs[0, 1]), dist_medias,
            "Distancia euclidiana media al origen\n(posición final)",
            "Distancia (unidades)", fmt="{:.1f}")

    _barras(fig.add_subplot(gs[1, 0]), t_totales,
            "Tiempo total de ejecución\n(todas las simulaciones)",
            "Tiempo (s)", fmt="{:.2f}")

    _barras(fig.add_subplot(gs[1, 1]), desv_distancias,
            "Desviación estándar de la distancia\nal origen",
            "Desviación estándar", fmt="{:.1f}")

    fig.suptitle("Análisis comparativo: Caminata aleatoria 1D · 2D · 3D",
                 fontsize=14, y=1.01, fontweight="bold")

    return _guardar(fig, "comparativo_dimensiones.png")
