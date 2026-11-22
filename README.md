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

Al cierre de cada mes, el sistema debe revisar cada tarjeta personalizada para verificar que el valor cobrado no supere el costo de la combinación más económica de pasajes y pases que cubra todos los viajes realizados. Si se identifica un cobro superior al mínimo, la diferencia se devuelve al usuario como saldo a favor. Para el análisis, el problema se modela sobre una sola tarjeta y un solo mes.

**Entradas:**

- **`viajes_por_dia`:** lista de enteros no negativos con la cantidad de viajes que realizó la tarjeta cada día del mes. La posición 0 corresponde al día 1 y un día sin viajes tiene un valor de 0. Su longitud `d` representa el número de días del mes, entre 28 y 31.
- **`cobrado`:** valor en pesos que se descontó a la tarjeta durante el mes. Este valor se utiliza únicamente para calcular la devolución correspondiente.
- **Tarifas del perfil general:** son fijas y se resumen en la siguiente tabla.

| Producto | Valor | Cobertura |
|---|---:|---|
| Pasaje sencillo | $3.900 | Un viaje |
| Pase diario | $9.500 | Viajes ilimitados durante un día calendario |
| Pase semanal | $36.000 | Viajes ilimitados durante 7 días consecutivos |
| Pase mensual | $135.000 | Viajes ilimitados durante 30 días consecutivos |

**Salidas:**

- **Costo mínimo:** valor en pesos de la combinación de productos más económica que cubre todos los viajes del mes (`costo_minimo`).
- **Devolución:** diferencia entre el valor cobrado y el costo mínimo, que nunca puede ser negativa (`liquidar_tope`). Si a la tarjeta se le cobró el mínimo o menos, la devolución es 0.

**Restricciones:**

- **Devolución exacta:** la devolución debe corresponder exactamente a la diferencia entre lo cobrado y la combinación más económica, sin devolver al usuario menos de lo que le corresponde ni más de lo que corresponde. Por esta razón, no se permiten aproximaciones y todos los valores se manejan como pesos enteros, sin decimales.
- **Cobertura completa:** la combinación elegida debe cubrir todos los días en los que se realizaron viajes. Un pase semanal o mensual cubre días consecutivos a partir del día en que se compra.
- **Ventana operativa:** la operación se ejecuta durante la noche del cierre de mes, dentro de la ventana de 4 horas (00:00 a 04:00) que comparte con las operaciones 1 y 2.
- **Volumen:** aproximadamente 950.000 tarjetas se utilizan al menos una vez al mes y todas deben liquidarse dentro de esa misma ventana.
- **Infraestructura:** se dispone de un único servidor de aproximadamente 500 W, sin procesamiento en paralelo ni distribuido.

| Elemento | Unidad | Límite del caso |
|---|---|---|
| Días del periodo (`d`) | días | 28 a 31 |
| Viajes por día | viajes | Entero mayor o igual a 0 |
| Costos y devoluciones | pesos enteros | Devolución mayor o igual a 0 |
| Tarjetas por cierre de mes | tarjetas | ≈ 950.000 |
| Ventana de ejecución | horas | 4 (00:00 – 04:00) |
| Potencia del servidor | vatios | ≈ 500 W |

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

#### Operación 3 · Franjas de congestión

Para la operación 3 bastan dos estructuras:

- **Lista de saldos (`list[int]`).** Contiene la serie de una estación: una posición por intervalo de 5 minutos, con el saldo neto de la plataforma (pasajeros que entraron menos los que los trenes alcanzaron a evacuar), que puede ser negativo. La lista se recibe y se recorre, pero nunca se modifica.
- **Tupla del tramo (`Tramo = tuple[int, int, int]`).** Representa la respuesta como `(inicio, fin, suma)`, con índices desde 0 e inclusivos. Es inmutable, así que un subproblema no puede alterar por accidente el resultado de otro, y ocupa espacio constante.

Dividir y vencer no necesita copiar sublistas. Cada subproblema se identifica con dos enteros, `bajo` y `alto`, que delimitan su rango dentro de la misma lista original. Si cada llamada recibiera una copia (`saldos[bajo:medio + 1]`), cada nivel de la recursión copiaría en total n saldos. Eso suma Θ(n log n) de trabajo adicional, pero la memoria máxima ocupada por las copias sería Θ(n), porque solo se mantienen las copias de una rama de recursión y sus tamaños forman una suma geométrica. Con índices, la memoria adicional se reduce a la pila de llamadas, de profundidad Θ(log n). Además, como la serie nunca se duplica ni se altera, se respeta la restricción de no modificar los datos originales.

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

La estrategia exhaustiva evalúa todas las combinaciones posibles de compra de productos tarifarios, sin almacenar los resultados de los subproblemas ya resueltos. Su complejidad espacial es Θ(d), la cual se encuentra determinada por la profundidad máxima de las llamadas recursivas. El análisis de su complejidad temporal se desarrolla en la sección 4.1.

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

### 2.3 Operación 3 · Franjas de congestión

#### Por qué el problema admite dividir y vencer

Si la serie se parte por la mitad, en `medio`, el tramo de mayor suma solo puede estar en uno de tres lugares:

1. **Completamente en la mitad izquierda** (`bajo … medio`).
2. **Completamente en la mitad derecha** (`medio + 1 … alto`).
3. **Cruzando el punto medio:** empieza en la izquierda y termina en la derecha, así que contiene obligatoriamente a `medio` y a `medio + 1`.

Los dos primeros casos son el mismo problema sobre la mitad de los datos, y se resuelven recursivamente. El tercero no es un problema recursivo: un tramo que cruza el medio es la unión de dos piezas independientes. Una es el mejor sufijo de la mitad izquierda, que termina en `medio`; la otra es el mejor prefijo de la mitad derecha, que empieza en `medio + 1`. Cada pieza se encuentra con un solo recorrido lineal desde el medio hacia afuera.

La respuesta del rango es la mayor de las tres. Como cualquier tramo consecutivo necesariamente pertenece a uno de estos casos, no se omite ninguna posibilidad y el algoritmo encuentra el máximo exacto, no una aproximación.

#### Recurrencia

Cada llamada sobre n intervalos hace dos llamadas sobre n/2 y un trabajo lineal para el tramo cruzado:

```text
T(1) = Θ(1)
T(n) = 2·T(n/2) + Θ(n)
```

Por el teorema maestro, con a = 2, b = 2 y f(n) = Θ(n), estamos en el caso 2, así que T(n) = Θ(n log n). Intuitivamente, hay log₂ n niveles de recursión y en cada nivel los recorridos de cruce suman, entre todos, n intervalos. El espacio adicional es Θ(log n), por la pila de llamadas. Para el histórico de dos años (n ≈ 166.000), la profundidad es de unas 18 llamadas.

#### Pseudocódigo

```text
TRAMO-MÁXIMO(saldos, bajo, alto):
    si bajo == alto:
        devolver (bajo, alto, saldos[bajo])
    medio ← (bajo + alto) // 2
    izq   ← TRAMO-MÁXIMO(saldos, bajo, medio)
    der   ← TRAMO-MÁXIMO(saldos, medio + 1, alto)
    cruce ← TRAMO-CRUZADO(saldos, bajo, medio, alto)
    devolver el de mayor suma entre izq, der y cruce

TRAMO-CRUZADO(saldos, bajo, medio, alto):
    mejor_izq ← −∞
    inicio ← medio
    suma ← 0
    para i desde medio bajando hasta bajo:
        suma ← suma + saldos[i]
        si suma > mejor_izq:
            mejor_izq ← suma
            inicio ← i

    mejor_der ← −∞
    fin ← medio + 1
    suma ← 0
    para j desde medio + 1 hasta alto:
        suma ← suma + saldos[j]
        si suma > mejor_der:
            mejor_der ← suma
            fin ← j

    devolver (inicio, fin, mejor_izq + mejor_der)
```

#### Ejemplo resuelto a mano

Serie de 8 intervalos (índices 0 a 7):

| Índice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Saldo | 3 | −5 | 4 | 2 | −1 | 6 | −8 | 2 |

La tabla muestra, para cada rango, los tres candidatos y el ganador. Los rangos de un solo intervalo son casos base y devuelven su propio saldo.

| Rango | Medio | Izquierdo | Derecho | Cruzado | Ganador |
|---|---:|---|---|---|---|
| [0, 1] | 0 | (0, 0, 3) | (1, 1, −5) | 3 + (−5) → (0, 1, −2) | **(0, 0, 3)** |
| [2, 3] | 2 | (2, 2, 4) | (3, 3, 2) | 4 + 2 → (2, 3, 6) | **(2, 3, 6)** |
| [4, 5] | 4 | (4, 4, −1) | (5, 5, 6) | −1 + 6 → (4, 5, 5) | **(5, 5, 6)** |
| [6, 7] | 6 | (6, 6, −8) | (7, 7, 2) | −8 + 2 → (6, 7, −6) | **(7, 7, 2)** |
| [0, 3] | 1 | (0, 0, 3) | (2, 3, 6) | Sufijo izq. −2 (desde 0) + prefijo der. 6 (hasta 3) → (0, 3, 4) | **(2, 3, 6)** |
| [4, 7] | 5 | (5, 5, 6) | (7, 7, 2) | Sufijo izq. 6 (desde 5) + prefijo der. −6 (hasta 7) → (5, 7, 0) | **(5, 5, 6)** |
| [0, 7] | 3 | (2, 3, 6) | (5, 5, 6) | Sufijo izq. 6 (desde 2) + prefijo der. 5 (hasta 5) → **(2, 5, 11)** | **(2, 5, 11)** |

En el último nivel, el cruce recorre hacia la izquierda desde el índice 3: las sumas acumuladas son 2, 6, 1 y 4, y la mejor es 6, empezando en el índice 2. Hacia la derecha desde el índice 4, las sumas son −1, 5, −3 y −1, y la mejor es 5, terminando en el índice 5.

**Respuesta: el tramo de los intervalos 2 a 5, con 4 + 2 − 1 + 6 = 11 pasajeros acumulados.** Ninguna de las dos mitades por sí sola encuentra este tramo; por eso hace falta el caso cruzado.

Conteo de operaciones del ejemplo, con el contador del código (cada intervalo sumado):

- Casos base: 8.
- Cruces de rangos de tamaño 2: 4 × 2 = 8.
- Cruces de rangos de tamaño 4: 2 × 4 = 8.
- Cruce del rango de tamaño 8: 8.

Total: **32 = n·(log₂ n + 1)**. La fuerza bruta, que evalúa todos los tramos sumando incrementalmente, hace n(n + 1)/2 = **36**. Con 8 intervalos casi no hay diferencia; la ventaja aparece al crecer n.

#### Cómo reduce el consumo energético frente a la fuerza bruta

El servidor consume una potencia aproximadamente constante, de unos 500 W bajo carga, así que la energía de un proceso es E = P × t, y el tiempo de ejecución influye directamente en el consumo. Reducir el tiempo de procesamiento puede reducir la energía utilizada.

La fuerza bruta evalúa los n(n + 1)/2 tramos posibles. Dividir y vencer hace del orden de n(log₂ n + 1) sumas. Para el histórico de dos años de una estación (n ≈ 166.000):

| Estrategia | Operaciones por estación | Para las 80 estaciones |
|---|---:|---:|
| Fuerza bruta, Θ(n²) | ≈ 1,38 × 10¹⁰ | ≈ 1,1 × 10¹² |
| Dividir y vencer, Θ(n log n) | ≈ 3,06 × 10⁶ | ≈ 2,4 × 10⁸ |

Dividir y vencer hace unas **4.500 veces menos operaciones**, y la proporción crece con la serie: si el histórico se duplica, la fuerza bruta cuadruplica su trabajo, mientras que dividir y vencer lo multiplica por poco más de 2.

Con las mediciones de ejecución se podrá estimar el consumo energético de ambas estrategias utilizando E = P × t, considerando la potencia del servidor y el tiempo que tarda cada algoritmo. Esto permite evaluar cuánto recurso se requiere para procesar el histórico completo de las estaciones.

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

Para el desarrollo del proyecto se utilizaron las siguientes herramientas y bibliotecas:

| Herramienta | Uso en el proyecto |
|---|---|
| Python 3.14.0 | Lenguaje utilizado para implementar las estrategias, desarrollar las pruebas y realizar las mediciones. |
| `random` (biblioteca estándar) | Generación de instancias sintéticas en [`datos.py`](src/tope_tarifario/datos.py). Se utiliza un generador `random.Random` con una semilla fija para garantizar que los datos sean reproducibles. |
| `time` (biblioteca estándar) | Medición de los tiempos de ejecución mediante `time.perf_counter()`, implementada en [`medicion.py`](src/tope_tarifario/medicion.py). |
| `matplotlib` | Generación de las gráficas de tiempo y número de operaciones frente al tamaño de la entrada. Es la única dependencia externa del proyecto. |
| Entorno virtual (`venv`) | Aislamiento de las dependencias del proyecto para evitar conflictos con otros entornos de Python. La carpeta `.venv/` se excluye del repositorio. |
| `requirements.txt` | Archivo que registra las dependencias necesarias para instalar y reproducir el entorno mediante `pip install -r requirements.txt` (8). |
| Git y GitHub | Control de versiones y trabajo colaborativo. Cada integrante trabaja en ramas `feature/<nombre>` creadas a partir de `development`, y los cambios se integran en esta última. La rama `main` conserva la versión estable del proyecto. El archivo `.gitignore` excluye elementos como `.venv/`, `__pycache__/` y archivos de configuración de los editores. |

Las estrategias, la solución exhaustiva y la regla actual se implementaron manualmente, sin utilizar bibliotecas de optimización ni herramientas externas que resuelvan el problema, de acuerdo con los requisitos del laboratorio. Además, el código sigue las convenciones de PEP 8 e incluye anotaciones de tipos (*type hints*) y documentación de funciones mediante *docstrings* con formato Google Style.

---

## 4. Evaluación del desempeño

### 4.1 Operación 4 · Tope tarifario

#### Complejidad temporal y espacial

En este análisis, `d` representa el número de días del periodo y `k` corresponde al número de días en los que se realizaron viajes (`k ≤ d`).

**Programación dinámica (`estrategia.py`).** El ciclo recorre los días una sola vez, desde el día `d` hasta el día 1. En un día sin viajes, únicamente copia el valor de `C(t + 1)`. En cambio, en un día con viajes, compara tres opciones: pagar los viajes de ese día, comprar un pase semanal o comprar un pase mensual. Cada comparación tiene un costo de Θ(1), porque consulta una posición de la tabla que ya está calculada.

El contador de `costo_minimo_contando` registra una operación por cada día sin viajes y tres por cada día con viajes. Por lo tanto, el total de operaciones se encuentra entre `d` y `3d`:

```text
T(d) = (d − k) · 1 + k · 3
d ≤ T(d) ≤ 3d
T(d) ∈ Θ(d)
```

El espacio adicional es Θ(d), porque se almacenan las listas `costos` y `elecciones`, cada una con `d + 2` posiciones (2.1).

**Exhaustiva (`exhaustivo.py`).** Esta estrategia no almacena los resultados de los subproblemas, por lo que vuelve a calcularlos cada vez que los encuentra. En cada día con viajes abre cuatro caminos: pagar los pasajes individuales y comprar un pase diario (ambos continúan en el día `t + 1`), comprar un pase semanal (continúa en el día `t + 7`) o comprar un pase mensual (continúa en el día `t + 30`).

Cuando todos los días tienen viajes, el número de llamadas cumple la siguiente recurrencia:

```text
T(d) = 2T(d − 1) + T(d − 7) + T(d − 30) + Θ(1)
```

Como `T(d) ≥ 2T(d − 1)`, al desarrollar la recurrencia nivel por nivel, como en un árbol de recursión, se obtiene una cota inferior de `2^d`. Es decir:

```text
T(d) ∈ Ω(2^d)
```

Esto significa que, cuando todos los días tienen viajes, cada día adicional duplica como mínimo el trabajo de la solución exhaustiva. Los días sin viajes no generan caminos nuevos, porque la función simplemente avanza al siguiente día. Por esta razón, en términos generales, el costo crece de forma exponencial respecto a `k`, es decir, los días con viajes, y no necesariamente respecto a todos los días del periodo.

Para un mes de 31 días con viajes todos los días, esto representa más de `2^31 ≈ 2.100 millones` de llamadas para una sola tarjeta.

El espacio adicional es Θ(d), correspondiente a la profundidad máxima de la pila de llamadas recursivas, ya que no se utiliza ninguna tabla para almacenar resultados.

**Regla actual (`regla_actual.py`).** Recorre cada día una sola vez: los días 1 a 30 se procesan dentro de sus bloques semanales y, si existe, el día 31 se procesa por separado. Por lo tanto, su complejidad temporal es Θ(d). Solo utiliza variables auxiliares como `total`, `costo_bloque` y los índices, por lo que su espacio adicional es Θ(1).

| Estrategia | Tiempo | Espacio adicional | ¿Resultado exacto? |
|---|---|---|---|
| Programación dinámica | Θ(d) | Θ(d) | Sí |
| Exhaustiva | Ω(2^k), exponencial en los días con viajes | Θ(d) (pila de recursión) | Sí |
| Regla actual | Θ(d) | Θ(1) | No (ver 5.1) |

**Contraste.** La programación dinámica y la regla actual pertenecen a la misma clase de complejidad temporal, Θ(d). Para un mes de 31 días, la programación dinámica realiza como máximo `3 · 31 = 93` operaciones, según el contador definido para esta estrategia.

Esto demuestra que encontrar el costo mínimo mediante programación dinámica no implica aumentar el orden de complejidad temporal respecto a la regla actual. Ambas estrategias recorren los días del periodo una sola vez. La diferencia principal está en el resultado: mientras la regla actual puede generar cobros superiores al mínimo, la programación dinámica encuentra la combinación de menor costo.

Por otro lado, la solución exhaustiva también encuentra el costo mínimo, pero su crecimiento exponencial hace que resulte poco práctica para tarjetas que registran viajes durante muchos días. Esto explica por qué una solución de este tipo no sería adecuada para procesar el volumen real de tarjetas dentro de la ventana operativa.

Cabe resaltar que la programación dinámica obtiene el mismo resultado exacto que la solución exhaustiva porque calcula cada subproblema una sola vez y almacena su resultado para reutilizarlo, evitando repetir cálculos innecesariamente.

#### Verificación

La verificación se realiza mediante el archivo [`pruebas.py`](src/tope_tarifario/pruebas.py), en el que se utiliza la solución exhaustiva como referencia para comparar los resultados obtenidos por la programación dinámica. Si ambas estrategias obtienen el mismo costo en diferentes instancias, se obtiene evidencia de que la tabla de programación dinámica se está construyendo correctamente y de que sus resultados coinciden con los de la solución exhaustiva.

Las instancias aleatorias se generan mediante [`datos.py`](src/tope_tarifario/datos.py), utilizando la semilla fija 2026. De esta manera, cualquier persona que ejecute las pruebas obtendrá exactamente las mismas instancias. Para ejecutarlas, se utiliza el siguiente comando:

```bash
python src/tope_tarifario/pruebas.py
```

Las pruebas se organizan en cinco grupos:

| Grupo | Función | Qué verifica |
|---|---|---|
| Casos límite | `probar_casos_limite` | Periodo vacío (`[]`), un día sin viajes, un mes completo sin viajes, un solo día con 1, 2, 3 y 10 viajes, meses de 28 a 31 días con muchos viajes y un pase semanal que se sale del mes. |
| Ejemplo a mano | `probar_ejemplo_a_mano` | La tabla de 2.2 fila por fila (C(1) a C(9)), las elecciones y las compras reconstruidas. |
| Instancias aleatorias | `probar_instancias_aleatorias` | 160 instancias en las que la programación dinámica y la solución exhaustiva obtienen el mismo costo. |
| Devolución exacta | `probar_devolucion_exacta` | Que la devolución sea exactamente igual a `cobrado - mínimo` y que nunca sea negativa. |
| Contraejemplo | `probar_contraejemplo` | Que la regla actual cobre 45.500 pesos frente a los 39.900 pesos del óptimo en la instancia de 5.1. |

**Casos límite.** Además de los casos sin viajes, se escogieron situaciones que permiten revisar los puntos en los que cambia la mejor decisión:

- Un día con 2 viajes cuesta 7.800 pesos en pasajes. Con 3 viajes conviene comprar el pase diario de 9.500 pesos, ya que los pasajes individuales costarían 11.700 pesos.
- Tres días con 3 viajes cuestan 28.500 pesos en pases diarios, valor que todavía es menor que el de un pase semanal. Con cuatro días, el costo de los pases diarios sería de 38.000 pesos, por lo que conviene comprar el pase semanal de 36.000 pesos.
- En meses de 28, 29 y 30 días con muchos viajes, el costo corresponde al pase mensual de 135.000 pesos. En un mes de 31 días, el pase mensual no alcanza a cubrir el último día, por lo que el costo es de 135.000 + 9.500 = 144.500 pesos, de acuerdo con el supuesto de 1.5.
- Un mes con viajes únicamente durante los últimos cuatro días puede cubrirse con un pase semanal comprado el día 27, aunque este alcance hasta el día 33. Esto permite comprobar el límite `min(t + 7, d + 1)` de la recurrencia.

**Instancias aleatorias.** Se probaron dos grupos de instancias:

- **120 periodos cortos:** de 1 a 12 días, con 10 instancias por tamaño y viajes en casi todos los días. Se utilizan estos tamaños porque la solución exhaustiva puede terminar su ejecución en un tiempo razonable.
- **40 meses reales:** de 28 a 31 días, con solo 6 a 12 días con viajes. Como la solución exhaustiva crece según los días con viajes y no únicamente según la duración del mes, estos casos permiten ejecutar las pruebas e incluir situaciones relacionadas con el pase mensual y el día 31.

En cada instancia no solo se compara el costo obtenido por ambas estrategias. También se revisa que:

- Las compras reconstruidas mediante `reconstruir_compras` cubran todos los días con viajes y sumen exactamente C(1). Para comprobarlo, se utiliza la función auxiliar `costo_de_compras`, que vuelve a calcular el costo a partir de las compras realizadas, sin consultar la tabla de programación dinámica.
- La regla actual nunca cobre menos que el costo mínimo, porque siempre construye una combinación válida de productos.
- La lista de entrada no se modifique después de ejecutar las funciones.

**Devolución exacta.** Esta es una de las restricciones principales del problema. Se comprueba mediante valores calculados manualmente: si se cobraron 45.500 pesos, se deben devolver 5.600; si se cobró exactamente el mínimo o un valor inferior, la devolución debe ser 0. También se realizan pruebas con 30 tarjetas aleatorias en las que el valor cobrado corresponde al calculado por la regla actual. En todos los casos, el valor cobrado menos la devolución debe coincidir exactamente con el costo mínimo obtenido por la solución exhaustiva.

**Resultado.** Todas las pruebas pasan y el script finaliza mostrando el mensaje `Todas las pruebas pasaron`.

**Limitación de la verificación.** La solución exhaustiva toma las decisiones de la misma forma que la programación dinámica, pero sin almacenar los resultados de los subproblemas. Por esta razón, permite detectar errores en los índices, el orden de llenado de la tabla y la reconstrucción de las compras, pero no necesariamente errores en el modelo del problema, como establecer incorrectamente la duración de un pase.

Para reducir este riesgo, también se utilizan el ejemplo resuelto manualmente y los casos límite, cuyos resultados se calcularon sin depender del código implementado.

#### Diseño de los experimentos

Los experimentos se realizan mediante [`medicion.py`](src/tope_tarifario/medicion.py), mientras que las instancias se generan con la función `generar_instancias` de [`datos.py`](src/tope_tarifario/datos.py), utilizando la semilla fija `2026`. Para cada tamaño de entrada, las tarjetas se generan una sola vez y las tres soluciones se ejecutan sobre las mismas instancias, lo que permite realizar una comparación bajo condiciones equivalentes.

Cada día tiene una probabilidad de 0,9 de registrar viajes. Cuando hay viajes, se generan entre 1 y 4. De esta manera, la cantidad de días con viajes aumenta a medida que crece `d`, lo que permite analizar el comportamiento de las estrategias frente a entradas de mayor tamaño.

Se utilizan tres series de experimentos:

| Serie | Tamaños `d` (días) | Tarjetas por tamaño | Soluciones medidas | Propósito |
|---|---|---:|---|---|
| 1 · Periodos cortos | 6, 8, 10, 12, 14, 16, 18 y 20 | 5 | DP, exhaustiva y regla actual | Comparar la programación dinámica con la solución exhaustiva en tamaños donde esta última todavía puede ejecutarse. |
| 2 · Periodos largos | 1.000, 2.000, 5.000, 10.000, 20.000, 50.000 y 100.000 | 3 | DP y regla actual | Analizar el crecimiento lineal de ambas estrategias con entradas de mayor tamaño. |
| 3 · Volumen real | 30 | 2.000 | DP y regla actual | Medir el tiempo por tarjeta para un periodo de 30 días y utilizarlo como base de la extrapolación. |

Los tamaños menores y mayores a 31 días se utilizan como instancias sintéticas para estudiar el crecimiento de los algoritmos. No representan la duración de un mes real, que en el caso planteado está entre 28 y 31 días.

Las condiciones de medición son las siguientes:

- **Parejas `d` y `2d`:** la serie 1 incluye las parejas 6→12, 8→16 y 10→20. La serie 2 incluye 1.000→2.000, 5.000→10.000, 10.000→20.000 y 50.000→100.000.
- **Repeticiones:** cada medición se repite 5 veces y se reporta el tiempo medio por tarjeta, con el propósito de reducir el efecto de las variaciones del sistema operativo.
- **Cronómetro:** `time.perf_counter()` mide únicamente el tiempo de ejecución de cada solución. La generación de los datos queda por fuera de la medición.
- **Verificación dentro del experimento:** antes de medir cada tamaño de la serie 1, se comprueba mediante `assert` que la programación dinámica y la solución exhaustiva obtengan el mismo costo para todas las tarjetas.
- **Operaciones elementales:** cada estrategia utiliza un contador propio. En la programación dinámica se cuentan las opciones evaluadas (`costo_minimo_contando`); en la solución exhaustiva, las llamadas recursivas (`costo_exhaustivo_contando`); y en la regla actual, los días procesados (`costo_regla_actual_contando`).
- **Límite de la solución exhaustiva:** las mediciones de esta estrategia se detienen en `d = 20`, donde alcanza un tiempo cercano a 0,29 segundos por tarjeta. Su crecimiento impide continuar con tamaños mayores en condiciones razonables de medición.
- **Equipo de medición:** procesador AMD Ryzen 5 7600X (6 núcleos, 12 hilos) y 32 GB de memoria RAM DDR5 a 4800 MHz, con Python 3.14.0. Las mediciones se ejecutaron en un solo hilo. El experimento completo tarda menos de 30 segundos.

#### Resultados

![Tiempo frente al tamaño – tope tarifario](graficas/tope_tarifario/tiempo_vs_n.png)

![Operaciones frente al tamaño – tope tarifario](graficas/tope_tarifario/operaciones_vs_n.png)

En las gráficas se observa el comportamiento de las tres estrategias a medida que aumenta el tamaño de la entrada. En el panel izquierdo se utiliza una escala logarítmica en el eje `y`, lo que permite visualizar las diferencias entre los tiempos de ejecución. En esta escala, la solución exhaustiva forma una línea recta ascendente, lo que indica un crecimiento exponencial, mientras que la programación dinámica y la regla actual se mantienen casi planas.

En el panel derecho, que utiliza una escala lineal, se observa que tanto el tiempo como el número de operaciones de la programación dinámica y de la regla actual aumentan de manera aproximadamente proporcional a `d`.

A continuación, se presentan algunas mediciones representativas de los experimentos:

| `d` | DP (ms) | Exhaustiva (ms) | Regla actual (ms) | Operaciones DP | Operaciones exhaustiva | Operaciones regla |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 0,0031 | 0,022 | 0,0009 | 17 | 218 | 6 |
| 10 | 0,0027 | 0,321 | 0,0013 | 28 | 2.846 | 10 |
| 12 | 0,0034 | 1,194 | 0,0014 | 34 | 11.400 | 12 |
| 16 | 0,0040 | 16,144 | 0,0018 | 46 | 158.031 | 16 |
| 20 | 0,0052 | 290,197 | 0,0019 | 58 | 2.813.425 | 20 |
| 10.000 | 2,707 | — | 0,726 | 28.019 | — | 10.000 |
| 20.000 | 5,456 | — | 1,429 | 56.028 | — | 20.000 |
| 100.000 | 28,589 | — | 7,146 | 280.090 | — | 100.000 |

#### Lo medido contra lo esperado

Para comparar el comportamiento experimental con el análisis teórico, se utilizan parejas de tamaños `d` y `2d`. Se calcula cuánto aumentan el tiempo de ejecución y el número de operaciones al duplicar el tamaño de la entrada.

| Pareja | Solución | Factor de tiempo | Factor de operaciones | Factor esperado |
|---|---|---:|---:|---:|
| 10 → 20 | Exhaustiva | ×905 | ×989 | ≈ 2^10 = 1.024 |
| 10 → 20 | DP | ×1,94 | ×2,04 | 2 |
| 10 → 20 | Regla actual | ×1,51 | ×2,00 | 2 |
| 10.000 → 20.000 | DP | ×2,02 | ×2,00 | 2 |
| 10.000 → 20.000 | Regla actual | ×1,97 | ×2,00 | 2 |
| 50.000 → 100.000 | DP | ×2,07 | ×2,00 | 2 |

A partir de estos resultados, se identifican los siguientes comportamientos:

- **Programación dinámica y regla actual:** al duplicar `d`, el número de operaciones se duplica. En la serie de periodos largos, el tiempo de ejecución aumenta aproximadamente entre 1,9 y 2,1 veces. Estos resultados coinciden con el crecimiento lineal esperado, Θ(d). En la programación dinámica se realizan aproximadamente 2,8 operaciones por día, debido a que el 90 % de los días tienen viajes y requieren evaluar tres opciones, mientras que los días sin viajes requieren una sola operación. Esto se mantiene dentro del rango `d ≤ T(d) ≤ 3d` establecido en el análisis de complejidad.

- **Solución exhaustiva:** al pasar de 10 a 20 días, el número de operaciones aumenta aproximadamente 989 veces, un valor cercano a `2^10 = 1.024`. El tiempo de ejecución aumenta aproximadamente 905 veces. Esto evidencia un crecimiento exponencial, coherente con la cota inferior Ω(2^d) obtenida para el caso en el que todos los días tienen viajes. El factor observado puede ser menor debido a que aproximadamente el 10 % de los días no registran viajes y no generan nuevas ramas de decisión. Cabe aclarar que esta medición es una evidencia empírica y no una demostración: muestra que, en estas instancias, cada día adicional casi duplica el trabajo, pero no prueba una cota superior. La recurrencia solo garantiza que el trabajo está entre Ω(2^d) y O(4^d), porque cada día con viajes abre como máximo cuatro caminos.

- **Diferencias en las mediciones:** en la serie de periodos cortos, los tiempos de la programación dinámica y de la regla actual son de pocos microsegundos. En estos tamaños, el costo fijo de llamar las funciones y crear las listas tiene una influencia importante sobre el tiempo total. Por esta razón, los factores de crecimiento presentan algunas variaciones. Por ejemplo, entre 6 y 12 días, la programación dinámica aumenta aproximadamente ×1,09, mientras que entre 10 y 20 días la regla actual aumenta ×1,51. Incluso se observa que la programación dinámica tarda más con 6 días que con 8. En la serie de periodos largos, este efecto pierde importancia y los factores se acercan a 2. El contador de operaciones no presenta estas variaciones, ya que no depende del tiempo de ejecución del computador.

- **Programación dinámica frente a regla actual:** ambas estrategias presentan crecimiento lineal, pero la programación dinámica tiene un mayor costo constante por día. Para `d = 100.000`, tarda 28,589 ms, frente a 7,146 ms de la regla actual. Esto representa una diferencia aproximada de cuatro veces, debido a que la programación dinámica evalúa varias opciones y almacena resultados en dos tablas por día. Sin embargo, ambas estrategias mantienen el mismo orden de complejidad temporal.

#### Extrapolación al volumen real

El tiempo total de un cierre de mes se estima multiplicando el tiempo promedio por tarjeta por el número total de tarjetas que deben procesarse, aproximadamente 950.000. Como las tarjetas se liquidan de manera independiente y una por una, el tiempo total aumenta proporcionalmente al número de tarjetas.

Para realizar esta estimación se utilizan los siguientes criterios:

- **Programación dinámica y regla actual:** no es necesario extrapolar el tamaño `d`, porque el tiempo por tarjeta se midió directamente para un periodo de 30 días, utilizando 2.000 tarjetas en la serie 3.
- **Solución exhaustiva:** no fue posible medir esta estrategia para 30 días debido a su crecimiento exponencial. Por esta razón, se hace una extrapolación empírica a partir del comportamiento observado entre `d = 10` y `d = 20`, donde el tiempo aumenta aproximadamente por un factor de 1,975 por cada día adicional. Partiendo de 0,290 segundos para `d = 20`, se estima el tiempo para 30 días mediante:

```text
t(30) ≈ 0,290 s · 1,975^10
t(30) ≈ 262 s por tarjeta
```

En este caso no sería adecuado utilizar una regla de tres lineal, ya que el crecimiento observado es exponencial y no proporcional al tamaño de la entrada. Este valor es una aproximación, no una garantía matemática: supone que el factor de 1,975 por día se mantiene entre 20 y 30 días, y corresponde a una tarjeta como las sintéticas, con viajes en aproximadamente el 90 % de los días.

Los tiempos estimados para procesar las 950.000 tarjetas son:

| Solución | Tiempo por tarjeta (d = 30) | Tiempo para 950.000 tarjetas | ¿Cabe en la ventana de 4 h? |
|---|---:|---:|---|
| Programación dinámica | 7,0 µs | ≈ 6,7 s | Sí |
| Regla actual | 2,6 µs | ≈ 2,5 s | Sí |
| Exhaustiva (estimada) | ≈ 262 s | ≈ 69.300 h (≈ 8 años) | No |

La programación dinámica permitiría liquidar todas las tarjetas en menos de 10 segundos, utilizando menos del 0,1 % de la ventana de 4 horas, que además comparte con las operaciones 1 y 2.

Por el contrario, la solución exhaustiva no sería viable para este volumen de procesamiento: necesitaría aproximadamente 8 años para completar un solo cierre de mes bajo las condiciones estimadas. Para un periodo de 31 días con viajes todos los días, el tiempo sería todavía mayor.

Estas estimaciones dependen del computador utilizado para realizar las mediciones, que no necesariamente tiene las mismas características del servidor del SITVM. También dependen de la distribución de los viajes en las tarjetas sintéticas. Las tarjetas reales que registran viajes durante menos días pueden requerir menos tiempo en la solución exhaustiva; sin embargo, las tarjetas con viajes frecuentes representan un costo computacional considerablemente mayor.

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

La regla actual decide cada bloque de días por separado: toma la opción más barata y no vuelve atrás, como haría una estrategia voraz. Esa forma de decidir sería suficiente, y daría el mínimo, en cualquiera de estos dos escenarios:

- **Solo existen el pasaje sencillo y el pase diario.** Ningún producto cubre más de un día, así que lo que se compra un día no cambia lo que conviene comprar otro. El mínimo del mes es simplemente la suma del mínimo de cada día.
- **Los pases son de calendario fijo.** Si el semanal solo pudiera usarse en las semanas 1–7, 8–14, 15–21, 22–28 y 29–30, y el mensual solo del día 1 al 30, cada bloque se podría decidir sin mirar los demás. En ese caso, la regla de bloques fijos del 1.5 daría exactamente el costo mínimo.

En el SITVM no se cumple ninguna de las dos condiciones. El semanal y el mensual cubren días consecutivos a partir del día en que se compran, y ese día puede ser cualquiera. Por eso, una compra condiciona los días siguientes, y el mejor momento para empezar un pase depende de los viajes que vienen después. Es lo que muestra el contraejemplo: el semanal óptimo empieza el día 4 y no el día 1. Para encontrar ese punto de inicio hay que comparar los subproblemas de todos los días posibles, que es justamente lo que hace la programación dinámica.

#### Recomendación

Recomendamos que el SITVM liquide el tope tarifario con la programación dinámica y deje de usar la regla simplificada.

**Qué gana frente a hoy:**

- **Cumple la política del tope sin excepciones.** La DP siempre encuentra la combinación más barata, así que la devolución es exactamente la diferencia frente al mínimo, sin un peso de más ni de menos. La regla actual puede cobrar de más cuando los viajes de una persona no coinciden con los bloques fijos: 5.600 pesos en el contraejemplo de ocho días.
- **Elimina la causa de las quejas sin costo adicional de tiempo.** Ya no hace falta tratar distinto a las tarjetas que más viajan, que hoy reciben la regla simplificada porque la exhaustiva no termina. Liquidar 950.000 tarjetas con la DP toma cerca de 6,7 s, menos del 0,1 % de la ventana de 4 h. La exhaustiva tardaría unos 8 años por cierre.
- **El costo energético es despreciable.** La DP consume unos 0,007 kWh más al año que la regla actual (6.1). A cambio, todos los usuarios reciben lo que les corresponde.
- **Deja trazabilidad.** Además del valor, la DP puede entregar la lista de compras que justifica cada liquidación. Sirve para responder una reclamación con el detalle de qué pases se consideraron.

**Riesgos y límites que debe conocer:**

- **Cambios de tarifa o de productos.** El tiempo crece de forma lineal con los días y con el número de productos, así que un pase nuevo (por ejemplo, uno quincenal) no compromete la ventana. Lo que sí cambia es el modelo: hay que agregar el producto a la recurrencia y volver a correr las pruebas contra la exhaustiva antes de usarlo en producción.
- **Pases que cruzan el cierre de mes.** La solución supone que cada mes se liquida por separado (1.5). Si el SITVM reconoce un semanal comprado el día 28 que sigue vigente en el mes siguiente, la liquidación tendría que mirar los dos meses juntos. Esa regla de negocio debe confirmarse con Recaudo.
- **Crecimiento del volumen.** El tiempo total crece en proporción al número de tarjetas. Aun si se multiplicaran por 100, la operación seguiría tomando del orden de minutos, muy lejos del límite de la ventana.
- **Las cifras de tiempo vienen de nuestro computador.** El servidor del SITVM puede ser más rápido o más lento. Antes del primer cierre conviene medir en el servidor real; el margen es tan amplio que la conclusión no debería cambiar. También conviene ejecutar la DP sobre los registros de algunos meses reales para cuantificar el monto total que se debe devolver.

### 5.2 Operación _X_ y comparación general
_Pendiente para la entrega del 23 de noviembre._

---

## 6. Implicaciones éticas, sociales y ambientales

### 6.1 Consumo energético

#### Operación 4 · Tope tarifario

La energía se estima con **kWh = kW × h**, con el servidor de 0,5 kW que informa el caso y los tiempos de la extrapolación (4.1). La operación corre una vez por mes, en el cierre, así que en un año son 12 ejecuciones.

| Solución | Horas por cierre | kWh por cierre | kWh por año (12 cierres) |
|---|---:|---:|---:|
| Programación dinámica | 0,00185 | 0,00093 | 0,011 |
| Regla actual | 0,00069 | 0,00035 | 0,004 |
| Exhaustiva (estimada) | ≈ 69.300 | ≈ 34.600 | ≈ 416.000 |

- **Regla actual frente a DP:** la DP consume unos **0,007 kWh más por año**. Es una cantidad despreciable, del orden de tener encendido un bombillo LED de 10 W durante menos de una hora. A cambio, la DP elimina los cobros de más que hoy genera la regla, como los 5.600 pesos del contraejemplo de 5.1.
- **Exhaustiva:** sus 34.600 kWh por cierre y 416.000 kWh por año son una cifra hipotética, que solo muestra la magnitud del problema. **No representan un consumo operativo real**, porque cada cierre tomaría casi 8 años y la ejecución nunca terminaría dentro de la ventana de 4 horas: en la práctica, la solución exhaustiva no se puede operar.
- **Supuestos:** son estimaciones. Se asume que el servidor consume sus 500 W solo durante el cálculo, y no se incluyen la lectura de datos, la escritura de las devoluciones ni el consumo del servidor en reposo, que es el mismo para todas las soluciones.

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

Los comandos se probaron desde una copia limpia del repositorio, con un entorno virtual nuevo.

```bash
# 1. Clonar el repositorio
git clone https://github.com/SESASAN/analisis-algoritmos-caso1-sitvm.git
cd analisis-algoritmos-caso1-sitvm

# 2. Crear y activar el entorno
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Pruebas de la operación 4 (terminan con "Todas las pruebas pasaron")
python src/tope_tarifario/pruebas.py

# 4. Mediciones y gráficas (menos de 30 s; se guardan en graficas/tope_tarifario/)
python src/tope_tarifario/medicion.py
```

`medicion.py` imprime en la terminal los factores al duplicar `d`, la extrapolación a 950.000 tarjetas y la energía estimada, y vuelve a generar `tiempo_vs_n.png` y `operaciones_vs_n.png`. Como la semilla es fija, las instancias y el número de operaciones son siempre los mismos; los tiempos cambian un poco según el computador.

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
