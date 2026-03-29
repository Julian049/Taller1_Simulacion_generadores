import math
import sys

def mid_square(seed, number_ri):
    """
    Genera números pseudoaleatorios usando el método de cuadrados medios.

    Args:
        seed (int): Semilla inicial (debe tener al menos 3 cifras).
        number_ri (int): Cantidad de números aleatorios a generar.

    Returns:
        list[float]: Lista de números pseudoaleatorios entre 0 y 1.

    Raises:
        Exception: Si la semilla tiene menos de 3 cifras.
    """
    list_ri = []
    seed_size = len(str(seed))

    if seed_size < 3:
        raise Exception("La semilla debe contener al menos un número de 3 cifras.")

    xi = seed ** 2
    extraction = extract_center(xi, seed_size)
    ri = extraction / (10 ** seed_size)
    list_ri.append(ri)

    for current_ri in range(number_ri - 1):
        xi = extraction ** 2
        extraction = extract_center(xi, seed_size)
        ri = extraction / (10 ** seed_size)
        list_ri.append(ri)

    return list_ri


def extract_center(number, size):
    """
    Extrae los dígitos centrales de un número dado un tamaño de ventana.

    Args:
        number (int): Número del cual se extraen los dígitos centrales.
        size (int): Tamaño de la semilla original, determina cuántos dígitos extraer.

    Returns:
        int: El número entero formado por los dígitos centrales.
    """
    new_number = ""
    if len(str(number)) < size * 2:
        difference = (size * 2) - len(str(number))
        new_number = ("0" * difference) + str(number)
    else:
        new_number = str(number)

    begin = size // 2
    end = begin + size
    middle_number = new_number[begin:end]
    return int(middle_number)


def congruence(xo, k, c, g, number_ri):
    """
    Genera números pseudoaleatorios usando el método de congruencia lineal mixta.

    La fórmula empleada es: x_(i+1) = (x_i * a + c) mod m
    donde a = 1 + 2k  y  m = 2^g.

    Args:
        xo (int): Valor semilla inicial. Debe estar en el rango [0, m].
        k (int): Parámetro para calcular el multiplicador a = 1 + 2k.
        c (int): Incremento (constante aditiva). Debe estar en el rango (0, m].
        g (int): Exponente para calcular el módulo m = 2^g. Debe ser mayor que 0.
        number_ri (int): Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[float]: Lista de números pseudoaleatorios entre 0 y 1.

    Raises:
        Exception: Si xo está fuera del rango [0, m].
        Exception: Si el multiplicador a está fuera del rango (1, m].
        Exception: Si el incremento c está fuera del rango (0, m].
        Exception: Si el módulo m es menor o igual a 0.
    """
    list_ri = []

    a = 1 + 2 * k
    m = 2 ** g

    if xo < 0 or xo > m:
        raise Exception(f"El valor semilla xo={xo} debe estar en el rango [0, {m}].")

    if a < 1 or a > m:
        raise Exception(f"El multiplicador a={a} debe estar en el rango (1, {m}].")

    if c < 0 or c > m:
        raise Exception(f"El incremento c={c} debe estar en el rango (0, {m}].")

    if m <= 0:
        raise Exception(f"El módulo m={m} debe ser mayor que 0. Verifique que g sea un entero positivo.")

    xi = ((xo * a) + c) % m
    ri = xi / (m - 1)
    list_ri.append(ri)

    for n in range(number_ri - 1):
        xi = ((xi * a) + c) % m
        ri = xi / (m - 1)
        list_ri.append(ri)

    return list_ri


def congruence_additive(xo, c, g, number_ri):
    """
    Genera números pseudoaleatorios usando congruencia aditiva (multiplicador = 1).

    Es un caso especial de congruencia lineal donde k=0, por lo que a = 1 + 2(0) = 1.
    La fórmula simplificada es: x_(i+1) = (x_i + c) mod m.

    Args:
        xo (int): Valor semilla inicial.
        c (int): Incremento constante. Debe estar en el rango (0, m].
        g (int): Exponente para calcular el módulo m = 2^g.
        number_ri (int): Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[float]: Lista de números pseudoaleatorios entre 0 y 1.
    """
    return congruence(xo, 0, c, g, number_ri)


def congruence_multiplicative(xo, k, g, number_ri):
    """
    Genera números pseudoaleatorios usando congruencia multiplicativa (sin incremento).

    Es un caso especial de congruencia lineal donde c=0.
    La fórmula simplificada es: x_(i+1) = (x_i * a) mod m.

    Args:
        xo (int): Valor semilla inicial.
        k (int): Parámetro para calcular el multiplicador a = 1 + 2k.
        g (int): Exponente para calcular el módulo m = 2^g.
        number_ri (int): Cantidad de números pseudoaleatorios a generar.

    Returns:
        list[float]: Lista de números pseudoaleatorios entre 0 y 1.
    """
    return congruence(xo, k, 0, g, number_ri)


def general_uniform(list_ri, range_min, range_max):
    """
    Transforma una lista de números pseudoaleatorios en el rango [0, 1]
    a una distribución uniforme en el intervalo [range_min, range_max].

    Args:
        list_ri (list[float]): Lista de números pseudoaleatorios entre 0 y 1.
        range_min (float): Límite inferior del intervalo deseado.
        range_max (float): Límite superior del intervalo deseado.

    Returns:
        list[float]: Lista de valores transformados al intervalo [range_min, range_max].
    """
    if range_min > range_max:
        temp = range_max
        range_max = range_min
        range_min = temp

    list_ni = []
    for ri in list_ri:
        ni = range_min + (range_max - range_min) * ri
        list_ni.append(ni)

    return list_ni


def uniform_distribution_congruence(xo, k, c, g, range_min, range_max, number_ni):
    """
    Genera una distribución uniforme usando el método de congruencia lineal mixta.

    Args:
        xo (int): Valor semilla inicial.
        k (int): Parámetro para el multiplicador a = 1 + 2k.
        c (int): Incremento constante.
        g (int): Exponente para el módulo m = 2^g.
        range_min (float): Límite inferior del intervalo de la distribución.
        range_max (float): Límite superior del intervalo de la distribución.
        number_ni (int): Cantidad de valores a generar.

    Returns:
        list[float]: Lista de valores con distribución uniforme en [range_min, range_max].
    """
    list_ri = congruence(xo, k, c, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_distribution_multiplicative(xo, k, g, range_min, range_max, number_ni):
    """
    Genera una distribución uniforme usando el método de congruencia multiplicativa.

    Args:
        xo (int): Valor semilla inicial.
        k (int): Parámetro para el multiplicador a = 1 + 2k.
        g (int): Exponente para el módulo m = 2^g.
        range_min (float): Límite inferior del intervalo de la distribución.
        range_max (float): Límite superior del intervalo de la distribución.
        number_ni (int): Cantidad de valores a generar.

    Returns:
        list[float]: Lista de valores con distribución uniforme en [range_min, range_max].
    """
    list_ri = congruence_multiplicative(xo, k, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_distribution_additive(xo, c, g, range_min, range_max, number_ni):
    """
    Genera una distribución uniforme usando el método de congruencia aditiva.

    Args:
        xo (int): Valor semilla inicial.
        c (int): Incremento constante.
        g (int): Exponente para el módulo m = 2^g.
        range_min (float): Límite inferior del intervalo de la distribución.
        range_max (float): Límite superior del intervalo de la distribución.
        number_ni (int): Cantidad de valores a generar.

    Returns:
        list[float]: Lista de valores con distribución uniforme en [range_min, range_max].
    """
    list_ri = congruence_additive(xo, c, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_mid_square(seed, range_min, range_max, number_ri):
    """
    Genera una distribución uniforme usando el método de cuadrados medios.

    Args:
        seed (int): Semilla inicial (debe tener al menos 3 cifras).
        range_min (float): Límite inferior del intervalo de la distribución.
        range_max (float): Límite superior del intervalo de la distribución.
        number_ri (int): Cantidad de valores a generar.

    Returns:
        list[float]: Lista de valores con distribución uniforme en [range_min, range_max].
    """
    list_ri = mid_square(seed, number_ri)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def box_muller(list_ri):
    """
    Transforma una lista de números pseudoaleatorios uniformes en pares de valores
    con distribución normal estándar usando el método de Box-Muller.

    Aplica la transformación:
        z0 = sqrt(-2 * ln(r_i))   * cos(2π * r_{i+1})
        z1 = sqrt(-2 * ln(r_i))   * sin(2π * r_{i+1})

    Args:
        list_ri (list[float]): Lista de números pseudoaleatorios en el rango [0, 1].
                               Su longitud debe ser par.

    Returns:
        list[list[float]]: Lista de pares [z0, z1], cada uno con distribución
                           normal estándar N(0, 1).

    Raises:
        Exception: Si la longitud de list_ri no es par.
        Exception: Si algún valor de list_ri es negativo.
        Exception: Si algún valor de list_ri es mayor que 1.
    """
    if len(list_ri) % 2 != 0:
        raise Exception("El tamaño de la lista de valores debe ser par.")

    _EPSILON = sys.float_info.min

    sanitized = []
    for i, ri in enumerate(list_ri):
        if ri < 0:
            raise Exception(
                f"El valor list_ri[{i}]={ri} es negativo. "
                "Los Ri deben pertenecer al intervalo [0, 1]."
            )
        if ri > 1:
            raise Exception(
                f"El valor list_ri[{i}]={ri} debe estar en el intervalo [0, 1]. "
                "Los números pseudoaleatorios Ri deben pertenecer a ese rango."
            )
        sanitized.append(ri if ri > 0 else _EPSILON)

    box_muller_list = []
    for i in range(0, len(sanitized) - 1, 2):
        z0 = math.sqrt(-2 * math.log(sanitized[i])) * math.cos(2 * math.pi * sanitized[i + 1])
        z1 = math.sqrt(-2 * math.log(sanitized[i])) * math.sin(2 * math.pi * sanitized[i + 1])
        box_muller_list.append([z0, z1])
    return box_muller_list


def normal_distribution(list_ri, mean, std_dev):
    """
    Genera valores con distribución normal a partir de números pseudoaleatorios
    uniformes aplicando la transformación de Box-Muller.

    Para cada par [z0, z1] obtenido de Box-Muller, transforma cada zi mediante:
        ni = mean + zi * std_dev

    Args:
        list_ri (list[float]): Lista de números pseudoaleatorios en el rango (0, 1].
                               Su longitud debe ser par.
        mean (float): Media (μ) de la distribución normal deseada.
        std_dev (float): Desviación estándar (σ) de la distribución normal deseada.
                         Debe ser mayor que 0.

    Returns:
        list[float]: Lista de valores con distribución normal N(mean, std_dev²).

    Raises:
        Exception: Si std_dev es menor o igual a 0.
        Exception: Propaga las excepciones de box_muller si list_ri no es válida.
    """
    if std_dev <= 0:
        raise Exception(
            f"La desviación estándar std_dev={std_dev} debe ser mayor que 0."
        )

    list_zi = box_muller(list_ri)
    list_ni = []
    for pair in list_zi:
        for zi in pair:
            ni = mean + (zi * std_dev)
            list_ni.append(ni)
    return list_ni


def normal_distribution_congruence(xo, k, c, g, mean, std_dev, number_ni):
    """
    Genera valores con distribución normal usando el método de congruencia lineal
    mixta como generador de números pseudoaleatorios base.

    Args:
        xo (int): Valor semilla inicial. Debe estar en el rango [0, m].
        k (int): Parámetro para calcular el multiplicador a = 1 + 2k.
        c (int): Incremento (constante aditiva). Debe estar en el rango (0, m].
        g (int): Exponente para calcular el módulo m = 2^g. Debe ser mayor que 0.
        mean (float): Media (μ) de la distribución normal deseada.
        std_dev (float): Desviación estándar (σ) de la distribución normal deseada.
                         Debe ser mayor que 0.
        number_ni (int): Cantidad de valores a generar. Debe ser un número par.

    Returns:
        list[float]: Lista de valores con distribución normal N(mean, std_dev²).

    Raises:
        Exception: Propaga las excepciones de congruence si los parámetros no son válidos.
        Exception: Propaga las excepciones de normal_distribution si mean o std_dev
                   no son válidos, o si number_ni no es par.
    """
    list_ri = congruence(xo, k, c, g, number_ni)
    return normal_distribution(list_ri, mean, std_dev)


def normal_distribution_mid_square(seed, mean, std_dev, number_ni):
    """
    Genera valores con distribución normal usando el método de cuadrados medios
    como generador de números pseudoaleatorios base.

    Args:
        seed (int): Semilla inicial (debe tener al menos 3 cifras).
        mean (float): Media (μ) de la distribución normal deseada.
        std_dev (float): Desviación estándar (σ) de la distribución normal deseada.
                         Debe ser mayor que 0.
        number_ni (int): Cantidad de valores a generar. Debe ser un número par.

    Returns:
        list[float]: Lista de valores con distribución normal N(mean, std_dev²).

    Raises:
        Exception: Si la semilla tiene menos de 3 cifras.
        Exception: Propaga las excepciones de normal_distribution si mean o std_dev
                   no son válidos, o si number_ni no es par.
    """
    list_ri = mid_square(seed, number_ni)
    return normal_distribution(list_ri, mean, std_dev)
