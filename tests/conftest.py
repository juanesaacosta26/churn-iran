"""Herramientas compartidas por las pruebas.

Las pruebas de funciones que todavía no están implementadas se SALTAN
(aparecen como "skipped") en lugar de fallar. Cuando alguien implementa su
función, sus pruebas empiezan a comprobar las cifras de referencia.
Ver qué falta:  pytest -q -rs      Meta del martes 10 de noviembre: 0 skipped.
"""
import pandas as pd
import pytest

from churn import config


def llamar(funcion, *args, **kwargs):
    """Llama `funcion`; si todavía lanza NotImplementedError, salta la prueba."""
    try:
        return funcion(*args, **kwargs)
    except NotImplementedError:
        pytest.skip(f"{funcion.__module__}.{funcion.__name__} aún no está implementada")


@pytest.fixture
def crudo():
    from churn.datos import cargar_crudo

    return cargar_crudo()


@pytest.fixture
def limpio():
    """Base limpia; salta si todavía no existe o cargar_limpio() no está lista."""
    from churn.datos import cargar_limpio

    if not config.DATA_PROCESADA.exists():
        pytest.skip("falta data/processed/clientes.csv (correr scripts/preparar_datos.py)")
    return llamar(cargar_limpio)


@pytest.fixture
def fixture_pred():
    return pd.read_csv(config.FIXTURE_PREDICCIONES)
