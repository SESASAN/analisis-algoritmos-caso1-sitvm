"""Generador de meses sintéticos con semilla fija para pruebas y mediciones."""

import random

# Probabilidad de que la tarjeta viaje un día cualquiera.
PROBABILIDAD_VIAJE: float = 0.9

# Máximo de viajes de una tarjeta en un día con viajes.
MAX_VIAJES_DIA: int = 4


def generar_mes(
    dias: int,
    rng: random.Random,
    probabilidad_viaje: float = PROBABILIDAD_VIAJE,
    max_viajes: int = MAX_VIAJES_DIA,
) -> list[int]:
    """Genera los viajes por día de una tarjeta durante un periodo.

    Args:
        dias: número de días del periodo.
        rng: generador con semilla fija.
        probabilidad_viaje: probabilidad de que un día tenga viajes.
        max_viajes: máximo de viajes en un día con viajes.

    Returns:
        Una lista de largo "dias" con los viajes de cada día.
    """
    viajes_por_dia: list[int] = []
    for _ in range(dias):
        if rng.random() < probabilidad_viaje:
            viajes_por_dia.append(rng.randint(1, max_viajes))
        else:
            viajes_por_dia.append(0)
    return viajes_por_dia


def generar_mes_disperso(
    dias: int,
    dias_con_viaje: int,
    rng: random.Random,
    max_viajes: int = MAX_VIAJES_DIA,
) -> list[int]:
    """Genera un periodo con un número exacto de días con viajes.

    Args:
        dias: número de días del periodo.
        dias_con_viaje: cuántos de esos días tienen viajes.
        rng: generador con semilla fija.
        max_viajes: máximo de viajes en un día con viajes.

    Returns:
        Una lista de largo "dias" con "dias_con_viaje" días distintos de 0.
    """
    viajes_por_dia = [0] * dias
    elegidos = rng.sample(range(dias), dias_con_viaje)
    for indice in elegidos:
        viajes_por_dia[indice] = rng.randint(1, max_viajes)
    return viajes_por_dia


def generar_instancias(
    dias: int,
    cantidad: int,
    semilla: int,
    probabilidad_viaje: float = PROBABILIDAD_VIAJE,
    max_viajes: int = MAX_VIAJES_DIA,
) -> list[list[int]]:
    """Genera varias tarjetas del mismo tamaño con una semilla fija.

    Args:
        dias: número de días de cada periodo.
        cantidad: cuántas tarjetas generar.
        semilla: semilla del generador, para reproducir la medición.
        probabilidad_viaje: probabilidad de que un día tenga viajes.
        max_viajes: máximo de viajes en un día con viajes.

    Returns:
        Una lista con "cantidad" tarjetas de largo "dias".
    """
    rng = random.Random(semilla)
    instancias: list[list[int]] = []
    for _ in range(cantidad):
        instancias.append(
            generar_mes(dias, rng, probabilidad_viaje, max_viajes)
        )
    return instancias