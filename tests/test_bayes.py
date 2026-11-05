"""Regresión logística bayesiana (Juanes, entrega de estadística bayesiana)."""
import numpy as np
import pytest

from churn import bayes, config
from churn.modelos import separar


def test_diagnosticos_con_datos_simulados():
    rng = np.random.default_rng(1)
    iid = rng.standard_normal((4, 2000))
    assert bayes.rhat(iid) < 1.01
    assert bayes.ess_bulk(iid) > 6000
    corrida = iid.copy()
    corrida[0] += 1                      # una cadena desplazada: no convergió
    assert bayes.rhat(corrida) > 1.05


def test_bayesiana_converge_y_coincide_con_la_clasica(limpio):
    ent, _ = separar(limpio)
    X = config.VARIABLES_MODELO
    m = bayes.ajustar(ent[X], ent[config.OBJETIVO], calentamiento=300, iteraciones=400)
    res = bayes.tabla_curso(m)
    mv = bayes.logistica_mv(ent[X], ent[config.OBJETIVO])
    assert res["rhat"].max() < 1.05
    assert m.divergencias.sum() == 0
    # con 2137 clientes la previa pesa poco: medias posteriores a menos de 0.5 EE de la clásica
    dif = (res["media"] - mv["beta"]).abs() / mv["ee"]
    assert dif.iloc[1:].max() < 0.5
    q = res.set_index("parametro")
    assert q.loc["quejas", "or_q2.5"] > 10          # OR de queja claramente mayor que 1


def test_logistica_clasica_queja(limpio):
    ent, _ = separar(limpio)
    mv = bayes.logistica_mv(ent[config.VARIABLES_MODELO], ent[config.OBJETIVO]).set_index("parametro")
    assert mv.loc["quejas", "or"] == pytest.approx(43.9, rel=0.02)


def test_previa_literatura_escala_y_fuentes(limpio):
    ent, _ = separar(limpio)
    X = config.VARIABLES_MODELO
    esc = bayes.Escalador.ajustar(ent[X])
    p = bayes.previa_literatura(esc, X)
    i = X.index("quejas")
    # β* = β · s  →  media 0.54 · s y desviación 1.0 · s
    assert p.mu_beta[i] == pytest.approx(0.54 * esc.desv[i])
    assert p.sd_beta[i] == pytest.approx(1.0 * esc.desv[i])
    assert p.sd_beta[X.index("edad")] == 2.5                     # sin evidencia: débil
    t = bayes.tabla_previas_literatura(X)
    assert t["fuente"].notna().all() and len(t) == len(X) + 1
