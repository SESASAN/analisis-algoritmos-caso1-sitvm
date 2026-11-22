"""Generador de series de saldos netos con semilla fija para las mediciones."""

import random

# Rango del saldo neto de un intervalo de 5 minutos, en pasajeros.
SALDO_MINIMO: int = -60
SALDO_MAXIMO: int = 60


def generar_serie(
    n: int,
    rng: random.Random,
    minimo: int = SALDO_MINIMO,
    maximo: int = SALDO_MAXIMO,
) -> list[int]:
    """Genera la serie de saldos netos de una estación.

    Args:
        n: número de intervalos de la serie.
        rng: generador con semilla fija.
        minimo: menor saldo posible de un intervalo.
        maximo: mayor saldo posible de un intervalo.

    Returns:
        Una lista de largo `n` con saldos entre `minimo` y `maximo`.
    """
    saldos: list[int] = []
    for _ in range(n):
        saldos.append(rng.randint(minimo, maximo))
    return saldos


def generar_series(
    n: int,
    cantidad: int,
    semilla: int,
    minimo: int = SALDO_MINIMO,
    maximo: int = SALDO_MAXIMO,
) -> list[list[int]]:
    """Genera varias series del mismo tamaño con una semilla fija.

    Args:
        n: número de intervalos de cada serie.
        cantidad: cuántas series generar.
        semilla: semilla del generador, para reproducir la medición.
        minimo: menor saldo posible de un intervalo.
        maximo: mayor saldo posible de un intervalo.

    Returns:
        Una lista con `cantidad` series de largo `n`.
    """
    rng = random.Random(semilla)
    series: list[list[int]] = []
    for _ in range(cantidad):
        series.append(generar_serie(n, rng, minimo, maximo))
    return series