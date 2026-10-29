"""Partición, modelos y métricas (Juanes, bloque 2)."""
import numpy as np
import pandas as pd
import pytest

from churn import config
from churn.evaluacion import metricas
from churn.modelos import comparar_modelos, entrenar, particion
from tests.conftest import llamar


def _separar(limpio):
    part = llamar(particion, limpio).set_index("fila_original")["conjunto"]
    conj = limpio["fila_original"].map(part)
    return limpio[conj == "entrenamiento"], limpio[conj == "prueba"]


def test_particion_tamanos(limpio):
    ent, pru = _separar(limpio)
    assert len(ent) == 2137 and len(pru) == 713
    assert pru[config.OBJETIVO].sum() == 112


def test_particion_sin_cruces(limpio):
    part = llamar(particion, limpio)
    assert part["fila_original"].is_unique
    assert set(part["fila_original"]) == set(limpio["fila_original"])


def test_metricas_prediccion_perfecta():
    m = llamar(metricas, np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9]))
    assert m["auc_roc"] == pytest.approx(1.0)
    assert m["falsos_negativos"] == 0 and m["falsos_positivos"] == 0


def test_logistica_auc_prueba(limpio):
    ent, pru = _separar(limpio)
    X = config.VARIABLES_MODELO
    modelo = llamar(entrenar, "logistica", ent[X], ent[config.OBJETIVO])
    prob = modelo.predict_proba(pru[X])[:, 1]
    assert llamar(metricas, pru[config.OBJETIVO], prob)["auc_roc"] >= 0.90


def test_comparar_modelos(limpio):
    ent, _ = _separar(limpio)
    X = config.VARIABLES_MODELO
    t = llamar(comparar_modelos, ent[X], ent[config.OBJETIVO], ["logistica", "arbol"])
    assert len(t) == 2
    assert t["auc_roc_media"].between(0.5, 1).all()


@pytest.mark.parametrize("ruta", [config.PREDICCIONES_BASE, config.PREDICCIONES_FINAL])
def test_predicciones_cumplen_contrato(ruta):
    if not ruta.exists():
        pytest.skip(f"aún no existe {ruta.name}")
    pred = pd.read_csv(ruta)
    assert list(pred.columns) == ["fila_original", "conjunto", "churn_real", "prob_churn", "modelo"]
    assert len(pred) == 713 and pred["churn_real"].sum() == 112
    assert pred["prob_churn"].between(0, 1).all()
