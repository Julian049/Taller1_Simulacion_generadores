"""
## 5. Prueba de Póker
Verifica la independencia de los números pseudoaleatorios analizando
los patrones formados por sus 5 dígitos decimales significativos,
comparando las frecuencias observadas de cada categoría contra
las frecuencias esperadas teóricas mediante un estadístico Chi-cuadrado.
"""

import matplotlib.pyplot as plt
from scipy.stats import chi2


def prueba_poker(secuencia, nivel_confianza=0.95):
    """
    Parámetros:
        secuencia: lista de números pseudoaleatorios entre 0 y 1
        nivel_confianza: nivel de confianza para la prueba (default 95%)
    Retorna:
        resultado: diccionario con todos los valores calculados
    """
    # Número de elementos en la secuencia
    N = len(secuencia)

    # Probabilidades teóricas de cada categoría (según docente)
    categorias = {
        "D - Todos diferentes": 0.3024,
        "O - Un par":           0.5040,
        "T - Dos Pares":        0.1080,
        "K - Tercia":           0.0720,
        "F - Full House":       0.0090,
        "P - Poker":            0.0045,
        "Q - Quintilla":        0.0001
    }

    # Frecuencias observadas inicializadas en 0
    frecuencias_observadas = {cat: 0 for cat in categorias}

    # Clasificar cada número según sus 5 dígitos significativos
    for numero in secuencia:
        digitos = str(int(round(numero * 100000))).zfill(5)[:5]
        conteo = {}
        for d in digitos:
            conteo[d] = conteo.get(d, 0) + 1
        frecuencias = sorted(conteo.values(), reverse=True)

        if frecuencias[0] == 5:
            frecuencias_observadas["Q - Quintilla"] += 1
        elif frecuencias[0] == 4:
            frecuencias_observadas["P - Poker"] += 1
        elif frecuencias[0] == 3 and frecuencias[1] == 2:
            frecuencias_observadas["F - Full House"] += 1
        elif frecuencias[0] == 3:
            frecuencias_observadas["K - Tercia"] += 1
        elif frecuencias[0] == 2 and len(frecuencias) > 1 and frecuencias[1] == 2:
            frecuencias_observadas["T - Dos Pares"] += 1
        elif frecuencias[0] == 2:
            frecuencias_observadas["O - Un par"] += 1
        else:
            frecuencias_observadas["D - Todos diferentes"] += 1

    # Calcular frecuencias esperadas y estadístico chi-cuadrado
    tabla = []
    chi2_calculado = 0

    for cat, prob in categorias.items():
        obs = frecuencias_observadas[cat]
        esp = N * prob
        contribucion = (obs - esp) ** 2 / esp
        chi2_calculado += contribucion
        tabla.append({
            "categoria": cat,
            "frecuencia_observada": obs,
            "probabilidad": prob,
            "frecuencia_esperada": round(esp, 4),
            "contribucion_chi2": round(contribucion, 6)
        })

    # Valor crítico chi-cuadrado para 6 grados de libertad
    chi2_critico = chi2.ppf(nivel_confianza, 6)

    # Verificar si la secuencia pasa la prueba
    aprueba = chi2_calculado < chi2_critico

    return {
        "N": N,
        "tabla": tabla,
        "chi2_calculado": round(chi2_calculado, 6),
        "chi2_critico": round(chi2_critico, 6),
        "grados_libertad": 6,
        "aprueba": aprueba
    }


def grafico_prueba_poker(resultado):
    """
    Parámetros:
        resultado: diccionario retornado por prueba_poker()
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    categorias = [fila["categoria"] for fila in resultado["tabla"]]
    frec_obs = [fila["frecuencia_observada"] for fila in resultado["tabla"]]
    frec_esp = [fila["frecuencia_esperada"] for fila in resultado["tabla"]]

    x = range(len(categorias))
    ancho = 0.35

    barras_obs = ax.bar([i - ancho/2 for i in x], frec_obs,
                        ancho, label="Frecuencia observada", color="steelblue")
    barras_esp = ax.bar([i + ancho/2 for i in x], frec_esp,
                        ancho, label="Frecuencia esperada", color="orange", alpha=0.7)

    for barra in barras_obs:
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.5,
                str(int(barra.get_height())), ha="center", va="bottom", fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(categorias, rotation=45, ha="right")
    ax.set_xlabel("Categorías", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title("Prueba de Póker: Frecuencias Observadas vs Esperadas",
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
    plt.savefig("grafico_prueba_poker.png", dpi=150)
    plt.show()
