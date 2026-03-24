"""
generador_congruencial.py
-------------------------
Adaptador del generador congruencial lineal mixto implementado por el equipo
en generators.py (Punto 3 del taller). Se reutiliza directamente la función
`congruence` para producir los números pseudoaleatorios que alimentan la
simulación de la caminata aleatoria.

Método: Congruencial Lineal Mixto
    Xᵢ₊₁ = (Xᵢ · a + c) mod m
    Donde a = 1 + 2k  y  m = 2^g

    Rᵢ = Xᵢ / (m - 1)   →  valor normalizado en [0, 1)
"""

import sys
import os

# ---------------------------------------------------------------------------
# Agregar la raíz del proyecto al path para importar generators.py
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from generators import congruence  # noqa: E402  (importación tras manipulación de path)


# ---------------------------------------------------------------------------
# Parámetros por defecto del generador congruencial
# Elegidos para maximizar el período: m = 2^32, a impar, c impar
# ---------------------------------------------------------------------------
DEFAULT_K = 1_664_525     # multiplier k  →  a = 1 + 2k = 3_329_051
DEFAULT_C = 1_013_904_223 # incremento c
DEFAULT_G = 32            # módulo m = 2^32


class GeneradorCongruencial:
    """
    Envuelve el generador congruencial del proyecto y provee un iterador
    de números pseudoaleatorios en [0, 1) listo para usar en la simulación.

    Atributos
    ----------
    semilla : int
        Valor semilla inicial X₀.
    k : int
        Parámetro del multiplicador (a = 1 + 2k).
    c : int
        Incremento constante.
    g : int
        Exponente del módulo (m = 2^g).
    """

    def __init__(self, semilla: int, k: int = DEFAULT_K,
                 c: int = DEFAULT_C, g: int = DEFAULT_G):
        """
        Inicializa el generador con una semilla y parámetros opcionales.

        Parámetros
        ----------
        semilla : int
            Semilla inicial X₀ para el generador.
        k : int, opcional
            Parámetro del multiplicador. Por defecto usa valor de período máximo.
        c : int, opcional
            Incremento. Por defecto usa valor de período máximo.
        g : int, opcional
            Exponente del módulo m = 2^g. Por defecto 32.
        """
        self.semilla = semilla
        self.k = k
        self.c = c
        self.g = g

    def generar(self, cantidad: int) -> list[float]:
        """
        Genera una lista de `cantidad` números pseudoaleatorios en [0, 1).

        Parámetros
        ----------
        cantidad : int
            Número de valores a generar.

        Retorna
        -------
        list[float]
            Lista de floats en [0, 1).
        """
        return congruence(self.semilla, self.k, self.c, self.g, cantidad)

    def generar_pasos(self, cantidad: int, dimensiones: int = 1) -> list[int]:
        """
        Transforma números pseudoaleatorios en pasos de caminata aleatoria.

        Para cada dimensión se genera un número Rᵢ en [0, 1):
          - Rᵢ < 0.5  →  paso = -1  (retroceso)
          - Rᵢ ≥ 0.5  →  paso = +1  (avance)

        Parámetros
        ----------
        cantidad : int
            Número de pasos a generar.
        dimensiones : int
            Número de dimensiones del espacio (1, 2 o 3).

        Retorna
        -------
        list[list[int]]
            Lista de `cantidad` vectores de paso, cada uno con `dimensiones` componentes.
        """
        total_ri = cantidad * dimensiones
        ri_values = congruence(self.semilla, self.k, self.c, self.g, total_ri)

        pasos = []
        idx = 0
        for _ in range(cantidad):
            vector = []
            for _ in range(dimensiones):
                vector.append(1 if ri_values[idx] >= 0.5 else -1)
                idx += 1
            pasos.append(vector)

        return pasos
