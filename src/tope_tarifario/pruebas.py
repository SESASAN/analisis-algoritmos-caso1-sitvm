"""Pruebas con assert de la operación 4 (tope tarifario)."""

import random

from datos import generar_instancias, generar_mes_disperso
from estrategia import (
    DIARIO,
    DURACION,
    MENSUAL,
    PASAJE,
    SEMANAL,
    costo_minimo,
    liquidar_tope,
    reconstruir_compras,
    tabla_costo_minimo,
)
from exhaustivo import costo_exhaustivo
from regla_actual import costo_regla_actual

SEMILLA: int = 2026

EJEMPLO_A_MANO: list[int] = [1, 0, 0, 2, 3, 2, 3, 3]


def costo_de_compras(
    viajes_por_dia: list[int], compras: list[tuple[int, str]]
) -> tuple[int, bool]:
    """Suma lo que cuestan unas compras y revisa que cubran todos los viajes.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del periodo.
        compras: parejas (día, producto) devueltas por reconstruir_compras.

    Returns:
        El costo total de las compras y si cubren todos los días con viajes.
    """
    precio = {"diario": DIARIO, "semanal": SEMANAL, "mensual": MENSUAL}
    d = len(viajes_por_dia)
    cubierto = [False] * (d + 1)
    total = 0
    for dia, producto in compras:
        if producto == "pasajes":
            total += viajes_por_dia[dia - 1] * PASAJE
        else:
            total += precio[producto]
        for t in range(dia, min(dia + DURACION[producto], d + 1)):
            cubierto[t] = True
    cubre = True
    for t in range(1, d + 1):
        if viajes_por_dia[t - 1] > 0 and not cubierto[t]:
            cubre = False
    return total, cubre


def verificar_instancia(viajes_por_dia: list[int]) -> None:
    """Compara una instancia contra la exhaustiva y su reconstrucción.

    Args:
        viajes_por_dia: viajes de la tarjeta en cada día del periodo.
    """
    original = list(viajes_por_dia)
    minimo = costo_minimo(viajes_por_dia)
    assert minimo == costo_exhaustivo(viajes_por_dia), viajes_por_dia
    _, elecciones = tabla_costo_minimo(viajes_por_dia)
    total, cubre = costo_de_compras(
        viajes_por_dia, reconstruir_compras(elecciones)
    )
    assert cubre, viajes_por_dia
    assert total == minimo, viajes_por_dia
    assert costo_regla_actual(viajes_por_dia) >= minimo, viajes_por_dia
    assert viajes_por_dia == original, "la entrada no debe modificarse"


def probar_casos_limite() -> None:
    """Prueba periodos vacíos, un solo día, meses completos y bordes."""
    # Periodo vacío y días sin viajes.
    assert costo_minimo([]) == 0
    assert costo_minimo([0]) == 0
    assert costo_minimo([0] * 31) == 0
    # Un solo día: pasajes hasta 2 viajes, diario desde 3.
    assert costo_minimo([1]) == PASAJE
    assert costo_minimo([2]) == 2 * PASAJE
    assert costo_minimo([3]) == DIARIO
    assert costo_minimo([10]) == DIARIO
    # Tres días con diario; cuatro días con semanal.
    assert costo_minimo([3, 3, 3]) == 3 * DIARIO
    assert costo_minimo([3, 3, 3, 3]) == SEMANAL
    # Todos los días con muchos viajes.
    for dias in (28, 29, 30):
        assert costo_minimo([5] * dias) == MENSUAL
    assert costo_minimo([5] * 31) == MENSUAL + DIARIO
    # Pase que se sale del mes.
    assert costo_minimo([0] * 26 + [3, 3, 3, 3]) == SEMANAL

    casos = [[], [0], [1], [2], [3], [3, 3, 3, 3], [0] * 26 + [3, 3, 3, 3]]
    for viajes_por_dia in casos:
        verificar_instancia(viajes_por_dia)


def probar_ejemplo_a_mano() -> None:
    """Prueba el ejemplo resuelto a mano en el README, fila por fila."""
    costos, elecciones = tabla_costo_minimo(EJEMPLO_A_MANO)
    assert costos[1:] == [
        39900, 36000, 36000, 36000, 36000, 26800, 19000, 9500, 0
    ]
    assert elecciones[1] == "pasajes"
    assert elecciones[4] == "semanal"
    assert reconstruir_compras(elecciones) == [(1, "pasajes"), (4, "semanal")]
    assert costo_minimo(EJEMPLO_A_MANO) == 39900
    assert costo_exhaustivo(EJEMPLO_A_MANO) == 39900


def probar_instancias_aleatorias() -> None:
    """Compara la DP con la exhaustiva en instancias aleatorias pequeñas."""
    total = 0
    # Periodos cortos de 1 a 12 días.
    for dias in range(1, 13):
        for viajes_por_dia in generar_instancias(dias, 10, SEMILLA + dias):
            verificar_instancia(viajes_por_dia)
            total += 1
    # Meses de 28 a 31 días con pocos días de viaje.
    rng = random.Random(SEMILLA)
    for _ in range(40):
        dias = rng.randint(28, 31)
        viajes_por_dia = generar_mes_disperso(dias, rng.randint(6, 12), rng)
        verificar_instancia(viajes_por_dia)
        total += 1
    assert total >= 20
    print(f"  {total} instancias aleatorias: DP == exhaustiva")


def probar_devolucion_exacta() -> None:
    """Prueba que la devolución sea cobrado."""
    # Contraejemplo.
    assert liquidar_tope(EJEMPLO_A_MANO, 45500) == 5600
    # Se cobró exactamente el mínimo.
    assert liquidar_tope(EJEMPLO_A_MANO, 39900) == 0
    # Se cobró menos que el mínimo.
    assert liquidar_tope(EJEMPLO_A_MANO, 30000) == 0
    assert liquidar_tope([], 0) == 0
    # Tarjetas al azar cobradas con la regla actual.
    for viajes_por_dia in generar_instancias(10, 30, SEMILLA):
        cobrado = costo_regla_actual(viajes_por_dia)
        devolucion = liquidar_tope(viajes_por_dia, cobrado)
        assert devolucion >= 0
        assert cobrado - devolucion == costo_exhaustivo(viajes_por_dia)


def probar_contraejemplo() -> None:
    """Prueba que la regla actual cobre más que el óptimo."""
    regla = costo_regla_actual(EJEMPLO_A_MANO)
    optimo = costo_minimo(EJEMPLO_A_MANO)
    assert regla == 45500
    assert optimo == 39900
    assert optimo == costo_exhaustivo(EJEMPLO_A_MANO)
    assert regla - optimo == 5600


def main() -> None:
    """Ejecuta todas las pruebas."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo a mano: OK")
    probar_instancias_aleatorias()
    print("Instancias aleatorias: OK")
    probar_devolucion_exacta()
    print("Devolución exacta: OK")
    probar_contraejemplo()
    print("Contraejemplo de la regla actual: OK")
    print("Todas las pruebas pasaron")


if __name__ == "__main__":
    main()