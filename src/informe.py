"""
Lógica del informe: arma, filtra y ordena columnas según un rol.

Las funciones reciben la configuración por parámetro (con valores por
defecto tomados de datos.py), así se pueden probar con otros datos.
"""

from src.datos import COLUMNAS, ROLES, CRITERIOS_VALIDOS, ORDENES_VALIDOS


def armar_filas(nombres, columnas=COLUMNAS):
    """
    Convierte una lista de nombres de columnas en una lista de tuplas
    (nombre, tipo, completitud).

    Args:
        nombres (list): nombres de las columnas que se quieren informar.
        columnas (dict): diccionario con los datos de cada columna.

    Returns:
        list: tuplas (nombre, tipo, completitud). Los nombres que no existen
        en `columnas` se descartan (filter) y se avisa por pantalla.
    """
    inexistentes = [n for n in nombres if n not in columnas]
    if inexistentes:
        print(f"Aviso: columnas inexistentes ignoradas: {inexistentes}")

    existentes = filter(lambda n: n in columnas, nombres)
    return list(map(
        lambda n: (n, columnas[n]["tipo"], columnas[n]["completitud"]),
        existentes,
    ))


def filtrar_por_completitud(filas, minimo=0):
    """
    Deja solo las filas cuyo % de completitud es mayor o igual a `minimo`.

    Args:
        filas (list): tuplas (nombre, tipo, completitud).
        minimo (float): umbral mínimo. Por defecto 0 (no filtra nada).

    Returns:
        list: filas que cumplen el umbral.
    """
    return list(filter(lambda fila: fila[2] >= minimo, filas))


def ordenar_filas(filas, criterio="completitud", orden="B"):
    """
    Ordena las filas por nombre o por completitud.

    Args:
        filas (list): tuplas (nombre, tipo, completitud).
        criterio (str): "nombre" o "completitud". Por defecto "completitud".
        orden (str): "A" ascendente o "B" descendente. Por defecto "B".

    Returns:
        list: nueva lista ordenada. Si el criterio o el orden no son válidos,
        avisa y usa los valores por defecto para que el programa no falle.
    """
    if criterio not in CRITERIOS_VALIDOS:
        print(f"Aviso: criterio '{criterio}' no válido. Se usa 'completitud'.")
        criterio = "completitud"
    if orden not in ORDENES_VALIDOS:
        print(f"Aviso: orden '{orden}' no válido. Se usa 'B'.")
        orden = "B"

    posicion = 0 if criterio == "nombre" else 2   # índice dentro de la tupla
    descendente = orden == "B"
    return sorted(filas, key=lambda fila: fila[posicion], reverse=descendente)


def generar_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """
    Genera el informe de columnas para un rol.

    Args:
        rol (str | None): nombre del rol. Si es None, se informan TODAS
            las columnas ordenadas por completitud descendente.
        roles (dict): configuración de los roles.
        columnas (dict): datos de las columnas.

    Returns:
        list: tuplas (nombre, tipo, completitud) filtradas y ordenadas.
        Lista vacía si el rol no existe.
    """
    if rol is None:
        filas = armar_filas(list(columnas.keys()), columnas)
        return ordenar_filas(filas, "completitud", "B")

    if rol not in roles:
        print(f"Aviso: el rol '{rol}' no existe. Roles: {list(roles.keys())}")
        return []

    config = roles[rol]
    filas = armar_filas(config["columnas"], columnas)
    # Primero se filtra y después se ordena: así se ordenan menos elementos.
    filas = filtrar_por_completitud(filas, config.get("minimo", 0))
    return ordenar_filas(filas, config["criterio"], config["orden"])


def mostrar_informe(filas, titulo="Informe de columnas"):
    """
    Imprime el informe como una tabla de texto.

    Args:
        filas (list): tuplas (nombre, tipo, completitud).
        titulo (str): título que se muestra arriba de la tabla.
    """
    print(f"\n=== {titulo} ===")
    if not filas:
        print("(sin columnas para mostrar)")
        return
    print(f"{'COLUMNA':<12}{'TIPO':<6}{'COMPLETITUD':>12}")
    for nombre, tipo, completitud in filas:
        print(f"{nombre:<12}{tipo:<6}{completitud:>11.1f}%")
