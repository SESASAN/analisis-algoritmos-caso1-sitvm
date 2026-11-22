"""Pruebas con assert de la operación 3 (franjas de congestión)."""

from typing import Callable

from datos import generar_series
from dividir_y_vencer import tramo_maximo_dyv, tramo_maximo_dyv_contando
from fuerza_bruta import (
    tramo_maximo_fuerza_bruta,
    tramo_maximo_fuerza_bruta_contando,
)
from kadane import tramo_maximo_kadane, tramo_maximo_kadane_contando

Tramo = tuple[int, int, int]  # (inicio, fin, suma)

SEMILLA: int = 2026

# Ejemplo resuelto a mano en el README (2.3), con respuesta (2, 5, 11).
EJEMPLO_A_MANO: list[int] = [3, -5, 4, 2, -1, 6, -8, 2]

ESTRATEGIAS: list[tuple[str, Callable[[list[int]], Tramo]]] = [
    ("fuerza bruta", tramo_maximo_fuerza_bruta),
    ("dividir y vencer", tramo_maximo_dyv),
    ("Kadane", tramo_maximo_kadane),
]

CONTANDO: list[tuple[str, Callable[[list[int]], tuple[Tramo, int]]]] = [
    ("fuerza bruta", tramo_maximo_fuerza_bruta_contando),
    ("dividir y vencer", tramo_maximo_dyv_contando),
    ("Kadane", tramo_maximo_kadane_contando),
]


def mayor_suma_directa(saldos: list[int]) -> int:
    """Calcula la mayor suma sumando cada tramo desde cero.

    Args:
        saldos: saldos netos por intervalo; no puede estar vacía.

    Returns:
        La mayor suma entre todos los tramos consecutivos.
    """
    mejor = saldos[0]
    for inicio in range(len(saldos)):
        for fin in range(inicio, len(saldos)):
            suma = sum(saldos[inicio:fin + 1])
            if suma > mejor:
                mejor = suma
    return mejor


def es_tramo_valido(saldos: list[int], tramo: Tramo) -> bool:
    """Revisa que el tramo esté dentro de la serie y sume lo que dice.

    Args:
        saldos: saldos netos por intervalo.
        tramo: tupla (inicio, fin, suma) devuelta por una estrategia.

    Returns:
        True si los índices son válidos y la suma coincide con la serie.
    """
    inicio, fin, suma = tramo
    if not 0 <= inicio <= fin < len(saldos):
        return False
    return sum(saldos[inicio:fin + 1]) == suma


def verificar_serie(saldos: list[int]) -> None:
    """Comprueba las tres estrategias sobre una serie.

    Args:
        saldos: saldos netos por intervalo; no puede estar vacía.
    """
    original = list(saldos)
    esperado = mayor_suma_directa(saldos)
    for (nombre, estrategia), (_, contando) in zip(ESTRATEGIAS, CONTANDO):
        tramo = estrategia(saldos)
        assert es_tramo_valido(saldos, tramo), (nombre, saldos, tramo)
        assert tramo[2] == esperado, (nombre, saldos, tramo)
        # La variante contando devuelve el mismo tramo que la oficial.
        assert contando(saldos)[0] == tramo, (nombre, saldos)
        assert saldos == original, "la serie no debe modificarse"


def probar_casos_limite() -> None:
    """Prueba series vacías, de un intervalo, negativas, positivas y ceros."""
    # Serie vacía: las tres estrategias fallan de forma explícita.
    for nombre, estrategia in ESTRATEGIAS:
        try:
            estrategia([])
        except ValueError:
            pass
        else:
            raise AssertionError(f"{nombre} debe rechazar la serie vacía")
    # Un solo intervalo, positivo o negativo.
    for nombre, estrategia in ESTRATEGIAS:
        assert estrategia([7]) == (0, 0, 7), nombre
        assert estrategia([-4]) == (0, 0, -4), nombre
    # Todos negativos: el intervalo menos negativo, nunca un tramo vacío.
    for nombre, estrategia in ESTRATEGIAS:
        assert estrategia([-3, -1, -7, -2]) == (1, 1, -1), nombre
        assert estrategia([-4, -2, -7, -1, -9]) == (3, 3, -1), nombre
    # Todos positivos: el tramo es la serie completa.
    for nombre, estrategia in ESTRATEGIAS:
        assert estrategia([2, 5, 1]) == (0, 2, 8), nombre
    # Ceros y empates: cualquier tramo con la suma máxima es válido.
    casos = [[0, 0, 0], [5, -5, 5], [4, -10, 4], [-2, 0, -1], [1, -1] * 5,
            [7], [-4], [-4, -2, -7, -1, -9], [2, 5, 1], EJEMPLO_A_MANO]
    for saldos in casos:
        verificar_serie(saldos)


def probar_ejemplo_a_mano() -> None:
    """Prueba el ejemplo resuelto a mano en el README."""
    for nombre, estrategia in ESTRATEGIAS:
        assert estrategia(EJEMPLO_A_MANO) == (2, 5, 11), nombre


def probar_series_aleatorias() -> None:
    """Compara las tres estrategias en series aleatorias pequeñas."""
    total = 0
    for n in range(1, 41):
        for saldos in generar_series(n, 5, SEMILLA + n):
            verificar_serie(saldos)
            total += 1
    assert total >= 20
    print(f"  {total} series aleatorias: las tres estrategias coinciden")


def probar_contadores() -> None:
    """Prueba que los contadores den el número de sumas esperado."""
    for saldos in generar_series(50, 3, SEMILLA):
        n = len(saldos)
        _, operaciones = tramo_maximo_fuerza_bruta_contando(saldos)
        assert operaciones == n * (n + 1) // 2
        _, operaciones = tramo_maximo_kadane_contando(saldos)
        assert operaciones == n
    # Para n potencia de 2, dividir y vencer suma n·(log2 n + 1) intervalos.
    for exponente in range(9):
        n = 2 ** exponente
        saldos = generar_series(n, 1, SEMILLA)[0]
        _, operaciones = tramo_maximo_dyv_contando(saldos)
        assert operaciones == n * (exponente + 1), n
    # En el ejemplo a mano: 36, 32 y 8 operaciones.
    assert tramo_maximo_fuerza_bruta_contando(EJEMPLO_A_MANO)[1] == 36
    assert tramo_maximo_dyv_contando(EJEMPLO_A_MANO)[1] == 32
    assert tramo_maximo_kadane_contando(EJEMPLO_A_MANO)[1] == 8


def main() -> None:
    """Ejecuta todas las pruebas."""
    probar_casos_limite()
    print("Casos límite: OK")
    probar_ejemplo_a_mano()
    print("Ejemplo a mano: OK")
    probar_series_aleatorias()
    print("Series aleatorias: OK")
    probar_contadores()
    print("Contadores de operaciones: OK")
    print("Todas las pruebas pasaron")


if __name__ == "__main__":
    main()