"""
## 4. Prueba de Kolmogorov-Smirnov (KS)
Verifica que la distribución acumulada de la secuencia pseudoaleatoria
se ajuste a la distribución uniforme teórica U(0,1), comparando las
frecuencias acumuladas observadas contra las esperadas por intervalo
y calculando la máxima diferencia entre ambas.
"""

import math
import matplotlib.pyplot as plt


def prueba_ks(secuencia, k=10, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        k: número de intervalos (default 10)
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Frecuencia esperada por intervalo
    frec_esperada = N / k

    # Contar frecuencias observadas por intervalo
    frecuencias_observadas = [0] * k
    for numero in secuencia:
        indice = min(int(numero * k), k - 1)
        frecuencias_observadas[indice] += 1

    # Calcular frecuencias acumuladas y diferencias
    tabla = []
    frec_obs_acumulada = 0
    frec_esp_acumulada = 0

    for i in range(k):
        limite_inicial = round(i / k, 2)
        limite_final = round((i + 1) / k, 2)

        frec_obs_acumulada += frecuencias_observadas[i]
        frec_esp_acumulada += frec_esperada

        p_obs_acumulada = frec_obs_acumulada / N
        p_esp_acumulada = frec_esp_acumulada / N
        diferencia = abs(p_obs_acumulada - p_esp_acumulada)

        tabla.append({
            "intervalo": f"{limite_inicial}-{limite_final}",
            "frec_observada": frecuencias_observadas[i],
            "frec_obs_acumulada": frec_obs_acumulada,
            "p_obs_acumulada": round(p_obs_acumulada, 6),
            "frec_esp_acumulada": frec_esp_acumulada,
            "p_esp_acumulada": round(p_esp_acumulada, 6),
            "diferencia": round(diferencia, 6)
        })

    # DMAX: la diferencia más grande
    dmax = max(fila["diferencia"] for fila in tabla)

    # DMAXP: valor crítico (equivalente al de la tabla del docente)
    dmaxp = 1.36 / math.sqrt(N)

    # Verificar si la secuencia pasa la prueba
    aprueba = dmax < dmaxp

    return {
        "N": N,
        "k": k,
        "tabla": tabla,
        "dmax": round(dmax, 6),
        "dmaxp": round(dmaxp, 6),
        "aprueba": aprueba
    }


def grafico_prueba_ks(resultado):
    """
    Parámetros:
        resultado: diccionario retornado por prueba_ks()
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    intervalos = [fila["intervalo"] for fila in resultado["tabla"]]
    p_obs = [fila["p_obs_acumulada"] for fila in resultado["tabla"]]
    p_esp = [fila["p_esp_acumulada"] for fila in resultado["tabla"]]
    diferencias = [fila["diferencia"] for fila in resultado["tabla"]]

    ax.plot(intervalos, p_obs, marker="o", color="steelblue",
            linewidth=2, label="P. Acumulada Observada")
    ax.plot(intervalos, p_esp, marker="s", color="orange",
            linewidth=2, linestyle="--", label="P. Acumulada Esperada")

    indice_dmax = diferencias.index(max(diferencias))
    ax.annotate(f"DMAX = {resultado['dmax']}",
                xy=(intervalos[indice_dmax], p_obs[indice_dmax]),
                xytext=(indice_dmax + 0.5, p_obs[indice_dmax] - 0.1),
                arrowprops=dict(arrowstyle="->", color="red"),
                fontsize=10, color="red")

    ax.set_xticks(range(len(intervalos)))
    ax.set_xticklabels(intervalos, rotation=45, ha="right")
    ax.set_xlabel("Intervalos", fontsize=12)
    ax.set_ylabel("Proporción Acumulada", fontsize=12)
    ax.set_title("Prueba Kolmogorov-Smirnov: FEC Observada vs Esperada",
                 fontsize=14, fontweight="bold")
    ax.legend()

    ax.text(0.02, 0.95,
            f"DMAX = {resultado['dmax']}\nDMAXP = {resultado['dmaxp']}\nn = {resultado['N']}",
            transform=ax.transAxes, fontsize=10, verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    texto = "APRUEBA ✓" if resultado["aprueba"] else "FALLA ✗"
    color_texto = "green" if resultado["aprueba"] else "red"
    ax.text(0.98, 0.05, texto, transform=ax.transAxes,
            fontsize=14, color=color_texto, ha="right", fontweight="bold")

    plt.tight_layout()
    plt.savefig("grafico_prueba_ks.png", dpi=150)
    plt.show()
