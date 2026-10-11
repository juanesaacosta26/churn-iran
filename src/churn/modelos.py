"""Modelos predictivos. Dueño: Juanes (Semanas 2 y 3)."""
import pandas as pd


def particion(df: pd.DataFrame) -> pd.DataFrame:
    """Divide en entrenamiento/prueba estratificado por churn (config.PROPORCION_PRUEBA,
    config.SEMILLA). Devuelve DataFrame [fila_original, conjunto] y lo guarda en
    config.PARTICION para que ambos usen la MISMA división."""
    raise NotImplementedError


def entrenar(nombre: str, X: pd.DataFrame, y: pd.Series):
    """Devuelve un modelo de sklearn ajustado. nombre ∈ {"logistica", "arbol",
    "bosque", "boosting"}."""
    raise NotImplementedError
