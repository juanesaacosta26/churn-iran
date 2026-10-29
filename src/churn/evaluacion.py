"""Métricas y gráficas de evaluación. Dueño: Juanes (bloque 2)."""


def metricas(y_real, prob, umbral: float = 0.5) -> dict:
    """AUC-ROC, AUC-PR, recall, precisión, F1, falsos positivos y falsos negativos.

    Claves del diccionario: auc_roc, auc_pr, recall, precision, f1,
    falsos_positivos, falsos_negativos.
    """
    raise NotImplementedError
