# Conciliación nocturna del recaudo del SITVM

**Análisis de Algoritmos · 2026-2 · Proyecto final · Caso de estudio 1**

**Integrantes:**
- Sebastián Jesús Pérez Araujo · sebastianperez1116036@correo.itm.edu.co ([@SESASAN](https://github.com/SESASAN))
- Geremy Santa Duque · geremysanta1117442@correo.itm.edu.co ([@GereSanta07](https://github.com/GereSanta07))
- Nathalie Gabriela Miranda Rejón · nathaliemiranda1117738@correo.itm.edu.co ([@NathyGaby04](https://github.com/NathyGaby04))
- Samuel Quiroz Rincón · samuelquiroz1113937@correo.itm.edu.co ([@Samuzarter](https://github.com/Samuzarter))

**Operaciones abordadas:**
- Operación 4: liquidación del tope tarifario (Laboratorio 4, programación dinámica)
- Operación _X_: _por definir_ (entrega del 23 de noviembre)

---

## 1. Análisis del problema

### 1.1 Descripción del problema computacional
_Pendiente para la entrega del 23 de noviembre._

> El proceso nocturno completo del SITVM (las cuatro operaciones), la ventana de 4 h y por qué hoy no cabe (> 8 h).

### 1.2 Entradas, salidas y restricciones

#### Operación 4 · Tope tarifario
> Entrada (`viajes_por_dia` de una tarjeta en un mes, más lo cobrado), salida (costo mínimo y devolución), unidades (pesos enteros, días del mes) y límites del caso: 950.000 tarjetas activas, meses de 28 a 31 días, tarifas del perfil general, ventana 00:00–04:00 la noche de cierre de mes y servidor de 500 W. Restricción del negocio: devolución exacta, ni un peso de más ni de menos.

| Producto | Valor | Cobertura |
|---|---|---|
| Pasaje sencillo | $3.900 | Un viaje |
| Pase diario | $9.500 | Viajes ilimitados durante un día calendario |
| Pase semanal | $36.000 | Viajes ilimitados durante 7 días consecutivos |
| Pase mensual | $135.000 | Viajes ilimitados durante 30 días consecutivos |

#### Operación _X_
_Pendiente para la entrega del 23 de noviembre._

### 1.3 Operaciones críticas del proceso
_Pendiente para la entrega del 23 de noviembre._

### 1.4 Costo energético del proceso actual (línea base)
_Pendiente para la entrega del 23 de noviembre._

### 1.5 Supuestos del equipo

Para desarrollar la solución del caso de liquidación del tope tarifario, el equipo estableció los siguientes supuestos de interpretación:

- **Interpretación de la regla simplificada actual:** se interpreta que los primeros treinta días del mes se dividen en bloques fijos: días 1 al 7, 8 al 14, 15 al 21, 22 al 28 y 29 al 30. Primero, para cada día se calcula el menor costo entre pagar los viajes con pasajes sencillos y utilizar el pase diario. Después, se suman los costos diarios de cada bloque y se limita ese valor al precio del pase semanal ($36.000). Finalmente, al acumulado de los primeros treinta días se le aplica el límite del pase mensual ($135.000). Por ejemplo, si durante los primeros siete días se realizan tres viajes diarios, el costo de los pasajes sería de $81.900. Al aplicar el pase diario, el costo de cada día queda en $9.500, para un acumulado de $66.500. Como este valor supera los $36.000 del pase semanal, la regla cobra $36.000 por ese bloque.

- **Meses de 31 días:** el pase mensual tiene una cobertura de treinta días, por lo que no se extiende automáticamente al día 31. En la interpretación de la regla actual, los primeros treinta días se procesan con los límites semanal y mensual, mientras que el día 31 se cobra por separado, aplicando el menor costo entre los pasajes sencillos y el pase diario.

- **Pases que exceden el mes:** cuando un pase semanal o mensual comprado en los últimos días del mes tiene una cobertura que supera el periodo analizado, se considera únicamente la cobertura correspondiente a los días restantes del mes. Sin embargo, se mantiene el precio completo del pase, ya que no se supone un descuento proporcional por los días que quedan fuera del periodo.

- **Perfiles diferenciales:** se supone que los perfiles tarifarios diferenciales conservan la misma estructura de productos y reglas de cobertura, pero utilizan tarifas distintas. La implementación de este laboratorio trabaja con los valores del perfil general definidos en el enunciado; los demás perfiles requerirían proporcionar sus tarifas correspondientes.

- **Validez de los datos:** se supone que las entradas son válidas y consisten en una lista de cantidades enteras no negativas, donde cada posición representa un día del mes y su valor indica la cantidad de viajes realizados. Una lista vacía representa un periodo sin viajes.

- **Procesamiento en memoria y un solo hilo:** las instancias se procesan en memoria, de manera secuencial y utilizando un único hilo de ejecución. No se contempla procesamiento paralelo ni almacenamiento externo durante la ejecución de los algoritmos.

- **Datos sintéticos:** para las pruebas y mediciones se utilizan instancias generadas artificialmente, con semillas fijas cuando se requiere reproducibilidad. Estos datos permiten evaluar el comportamiento de los algoritmos sin utilizar información personal o registros reales de tarjetas.

- **Exactitud de la liquidación:** el costo óptimo debe cubrir todos los viajes del periodo al menor valor posible. La devolución debe corresponder exactamente a la diferencia entre el valor cobrado y el costo mínimo, sin generar devoluciones negativas.

---

## 2. Diseño de la solución

### 2.1 Estructuras de datos seleccionadas

#### Operación 4 · Tope tarifario

| Estructura | Qué almacena | Motivo de elección |
|---|---|---|
| Lista de enteros `viajes_por_dia` | Cantidad de viajes de cada día. La posición 0 representa el día 1. | Es la información de entrada. Su longitud indica cuántos días tiene el periodo (normalmente entre 28 y 31), por lo que no es necesario asumir que todos tienen 30 días. |
| Lista `costos` de tamaño d + 2 | `costos[t]` = C(t). El valor `costos[d+1] = 0` corresponde al caso base. | Los estados van del día 1 al d + 1 y no tienen posiciones intermedias vacías. Al usar una lista, consultar un día cuesta O(1). Un diccionario no sería necesario porque todos los estados se calculan y ocuparía más memoria. |
| Lista `elecciones` de tamaño d + 2 | Producto seleccionado para cada día. | Permite reconstruir las compras realizadas y verificar que su costo total sea exactamente C(1). Sin esta lista solo conoceríamos el costo mínimo. |
| Tupla `PASES` | Nombre, precio y días de cobertura de los pases semanal y mensual. | Permite evaluar los pases mediante un solo ciclo. Si cambian las tarifas, se pueden modificar sus valores sin alterar la lógica principal. |
| Enteros en pesos | Valores de todos los costos. | Permiten calcular las devoluciones sin errores de redondeo que podrían aparecer al utilizar `float`. |

**Espacio:** Θ(d), donde d representa la cantidad de días del periodo. Si únicamente se necesitara conocer el costo mínimo, bastaría con conservar una ventana de 31 posiciones, porque ningún pase consulta más de 30 días hacia adelante. Sin embargo, se almacena toda la tabla para poder reconstruir las compras y revisar cada liquidación.

#### Operación _X_
_Pendiente para la entrega del 23 de noviembre._

### 2.2 Operación 4 · Tope tarifario

#### Por qué el problema admite programación dinámica

**Subestructura óptima.** El costo de una tarjeta puede dividirse en dos partes:

- Lo que se compra el primer día con viajes que todavía falta por pagar.
- El costo mínimo de cubrir los días restantes del periodo.

La segunda parte representa el mismo problema, pero comienza en un día posterior. Para tomar la siguiente decisión solo necesitamos saber desde qué día todavía hay viajes por pagar. Así, podemos resolver el problema completo utilizando las soluciones óptimas de problemas más pequeños.

Además, el costo de los días restantes también debe ser óptimo. Si se utilizara una solución más costosa de lo necesario, podríamos reemplazarla por la alternativa más barata y reducir el total. Por eso, una solución que no optimice el resto tampoco puede ser óptima para el problema completo.

**Subproblemas que se repiten.** En el ejemplo resuelto a mano (más abajo), el estado C(8), que representa el costo de pagar desde el día 8 hasta el final del periodo, se alcanza mediante dos caminos:

- **Camino A:** comprar un pase semanal el día 1, que cubre del día 1 al 7.
- **Camino B:** comprar un pasaje el día 1, no comprar nada los días 2 y 3 porque no hay viajes, y pagar únicamente los viajes de cada día entre el 4 y el 7.

Con C(9) ocurre algo similar. Se puede llegar a este estado de dos maneras:

- Comprar un semanal en cualquier día con viajes entre el 4 y el 8. Los días que queden por fuera del periodo se recortan hasta llegar al día 9.
- Pagar únicamente los viajes del día 8.

Los días 2 y 3 no afectan estas decisiones porque no tienen viajes. La recurrencia simplemente toma el costo del día siguiente y no realiza ninguna compra.

Una solución exhaustiva vuelve a calcular C(8) y C(9) cada vez que encuentra esos caminos. En cambio, la programación dinámica guarda sus resultados y los reutiliza.

**Por qué no basta decidir día por día.** Los pases semanal y mensual cubren varios días al mismo tiempo. Por ejemplo, si se compra un semanal en el día t, los seis días siguientes ya quedan cubiertos. Por eso, elegir el precio más barato para cada día de manera independiente no permite identificar todas las combinaciones posibles.

#### Ejemplo resuelto a mano

**Datos de entrada:** viajes = [1, 0, 0, 2, 3, 2, 3, 3]. El caso base es C(9) = 0.

| Día | Viajes | Solo ese día | Semanal | Mensual | C | Gana |
|---|---|---|---|---|---|---|
| 9 | — | — | — | — | 0 | caso base |
| 8 | 3 | 9.500 + 0 = 9.500 | 36.000 + C(9) = 36.000 | 135.000 | 9.500 | diario |
| 7 | 3 | 9.500 + 9.500 = 19.000 | 36.000 | 135.000 | 19.000 | diario |
| 6 | 2 | 7.800 + 19.000 = 26.800 | 36.000 | 135.000 | 26.800 | pasajes |
| 5 | 3 | 9.500 + 26.800 = 36.300 | 36.000 | 135.000 | 36.000 | semanal |
| 4 | 2 | 7.800 + 36.000 = 43.800 | 36.000 + C(9) = 36.000 | 135.000 | 36.000 | semanal |
| 3 | 0 | se copia C(4) | | | 36.000 | — |
| 2 | 0 | se copia C(3) | | | 36.000 | — |
| 1 | 1 | 3.900 + 36.000 = 39.900 | 36.000 + C(8) = 45.500 | 135.000 | **39.900** | pasaje |

**Interpretación de los resultados:**

- **Día 5:** la diferencia entre pagar por separado y comprar el semanal es de apenas 300 pesos. Los pagos diarios de los días 5 al 8 suman 36.300, mientras que el semanal cuesta 36.000.
- **Día 1:** comprar el semanal desde este día resulta más caro por dos motivos: cubre los días 2 y 3, que no tienen viajes, y no alcanza a cubrir el día 8, que debe pagarse por separado (C(8) = 9.500). Por eso, esta alternativa cuesta 36.000 + 9.500 = 45.500. Es mejor pagar el pasaje del primer día y comenzar el semanal en el día 4.

**Compras seleccionadas.** Para reconstruirlas, se comienza en el día 1 y se sigue la opción que ganó en cada fila:

- **Día 1:** se compra un pasaje de 3.900.
- **Días 2 y 3:** no se compra nada porque no hay viajes.
- **Día 4:** se compra un semanal de 36.000. Este cubre hasta el día 10, por lo que ya no es necesario realizar más compras durante el periodo.

**Costo total: 39.900.** Los resultados de los días 5 al 8 no se utilizan en la reconstrucción, porque el semanal comprado el día 4 ya cubre esos viajes.

**Comparación con la regla actual:**

- La primera semana, del día 1 al 7, suma 38.500 y se aplica el tope de 36.000.
- El día 8 pertenece a otro bloque y se cobra por separado: 9.500.
- **El total cobrado por la regla es 45.500, es decir, 5.600 pesos más que el costo óptimo.**

Esto sucede porque la regla actual solo aplica el descuento semanal al bloque fijo de los días 1 a 7, mientras que la mejor opción es comenzar el semanal en el día 4. Si se pagara cada día de forma independiente, el total sería de 48.000.

#### Recurrencia

```text
hoy(t) = min(viajes_t · 3.900, 9.500)

C(d+1) = 0
C(t)   = C(t+1)                                   si el día t no tiene viajes
C(t)   = mín{ hoy(t) + C(t+1),
              36.000  + C(min(t+7,  d+1)),
              135.000 + C(min(t+30, d+1)) }       si tiene viajes
```

**Significado de cada elemento:**

- **C(t):** representa el costo mínimo para cubrir los viajes desde el día t hasta el final del periodo. Se asume que los días anteriores ya están pagos y que ninguna compra anterior cubre el día actual. El resultado final es C(1), y la devolución se calcula como `max(0, cobrado − C(1))`.
- **hoy(t):** calcula la alternativa más económica para pagar únicamente el día t, comparando los pasajes individuales con el pase diario. A partir de 3 viajes conviene el diario, porque 11.700 es mayor que 9.500.
- **Las tres alternativas:** cada opción suma el precio de la compra actual al costo mínimo de los días que todavía quedan sin cubrir. Si se paga solo el día actual, se continúa desde t + 1; con el semanal, desde t + 7; y con el mensual, desde t + 30.
- **El límite d + 1:** evita consultar posiciones fuera de la tabla cuando un pase supera la duración del periodo. En ese caso, se llega al caso base.
- **Días sin viajes:** no requieren compras, por lo que se conserva el costo calculado para el día siguiente.

**Caso base.** C(d + 1) = 0, porque representa una posición en la que ya no quedan días por pagar.

**Orden de cálculo.** Como cada estado depende de días posteriores, primero se calcula C(d + 1) y luego se avanza en sentido descendente hasta C(1). De esta manera, cuando se necesita consultar otro estado, su valor ya está calculado.

#### Estrategias diseñadas

**Programación dinámica (propuesta)**

```text
función costo_minimo(viajes):
    d ← largo(viajes)
    costos[1..d+1] ← 0
    elecciones[1..d+1] ← "nada"

    para t desde d hasta 1:
        si viajes[t] = 0:
            costos[t] ← costos[t+1]
            continuar

        costos[t] ← hoy(t) + costos[t+1]
        elecciones[t] ← "pasajes" si viajes[t]·3900 < 9500, si no "diario"

        para cada (nombre, precio, L) en [(semanal, 36000, 7), (mensual, 135000, 30)]:
            cand ← precio + costos[min(t+L, d+1)]
            si cand < costos[t]:
                costos[t] ← cand
                elecciones[t] ← nombre

    devolver costos[1]
```

El tiempo de ejecución es Θ(d), ya que para cada día se revisan como máximo tres alternativas. El espacio utilizado también es Θ(d), debido a las dos tablas.

**Exhaustiva (solución exacta para verificar)**

```text
función exh(viajes, t):
    si t > d: devolver 0
    si viajes[t] = 0: devolver exh(viajes, t+1)

    mejor ← viajes[t] * 3900 + exh(viajes, t+1)
    mejor ← min(mejor, 9500 + exh(viajes, t+1))
    mejor ← min(mejor, 36000 + exh(viajes, t+7))
    mejor ← min(mejor, 135000 + exh(viajes, t+30))

    devolver mejor
```

Esta estrategia prueba todas las combinaciones posibles sin almacenar los resultados de los subproblemas. Su espacio es Θ(d), debido a la profundidad de las llamadas recursivas. El análisis de tiempo se presenta en §4.1.

**Regla actual (línea base).**

1. Para cada día con viajes, se calcula hoy(t).
2. Los días del 1 al 30 se dividen en semanas fijas: 1–7, 8–14, 15–21, 22–28 y 29–30. Cada bloque tiene un cobro máximo de 36.000.
3. Después de aplicar los topes semanales, el total de los días 1 a 30 no puede superar 135.000. Esto equivale a aplicar un pase mensual que comienza el día 1.
4. Si existe un día 31, sus viajes se cobran por separado utilizando hoy(t).

```text
función regla_actual(viajes):
    n ← min(d, 30)
    total ← 0

    para cada bloque de 7 días dentro de 1..n:
        total ← total + min(Σ hoy(t) en el bloque, 36000)

    total ← min(total, 135000)

    para t de 31 a d:
        total ← total + hoy(t)

    devolver total
```

Su tiempo de ejecución es Θ(d), igual que el de la programación dinámica. La diferencia entre ambas está en el resultado que calculan, no en el costo computacional.

**Alcance de la regla.** Esta interpretación está pensada para liquidar un solo mes, es decir, cuando d ≤ 31. A partir del día 31, los viajes se cobran con hoy(t), sin aplicar nuevos topes. En la Serie 2 de `medicion.py`, la regla se ejecuta hasta d = 100.000 únicamente para medir su tiempo de ejecución, que sigue siendo Θ(d). Para periodos mayores a 31 días, sus cobros no se comparan con el óptimo. Por ejemplo, con `[3] * 60`, la regla cobra 420.000, mientras que la DP calcula 270.000.

**Diagrama de dependencias de la DP**

```text
C(t) ──hoy────▶ C(t+1)
  ├───semanal─▶ C(min(t+7,  d+1))
  └───mensual─▶ C(min(t+30, d+1))

orden de cálculo: C(d+1) → C(d) → … → C(2) → C(1)
```

### 2.3 Operación _X_
_Pendiente para la entrega del 23 de noviembre._

---

## 3. Implementación

### 3.1 Operación 4 · Tope tarifario

Código en [`src/tope_tarifario/`](src/tope_tarifario/):

| Módulo | Contenido |
|---|---|
| [`estrategia.py`](src/tope_tarifario/estrategia.py) | `costo_minimo` (programación dinámica) y `liquidar_tope` |
| [`exhaustivo.py`](src/tope_tarifario/exhaustivo.py) | `costo_exhaustivo`, que prueba todas las combinaciones |
| [`regla_actual.py`](src/tope_tarifario/regla_actual.py) | `costo_regla_actual`, la regla simplificada de hoy |
| [`datos.py`](src/tope_tarifario/datos.py) | Generador de meses sintéticos con semilla fija |
| [`pruebas.py`](src/tope_tarifario/pruebas.py) | Pruebas con `assert` |
| [`medicion.py`](src/tope_tarifario/medicion.py) | Experimentos y gráficas |

#### Decisiones de implementación de `estrategia.py`

1. **Tabla calculada con un ciclo, sin recursión.** Python tiene un límite de profundidad para las llamadas recursivas, y cada llamada también agrega un costo. Por eso se utiliza un ciclo `for t in range(d, 0, -1)`, que deja claro el orden de cálculo y permite medir periodos de cientos de miles de días.

2. **Listas indexadas desde 1 hasta d + 1.** De esta forma, el código sigue la misma numeración que la recurrencia. La posición 0 no se utiliza y `costos[d+1] = 0` queda establecida desde la inicialización.

3. **Control del límite de los pases con `min(t + dias, d + 1)`.** Esto evita acceder a posiciones que no existen en la lista y representa el supuesto de que cada periodo se liquida de manera independiente.

4. **Uso de enteros para los precios.** Todos los valores se manejan en pesos enteros para obtener devoluciones exactas.

5. **Precios y duraciones definidos como datos.** Los precios se encuentran en las constantes `PASAJE`, `DIARIO`, `SEMANAL` y `MENSUAL`. Los pases de varios días se organizan en la tupla `PASES`, que almacena su nombre, precio y duración. También existe el diccionario `DURACION`, utilizado para reconstruir las compras. Así, los valores se mantienen separados de la lógica principal.

6. **Desempate mediante comparación estricta.** Se utiliza `<` al comparar los costos. Si dos alternativas tienen el mismo precio, se conserva la que se evaluó primero. Por ejemplo, para `[3] * 31`, comprar el diario el día 1 y el mensual el día 2 cuesta lo mismo que comprar el mensual el día 1 y el diario el día 31: 144.500 pesos. Sin embargo, gana la primera combinación porque se evalúa antes. Esto no modifica el costo mínimo, pero sí determina qué compras aparecen en la reconstrucción.

7. **Separación del costo y la reconstrucción.** La función `costo_minimo` devuelve únicamente el valor entero que solicita el esqueleto. Las compras se recuperan utilizando `reconstruir_compras`, que sigue las elecciones guardadas y salta los días cubiertos por cada pase. Las pruebas comprueban que las compras cubran todos los viajes y sumen exactamente C(1).

8. **Cálculo de la devolución.** `liquidar_tope` utiliza la expresión `max(0, cobrado - costo_minimo(viajes))`, garantizando que el valor devuelto nunca sea negativo.

9. **Contador de operaciones y reutilización de la recurrencia.** Las funciones `costo_minimo` y `costo_minimo_contando` utilizan `_llenar_tablas`, que contiene la única implementación de la recurrencia. Así se evita duplicar la lógica. El contador registra una operación por cada día sin viajes y tres por cada día con viajes, correspondientes a las alternativas evaluadas. Por esta razón, la función `costo_minimo` también realiza el conteo, aunque no devuelva ese valor. Este trabajo adicional consiste en incrementar un entero por día y se mantiene dentro de Θ(d).

#### Decisiones de implementación de `exhaustivo.py` y `regla_actual.py`

1. **Solución exhaustiva mediante recursividad.** Se implementó `costo_exhaustivo` evaluando las cuatro alternativas disponibles: pasajes sencillos, pase diario, pase semanal y pase mensual. Claramente para cada alternativa se realiza el calculo de su costo y se continúa desde el primer día que todavía falta por cubrir. Finalmente, se selecciona el menor de los cuatro resultados. Cabe resaltar que no se utiliza ninguna técnica de optimización, ni se almacenan resultados anteriores, porque el propósito es probar todas las combinaciones posibles y utilizar esta solución como referencia para verificar la programación dinámica.

2. **Tratamiento de días sin viajes.** Cuando un día no registra viajes, la función continúa directamente al siguiente día sin realizar ninguna compra. Lo anterior evita considerar productos innecesarios.

3. **Límites de cobertura.** Cuando un pase supera la duración del periodo, se limita el siguiente estado al último día disponible más uno. De esta manera, no se realizan accesos fuera del periodo.

4. **Implementación de la regla actual.** `costo_regla_actual` calcula primero el costo diario más económico entre los pasajes sencillos y el pase diario. Después aplica los topes semanales sobre los bloques fijos establecidos en el README (días 1–7, 8–14, 15–21, 22–28 y 29–30), seguido del tope mensual de 135.000 pesos. Si existe un día 31, se cobra por separado.

5. **Uso de las mismas tarifas.** Ambos módulos importan las constantes de `estrategia.py`, evitando duplicar los precios de los productos y manteniendo una única referencia para las tarifas.

### 3.2 Operación _X_
_Pendiente para la entrega del 23 de noviembre._

### 3.3 Tecnologías y herramientas
> Python (versión), matplotlib, entorno virtual y `requirements.txt`.

---

## 4. Evaluación del desempeño

### 4.1 Operación 4 · Tope tarifario

#### Complejidad temporal y espacial
> Complejidad de la programación dinámica, de la exhaustiva y de la regla actual, y su contraste.

#### Verificación
> Cómo se verificó y qué casos cubre [`pruebas.py`](src/tope_tarifario/pruebas.py):
> - Casos límite (mes vacío, un día, sin viajes, todos los días con viajes, pase que se sale del mes).
> - El ejemplo a mano de §2.2.
> - Al menos 20 instancias aleatorias con semilla fija en las que la programación dinámica coincide con la exhaustiva.
> - Que `liquidar_tope` devuelve exactamente cobrado − mínimo y nunca un valor negativo.
> - La instancia del contraejemplo de §5.1.

#### Diseño de los experimentos
> Lo implementado en [`datos.py`](src/tope_tarifario/datos.py) y [`medicion.py`](src/tope_tarifario/medicion.py): semilla, número de repeticiones, tamaños d (al menos seis, con una pareja d y 2d), viajes en casi todos los días, y la exhaustiva solo en periodos cortos. La programación dinámica se lleva a tamaños mucho mayores. Se mide solo la ejecución, con `perf_counter`.

#### Resultados

![Tiempo frente al tamaño – tope tarifario](graficas/tope_tarifario/tiempo_vs_n.png)

![Operaciones frente al tamaño – tope tarifario](graficas/tope_tarifario/operaciones_vs_n.png)

#### Lo medido contra lo esperado
> Con la pareja d → 2d: cuánto se multiplicaron el tiempo y las operaciones de cada solución, si coincide con la complejidad y por qué hay diferencias.

#### Extrapolación al volumen real
> Tiempo estimado para unas 950.000 tarjetas con la programación dinámica, la regla actual y la exhaustiva, comparado con la ventana de 4 h. Justifiquen la forma de la curva antes de extrapolar y digan cuándo la exhaustiva no terminaría.

### 4.2 Operación _X_
_Pendiente para la entrega del 23 de noviembre._

---

## 5. Análisis comparativo

### 5.1 Operación 4 · Tope tarifario

#### Contraejemplo de la regla actual

Se utilizó la siguiente instancia para comparar el procedimiento actual con la solución óptima:

**Entrada:** `viajes = [1, 0, 0, 2, 3, 2, 3, 3]`

La instancia representa ocho días de actividad de una tarjeta, donde cada posición indica la cantidad de viajes realizados en ese día.

**Resultado de la regla actual:**

- Días 1 al 7: el costo de los viajes, aplicando el menor valor entre pasajes sencillos y pase diario, es de 38.500 pesos. Al superar el tope semanal, se cobran 36.000 pesos.
- Día 8: se realizan tres viajes, cuyo costo más económico es el pase diario de 9.500 pesos.
- Total cobrado: **45.500 pesos**.

**Resultado de la estrategia óptima:**

La programación dinámica encuentra una combinación más económica:

- Día 1: un pasaje sencillo de 3.900 pesos.
- Días 2 y 3: no se realizan viajes.
- Día 4: un pase semanal de 36.000 pesos, que cubre hasta el día 10.

El costo mínimo es de **39.900 pesos**.

**Comparación de resultados:**

| Método | Costo |
|---|---:|
| Regla actual | $45.500 |
| Programación dinámica | $39.900 |
| Solución exhaustiva | $39.900 |
| Diferencia cobrada de más | **$5.600** |

La solución exhaustiva coincide con la programación dinámica, lo que permite utilizarla como referencia independiente para comprobar el resultado.

El contraejemplo demuestra que la regla actual no siempre encuentra la combinación más económica. Su limitación consiste en aplicar los topes semanales sobre bloques fijos, sin considerar que puede ser más conveniente comenzar un pase semanal en un día posterior.

#### Condición contraria

Una estrategia voraz podría ser adecuada si las decisiones de compra no afectaran la cobertura de días posteriores y existiera una propiedad que garantizara que elegir la alternativa localmente más económica siempre conduce al costo global mínimo. En el problema actual esto no se cumple, porque los pases de varios días pueden cubrir viajes futuros y modificar el costo total.

#### Recomendación
> Qué estrategia adoptar, qué gana el SITVM frente a hoy y qué riesgo o límite debe conocer.

### 5.2 Operación _X_ y comparación general
_Pendiente para la entrega del 23 de noviembre._

---

## 6. Implicaciones éticas, sociales y ambientales

### 6.1 Consumo energético

#### Operación 4 · Tope tarifario
> kWh = kW × h con 500 W, para la regla actual, la programación dinámica y la exhaustiva, declarados como estimaciones. Proyección a un año de la diferencia entre la regla actual y la programación dinámica: la operación corre en 12 cierres de mes.

#### Proceso completo
_Pendiente para la entrega del 23 de noviembre._

### 6.2 Preguntas de impacto del caso (personas, normativa, crecimiento)
_Pendiente para la entrega del 23 de noviembre._

### 6.3 Consecuencias sobre las personas
_Pendiente para la entrega del 23 de noviembre._

### 6.4 Marco normativo y buenas prácticas
_Pendiente para la entrega del 23 de noviembre._

### 6.5 Sostenibilidad de la decisión
_Pendiente para la entrega del 23 de noviembre._

---

## 7. Conclusiones
_Pendiente para la entrega del 23 de noviembre._

---

## 8. Reproducción

```bash
# 1. Crear y activar el entorno
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Pruebas de la operación 4
python src/tope_tarifario/pruebas.py

# 3. Mediciones y gráficas (se guardan en graficas/tope_tarifario/)
python src/tope_tarifario/medicion.py
```

> Ajusten los comandos a como quede el código (por ejemplo, `python -m src.tope_tarifario.pruebas` si usan imports de paquete).

### Estructura del repositorio

```
.
├── README.md
├── requirements.txt
├── src/
│   └── tope_tarifario/
│       ├── estrategia.py
│       ├── exhaustivo.py
│       ├── regla_actual.py
│       ├── datos.py
│       ├── pruebas.py
│       └── medicion.py
└── graficas/
    └── tope_tarifario/
        ├── tiempo_vs_n.png
        └── operaciones_vs_n.png
```
