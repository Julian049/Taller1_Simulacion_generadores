"""
simulacion_caminata.py
-----------------------
Módulo principal de simulación de caminatas aleatorias simétricas en 1D, 2D y 3D.

La caminata aleatoria (random walk) modela el movimiento de la rana estadística:
desde el origen, en cada paso la rana se desplaza ±1 en cada eje con probabilidad
p = 0.5, utilizando el generador congruencial lineal mixto del proyecto.

Estructura de datos principal
------------------------------
ResultadoSimulacion (dict):
    {
        "posiciones_finales": list[tuple],   # posición final de cada simulación
        "retornos_origen":    list[bool],    # True si la rana volvió al origen
        "tiempos":            list[float],   # tiempo de ejecución por simulación (s)
        "dimensiones":        int,           # 1, 2 o 3
        "n_pasos":            int,           # pasos por simulación
        "n_simulaciones":     int,           # total de simulaciones ejecutadas
    }
"""

import time
from generador_congruencial import GeneradorCongruencial


# ---------------------------------------------------------------------------
# Funciones de simulación por dimensión
# ---------------------------------------------------------------------------

def simular_1d(semilla_base: int, n_pasos: int,
               n_simulaciones: int, pasos_retorno: int = 1000) -> dict:
    """
    Ejecuta múltiples simulaciones de caminata aleatoria en una dimensión.

    En cada simulación se genera una secuencia de n_pasos valores pseudoaleatorios
    con el generador congruencial; cada valor determina si la rana avanza (+1) o
    retrocede (-1). Se registra la posición final y si la rana pasó por el origen
    en los primeros `pasos_retorno` pasos.

    Parámetros
    ----------
    semilla_base : int
        Semilla inicial. Cada simulación usa semilla_base + i para garantizar
        independencia entre simulaciones.
    n_pasos : int
        Número de pasos por simulación.
    n_simulaciones : int
        Cantidad de simulaciones independientes a ejecutar.
    pasos_retorno : int
        Número de pasos iniciales en los que se detecta retorno al origen.

    Retorna
    -------
    dict
        ResultadoSimulacion con claves: posiciones_finales, retornos_origen,
        tiempos, dimensiones, n_pasos, n_simulaciones.
    """
    posiciones_finales = []
    retornos_origen = []
    tiempos = []

    for i in range(n_simulaciones):
        t_inicio = time.perf_counter()

        # Semilla diferente por simulación para garantizar independencia
        semilla = semilla_base + i * 1_000_003  # prima para dispersar semillas
        gen = GeneradorCongruencial(semilla)
        ri_values = gen.generar(n_pasos)

        posicion = 0
        retorno = False

        for j, ri in enumerate(ri_values):
            posicion += 1 if ri >= 0.5 else -1

            # Detectar retorno al origen en los primeros pasos_retorno pasos
            if j < pasos_retorno and posicion == 0:
                retorno = True

        posiciones_finales.append((posicion,))  # tupla para uniformidad entre dims
        retornos_origen.append(retorno)
        tiempos.append(time.perf_counter() - t_inicio)

    return {
        "posiciones_finales": posiciones_finales,
        "retornos_origen":    retornos_origen,
        "tiempos":            tiempos,
        "dimensiones":        1,
        "n_pasos":            n_pasos,
        "n_simulaciones":     n_simulaciones,
    }


def simular_2d(semilla_base: int, n_pasos: int,
               n_simulaciones: int, pasos_retorno: int = 1000) -> dict:
    """
    Ejecuta múltiples simulaciones de caminata aleatoria en dos dimensiones.

    En cada paso la rana se desplaza ±1 en el eje X y ±1 en el eje Y de forma
    independiente. Se requieren 2 números pseudoaleatorios por paso.

    Parámetros
    ----------
    semilla_base : int
        Semilla base; cada simulación usa semilla_base + i * 1_000_003.
    n_pasos : int
        Número de pasos por simulación.
    n_simulaciones : int
        Cantidad de simulaciones independientes.
    pasos_retorno : int
        Pasos iniciales en los que se evalúa retorno al origen.

    Retorna
    -------
    dict
        ResultadoSimulacion con posiciones finales como tuplas (x, y).
    """
    posiciones_finales = []
    retornos_origen = []
    tiempos = []

    for i in range(n_simulaciones):
        t_inicio = time.perf_counter()

        semilla = semilla_base + i * 1_000_003
        gen = GeneradorCongruencial(semilla)
        # 2 valores por paso: primero para X, segundo para Y
        ri_values = gen.generar(n_pasos * 2)

        x, y = 0, 0
        retorno = False

        for j in range(n_pasos):
            x += 1 if ri_values[j * 2]     >= 0.5 else -1
            y += 1 if ri_values[j * 2 + 1] >= 0.5 else -1

            if j < pasos_retorno and x == 0 and y == 0:
                retorno = True

        posiciones_finales.append((x, y))
        retornos_origen.append(retorno)
        tiempos.append(time.perf_counter() - t_inicio)

    return {
        "posiciones_finales": posiciones_finales,
        "retornos_origen":    retornos_origen,
        "tiempos":            tiempos,
        "dimensiones":        2,
        "n_pasos":            n_pasos,
        "n_simulaciones":     n_simulaciones,
    }


def simular_3d(semilla_base: int, n_pasos: int,
               n_simulaciones: int, pasos_retorno: int = 1000) -> dict:
    """
    Ejecuta múltiples simulaciones de caminata aleatoria en tres dimensiones.

    En cada paso la rana se desplaza ±1 en los ejes X, Y y Z de forma independiente.
    Se requieren 3 números pseudoaleatorios por paso.

    Parámetros
    ----------
    semilla_base : int
        Semilla base; cada simulación usa semilla_base + i * 1_000_003.
    n_pasos : int
        Número de pasos por simulación.
    n_simulaciones : int
        Cantidad de simulaciones independientes.
    pasos_retorno : int
        Pasos iniciales en los que se evalúa retorno al origen.

    Retorna
    -------
    dict
        ResultadoSimulacion con posiciones finales como tuplas (x, y, z).
    """
    posiciones_finales = []
    retornos_origen = []
    tiempos = []

    for i in range(n_simulaciones):
        t_inicio = time.perf_counter()

        semilla = semilla_base + i * 1_000_003
        gen = GeneradorCongruencial(semilla)
        ri_values = gen.generar(n_pasos * 3)

        x, y, z = 0, 0, 0
        retorno = False

        for j in range(n_pasos):
            x += 1 if ri_values[j * 3]     >= 0.5 else -1
            y += 1 if ri_values[j * 3 + 1] >= 0.5 else -1
            z += 1 if ri_values[j * 3 + 2] >= 0.5 else -1

            if j < pasos_retorno and x == 0 and y == 0 and z == 0:
                retorno = True

        posiciones_finales.append((x, y, z))
        retornos_origen.append(retorno)
        tiempos.append(time.perf_counter() - t_inicio)

    return {
        "posiciones_finales": posiciones_finales,
        "retornos_origen":    retornos_origen,
        "tiempos":            tiempos,
        "dimensiones":        3,
        "n_pasos":            n_pasos,
        "n_simulaciones":     n_simulaciones,
    }


# ---------------------------------------------------------------------------
# Función de análisis estadístico
# ---------------------------------------------------------------------------

def analizar_resultado(resultado: dict) -> dict:
    """
    Calcula estadísticas descriptivas sobre los resultados de simulación.

    Computa media, varianza, desviación estándar y probabilidad de retorno
    al origen para el conjunto de simulaciones ejecutadas.

    Parámetros
    ----------
    resultado : dict
        Diccionario ResultadoSimulacion generado por simular_Xd().

    Retorna
    -------
    dict
        Diccionario con las siguientes claves:
        - "prob_retorno"   : float, fracción de simulaciones con retorno al origen
        - "media_distancia": float, distancia euclidiana media al origen
        - "desv_distancia" : float, desviación estándar de la distancia al origen
        - "tiempo_total"   : float, tiempo total de ejecución en segundos
        - "tiempo_medio"   : float, tiempo promedio por simulación
        - "coords_medias"  : tuple, valor medio de cada coordenada
    """
    posiciones = resultado["posiciones_finales"]
    retornos   = resultado["retornos_origen"]
    tiempos    = resultado["tiempos"]
    dims       = resultado["dimensiones"]
    n          = resultado["n_simulaciones"]

    # Distancia euclidiana al origen para cada simulación
    distancias = [sum(c ** 2 for c in pos) ** 0.5 for pos in posiciones]

    media_dist = sum(distancias) / n
    var_dist   = sum((d - media_dist) ** 2 for d in distancias) / n
    desv_dist  = var_dist ** 0.5

    prob_retorno = sum(retornos) / n

    t_total = sum(tiempos)
    t_medio = t_total / n

    # Media de cada coordenada por separado
    coords_medias = tuple(
        sum(pos[d] for pos in posiciones) / n for d in range(dims)
    )

    return {
        "prob_retorno":    prob_retorno,
        "media_distancia": media_dist,
        "desv_distancia":  desv_dist,
        "tiempo_total":    t_total,
        "tiempo_medio":    t_medio,
        "coords_medias":   coords_medias,
    }
