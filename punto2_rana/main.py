"""
main.py
--------
Punto 2 — La rana estadística en mundos paralelos.

Cubre exclusivamente lo que debe ir en el código:
  Sección 1 — Simulación computacional unidimensional
  Sección 2 — Visualización y análisis de resultados en 1D
  Sección 3 — Extensión multidimensional (2D y 3D)

Uso:
    python main.py [--semilla SEMILLA] [--simulaciones N] [--pasos P] [--modo MODO]

    --semilla      Semilla base del generador (default: 12345)
    --simulaciones Número de simulaciones independientes (default: 100)
    --pasos        Pasos por simulación (default: 1000000)
    --modo         'completo' | 'rapido' (10 sims x 10000 pasos, para pruebas)
"""

import argparse
import os
import sys
import math

# Agrega la raíz del proyecto al path para importar generators.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulacion_caminata import simular_1d, simular_2d, simular_3d, analizar_resultado
from visualizacion import (
    graficar_histograma_1d,
    graficar_trayectoria_1d,
    graficar_scatter_2d,
    graficar_heatmap_2d,
    graficar_scatter_3d,
    graficar_proyecciones_3d,
    graficar_comparativo,
)


def _separador(titulo: str) -> None:
    """Imprime un separador de sección en consola."""
    print("\n" + "=" * 65)
    print(f"  {titulo}")
    print("=" * 65)


def main():
    # ------------------------------------------------------------------
    # Argumentos de línea de comando
    # ------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Caminata aleatoria — La rana estadística")
    parser.add_argument("--semilla",      type=int, default=12345,
                        help="Semilla base del generador congruencial (default: 12345)")
    parser.add_argument("--simulaciones", type=int, default=100,
                        help="Número de simulaciones independientes (default: 100)")
    parser.add_argument("--pasos",        type=int, default=1_000_000,
                        help="Pasos por simulación (default: 1 000 000)")
    parser.add_argument("--modo",         type=str, default="completo",
                        choices=["completo", "rapido"],
                        help="'rapido': 10 sims x 10 000 pasos para verificación rápida")
    args = parser.parse_args()

    semilla       = args.semilla
    n_sims        = args.simulaciones
    n_pasos       = args.pasos
    pasos_retorno = 1000  # ventana de pasos en la que se detecta retorno al origen

    if args.modo == "rapido":
        n_sims  = 10
        n_pasos = 10_000
        print("[MODO RÁPIDO] 10 simulaciones × 10 000 pasos")

    print(f"\n  Semilla base       : {semilla}")
    print(f"  Simulaciones       : {n_sims}")
    print(f"  Pasos/simulación   : {n_pasos:,}")
    print(f"  Generador          : Congruencial Lineal Mixto (generators.py)")

    # ==================================================================
    # SECCIÓN 1 — Simulación computacional unidimensional
    # ==================================================================
    _separador("SECCIÓN 1 — Simulación computacional unidimensional")

    print(f"\n  Ejecutando {n_sims} simulaciones de {n_pasos:,} pasos en 1D...")

    resultado_1d = simular_1d(semilla, n_pasos, n_sims, pasos_retorno)
    stats_1d     = analizar_resultado(resultado_1d)

    print(f"  Completado.")
    print(f"\n  Métricas 1D:")
    print(f"    Posición media final       : {stats_1d['coords_medias'][0]:.2f}")
    print(f"    Distancia media al origen  : {stats_1d['media_distancia']:.2f}")
    print(f"    Desv. estándar distancia   : {stats_1d['desv_distancia']:.2f}")
    print(f"    sigma teórica (sqrt N)     : {math.sqrt(n_pasos):.2f}")
    print(f"    Tiempo total ejecución     : {stats_1d['tiempo_total']:.4f} s")
    print(f"    Tiempo medio/simulación    : {stats_1d['tiempo_medio'] * 1000:.4f} ms")

    # ==================================================================
    # SECCIÓN 2 — Visualización y análisis de resultados en 1D
    # ==================================================================
    _separador("SECCIÓN 2 — Visualización y análisis de resultados en 1D")

    ruta_h1d = graficar_histograma_1d(resultado_1d, stats_1d)
    ruta_t1d = graficar_trayectoria_1d(semilla, min(5000, n_pasos))

    print(f"  Figuras generadas:")
    print(f"    Histograma 1D    → {ruta_h1d}")
    print(f"    Trayectoria 1D   → {ruta_t1d}")

    print(f"\n  Análisis estadístico:")
    print(f"    Forma del histograma: campana gaussiana (distribución normal),")
    print(f"    predicha por el Teorema Central del Límite.")
    print(f"    Tras {n_pasos:,} pasos la posición final converge a N(0, N).")
    print(f"    Simetría : media observada = {stats_1d['coords_medias'][0]:.2f}  (valor esperado = 0)")
    print(f"    Dispersión: sigma observada = {stats_1d['desv_distancia']:.2f}  |  sigma teórica = {math.sqrt(n_pasos):.2f}")

    # ==================================================================
    # SECCIÓN 3 — Extensión multidimensional (2D y 3D)
    # ==================================================================
    _separador("SECCIÓN 3 — Extensión multidimensional (2D y 3D)")

    # ------------------------------------------------------------------
    # 2D
    # ------------------------------------------------------------------
    print(f"\n  [2D] Ejecutando {n_sims} simulaciones de {n_pasos:,} pasos...")

    resultado_2d = simular_2d(semilla, n_pasos, n_sims, pasos_retorno)
    stats_2d     = analizar_resultado(resultado_2d)

    print(f"  Completado.")
    print(f"\n  Métricas 2D:")
    print(f"    Distancia media al origen  : {stats_2d['media_distancia']:.2f}")
    print(f"    Desv. estándar distancia   : {stats_2d['desv_distancia']:.2f}")
    print(f"    P(retorno al origen)       : {stats_2d['prob_retorno']:.6f}")
    print(f"    Tiempo total ejecución     : {stats_2d['tiempo_total']:.4f} s")
    print(f"    Tiempo medio/simulación    : {stats_2d['tiempo_medio'] * 1000:.4f} ms")

    ruta_s2d = graficar_scatter_2d(resultado_2d)
    ruta_h2d = graficar_heatmap_2d(resultado_2d)
    print(f"\n  Figuras generadas:")
    print(f"    Scatter 2D       → {ruta_s2d}")
    print(f"    Heatmap 2D       → {ruta_h2d}")

    # ------------------------------------------------------------------
    # 3D
    # ------------------------------------------------------------------
    print(f"\n  [3D] Ejecutando {n_sims} simulaciones de {n_pasos:,} pasos...")

    resultado_3d = simular_3d(semilla, n_pasos, n_sims, pasos_retorno)
    stats_3d     = analizar_resultado(resultado_3d)

    print(f"  Completado.")
    print(f"\n  Métricas 3D:")
    print(f"    Distancia media al origen  : {stats_3d['media_distancia']:.2f}")
    print(f"    Desv. estándar distancia   : {stats_3d['desv_distancia']:.2f}")
    print(f"    P(retorno al origen)       : {stats_3d['prob_retorno']:.6f}")
    print(f"    Tiempo total ejecución     : {stats_3d['tiempo_total']:.4f} s")
    print(f"    Tiempo medio/simulación    : {stats_3d['tiempo_medio'] * 1000:.4f} ms")

    ruta_s3d = graficar_scatter_3d(resultado_3d)
    ruta_p3d = graficar_proyecciones_3d(resultado_3d)
    print(f"\n  Figuras generadas:")
    print(f"    Scatter 3D       → {ruta_s3d}")
    print(f"    Proyecciones 3D  → {ruta_p3d}")

    # ------------------------------------------------------------------
    # Gráfico comparativo entre las tres dimensiones
    # ------------------------------------------------------------------
    ruta_cmp = graficar_comparativo(stats_1d, stats_2d, stats_3d,
                                     resultado_1d, resultado_2d, resultado_3d)
    print(f"    Comparativo      → {ruta_cmp}")

    # ------------------------------------------------------------------
    # Cuadro de eficiencia computacional (1D / 2D / 3D)
    # ------------------------------------------------------------------
    print(f"\n  Cuadro de eficiencia computacional:")
    t1 = stats_1d["tiempo_total"]
    encabezado = f"  {'Dim':<5} {'T. total (s)':>14} {'T. medio (ms)':>15} {'RNG/sim':>12} {'Overhead':>10}"
    print(encabezado)
    print("  " + "-" * (len(encabezado) - 2))
    filas = [
        ("1D", t1,                       stats_1d["tiempo_medio"], n_pasos,     "base"),
        ("2D", stats_2d["tiempo_total"], stats_2d["tiempo_medio"], n_pasos * 2, f"x{stats_2d['tiempo_total'] / t1:.2f}"),
        ("3D", stats_3d["tiempo_total"], stats_3d["tiempo_medio"], n_pasos * 3, f"x{stats_3d['tiempo_total'] / t1:.2f}"),
    ]
    for dim, tt, tm, rng, oh in filas:
        print(f"  {dim:<5} {tt:>14.4f} {tm * 1000:>15.4f} {rng:>12,} {oh:>10}")

    # ------------------------------------------------------------------
    # P(retorno al origen | primeros 1000 pasos) por dimensión
    # ------------------------------------------------------------------
    print(f"\n  Probabilidad estimada de retorno al origen (primeros {pasos_retorno} pasos):")
    print(f"  {'Dimensión':<12} {'P(retorno)'}")
    print(f"  {'-'*26}")
    print(f"  {'1D':<12} {stats_1d['prob_retorno']:.6f}")
    print(f"  {'2D':<12} {stats_2d['prob_retorno']:.6f}")
    print(f"  {'3D':<12} {stats_3d['prob_retorno']:.6f}")

    print(f"\n{'='*65}")
    print(f"  Todas las figuras guardadas en: punto2_rana/figuras/")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
