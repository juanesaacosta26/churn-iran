"""Priorización (Ianis, bloques 2 y 3). Corre sobre el fixture."""
import pytest

from churn.priorizacion import capacidad, costo_por_umbral, tabla_deciles
from tests.conftest import llamar


def test_deciles_suman_el_total(fixture_pred):
    t = llamar(tabla_deciles, fixture_pred)
    assert len(t) == 10
    assert t["n"].sum() == len(fixture_pred)
    assert t["churn_reales"].sum() == fixture_pred["churn_real"].sum()


def test_deciles_acumulado_termina_en_100(fixture_pred):
    t = llamar(tabla_deciles, fixture_pred)
    assert t["pct_acumulado"].iloc[-1] == pytest.approx(100)
    assert t["pct_acumulado"].is_monotonic_increasing


def test_capacidad_crece_con_el_porcentaje(fixture_pred):
    t = llamar(capacidad, fixture_pred, (0.10, 0.20, 0.30))
    assert t["churn_capturados"].is_monotonic_increasing
    assert t["contactados"].tolist() == [round(p * len(fixture_pred)) for p in (0.1, 0.2, 0.3)]


def test_costo_con_k_mayor_pesa_mas(fixture_pred):
    c2 = llamar(costo_por_umbral, fixture_pred, 2, 1).set_index("umbral")
    c10 = llamar(costo_por_umbral, fixture_pred, 10, 1).set_index("umbral")
    assert (c10["costo"] >= c2["costo"]).all()
