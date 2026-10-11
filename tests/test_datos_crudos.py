"""Pruebas de la base original. Deben pasar desde el día 1."""
from churn import config
from churn.datos import cargar_crudo


def test_forma():
    df = cargar_crudo()
    assert df.shape == (3150, 15)  # 14 columnas + fila_original


def test_columnas_en_espanol():
    df = cargar_crudo()
    assert set(config.COLUMNAS.values()) <= set(df.columns)


def test_sin_faltantes_y_churn_binario():
    df = cargar_crudo()
    assert df.isna().sum().sum() == 0
    assert set(df["churn"].unique()) == {0, 1}


def test_tasa_churn():
    df = cargar_crudo()
    assert round(df["churn"].mean(), 3) == 0.157
