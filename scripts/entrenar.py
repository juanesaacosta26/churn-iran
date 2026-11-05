"""Entrena los modelos y escribe las predicciones con el formato del contrato.

Dueño: Juanes (bloque 2). Correr con:
    python scripts/entrenar.py                          # logística -> predicciones_base.csv
    python scripts/entrenar.py --final --modelo bosque  # modelo elegido -> predicciones_final.csv
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_limpio  # noqa: E402
from churn.evaluacion import metricas  # noqa: E402
from churn.modelos import entrenar, particion, separar  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--final", action="store_true", help="escribe predicciones_final.csv")
    p.add_argument("--modelo", default="logistica", help="nombre para modelos.entrenar()")
    args = p.parse_args()

    df = cargar_limpio()
    part = particion(df, guardar=True)
    ent, pru = separar(df, part)
    print(f"Partición: {len(ent)} entrenamiento, {len(pru)} prueba "
          f"({int(pru[config.OBJETIVO].sum())} abandonos en prueba) -> {config.PARTICION.name}")

    X = config.VARIABLES_MODELO
    modelo = entrenar(args.modelo, ent[X], ent[config.OBJETIVO])
    prob = modelo.predict_proba(pru[X])[:, 1]
    m = metricas(pru[config.OBJETIVO], prob)
    print(f"{args.modelo} en prueba: " + json.dumps({k: round(v, 3) for k, v in m.items()}))

    pred = pd.DataFrame({
        "fila_original": pru["fila_original"].to_numpy(),
        "conjunto": "prueba",
        "churn_real": pru[config.OBJETIVO].astype(int).to_numpy(),
        "prob_churn": prob,
        "modelo": args.modelo,
    })
    destino = config.PREDICCIONES_FINAL if args.final else config.PREDICCIONES_BASE
    pred.to_csv(destino, index=False)
    print(f"-> {destino.relative_to(config.RAIZ)}")

    if args.modelo == "logistica":
        coef = pd.DataFrame({
            "variable": X,
            "coef_estandarizado": modelo.named_steps["modelo"].coef_[0],
        })
        coef["razon_momios_1de"] = np.exp(coef["coef_estandarizado"])  # por 1 desviación estándar
        coef.sort_values("coef_estandarizado", key=abs, ascending=False).to_csv(
            config.TABLAS / "logistica_coeficientes.csv", index=False)
        pd.DataFrame([{"modelo": args.modelo, **m}]).to_csv(
            config.TABLAS / "metricas_prueba_logistica.csv", index=False)


if __name__ == "__main__":
    main()
