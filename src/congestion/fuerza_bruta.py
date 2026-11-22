"""Tramo de mayor congestión de una estación por fuerza bruta.

Cada posición de la serie es el saldo neto de la plataforma en un intervalo
de 5 minutos: pasajeros que entraron menos pasajeros evacuados. Puede ser
negativo. Se busca el tramo de intervalos consecutivos con la mayor suma.

Contrato común de las estrategias de esta operación: se devuelve una tupla
(inicio, fin, suma) con índices desde 0 e inclusivos, de modo que
suma == sum(saldos[inicio:fin + 1]). Si todos los saldos son negativos, el
tramo es el intervalo menos negativo. Ante empates, cualquier tramo con la
suma máxima es válido.
"""

Tramo = tuple[int, int, int]  # (inicio, fin, suma)


def tramo_maximo_fuerza_bruta_contando(
    saldos: list[int],
) -> tuple[Tramo, int]:
    """Calcula el tramo de mayor suma mediante fuerza bruta.

    Operación elemental: cada intervalo sumado. Se cuenta una operación
    cada vez que se incorpora un saldo a la suma de un tramo.

    Args:
        saldos: Saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        Una tupla (tramo, operaciones): el tramo (inicio, fin, suma) de
        mayor suma y el número de intervalos sumados.

    Raises:
        ValueError: Si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie de saldos no puede estar vacía")

    mejor_suma = saldos[0]
    mejor_inicio = 0
    mejor_fin = 0
    operaciones = 0

    for inicio in range(len(saldos)):
        suma_actual = 0

        for fin in range(inicio, len(saldos)):
            suma_actual += saldos[fin]
            operaciones += 1

            if suma_actual > mejor_suma:
                mejor_suma = suma_actual
                mejor_inicio = inicio
                mejor_fin = fin

    tramo = (mejor_inicio, mejor_fin, mejor_suma)
    return tramo, operaciones


def tramo_maximo_fuerza_bruta(saldos: list[int]) -> Tramo:
    """Calcula el tramo de mayor congestión por fuerza bruta.

    Args:
        saldos: Saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        El tramo (inicio, fin, suma) de mayor suma, con índices desde 0 e
        inclusivos.

    Raises:
        ValueError: Si la serie está vacía.
    """
    tramo, _ = tramo_maximo_fuerza_bruta_contando(saldos)
    return tramo
