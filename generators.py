def mid_square(seed, number_ri):
    list_ri = []
    seed_size = len(str(seed))

    if seed_size < 3:
        raise Exception("La semilla debe contener al menos un numero de 3 cifras")

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
    list_ri = []

    a = 1 + 2 * k
    m = 2 ** g

    xi = ((xo * a) + c) % m
    ri = xi / (m - 1)
    list_ri.append(ri)

    for n in range(number_ri - 1):
        xi = ((xi * a) + c) % m
        ri = xi / (m - 1)
        list_ri.append(ri)

    return list_ri


def congruence_additive(xo, c, g, number_ri):
    return congruence(xo, 0, c, g, number_ri)


def congruence_multiplicative(xo, k, g, number_ri):
    return congruence(xo, k, 0, g, number_ri)


# Distribuciones uniforme y normal

def general_uniform(list_ri, range_min, range_max):
    list_ni = []
    for ri in list_ri:
        ni = range_min + (range_max - range_min) * ri
        list_ni.append(ni)

    return list_ni


def uniform_distribution_congruence(xo, k, c, g, range_min, range_max, number_ni):
    list_ri = congruence(xo, k, c, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_distribution_multiplicative(xo, k, g, range_min, range_max, number_ni):
    list_ri = congruence_multiplicative(xo, k, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_distribution_additive(xo, c, g, range_min, range_max, number_ni):
    list_ri = congruence_additive(xo, c, g, number_ni)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


def uniform_mid_square(seed, range_min, range_max, number_ri):
    list_ri = mid_square(seed, number_ri)
    list_ni = general_uniform(list_ri, range_min, range_max)

    return list_ni


if __name__ == '__main__':
    list = uniform_distribution_congruence(7, 100, 21, 12, 4, 100, 20)
    for ni in list:
        print(ni)
