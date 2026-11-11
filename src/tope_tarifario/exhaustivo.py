"""Solución exhaustiva del tope tarifario, usada como juez de la DP.

Prueba todas las combinaciones de compras sin memoización ni tablas, por lo
que su costo es exponencial a propósito.
"""


def costo_exhaustivo(viajes_por_dia: list[int]) -> int:
    """Calcula el mismo costo probando todas las combinaciones de productos.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo mínimo en pesos.
    """
    # TODO: solo para instancias pequeñas; su costo es exponencial.
    raise NotImplementedError("Pendiente de implementar")
