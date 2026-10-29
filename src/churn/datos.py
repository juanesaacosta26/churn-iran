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
    """TODO (Ianis, bloque 1): leer data/processed/clientes.csv generado por
    scripts/preparar_datos.py y devolverlo con los tipos correctos.

    Debe devolver 2850 filas. Si el archivo no existe, lanzar FileNotFoundError
    con un mensaje que diga que primero hay que correr scripts/preparar_datos.py.
    """
    raise NotImplementedError("Lo implementa Ianis en el bloque 1")
