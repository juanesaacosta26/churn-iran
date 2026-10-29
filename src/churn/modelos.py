"""Modelos predictivos. Dueño: Juanes (bloque 2)."""
import pandas as pd


def particion(df: pd.DataFrame) -> pd.DataFrame:
    """Divide en entrenamiento/prueba estratificado por churn (config.PROPORCION_PRUEBA,
    config.SEMILLA). Devuelve DataFrame [fila_original, conjunto] y lo guarda en
    config.PARTICION para que ambos usen la MISMA división.

    Referencia: 2137 en entrenamiento, 713 en prueba, 112 abandonos en prueba.
    """
    raise NotImplementedError


def entrenar(nombre: str, X: pd.DataFrame, y: pd.Series):
    """Devuelve un modelo de sklearn ajustado. nombre ∈ {"logistica", "arbol",
    "bosque", "boosting"}. "boosting" es opcional.

    Referencia: la logística con config.VARIABLES_MODELO da AUC-ROC ≈ 0.933 en prueba.
    """
    raise NotImplementedError


def comparar_modelos(X: pd.DataFrame, y: pd.Series, nombres: list) -> pd.DataFrame:
    """Validación cruzada estratificada (config.PLIEGUES_CV) SOLO sobre entrenamiento.

    Columnas: modelo, auc_roc_media, auc_roc_desv, auc_pr_media, auc_pr_desv,
    recall_media, recall_desv.
    """
    raise NotImplementedError
