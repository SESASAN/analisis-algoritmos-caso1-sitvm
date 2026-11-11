"""Estrategia de programación dinámica para la liquidación del tope tarifario.

Define las tarifas del perfil general, que los demás módulos importan desde
aquí, y las funciones que calculan el costo mínimo de cubrir los viajes de un
periodo y la devolución que corresponde a una tarjeta.

Las tablas se indexan por día, del 1 al d + 1: la posición t guarda C(t), lo
mínimo para pagar del día t al final, y la posición d + 1 es el caso base. La
posición 0 no se usa.
"""

PASAJE: int = 3900
DIARIO: int = 9500
SEMANAL: int = 36000
MENSUAL: int = 135000

# Pases de varios días: (nombre, precio, días consecutivos que cubre).
PASES: tuple[tuple[str, int, int], ...] = (
    ("semanal", SEMANAL, 7),
    ("mensual", MENSUAL, 30),
)

# Días que cubre cada elección, para saltarlos al reconstruir.
DURACION: dict[str, int] = {
    "pasajes": 1,
    "diario": 1,
    "semanal": 7,
    "mensual": 30,
}

# Opciones que se comparan en un día con viajes: pagar solo hoy y cada pase.
OPCIONES_POR_DIA: int = 1 + len(PASES)


def _llenar_tablas(
    viajes_por_dia: list[int],
) -> tuple[list[int], list[str], int]:
    """Llena las tablas de costos y elecciones de atrás hacia adelante.

    Es la única implementación de la recurrencia; las funciones públicas se
    apoyan en ella para no duplicar la lógica.

    Operación elemental: cada opción evaluada. Un día con viajes evalúa
    OPCIONES_POR_DIA opciones (pagar solo hoy, semanal y mensual) y un día sin
    viajes evalúa una (copiar C(t + 1)).

    Args:
        viajes_por_dia: Viajes de cada día; el índice 0 es el día 1. No se
            modifica.

    Returns:
        Una tupla (costos, elecciones, operaciones). costos[t] es C(t),
        elecciones[t] es lo que se compra el día t si el problema empezara
        ahí ("nada" si no hay viajes) y operaciones es el total de opciones
        evaluadas.
    """
    d = len(viajes_por_dia)
    costos = [0] * (d + 2)  # costos[d + 1] = 0 es el caso base
    elecciones = ["nada"] * (d + 2)
    operaciones = 0
    for t in range(d, 0, -1):  # del último día al primero
        viajes = viajes_por_dia[t - 1]
        if viajes == 0:
            costos[t] = costos[t + 1]
            operaciones += 1
            continue
        # Opción (a): pagar solo hoy, con pasajes sencillos o pase diario.
        sencillos = viajes * PASAJE
        if sencillos < DIARIO:
            mejor, eleccion = sencillos + costos[t + 1], "pasajes"
        else:
            mejor, eleccion = DIARIO + costos[t + 1], "diario"
        # Opciones (b) y (c): un pase que empieza hoy; si se sale del
        # periodo, lo que queda es el caso base.
        for nombre, precio, dias in PASES:
            candidato = precio + costos[min(t + dias, d + 1)]
            if candidato < mejor:
                mejor, eleccion = candidato, nombre
        costos[t] = mejor
        elecciones[t] = eleccion
        operaciones += OPCIONES_POR_DIA
    return costos, elecciones, operaciones


def tabla_costo_minimo(
    viajes_por_dia: list[int],
) -> tuple[list[int], list[str]]:
    """Calcula la tabla completa de la programación dinámica.

    Args:
        viajes_por_dia: Viajes de cada día; el índice 0 es el día 1. No se
            modifica.

    Returns:
        Una tupla (costos, elecciones) indexada por día, del 1 al d + 1.
        costos[t] es C(t) y costos[d + 1] = 0 es el caso base; elecciones[t]
        es "nada", "pasajes", "diario", "semanal" o "mensual".
    """
    costos, elecciones, _ = _llenar_tablas(viajes_por_dia)
    return costos, elecciones


def reconstruir_compras(elecciones: list[str]) -> list[tuple[int, str]]:
    """Lista qué se compra y qué día, siguiendo las elecciones óptimas.

    Parte del día 1 y, después de cada compra, salta los días que esa compra
    ya cubre: las elecciones guardadas en esos días no se usan.

    Args:
        elecciones: Elecciones por día devueltas por tabla_costo_minimo.

    Returns:
        Parejas (día, producto) de una solución óptima, con los días
        contados desde 1. "pasajes" significa pagar con pasajes sencillos
        todos los viajes de ese día.
    """
    d = len(elecciones) - 2
    compras: list[tuple[int, str]] = []
    t = 1
    while t <= d:
        eleccion = elecciones[t]
        if eleccion == "nada":
            t += 1
            continue
        compras.append((t, eleccion))
        t += DURACION[eleccion]
    return compras


def costo_minimo(viajes_por_dia: list[int]) -> int:
    """Calcula el costo de la combinación más barata que cubre los viajes.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes. El índice 0
            es el primer día; un día sin viajes vale 0.

    Returns:
        El costo mínimo en pesos.
    """
    costos, _ = tabla_costo_minimo(viajes_por_dia)
    return costos[1]


def costo_minimo_contando(viajes_por_dia: list[int]) -> tuple[int, int]:
    """Calcula el costo mínimo y cuántas operaciones elementales hizo.

    La operación elemental es cada opción evaluada (ver _llenar_tablas): 3
    por día con viajes y 1 por día sin viajes, así que el total crece en
    forma lineal con d.

    Args:
        viajes_por_dia: Viajes de cada día; el índice 0 es el día 1. No se
            modifica.

    Returns:
        Una tupla (costo, operaciones): el costo mínimo en pesos y el número
        de opciones evaluadas.
    """
    costos, _, operaciones = _llenar_tablas(viajes_por_dia)
    return costos[1], operaciones


def liquidar_tope(viajes_por_dia: list[int], cobrado: int) -> int:
    """Calcula la devolución que corresponde al usuario.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del mes.
        cobrado: pesos que se le cobraron durante el mes.

    Returns:
        La diferencia entre lo cobrado y el costo mínimo, nunca negativa.
    """
    return max(0, cobrado - costo_minimo(viajes_por_dia))
