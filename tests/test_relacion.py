"""Relación con el abandono (Juanes, bloque 1)."""
import pytest

from churn.relacion import correlacion_con_churn, redundancias, tasa_por_categoria
from tests.conftest import llamar


def test_quejas_es_la_mas_correlacionada(crudo):
    t = llamar(correlacion_con_churn, crudo)
    assert t.iloc[0]["variable"] == "quejas"
    assert t.iloc[0]["pearson_pb"] == pytest.approx(0.53, abs=0.01)
    assert list(t["variable"][:3]) == ["quejas", "estado", "frecuencia_llamadas"]


def test_correlacion_excluye_id_y_objetivo(crudo):
    t = llamar(correlacion_con_churn, crudo)
    assert not {"fila_original", "churn"} & set(t["variable"])


def test_tasa_por_queja(crudo):
    t = llamar(tasa_por_categoria, crudo, "quejas").set_index("nivel")
    assert t.loc[1, "tasa_churn"] > 0.8
    assert t.loc[0, "tasa_churn"] < 0.11
    assert t["n"].sum() == len(crudo)


def test_redundancia_uso(limpio):
    t = llamar(redundancias, limpio)
    pares = {frozenset((a, b)) for a, b in zip(t["var_1"], t["var_2"])}
    assert frozenset(("segundos_uso", "frecuencia_llamadas")) in pares
    assert (t[["vif_1", "vif_2"]] >= 1).all().all()
