"""Priorización para el equipo de retención. Dueña: Ianis (bloques 2 y 3).

Recibe un archivo de predicciones con el formato de docs/contrato_predicciones.md.
Mientras no exista el de Juanes, usar data/processed/fixtures/predicciones_ejemplo.csv.
"""
import pandas as pd


def tabla_deciles(pred: pd.DataFrame) -> pd.DataFrame:
    """Ordena por prob_churn y parte en 10 deciles. Por decil: n, churn reales,
    tasa, lift y % acumulado de churners capturados.

    Columnas: decil (1 = mayor riesgo), n, churn_reales, tasa, lift, pct_acumulado (0–100).
    Referencia con predicciones_base.csv: el decil 1 captura 56 de 112.
    """
    raise NotImplementedError


def costo_por_umbral(pred: pd.DataFrame, costo_fn: float, costo_fp: float) -> pd.DataFrame:
    """Para umbrales de 0.05 a 0.95: FP, FN y costo total = FN*costo_fn + FP*costo_fp.

    Columnas: umbral, falsos_positivos, falsos_negativos, costo.
    Con k de config.K_COSTOS: costo_fn = k, costo_fp = 1.
    """
    raise NotImplementedError


def capacidad(pred: pd.DataFrame, porcentajes=(0.10, 0.20, 0.30)) -> pd.DataFrame:
    """Si el equipo solo puede contactar al p% de mayor riesgo: cuántos churners
    captura y qué precisión tiene.

    Columnas: porcentaje, contactados (= round(p · n)), churn_capturados,
    pct_capturado (0–100), precision.
    Referencia con predicciones_base.csv: con el 20 % se captura ≈ 77 %.
    """
    raise NotImplementedError
