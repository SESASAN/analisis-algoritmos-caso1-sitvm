
"""Regla simplificada que el SITVM aplica hoy para el tope tarifario.

Implementa la interpretación acordada por el equipo y documentada en el
README (§2.2, Regla actual).
"""

from estrategia import DIARIO, MENSUAL, PASAJE, SEMANAL


def costo_regla_actual(viajes_por_dia: list[int]) -> int:
    """Calcula lo que cobra hoy la regla simplificada del sistema.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo cobrado en pesos.
    """
    dias = len(viajes_por_dia)
    limite_mes = min(dias, 30)
    total = 0

    # Aplicar el tope semanal a los bloques fijos de los primeros 30 días.
    for inicio in range(0, limite_mes, 7):
        fin = min(inicio + 7, limite_mes)
        costo_bloque = 0

        for indice in range(inicio, fin):
            viajes = viajes_por_dia[indice]
            costo_dia = min(viajes * PASAJE, DIARIO)
            costo_bloque += costo_dia

        total += min(costo_bloque, SEMANAL)

    # Aplicar el tope mensual a los primeros 30 días.
    total = min(total, MENSUAL)

    # Los días posteriores al día 30 se cobran por separado.
    for indice in range(30, dias):
        viajes = viajes_por_dia[indice]
        total += min(viajes * PASAJE, DIARIO)

    return total
