"""
## 3. Prueba Chi-Cuadrado
Verifica que los números pseudoaleatorios se distribuyan de manera uniforme
en el intervalo [0,1], comparando las frecuencias observadas en cada
subintervalo contra las frecuencias esperadas teóricas.
"""

import math
import matplotlib.pyplot as plt
from scipy.stats import chi2


def prueba_chi_cuadrado(secuencia, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados

    Nota: el número de intervalos k se calcula automáticamente como
    max(10, int(sqrt(N))) según el tamaño de la secuencia.
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Número de intervalos calculado automáticamente según tamaño de la secuencia
    k = max(10, int(math.sqrt(N)))

    # Frecuencia esperada en cada intervalo
    frecuencia_esperada = N / k

    # Contar frecuencias observadas en cada intervalo
    frecuencias_observadas = [0] * k
    for numero in secuencia:
        indice = int(numero * k)
        if indice == k:  # caso borde: cuando número es exactamente 1.0
            indice = k - 1
        frecuencias_observadas[indice] += 1

    # Calcular estadístico chi-cuadrado
    chi2_calculado = sum(
        (obs - frecuencia_esperada) ** 2 / frecuencia_esperada
        for obs in frecuencias_observadas
    )

    # Valor crítico chi-cuadrado exacto para k-1 grados de libertad
    gl = k - 1
    chi2_critico = chi2.ppf(nivel_confianza, gl)

    # Verificar si la secuencia pasa la prueba
    aprueba = chi2_calculado < chi2_critico

    return {
        "N": N,
        "k": k,
        "frecuencias_observadas": frecuencias_observadas,
        "frecuencia_esperada": round(frecuencia_esperada, 6),
        "chi2_calculado": round(chi2_calculado, 6),
        "chi2_critico": round(chi2_critico, 6),
        "grados_libertad": gl,
        "aprueba": aprueba
    }


def grafico_prueba_chi_cuadrado(resultado):
    """
    Parámetros:
        resultado: diccionario retornado por prueba_chi_cuadrado()
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    k = resultado["k"]
    intervalos = [f"{i/k:.1f}-{(i+1)/k:.1f}" for i in range(k)]
    frecuencias_observadas = resultado["frecuencias_observadas"]
    frecuencia_esperada = resultado["frecuencia_esperada"]

    x = range(k)
    ancho = 0.35

    barras_obs = ax.bar([i - ancho/2 for i in x], frecuencias_observadas,
                        ancho, label="Frecuencia observada", color="steelblue")
    barras_esp = ax.bar([i + ancho/2 for i in x], [frecuencia_esperada] * k,
                        ancho, label="Frecuencia esperada", color="orange", alpha=0.7)

    for barra in barras_obs:
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.1,
                str(int(barra.get_height())), ha="center", va="bottom", fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(intervalos, rotation=45, ha="right")
    ax.set_xlabel("Intervalos", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title("Prueba Chi-Cuadrado: Frecuencias Observadas vs Esperadas",
                 fontsize=14, fontweight="bold")
    ax.legend()

    ax.text(0.98, 0.95,
            f"χ² calculado = {resultado['chi2_calculado']}\n"
            f"χ² crítico = {resultado['chi2_critico']}\n"
            f"Grados de libertad = {resultado['grados_libertad']}",
            transform=ax.transAxes, fontsize=10,
            verticalalignment="top", horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    texto = "APRUEBA ✓" if resultado["aprueba"] else "FALLA ✗"
    color_texto = "green" if resultado["aprueba"] else "red"
    ax.text(0.02, 0.95, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto, verticalalignment="top", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_prueba_chi_cuadrado.png", dpi=150)
    plt.show()
