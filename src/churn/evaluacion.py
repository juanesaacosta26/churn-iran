"""Métricas y gráficas de evaluación. Dueño: Juanes (bloque 2)."""
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def metricas(y_real, prob, umbral: float = 0.5) -> dict:
    """AUC-ROC, AUC-PR, recall, precisión, F1, falsos positivos y falsos negativos.

    Claves del diccionario: auc_roc, auc_pr, recall, precision, f1,
    falsos_positivos, falsos_negativos.
    """
    y = np.asarray(y_real).astype(int)
    p = np.asarray(prob, dtype=float)
    pred = (p >= umbral).astype(int)
    vp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    recall = vp / (vp + fn) if vp + fn else 0.0
    precision = vp / (vp + fp) if vp + fp else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "auc_roc": float(roc_auc_score(y, p)),
        "auc_pr": float(average_precision_score(y, p)),
        "recall": recall,
        "precision": precision,
        "f1": f1,
        "falsos_positivos": fp,
        "falsos_negativos": fn,
    }
