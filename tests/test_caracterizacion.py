"""Caracterización (Ianis, bloque 2)."""
import pytest

from churn.caracterizacion import tabla_categoricas, tabla_numericas
from tests.conftest import llamar


def test_medianas_de_uso(limpio):
    t = llamar(tabla_numericas, limpio).set_index("variable")
    assert t.loc["segundos_uso", "mediana_abandona"] == pytest.approx(1256.5)
    assert t.loc["segundos_uso", "mediana_permanece"] == pytest.approx(3596.5)
    assert t.loc["frecuencia_llamadas", "mediana_abandona"] == pytest.approx(29)
    assert t.loc["frecuencia_llamadas", "mediana_permanece"] == pytest.approx(64)


def test_numericas_ordenadas_por_efecto(limpio):
    t = llamar(tabla_numericas, limpio)
    efectos = t["efecto"].abs().tolist()
    assert efectos == sorted(efectos, reverse=True)


@pytest.mark.parametrize("variable, nivel, tasa", [
    ("quejas", 1, 0.826), ("quejas", 0, 0.098),
    ("estado", 2, 0.475), ("estado", 1, 0.056),
    ("plan_tarifa", 2, 0.026), ("plan_tarifa", 1, 0.168),
])
def test_tasas_categoricas(limpio, variable, nivel, tasa):
    t = llamar(tabla_categoricas, limpio)
    fila = t[(t["variable"] == variable) & (t["nivel"] == nivel)]
    assert len(fila) == 1
    assert fila["tasa_churn"].iloc[0] == pytest.approx(tasa, abs=0.001)
