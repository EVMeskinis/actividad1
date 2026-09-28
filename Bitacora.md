# Bitácora – Actividad 1

**Fecha:** Entrega 28 de septiembre 2026

Debo reconocer que me costó arrancar la actividad porque tenía muchas dudas sobre la estructura y el punto de partida.

En un momento de la clase previa a esta entrega, Sofía nos sugirió que arrancáramos a pensar un rol, entonces tomé ese puntapié. Asimismo, entendí que se podía usar más de un archivo dentro del directorio `src`, y me pareció la manera más fácil para mí.

Debí recurrir a la IA para que me ayude con las partes técnicas del armado y para ir entendiendo las estructuras que fuimos viendo en clase; sinceramente, necesitaba que me dé ejemplos prácticos concretos y me ayude a ir entendiendo la lógica. Además, si bien yo tenía cuenta en GitHub, la IA me ayudó a armar un nuevo repositorio.

Adicionalmente, respecto al archivo **datos.py**, la IA me recomendó que allí solo guardara información, porque además de mi propia comodidad y utilidad para poder entender y concretar el caso, es ventajoso a los fines de la reutilización eficiente, ya que si, hipotéticamente, se requiriese un cambio en las columnas o los roles, se modificaría este archivo y las funciones de `informe.py` no se tocarían.

En este orden de ideas, la IA me sugirió que configurara los tres roles para que cada uno pruebe algo distinto: el docente ordena por nombre ascendente y sin umbral mínimo, el investigador por completitud descendente con umbral 80 (CAT_OCUP y GDECCFR quedan fuera porque su completitud no llega al umbral mínimo), y el analista por completitud ascendente con umbral 50.

## Armado

Es dable destacar que los porcentajes de completitud son inventados, simplemente los elegí para que sean creíbles: 100 en datos que siempre se registran (PONDERA, ANO4, REGION); CAT_OCUP bajo (45,3) porque solo aplica a personas ocupadas; ITF y GDECCFR incompletos porque mucha gente no declara ingresos. Pero, sobre todo, para poder probar el filtro: con los umbrales de 80 y 50, cada rol da un resultado distinto. Si todos fueran 100, el filtro nunca excluiría nada.

### Parte 1: las columnas

La consigna pide guardar tres cosas de cada columna: nombre, tipo de dato y porcentaje de completitud.

Esto se podría haber pensado como una lista de tuplas:

```python
COLUMNAS = [
    ("PONDERA", "int", 100.0),
    ("EDAD", "int", 99.8),
]
```

Funciona, pero para encontrar EDAD habría que recorrer toda la lista si no conozco el índice de la posición donde se encuentra el elemento al que quisiera acceder. Por eso elegí un diccionario de diccionarios, porque buscar por clave (nombre de las columnas): `COLUMNAS["EDAD"]` es inmediato, sin importar si hay 11 o 500 columnas. Entonces, esto tiene dos ventajas: puedo acceder directamente, por ejemplo: `COLUMNAS["EDAD"]["completitud"]`, y si mañana quisiera agregar un dato más de cada columna sumaría una clave sin romper el código.

### Parte 2: los roles

La misma idea: un diccionario donde la clave es el nombre del rol.

Las columnas las puse en una lista y al docente no le establecí un porcentaje mínimo de completitud, pero al investigador y analista sí para poder probar ambos casos.

Al final agregué dos tuplas con los valores permitidos, que después usa el archivo `informe.py` para validar:

```python
CRITERIOS_VALIDOS = ("nombre", "completitud")
ORDENES_VALIDOS = ("A", "B")
```

Son tuplas y no listas porque no deberían cambiar.

### informe.py

Luego del archivo de datos, arranqué con **informe.py**. Tiene cinco funciones que trabajan como una línea de producción, cada una hace una sola tarea y le pasa el resultado a la siguiente:

- **A. `armar_filas`:** toma los nombres de las columnas y busca sus datos.
- **B. `filtrar_por_completitud`:** saca las que no llegan al mínimo.
- **C. `ordenar_filas`:** las ordena según el criterio.
- **D. `generar_informe`:** coordina las tres anteriores según el rol.
- **E. `mostrar_informe`:** imprime la tabla.

Separarlas así es lo que las hace reutilizables: si en otro momento piden otro filtro, agregaría una función sin tocar las demás.

## A. armar_filas

En `armar_filas` usé `lambda` que recibe `n` y devuelve `True` si `n` es una clave de `COLUMNAS`. A su vez, `filter` recorre la lista de columnas y se queda solo con los elementos para los que la función da `True` (lo entiendo como filtrar una columna en Excel).

`map` recorre la lista y transforma cada elemento con la función. Me costó entender su uso, pero su aplicación la pensé así. La clave la uso para abrir y sacar los datos:

```python
columnas["EDAD"]
columnas["EDAD"]["tipo"]
columnas["EDAD"]["completitud"]
```

O sea, el `map` arma con eso la tupla `("EDAD", "int", 99.8)`:

```python
lambda n: (n, columnas[n]["tipo"], columnas[n]["completitud"])
```

En resumen, esta función:

1. Filtra para quedarse solo con las columnas que existen. Si no lo hiciera, por ejemplo, `columnas["SEXO"]` rompería el programa con un `KeyError`.
2. Transforma cada nombre en una tupla (para evitar cambios accidentales) con sus tres datos.

La IA me ayudó a entender la diferencia entre list comprehension y `for` con `.append`, y así poder elegir lo más conveniente para mi código. Las dos recorren la lista una vez, así que hacen la misma cantidad de trabajo. La diferencia está en que, en cada vuelta, Python tiene que buscar el método `.append` y llamarlo, mientras que la comprehension está optimizada internamente para construir la lista de una. En listas grandes suele ser más rápida. Entonces:

- **Legibilidad:** en una línea se lee "quedate con los nombres que no están en columnas", sin tener que seguir un bucle.
- **Eficiencia:** evita llamar a `.append` en cada vuelta.
- **Criterio de uso:** la lógica es simple (recorrer, filtrar, guardar). Si fuera más compleja, elegiría el `for`.

## B. filtrar_por_completitud

```python
return list(filter(lambda fila: fila[2] >= minimo, filas))
```

- `filas` son las tuplas que devolvió `armar_filas`, por ejemplo `("EDAD", "int", 99.8)`.
- `fila[2]` es la completitud, la posición 2 de la tupla. `fila[0]` es el nombre y `fila[1]` el tipo.
- `filter` se queda solo con las filas cuya completitud es mayor o igual al mínimo.

Establecí por defecto `minimo=0`, es decir, si no se indica un mínimo, no filtra nada. Por eso sirve para el docente, que no tiene umbral.

## C. ordenar_filas

Por defecto, `criterio="completitud"` y `orden="B"`, que también se usan en caso de que un criterio u orden sean inválidos. La función tiene dos partes:

- **Validación:** revisa que el criterio y el orden estén entre los permitidos, usando las tuplas que definí en `datos.py`. Por ejemplo, si alguien pide ordenar por "promedio", en lugar de romper el código, avisa y usa el valor por defecto.
- **Ordenamiento:** la posición decide por qué dato de la tupla ordenar: si el criterio es "nombre", la posición 0; si no, la 2 (completitud). `descendente` vale `True` si el orden es "B" y `False` si es "A".

`sorted` devuelve una lista nueva ordenada y no modifica la original.

## D. generar_informe

Tiene tres caminos posibles.

**Camino 1: sin rol (`rol is None`).** `rol=None` como parámetro significa que, si llamo `generar_informe()` sin nada entre paréntesis, `rol` vale `None`. `columnas.keys()` devuelve todas las claves del diccionario, o sea, los 11 nombres. `list(...)` las convierte en lista, que es lo que espera `armar_filas`. No filtra: ordena directo por completitud descendente.

**Camino 2: rol inexistente.** Ejemplo: "gerente", que no está entre las claves de `roles`: el programa avisa, muestra los roles disponibles y devuelve una lista vacía. Devuelve `[]` en lugar de romperse para que `mostrar_informe` pueda seguir funcionando: recibe una lista vacía e imprime "(sin columnas para mostrar)".

**Camino 3: rol válido.**

1. `config = roles[rol]` saca el diccionario chico del rol. Si es el investigador, `config` es `{"columnas": [...], "criterio": "completitud", "orden": "B", "minimo": 80}`.
2. `armar_filas` convierte sus nombres en tuplas.
3. `filtrar_por_completitud` aplica el mínimo. Con `.get("minimo", 0)`, si el rol no tiene mínimo usa 0.
4. `ordenar_filas` ordena según el criterio y el orden del rol.

Se filtra antes de ordenar.

**Pregunta que me hice:** ¿qué pasaría si al llamar a la función sin nada quisiera que salga el informe del docente? Posibles soluciones:

- Cambiar el camino 1 y reescribirlo, sin el `return`, para que siga hasta el camino 3:

  ```python
  if rol is None:
      rol = "docente"
  ```

- Cambiar el valor por defecto (`rol="docente"`): es lo más corto, pero si se pasa `None` explícitamente, sigue saliendo el informe de todas las columnas.
- Usar una constante `ROL_POR_DEFECTO = "docente"` en `datos.py` y usarla en `informe.py` con `rol = ROL_POR_DEFECTO` (agregándola previamente al import).

## E. mostrar_informe

Finalmente, la IA me ayudó a armar la función `mostrar_informe` de manera que las columnas se vean de manera ordenada y pareja.

## Adicionales

La IA me ayudó a:

1. Detectar un problema con VS Code en modo restringido.
2. Agregar como extensión Flake8, herramienta para chequear que mi código cumpla con la PEP 8, porque aún me cuesta sacarme el "chip" Pascal en Geany. Gracias a ello, descubrí varios errores: alinear con espacios extra, líneas de más de 79 caracteres, y observé cómo partirlas en el código.
3. Entender por qué me aparecía una nueva carpeta en `src` llamada `__pycache__`.
4. Entender el funcionamiento de un commit, su carga e importancia.
5. Entender que `dict()` también crea diccionarios y el uso de `.get()`.

Además:

- Probé `.keys()` en otros ejemplos vistos en clases teóricas para fijar su funcionamiento.
- Realicé varias pruebas en Jupyter a medida que me iban surgiendo dudas o inquietudes sobre mi código y lo que retornaba la función. Ejemplo: la columna SEXO que no existe, el rol "gerente", el criterio "promedio" con orden "X", y el empate entre PONDERA y ESTADO.
- El notebook daba `NameError` aunque yo había importado la función; al reiniciar y ejecutar todo entendí que las celdas corren de arriba hacia abajo y que el import estaba después.
- Al usar el `.gitignore` para que no aparezcan carpetas no deseadas en el repositorio, me di cuenta de que no ignoraba `__pycache__`, ya que la carpeta seguía en color verde. Logré reconocer que el problema eran los espacios al principio de las líneas.
- Como mencioné al inicio, en caso de que tenga que agregar una columna nueva, solo modifico el archivo `datos.py`. En el informe sin rol aparece automáticamente, porque `generar_informe` usa `list(columnas.keys())`. En un rol, aparece solo si se agrega su nombre a la lista de columnas de ese rol. Alternativa: si el rol usa `"columnas": list(COLUMNAS.keys())`, ve todas las columnas, incluidas las nuevas, sin escribirlas a mano. Funciona porque `COLUMNAS` se define antes que `ROLES`.

## Modificaciones del examen

### Modificación 1: rol gestor_politicas

- **Qué pedía:** agregar un rol `gestor_politicas` que vea REGION, AGLOMERADO, MAS_500, ITF y GDECCFR, ordenado por completitud descendente y sin umbral.
- **Qué cambié y dónde:** agregué el rol en `ROLES`, dentro de `datos.py`. No toqué `informe.py`.
- **Por qué así:** las funciones de `informe.py` tratan a todos los roles por igual, así que un rol nuevo funciona sin modificarlas. No incluí `"minimo"` porque `generar_informe` usa `config.get("minimo", 0)`: si el rol no tiene mínimo, usa 0 y no filtra nada. Cargué las columnas en el orden del enunciado, porque REGION y AGLOMERADO empatan en 100 y `sorted` respeta el orden de la lista.
- **Caso de prueba:** en el notebook, el informe del rol mostró REGION, AGLOMERADO, MAS_500, ITF y GDECCFR, en ese orden y sin filtrar, tal como había predicho antes de ejecutar.

### Modificación 2: columna NIVEL_ED

- **Qué pedía:** agregar la columna NIVEL_ED (int, 88 % de completitud) sin tocar los roles, e indicar en qué informes aparece y por qué.
- **Qué cambié y dónde:** agregué `"NIVEL_ED": {"tipo": "int", "completitud": 88.0}` en `COLUMNAS`, dentro de `datos.py`.
- **Por qué aparece solo sin rol:** sin rol, `generar_informe` toma todas las columnas con `list(columnas.keys())`, por eso la columna nueva aparece automáticamente. Los roles tienen su propia lista de columnas escrita a mano, y NIVEL_ED no está en ninguna. Para que un rol la vea, habría que agregarla a su lista.
- **Caso de prueba:** en el informe sin rol apareció NIVEL_ED con 88,0 %, entre MAS_500 e ITF; en los cuatro roles no apareció.
- **Qué no funcionó:** la primera vez NIVEL_ED no aparecía. Me di cuenta de que Python seguía usando la versión anterior de `datos.py`: tuve que guardar el archivo y reiniciar el kernel antes de ejecutar todo.

### Modificación 3: uso de filter() y map()

- **Qué pedía:** explicar las ventajas de `filter()`/`map()` frente a un `for`, si los había usado.
- **Dónde los usé:** en `armar_filas`, `filter()` descarta las columnas inexistentes y `map()` convierte cada nombre en una tupla; en `filtrar_por_completitud`, `filter()` se queda con las filas que llegan al mínimo.
- **Ventajas frente al for:** el código dice qué hace y no cómo recorrer la lista; no necesita una lista vacía ni `append`, así que hay menos variables auxiliares y menos errores; no crea listas intermedias; y cada función hace una sola tarea, lo que facilita modificarla.
- **Caso de prueba:** `filtrar_por_completitud(filas, 80)` dejó afuera CAT_OCUP y GDECCFR.

