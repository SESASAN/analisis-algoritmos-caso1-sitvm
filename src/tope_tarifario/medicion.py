"""Experimentos de tiempo y operaciones, y gráficas de la operación 4."""

import time
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from datos import generar_instancias
from estrategia import costo_minimo, costo_minimo_contando
from exhaustivo import costo_exhaustivo, costo_exhaustivo_contando
from regla_actual import costo_regla_actual, costo_regla_actual_contando

SEMILLA: int = 2026
REPETICIONES: int = 5

# Serie 1: periodos cortos, donde la exhaustiva alcanza a ejecutarse.
TAMANOS_PEQUENOS: list[int] = [6, 8, 10, 12, 14, 16, 18, 20]
TARJETAS_PEQUENAS: int = 5

# Serie 2: periodos largos, solo para la DP y la regla actual.
TAMANOS_GRANDES: list[int] = [
    1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000
]
TARJETAS_GRANDES: int = 3

# Volumen real del caso.
DIAS_MES: int = 30
TARJETAS_MES: int = 2_000
TARJETAS_REALES: int = 950_000
VENTANA_HORAS: float = 4.0
POTENCIA_KW: float = 0.5
CIERRES_POR_ANO: int = 12

CARPETA_GRAFICAS: Path = (
    Path(__file__).resolve().parents[2] / "graficas" / "tope_tarifario"
)

# Colores y marcadores de cada solución, iguales en todas las gráficas.
ESTILO: dict[str, tuple[str, str]] = {
    "Programación dinámica": ("#2a78d6", "o"),
    "Exhaustiva": ("#eb6834", "s"),
    "Regla actual": ("#1baf7a", "^"),
}


def medir_tiempo(
    funcion: Callable[[list[int]], int],
    instancias: list[list[int]],
    repeticiones: int,
) -> float:
    """Mide el tiempo medio de una solución sobre unas instancias.

    Args:
        funcion: solución que recibe viajes_por_dia.
        instancias: tarjetas sobre las que se mide.
        repeticiones: veces que se repite la medición.

    Returns:
        El tiempo medio por tarjeta, en segundos.
    """
    total = 0.0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        for viajes_por_dia in instancias:
            funcion(viajes_por_dia)
        total += time.perf_counter() - inicio
    return total / (repeticiones * len(instancias))


def contar_operaciones(
    funcion: Callable[[list[int]], tuple[int, int]],
    instancias: list[list[int]],
) -> float:
    """Cuenta las operaciones elementales medias de una solución.

    Args:
        funcion: versión de la solución que devuelve (costo, operaciones).
        instancias: tarjetas sobre las que se cuenta.

    Returns:
        El número medio de operaciones por tarjeta.
    """
    total = 0
    for viajes_por_dia in instancias:
        _, operaciones = funcion(viajes_por_dia)
        total += operaciones
    return total / len(instancias)


def serie_pequena() -> dict[str, dict[str, list[float]]]:
    """Mide las tres soluciones en periodos cortos.

    Returns:
        Para cada solución, sus listas de tiempos y de operaciones.
    """
    resultados: dict[str, dict[str, list[float]]] = {}
    for nombre in ESTILO:
        resultados[nombre] = {"tiempo": [], "operaciones": []}
    for dias in TAMANOS_PEQUENOS:
        instancias = generar_instancias(dias, TARJETAS_PEQUENAS, SEMILLA)
        for viajes_por_dia in instancias:
            esperado = costo_exhaustivo(viajes_por_dia)
            assert costo_minimo(viajes_por_dia) == esperado, viajes_por_dia
        mediciones = [
            ("Programación dinámica", costo_minimo, costo_minimo_contando),
            ("Exhaustiva", costo_exhaustivo, costo_exhaustivo_contando),
            ("Regla actual", costo_regla_actual, costo_regla_actual_contando),
        ]
        for nombre, funcion, contando in mediciones:
            resultados[nombre]["tiempo"].append(
                medir_tiempo(funcion, instancias, REPETICIONES)
            )
            resultados[nombre]["operaciones"].append(
                contar_operaciones(contando, instancias)
            )
        print(f"  d = {dias}: DP == exhaustiva en {len(instancias)} tarjetas")
    return resultados


def serie_grande() -> dict[str, dict[str, list[float]]]:
    """Mide la DP y la regla actual en periodos largos.

    Returns:
        Para cada solución, sus listas de tiempos y de operaciones.
    """
    resultados: dict[str, dict[str, list[float]]] = {
        "Programación dinámica": {"tiempo": [], "operaciones": []},
        "Regla actual": {"tiempo": [], "operaciones": []},
    }
    for dias in TAMANOS_GRANDES:
        instancias = generar_instancias(dias, TARJETAS_GRANDES, SEMILLA)
        mediciones = [
            ("Programación dinámica", costo_minimo, costo_minimo_contando),
            ("Regla actual", costo_regla_actual, costo_regla_actual_contando),
        ]
        for nombre, funcion, contando in mediciones:
            resultados[nombre]["tiempo"].append(
                medir_tiempo(funcion, instancias, REPETICIONES)
            )
            resultados[nombre]["operaciones"].append(
                contar_operaciones(contando, instancias)
            )
    return resultados


def graficar(
    pequena: dict[str, dict[str, list[float]]],
    grande: dict[str, dict[str, list[float]]],
    medida: str,
    etiqueta_y: str,
    archivo: str,
) -> None:
    """Dibuja una medida en dos paneles: periodos cortos y largos.

    Args:
        pequena: resultados de la serie de periodos cortos.
        grande: resultados de la serie de periodos largos.
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
    eje_1.set_yscale("log")
    eje_1.set_title("Periodos cortos: DP, exhaustiva y regla actual")
    eje_1.set_xlabel("Días del periodo, d (días)")
    eje_1.set_ylabel(etiqueta_y + " (escala logarítmica)")
    for nombre, valores in grande.items():
        color, marcador = ESTILO[nombre]
        datos = [valor * escala for valor in valores[medida]]
        eje_2.plot(TAMANOS_GRANDES, datos, color=color, marker=marcador,
                   linewidth=2, markersize=8, label=nombre)
    eje_2.set_title("Periodos largos: DP y regla actual")
    eje_2.set_xlabel("Días del periodo, d (días)")
    eje_2.set_ylabel(etiqueta_y)
    for eje in (eje_1, eje_2):
        eje.grid(True, color="#dddddd", linewidth=0.8)
        eje.legend()
    figura.suptitle(etiqueta_y + " frente al tamaño · tope tarifario")
    figura.tight_layout()
    CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
    figura.savefig(CARPETA_GRAFICAS / archivo, dpi=150)
    plt.close(figura)


def imprimir_tabla(
    tamanos: list[int], resultados: dict[str, dict[str, list[float]]]
) -> None:
    """Imprime el tiempo y las operaciones medias de cada tamaño.

    Args:
        tamanos: tamaños medidos en la serie.
        resultados: resultados de la serie.
    """
    for i, d in enumerate(tamanos):
        for nombre, valores in resultados.items():
            print(f"  d = {d}, {nombre}: "
                  f"{valores['tiempo'][i] * 1000:.4f} ms, "
                  f"{valores['operaciones'][i]:.0f} operaciones")


def imprimir_factores(
    tamanos: list[int], resultados: dict[str, dict[str, list[float]]]
) -> None:
    """Imprime cuánto se multiplican tiempo y operaciones al duplicar d.

    Args:
        tamanos: tamaños medidos en la serie.
        resultados: resultados de la serie.
    """
    for i, d in enumerate(tamanos):
        if 2 * d not in tamanos:
            continue
        j = tamanos.index(2 * d)
        for nombre, valores in resultados.items():
            factor_t = valores["tiempo"][j] / valores["tiempo"][i]
            factor_o = valores["operaciones"][j] / valores["operaciones"][i]
            print(f"  d = {d} -> {2 * d}, {nombre}: tiempo x{factor_t:.2f}, "
                  f"operaciones x{factor_o:.2f}")


def extrapolar(pequena: dict[str, dict[str, list[float]]]) -> None:
    """Extrapola cada solución al volumen real y estima su energía.

    Args:
        pequena: resultados de la serie corta, para estimar la exhaustiva.
    """
    instancias = generar_instancias(DIAS_MES, TARJETAS_MES, SEMILLA)
    tiempo_dp = medir_tiempo(costo_minimo, instancias, REPETICIONES)
    tiempo_regla = medir_tiempo(costo_regla_actual, instancias, REPETICIONES)
    # La exhaustiva no se puede medir en 30 días: se toma su factor de
    # crecimiento por día entre d = 10 y d = 20 y se lleva hasta d = 30.
    tiempos = pequena["Exhaustiva"]["tiempo"]
    t_10 = tiempos[TAMANOS_PEQUENOS.index(10)]
    t_20 = tiempos[TAMANOS_PEQUENOS.index(20)]
    factor_dia = (t_20 / t_10) ** (1 / 10)
    tiempo_exh = t_20 * factor_dia ** (DIAS_MES - 20)
    print(f"  Factor de la exhaustiva por día adicional: x{factor_dia:.3f}")
    filas = [
        ("Programación dinámica", tiempo_dp),
        ("Regla actual", tiempo_regla),
        ("Exhaustiva (estimada)", tiempo_exh),
    ]
    horas_por_ano: dict[str, float] = {}
    for nombre, por_tarjeta in filas:
        horas = por_tarjeta * TARJETAS_REALES / 3600
        kwh = POTENCIA_KW * horas
        cabe = "sí" if horas <= VENTANA_HORAS else "no"
        horas_por_ano[nombre] = horas * CIERRES_POR_ANO
        print(f"  {nombre}: {por_tarjeta * 1e6:.2f} µs por tarjeta, "
              f"{horas:.4g} h por cierre, cabe en 4 h: {cabe}, "
              f"{kwh:.4g} kWh por cierre, "
              f"{kwh * CIERRES_POR_ANO:.4g} kWh por año")
    diferencia = (
        horas_por_ano["Programación dinámica"] - horas_por_ano["Regla actual"]
    )
    print(f"  Diferencia anual DP - regla: {POTENCIA_KW * diferencia:.4g} kWh")


def main() -> None:
    """Ejecuta los experimentos, imprime los resultados y guarda gráficas."""
    print("Serie 1: periodos cortos")
    pequena = serie_pequena()
    imprimir_tabla(TAMANOS_PEQUENOS, pequena)
    print("Serie 2: periodos largos")
    grande = serie_grande()
    imprimir_tabla(TAMANOS_GRANDES, grande)
    print("Factores al duplicar d")
    imprimir_factores(TAMANOS_PEQUENOS, pequena)
    imprimir_factores(TAMANOS_GRANDES, grande)
    print("Volumen real: 950.000 tarjetas de 30 días")
    extrapolar(pequena)
    graficar(pequena, grande, "tiempo", "Tiempo medio por tarjeta (ms)",
             "tiempo_vs_n.png")
    graficar(pequena, grande, "operaciones",
             "Operaciones medias por tarjeta", "operaciones_vs_n.png")
    print(f"Gráficas guardadas en {CARPETA_GRAFICAS}")


if __name__ == "__main__":
    main()
