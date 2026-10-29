"""Crea un archivo de predicciones de EJEMPLO para que Ianis pueda trabajar la
priorización sin esperar el modelo de Juanes. No usar sus cifras en el informe.

Ya se corrió una vez; el resultado está en data/processed/fixtures/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

import pandas as pd  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_crudo  # noqa: E402


def main():
    df = cargar_crudo()
    cols = [c for c in df.columns if c not in ("fila_original", "churn")]
    df = df.drop_duplicates(subset=cols + ["churn"]).reset_index(drop=True)
    X, y = df[["segundos_uso", "frecuencia_llamadas", "quejas"]], df["churn"]  # modelo simple a propósito
    Xtr, Xte, ytr, yte, itr, ite = train_test_split(
        X, y, df["fila_original"], test_size=config.PROPORCION_PRUEBA,
        stratify=y, random_state=config.SEMILLA)
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
    out = pd.DataFrame({"fila_original": ite.values, "conjunto": "prueba",
                        "churn_real": yte.values, "prob_churn": m.predict_proba(Xte)[:, 1].round(4),
                        "modelo": "fixture_logistica_3vars"})
    config.FIXTURE_PREDICCIONES.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.FIXTURE_PREDICCIONES, index=False)
    print(f"{len(out)} filas -> {config.FIXTURE_PREDICCIONES}")


if __name__ == "__main__":
    main()
