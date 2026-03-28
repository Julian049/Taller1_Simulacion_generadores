"""
## 1. Prueba de Medias
Verifica que la media de la secuencia pseudoaleatoria sea estadísticamente
cercana a 0.5, valor esperado de una distribución uniforme U(0,1).
"""

import math
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2


def prueba_medias(secuencia, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Calcular la media muestral
    media_muestral = sum(secuencia) / N

    # Valor Z calculado dinámicamente según nivel de confianza
    z = norm.ppf(1 - (1 - nivel_confianza) / 2)

    # Media teórica para U(0,1)
    media_teorica = 0.5

    # Intervalo de confianza
    margen = z * (1 / math.sqrt(12 * N))
    limite_inferior = media_teorica - margen
    limite_superior = media_teorica + margen

    # Verificar si la secuencia pasa la prueba
    aprueba = limite_inferior <= media_muestral <= limite_superior

    return {
        "N": N,
        "media_muestral": round(media_muestral, 6),
        "media_teorica": media_teorica,
        "valor_z": round(z, 6),
        "margen": round(margen, 6),
        "limite_inferior": round(limite_inferior, 6),
        "limite_superior": round(limite_superior, 6),
        "aprueba": aprueba
    }


def grafico_prueba_medias(resultado):
    """
    Gráfico para una sola secuencia: muestra la media muestral
    frente al intervalo de confianza y la media teórica.

    Parámetros:
        resultado: diccionario retornado por prueba_medias()
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Línea de la media teórica
    ax.axhline(y=resultado["media_teorica"], color="blue",
               linestyle="--", label="Media teórica (0.5)")

    # Intervalo de confianza como franja
    ax.axhspan(resultado["limite_inferior"], resultado["limite_superior"],
               alpha=0.2, color="green", label="Intervalo de confianza 95%")

    # Líneas de los límites
    ax.axhline(y=resultado["limite_inferior"], color="green", linestyle=":", linewidth=1)
    ax.axhline(y=resultado["limite_superior"], color="green", linestyle=":", linewidth=1)

    # Punto de la media muestral
    color_punto = "blue" if resultado["aprueba"] else "red"
    ax.plot(0.5, resultado["media_muestral"], "o",
            color=color_punto, markersize=12,
            label=f"Media muestral ({resultado['media_muestral']})")

    # Etiquetas y formato
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Prueba de Medias — Secuencia única", fontsize=14, fontweight="bold")
    ax.set_ylabel("Valor", fontsize=12)
    ax.set_xticks([])
    ax.legend(loc="upper right")

    # Resultado en el gráfico
    texto = "APRUEBA ✓" if resultado["aprueba"] else "FALLA ✗"
    color_texto = "green" if resultado["aprueba"] else "red"
    ax.text(0.5, 0.1, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto, ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_prueba_medias.png", dpi=150)
    plt.show()


def grafico_distribucion_medias(lista_medias, nivel_confianza=0.95):
    """
    Gráfico para múltiples simulaciones: muestra la distribución
    de las medias calculadas de cada simulación (ej: 100 simulaciones de la rana).

    Parámetros:
        lista_medias: lista de medias, una por cada simulación
        nivel_confianza: nivel de confianza (default 95%)
    """
    N = len(lista_medias)
    media_global = sum(lista_medias) / N
    media_teorica = 0.5

    # Intervalo de confianza de la distribución de medias
    z = norm.ppf(1 - (1 - nivel_confianza) / 2)
    desviacion = (sum((m - media_global)**2 for m in lista_medias) / (N - 1)) ** 0.5
    margen = z * desviacion / math.sqrt(N)
    limite_inferior = media_teorica - margen
    limite_superior = media_teorica + margen

    fig, ax = plt.subplots(figsize=(10, 5))

    # Histograma de medias
    ax.hist(lista_medias, bins=20, color="steelblue", alpha=0.7,
            edgecolor="black", label="Distribución de medias")

    # Línea de la media teórica
    ax.axvline(x=media_teorica, color="blue", linestyle="--",
               linewidth=2, label="Media teórica (0.5)")

    # Línea de la media global calculada
    ax.axvline(x=media_global, color="red", linestyle="-",
               linewidth=2, label=f"Media global ({round(media_global, 4)})")

    # Intervalo de confianza
    ax.axvspan(limite_inferior, limite_superior, alpha=0.15,
               color="green", label=f"Intervalo de confianza 95%")

    # Formato
    ax.set_xlabel("Media de cada simulación", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title("Prueba de Medias — Distribución de medias por simulación",
                 fontsize=14, fontweight="bold")
    ax.legend()

    # Información estadística
    aprueba = limite_inferior <= media_global <= limite_superior
    texto = "APRUEBA ✓" if aprueba else "FALLA ✗"
    color_texto = "green" if aprueba else "red"
    ax.text(0.98, 0.95,
            f"Simulaciones = {N}\nMedia global = {round(media_global, 6)}\n"
            f"LI = {round(limite_inferior, 6)}\nLS = {round(limite_superior, 6)}",
            transform=ax.transAxes, fontsize=10,
            verticalalignment="top", horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    ax.text(0.02, 0.95, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto,
            verticalalignment="top", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_distribucion_medias.png", dpi=150)
    plt.show()
