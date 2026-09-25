# ---------------------------------------------------------------------------
# 1) COLUMNAS: diccionario cuya CLAVE es el nombre de la columna y cuyo
#    VALOR es otro diccionario con el tipo y el % de completitud (0 a 100).
# ---------------------------------------------------------------------------
COLUMNAS = {
    "PONDERA": {"tipo": "int", "completitud": 100.0},
    "ESTADO": {"tipo": "int", "completitud": 100.0},
    "CAT_OCUP": {"tipo": "int", "completitud": 45.3},
    "EDAD": {"tipo": "int", "completitud": 99.8},
    "REGION": {"tipo": "int", "completitud": 100.0},
    "AGLOMERADO": {"tipo": "int", "completitud": 100.0},
    "ANO4": {"tipo": "int", "completitud": 100.0},
    "TRIMESTRE": {"tipo": "int", "completitud": 100.0},
    "ITF": {"tipo": "int", "completitud": 82.6},
    "MAS_500": {"tipo": "str", "completitud": 97.1},
    "GDECCFR": {"tipo": "int", "completitud": 76.4},
}
# ---------------------------------------------------------------------------
# 2) ROLES: diccionario cuya CLAVE es el nombre del rol.
#    - "columnas": lista con las columnas de interés
#    - "criterio": orden elegido "nombre" o "completitud"
#    - "orden": forma de ordenarlo "A" (ascendente) o "B" (descendente)
#    - "minimo": % mínimo de completitud (si no está, no se filtra)
# ---------------------------------------------------------------------------
ROLES = {
    "docente": {
        "columnas": ["EDAD", "ESTADO", "REGION", "ANO4", "TRIMESTRE"],
        "criterio": "nombre",
        "orden": "A",
    },
    "investigador": {
        "columnas": [
            "PONDERA", "ESTADO", "CAT_OCUP", "EDAD", "ITF", "GDECCFR",
        ],
        "criterio": "completitud",
        "orden": "B",
        "minimo": 80,
    },
    "analista": {
        "columnas": ["AGLOMERADO", "MAS_500", "ITF", "GDECCFR", "REGION"],
        "criterio": "completitud",
        "orden": "A",
        "minimo": 50,
    },
}

# Valores permitidos (sirven para validar la configuración de los roles)
CRITERIOS_VALIDOS = ("nombre", "completitud")
ORDENES_VALIDOS = ("A", "B")
