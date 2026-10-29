"""Base limpia (Ianis, bloque 1)."""
from churn import config


def test_limpia_tiene_2850_filas(limpio):
    assert len(limpio) == 2850


def test_limpia_tiene_446_abandonos(limpio):
    assert limpio[config.OBJETIVO].sum() == 446


def test_limpia_sin_duplicados(limpio):
    assert not limpio.drop(columns=["fila_original"]).duplicated().any()


def test_limpia_fila_original_unica(limpio):
    assert limpio["fila_original"].is_unique


def test_limpia_sin_columna_de_edad_redundante(limpio):
    assert config.COLUMNA_EDAD_A_QUITAR not in limpio.columns
