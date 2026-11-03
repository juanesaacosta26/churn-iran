"""Carga de datos.

- cargar_crudo(): YA FUNCIONA. Lee el CSV original tal cual (3150 filas).
- cargar_limpio(): dueña Ianis (bloque 1). Lee data/processed/clientes.csv.
"""
import pandas as pd

from churn import config


def cargar_crudo(ruta=config.DATA_RAW) -> pd.DataFrame:
    """Lee el CSV original de UCI (separado por comas) y renombra columnas al español.

    Agrega `fila_original` (1..3150) como identificador del cliente, porque la base no trae ID.
    """
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    df.columns = [" ".join(c.split()) for c in df.columns]  # el CSV trae dobles espacios
    df = df.rename(columns=config.COLUMNAS)
    df.insert(0, "fila_original", range(1, len(df) + 1))
    return df


def cargar_limpio(ruta=config.DATA_PROCESADA) -> pd.DataFrame:
    """Lee la base limpia y devuelve los datos con los tipos correctos."""

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró clientes.csv. "
            "Primero debes correr scripts/preparar_datos.py."
        )

    df = pd.read_csv(ruta)

    if len(df) != 2850:
        raise ValueError(
            f"La base limpia debe tener 2850 filas, pero tiene {len(df)}."
        )

    return df