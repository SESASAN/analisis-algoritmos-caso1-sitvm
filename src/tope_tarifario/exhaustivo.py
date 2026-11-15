"""Solución exhaustiva del tope tarifario, usada como juez de la DP.

Prueba todas las combinaciones de compras sin memoización ni tablas, por lo
que su costo es exponencial a propósito.
"""

from estrategia import DIARIO, MENSUAL, PASAJE, SEMANAL


def costo_exhaustivo(viajes_por_dia: list[int]) -> int:
    """Calcula el mismo costo probando todas las combinaciones de productos.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo mínimo en pesos.
    """
    costo, _ = costo_exhaustivo_contando(viajes_por_dia)
    return costo


def costo_exhaustivo_contando(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Calcula el costo exhaustivo y cuántas combinaciones exploró.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.

    Returns:
        El costo mínimo en pesos y el número de llamadas a explorar.
    """
    dias = len(viajes_por_dia)
    llamadas = [0]

    def explorar(dia: int) -> int:
        """Prueba todas las compras posibles desde el día indicado.

        Args:
            dia: índice del primer día que todavía falta por cubrir.

        Returns:
            El menor costo posible desde ese día hasta el final.
        """
        llamadas[0] += 1
        if dia >= dias:
            return 0

        viajes = viajes_por_dia[dia]

        if viajes == 0:
            return explorar(dia + 1)

        # Alternativa 1: pagar todos los viajes con pasajes sencillos.
        costo_pasajes = viajes * PASAJE + explorar(dia + 1)

        # Alternativa 2: comprar un pase diario.
        costo_diario = DIARIO + explorar(dia + 1)

        # Alternativa 3: comprar un pase semanal.
        costo_semanal = SEMANAL + explorar(min(dia + 7, dias))

        # Alternativa 4: comprar un pase mensual.
        costo_mensual = MENSUAL + explorar(min(dia + 30, dias))

        return min(
            costo_pasajes,
            costo_diario,
            costo_semanal,
            costo_mensual,
        )

    costo = explorar(0)
    return costo, llamadas[0]