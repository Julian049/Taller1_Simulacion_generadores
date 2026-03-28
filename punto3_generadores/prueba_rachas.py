"""
## 6. Prueba de Rachas
Verifica la aleatoriedad de la secuencia pseudoaleatoria detectando
patrones de agrupamiento por encima o por debajo de la mediana.
Clasifica cada número como (+) si es mayor o igual a la mediana
y (-) si es menor, contando las rachas resultantes y comparando
contra los valores esperados teóricos mediante un estadístico Z.
"""

import math
import matplotlib.pyplot as plt
from scipy.stats import norm


def prueba_rachas(secuencia, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Calcular la mediana de la secuencia
    secuencia_ordenada = sorted(secuencia)
    if N % 2 == 0:
        mediana = (secuencia_ordenada[N//2 - 1] + secuencia_ordenada[N//2]) / 2
    else:
        mediana = secuencia_ordenada[N//2]

    # Mediana teórica para U(0,1)
    mediana_teorica = 0.5

    # Clasificar cada número como + o -
    signos = []
    for numero in secuencia:
        if numero >= mediana:
            signos.append("+")
        else:
            signos.append("-")

    # Contar total de + y total de -
    n1 = signos.count("+")
    n2 = signos.count("-")

    # Contar rachas totales
    rachas = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i-1]:
            rachas += 1

    # Rachas esperadas y varianza esperada
    rachas_esperadas = ((2 * n1 * n2) / N) + 1
    varianza_esperada = (2 * n1 * n2 * (2 * n1 * n2 - N)) / (N**2 * (N - 1))

    # Estadístico Z
    z_calculado = (rachas - rachas_esperadas) / math.sqrt(varianza_esperada)

    # Valor crítico Z calculado dinámicamente según nivel de confianza
    z_critico = norm.ppf(1 - (1 - nivel_confianza) / 2)

    # Rango de aceptación
    rango_minimo = -z_critico
    rango_maximo = z_critico

    # Verificar si la secuencia pasa la prueba
    aprueba = rango_minimo <= z_calculado <= rango_maximo

    return {
        "N": N,
        "mediana": round(mediana, 6),
        "mediana_teorica": mediana_teorica,
        "n1_positivos": n1,
        "n2_negativos": n2,
        "rachas_observadas": rachas,
        "rachas_esperadas": round(rachas_esperadas, 6),
        "varianza_esperada": round(varianza_esperada, 6),
        "z_calculado": round(z_calculado, 6),
        "z_critico": round(z_critico, 6),
        "rango_minimo": round(rango_minimo, 6),
        "rango_maximo": round(rango_maximo, 6),
        "aprueba": aprueba
    }


def grafico_prueba_rachas(resultado):
    """
    Parámetros:
        resultado: diccionario retornado por prueba_rachas()
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    categorias = ["Rachas\nObservadas", "Rachas\nEsperadas"]
    valores = [resultado["rachas_observadas"], resultado["rachas_esperadas"]]
    colores = ["steelblue", "orange"]

    barras = ax.bar(categorias, valores, color=colores,
                    width=0.4, edgecolor="black", linewidth=0.8)

    margen = resultado["z_critico"] * math.sqrt(resultado["varianza_esperada"])
    ax.errorbar(1, resultado["rachas_esperadas"],
                yerr=margen, fmt="none", color="red", capsize=8, linewidth=2,
                label=f"Intervalo de confianza 95%\n(±{round(margen, 2)})")

    for barra, valor in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.3,
                str(round(valor, 2)), ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    ax.set_ylabel("Número de Rachas", fontsize=12)
    ax.set_title("Prueba de Rachas: Observadas vs Esperadas",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper right")
    ax.set_ylim(0, max(valores) + 15)

    ax.text(0.02, 0.95,
            f"Z calculado = {resultado['z_calculado']}\n"
            f"Z crítico = ±{resultado['z_critico']}\n"
            f"n1(+) = {resultado['n1_positivos']}\n"
            f"n2(-) = {resultado['n2_negativos']}\n"
            f"Mediana = {resultado['mediana']}",
            transform=ax.transAxes, fontsize=10, verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    texto = "APRUEBA ✓" if resultado["aprueba"] else "FALLA ✗"
    color_texto = "green" if resultado["aprueba"] else "red"
    ax.text(0.98, 0.05, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto, ha="right", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_prueba_rachas.png", dpi=150)
    plt.show()
