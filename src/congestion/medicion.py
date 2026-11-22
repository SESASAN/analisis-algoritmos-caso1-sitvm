"""Experimentos de tiempo y operaciones, y gráficas de la operación 3."""

import time
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from datos import generar_series
from dividir_y_vencer import tramo_maximo_dyv, tramo_maximo_dyv_contando
from fuerza_bruta import (
    tramo_maximo_fuerza_bruta,
    tramo_maximo_fuerza_bruta_contando,
)
from kadane import tramo_maximo_kadane, tramo_maximo_kadane_contando

Tramo = tuple[int, int, int]  # (inicio, fin, suma)

SEMILLA: int = 2026
REPETICIONES: int = 3

# Serie 1: series cortas, donde la fuerza bruta alcanza a ejecutarse.
TAMANOS_PEQUENOS: list[int] = [250, 500, 1_000, 2_000, 4_000, 8_000]
SERIES_PEQUENAS: int = 3

# Serie 2: series largas, solo para dividir y vencer y Kadane.
TAMANOS_GRANDES: list[int] = [
    10_000, 20_000, 41_500, 83_000, 166_000, 332_000
]
SERIES_GRANDES: int = 3

# Volumen real del caso.
INTERVALOS_REALES: int = 166_000
ESTACIONES: int = 80
VENTANA_HORAS: float = 4.0
POTENCIA_KW: float = 0.5

CARPETA_GRAFICAS: Path = (
    Path(__file__).resolve().parents[2] / "graficas" / "congestion"
)

# Colores y marcadores de cada estrategia, iguales en todas las gráficas.
ESTILO: dict[str, tuple[str, str]] = {
    "Kadane": ("#2a78d6", "o"),
    "Fuerza bruta": ("#eb6834", "s"),
    "Dividir y vencer": ("#1baf7a", "^"),
}


def medir_tiempo(
    funcion: Callable[[list[int]], Tramo],
    series: list[list[int]],
    repeticiones: int,
) -> float:
    """Mide el tiempo medio de una estrategia sobre unas series.

    Args:
        funcion: estrategia que recibe la serie de saldos.
        series: series sobre las que se mide.
        repeticiones: veces que se repite la medición.

    Returns:
        El tiempo medio por serie, en segundos.
    """
    total = 0.0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        for saldos in series:
            funcion(saldos)
        total += time.perf_counter() - inicio
    return total / (repeticiones * len(series))


def contar_operaciones(
    funcion: Callable[[list[int]], tuple[Tramo, int]],
    series: list[list[int]],
) -> float:
    """Cuenta las operaciones elementales medias de una estrategia.

    Args:
        funcion: versión de la estrategia que devuelve (tramo, operaciones).
        series: series sobre las que se cuenta.

    Returns:
        El número medio de intervalos sumados por serie.
    """
    total = 0
    for saldos in series:
        _, operaciones = funcion(saldos)
        total += operaciones
    return total / len(series)


def medir_serie(
    tamanos: list[int],
    cantidad: int,
    estrategias: list[tuple[str, Callable, Callable]],
) -> dict[str, dict[str, list[float]]]:
    """Mide unas estrategias en varios tamaños y verifica sus sumas.

    Args:
        tamanos: tamaños n de las series.
        cantidad: series por tamaño.
        estrategias: tuplas (nombre, función, función contando).

    Returns:
        Para cada estrategia, sus listas de tiempos y de operaciones.
    """
    resultados: dict[str, dict[str, list[float]]] = {}
    for nombre, _, _ in estrategias:
        resultados[nombre] = {"tiempo": [], "operaciones": []}
    for n in tamanos:
        series = generar_series(n, cantidad, SEMILLA)
        for saldos in series:
            sumas = [funcion(saldos)[2] for _, funcion, _ in estrategias]
            assert len(set(sumas)) == 1, (n, sumas)
        for nombre, funcion, contando in estrategias:
            resultados[nombre]["tiempo"].append(
                medir_tiempo(funcion, series, REPETICIONES)
            )
            resultados[nombre]["operaciones"].append(
                contar_operaciones(contando, series)
            )
        print(f"  n = {n}: las estrategias coinciden en {cantidad} series")
    return resultados


def imprimir_tabla(
    tamanos: list[int], resultados: dict[str, dict[str, list[float]]]
) -> None:
    """Imprime el tiempo y las operaciones medias de cada tamaño.

    Args:
        tamanos: tamaños medidos en la serie.
        resultados: resultados de la serie.
    """
    for i, n in enumerate(tamanos):
        for nombre, valores in resultados.items():
            print(f"  n = {n}, {nombre}: "
                  f"{valores['tiempo'][i] * 1000:.4f} ms, "
                  f"{valores['operaciones'][i]:.0f} operaciones")


def imprimir_factores(
    tamanos: list[int], resultados: dict[str, dict[str, list[float]]]
) -> None:
    """Imprime cuánto se multiplican tiempo y operaciones al duplicar n.

    Args:
        tamanos: tamaños medidos en la serie.
        resultados: resultados de la serie.
    """
    for i, n in enumerate(tamanos):
        if 2 * n not in tamanos:
            continue
        j = tamanos.index(2 * n)
        for nombre, valores in resultados.items():
            factor_t = valores["tiempo"][j] / valores["tiempo"][i]
            factor_o = valores["operaciones"][j] / valores["operaciones"][i]
            print(f"  n = {n} -> {2 * n}, {nombre}: tiempo x{factor_t:.2f}, "
                  f"operaciones x{factor_o:.2f}")


def extrapolar(
    pequena: dict[str, dict[str, list[float]]],
    grande: dict[str, dict[str, list[float]]],
) -> None:
    """Extrapola cada estrategia al volumen real y estima su energía.

    Args:
        pequena: resultados de la serie corta, para la fuerza bruta.
        grande: resultados de la serie larga, para DyV y Kadane.
    """
    i = TAMANOS_GRANDES.index(INTERVALOS_REALES)
    tiempo_dyv = grande["Dividir y vencer"]["tiempo"][i]
    tiempo_kadane = grande["Kadane"]["tiempo"][i]
    # La fuerza bruta no se mide en 166.000: es Θ(n²), así que su tiempo
    # se escala con el cuadrado de la razón entre tamaños.
    n_mayor = TAMANOS_PEQUENOS[-1]
    t_mayor = pequena["Fuerza bruta"]["tiempo"][-1]
    tiempo_fb = t_mayor * (INTERVALOS_REALES / n_mayor) ** 2
    filas = [
        ("Kadane", tiempo_kadane),
        ("Dividir y vencer", tiempo_dyv),
        ("Fuerza bruta (estimada)", tiempo_fb),
    ]
    for nombre, por_estacion in filas:
        horas = por_estacion * ESTACIONES / 3600
        kwh = POTENCIA_KW * horas
        cabe = "sí" if horas <= VENTANA_HORAS else "no"
        print(f"  {nombre}: {por_estacion:.4g} s por estación, "
              f"{horas:.4g} h para {ESTACIONES} estaciones, "
              f"cabe en 4 h: {cabe}, {kwh:.4g} kWh")


def graficar(
    pequena: dict[str, dict[str, list[float]]],
    grande: dict[str, dict[str, list[float]]],
    medida: str,
    etiqueta_y: str,
    archivo: str,
) -> None:
    """Dibuja una medida en dos paneles: series cortas y largas.

    Args:
        pequena: resultados de la serie de series cortas.
        grande: resultados de la serie de series largas.
        medida: "tiempo" u "operaciones".
        etiqueta_y: rótulo del eje y, con unidades.
        archivo: nombre del archivo PNG.
    """
    figura, (eje_1, eje_2) = plt.subplots(1, 2, figsize=(12, 5))
    escala = 1000.0 if medida == "tiempo" else 1.0
    for nombre, valores in pequena.items():
        color, marcador = ESTILO[nombre]
        datos = [valor * escala for valor in valores[medida]]
        eje_1.plot(TAMANOS_PEQUENOS, datos, color=color, marker=marcador,
                   linewidth=2, markersize=8, label=nombre)
    eje_1.set_xscale("log")
    eje_1.set_yscale("log")
    eje_1.set_title("Series cortas: las tres estrategias")
    eje_1.set_xlabel("Intervalos de la serie, n (escala logarítmica)")
    eje_1.set_ylabel(etiqueta_y + " (escala logarítmica)")
    for nombre, valores in grande.items():
        color, marcador = ESTILO[nombre]
        datos = [valor * escala for valor in valores[medida]]
        eje_2.plot(TAMANOS_GRANDES, datos, color=color, marker=marcador,
                   linewidth=2, markersize=8, label=nombre)
    eje_2.set_title("Series largas: dividir y vencer y Kadane")
    eje_2.set_xlabel("Intervalos de la serie, n")
    eje_2.set_ylabel(etiqueta_y)
    for eje in (eje_1, eje_2):
        eje.grid(True, color="#dddddd", linewidth=0.8)
        eje.legend()
    figura.suptitle(etiqueta_y + " frente al tamaño · franjas de congestión")
    figura.tight_layout()
    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
    figura.savefig(CARPETA_GRAFICAS / archivo, dpi=150)
    plt.close(figura)


def main() -> None:
    """Ejecuta los experimentos, imprime los resultados y guarda gráficas."""
    print("Serie 1: series cortas")
    pequena = medir_serie(TAMANOS_PEQUENOS, SERIES_PEQUENAS, [
        ("Kadane", tramo_maximo_kadane, tramo_maximo_kadane_contando),
        ("Fuerza bruta", tramo_maximo_fuerza_bruta,
         tramo_maximo_fuerza_bruta_contando),
        ("Dividir y vencer", tramo_maximo_dyv, tramo_maximo_dyv_contando),
    ])
    imprimir_tabla(TAMANOS_PEQUENOS, pequena)
    print("Serie 2: series largas")
    grande = medir_serie(TAMANOS_GRANDES, SERIES_GRANDES, [
        ("Kadane", tramo_maximo_kadane, tramo_maximo_kadane_contando),
        ("Dividir y vencer", tramo_maximo_dyv, tramo_maximo_dyv_contando),
    ])
    imprimir_tabla(TAMANOS_GRANDES, grande)
    print("Factores al duplicar n")
    imprimir_factores(TAMANOS_PEQUENOS, pequena)
    imprimir_factores(TAMANOS_GRANDES, grande)
    print("Volumen real: 80 estaciones de 166.000 intervalos")
    extrapolar(pequena, grande)
    graficar(pequena, grande, "tiempo", "Tiempo medio por serie (ms)",
             "tiempo_vs_n.png")
    graficar(pequena, grande, "operaciones",
             "Intervalos sumados por serie", "operaciones_vs_n.png")
    print(f"Gráficas guardadas en {CARPETA_GRAFICAS}")


if __name__ == "__main__":
    main()
