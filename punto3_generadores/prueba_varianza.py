"""
## 2. Prueba de Varianza
Verifica que la varianza de la secuencia pseudoaleatoria sea estadísticamente
cercana a 1/12 ≈ 0.0833, valor esperado de una distribución uniforme U(0,1).
"""

import math
import matplotlib.pyplot as plt
from scipy.stats import chi2


def prueba_varianza(secuencia, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Media muestral
    media = sum(secuencia) / N

    # Varianza muestral
    varianza_muestral = sum((x - media) ** 2 for x in secuencia) / (N - 1)

    # Varianza teórica para U(0,1)
    varianza_teorica = 1 / 12

    # Nivel de significancia y grados de libertad
    alpha = 1 - nivel_confianza
    gl = N - 1

    # Valores críticos Chi-cuadrado exactos
    chi2_inferior = chi2.ppf(alpha / 2, gl)
    chi2_superior = chi2.ppf(1 - alpha / 2, gl)

    # Intervalo de confianza para la varianza
    limite_inferior = chi2_inferior / (12 * gl)
    limite_superior = chi2_superior / (12 * gl)

    # Verificar si la secuencia pasa la prueba
    aprueba = limite_inferior <= varianza_muestral <= limite_superior

    return {
        "N": N,
        "varianza_muestral": round(varianza_muestral, 6),
        "varianza_teorica": round(varianza_teorica, 6),
        "alpha": round(alpha, 4),
        "grados_libertad": gl,
        "chi2_inferior": round(chi2_inferior, 6),
        "chi2_superior": round(chi2_superior, 6),
        "limite_inferior": round(limite_inferior, 6),
        "limite_superior": round(limite_superior, 6),
        "aprueba": aprueba
    }


def grafico_prueba_varianza(resultado):
    """
    Parámetros:
        resultado: diccionario retornado por prueba_varianza()
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Línea de la varianza teórica
    ax.axhline(y=resultado["varianza_teorica"], color="blue",
               linestyle="--", label=f"Varianza teórica (1/12 ≈ {resultado['varianza_teorica']})")

    # Intervalo de confianza como franja
    ax.axhspan(resultado["limite_inferior"], resultado["limite_superior"],
               alpha=0.2, color="green", label="Intervalo de confianza 95%")

    # Líneas de los límites
    ax.axhline(y=resultado["limite_inferior"], color="green", linestyle=":", linewidth=1)
    ax.axhline(y=resultado["limite_superior"], color="green", linestyle=":", linewidth=1)

    # Punto de la varianza muestral
    color_punto = "blue" if resultado["aprueba"] else "red"
    ax.plot(0.5, resultado["varianza_muestral"], "o",
            color=color_punto, markersize=12,
            label=f"Varianza muestral ({resultado['varianza_muestral']})")

    # Etiquetas y formato
    ax.set_xlim(0, 1)
    ax.set_ylim(0, resultado["limite_superior"] + 0.05)
    ax.set_title("Prueba de Varianza", fontsize=14, fontweight="bold")
    ax.set_ylabel("Valor", fontsize=12)
    ax.set_xticks([])
    ax.legend(loc="upper right")

    # Resultado en el gráfico
    texto = "APRUEBA ✓" if resultado["aprueba"] else "FALLA ✗"
    color_texto = "green" if resultado["aprueba"] else "red"
    ax.text(0.5, 0.1, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto, ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_prueba_varianza.png", dpi=150)
    plt.show()
