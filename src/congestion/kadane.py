"""Tramo de mayor congestión de una estación con el algoritmo de Kadane.

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


def tramo_maximo_kadane_contando(saldos: list[int]) -> tuple[Tramo, int]:
    """Calcula el tramo de mayor congestión y cuenta las operaciones.

    Operación elemental: cada intervalo recorrido, una suma por intervalo.

    Args:
        saldos: saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        El tramo (inicio, fin, suma) de mayor suma y el número de
        intervalos sumados.

    Raises:
        ValueError: si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie de saldos no puede estar vacía")

    mejor_inicio = 0
    mejor_fin = 0
    mejor_suma = saldos[0]
    inicio_actual = 0
    suma_actual = 0
    operaciones = 0

    for i in range(len(saldos)):
        if suma_actual <= 0:
            suma_actual = saldos[i]
            inicio_actual = i
        else:
            suma_actual += saldos[i]
        operaciones += 1

        if suma_actual > mejor_suma:
            mejor_suma = suma_actual
            mejor_inicio = inicio_actual
            mejor_fin = i

    tramo = (mejor_inicio, mejor_fin, mejor_suma)
    return tramo, operaciones


def tramo_maximo_kadane(saldos: list[int]) -> Tramo:
    """Calcula el tramo de mayor congestión con el algoritmo de Kadane.

    Args:
        saldos: saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        El tramo (inicio, fin, suma) de mayor suma, con índices desde 0 e
        inclusivos.

    Raises:
        ValueError: si la serie está vacía.
    """
    tramo, _ = tramo_maximo_kadane_contando(saldos)
    return tramo