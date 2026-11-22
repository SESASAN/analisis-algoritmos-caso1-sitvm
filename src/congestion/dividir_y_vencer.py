"""Tramo de mayor congestión de una estación por dividir y vencer.

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


def _tramo_cruzado(
    saldos: list[int], bajo: int, medio: int, alto: int, contador: list[int]
) -> Tramo:
    """Busca el mejor tramo que cruza el punto medio.

    Crece hacia la izquierda desde medio y hacia la derecha desde medio + 1,
    y une las dos mejores mitades.

    Args:
        saldos: Saldos netos por intervalo. No se modifica.
        bajo: Primer índice del rango.
        medio: Último índice de la mitad izquierda.
        alto: Último índice del rango.
        contador: Lista de un elemento que acumula las operaciones.

    Returns:
        El mejor tramo (inicio, fin, suma) que incluye medio y medio + 1.
    """
    mejor_izq = saldos[medio]
    inicio = medio
    suma = 0
    for i in range(medio, bajo - 1, -1):
        suma += saldos[i]
        if suma > mejor_izq:
            mejor_izq, inicio = suma, i
    mejor_der = saldos[medio + 1]
    fin = medio + 1
    suma = 0
    for j in range(medio + 1, alto + 1):
        suma += saldos[j]
        if suma > mejor_der:
            mejor_der, fin = suma, j
    contador[0] += alto - bajo + 1  # cada intervalo del rango se suma una vez
    return inicio, fin, mejor_izq + mejor_der


def _tramo_maximo(
    saldos: list[int], bajo: int, alto: int, contador: list[int]
) -> Tramo:
    """Resuelve el rango [bajo, alto] dividiéndolo en dos mitades.

    Args:
        saldos: Saldos netos por intervalo. No se modifica.
        bajo: Primer índice del rango.
        alto: Último índice del rango.
        contador: Lista de un elemento que acumula las operaciones.

    Returns:
        El mejor tramo (inicio, fin, suma) dentro del rango.
    """
    if bajo == alto:  # caso base: un solo intervalo
        contador[0] += 1
        return bajo, alto, saldos[bajo]
    medio = (bajo + alto) // 2
    izquierdo = _tramo_maximo(saldos, bajo, medio, contador)
    derecho = _tramo_maximo(saldos, medio + 1, alto, contador)
    cruzado = _tramo_cruzado(saldos, bajo, medio, alto, contador)
    return max(izquierdo, derecho, cruzado, key=lambda tramo: tramo[2])


def tramo_maximo_dyv_contando(saldos: list[int]) -> tuple[Tramo, int]:
    """Calcula el tramo de mayor congestión y cuenta las operaciones.

    Operación elemental: cada intervalo sumado. Un caso base suma su único
    intervalo y cada cruce suma una vez todos los intervalos de su rango,
    así que el total es del orden de n log n.

    Args:
        saldos: Saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        Una tupla (tramo, operaciones): el tramo (inicio, fin, suma) de mayor
        suma y el número de intervalos sumados.

    Raises:
        ValueError: Si la serie está vacía.
    """
    if not saldos:
        raise ValueError("la serie de saldos no puede estar vacía")
    contador = [0]
    tramo = _tramo_maximo(saldos, 0, len(saldos) - 1, contador)
    return tramo, contador[0]


def tramo_maximo_dyv(saldos: list[int]) -> Tramo:
    """Calcula el tramo de mayor congestión por dividir y vencer.

    Args:
        saldos: Saldos netos por intervalo; no puede estar vacía. No se
            modifica.

    Returns:
        El tramo (inicio, fin, suma) de mayor suma, con índices desde 0 e
        inclusivos.

    Raises:
        ValueError: Si la serie está vacía.
    """
    tramo, _ = tramo_maximo_dyv_contando(saldos)
    return tramo
