"""Genera las tablas del objetivo específico 1 (relación de cada variable con el abandono).

Dueño: Juanes (bloque 1). Correr con:  python scripts/relacionar.py

Salidas:
- reports/tablas/relacion_churn.csv        correlación de cada predictor con churn
- reports/tablas/tasa_por_categoria.csv    tasa de churn por nivel de cada variable categórica

Usa la base limpia si ya existe (data/processed/clientes.csv y cargar_limpio() implementada);
si no, usa la base cruda y lo avisa. Después de la reunión 1 se usará siempre la limpia.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

import pandas as pd  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_crudo, cargar_limpio  # noqa: E402
from churn.relacion import correlacion_con_churn, tasa_por_categoria  # noqa: E402


def cargar_base():
    """Devuelve (df, nombre_de_la_base). Prefiere la limpia; si no está lista, la cruda."""
    try:
        return cargar_limpio(), "limpia"
    except (NotImplementedError, FileNotFoundError):
        print("Aviso: la base limpia aún no está disponible; se usa la base cruda (3150 filas).")
        return cargar_crudo(), "cruda"


def main():
    df, base = cargar_base()
    config.TABLAS.mkdir(parents=True, exist_ok=True)

    corr = correlacion_con_churn(df)
    corr.insert(0, "base", base)
    ruta_corr = config.TABLAS / "relacion_churn.csv"
    corr.to_csv(ruta_corr, index=False)

    categoricas = [c for c in config.CATEGORICAS if c in df.columns]
    tasas = pd.concat(
        [tasa_por_categoria(df, c).assign(variable=c) for c in categoricas], ignore_index=True
    )[["variable", "nivel", "n", "tasa_churn"]]
    tasas.insert(0, "base", base)
    ruta_tasas = config.TABLAS / "tasa_por_categoria.csv"
    tasas.to_csv(ruta_tasas, index=False)

    print(f"Base usada: {base} ({len(df)} filas, tasa de churn {df[config.OBJETIVO].mean():.3f})")
    print("\nTres variables más relacionadas con el abandono:")
    print(corr.head(3)[["variable", "pearson_pb", "spearman"]].round(3).to_string(index=False))
    print(f"\nGuardado: {ruta_corr.relative_to(config.RAIZ)}")
    print(f"Guardado: {ruta_tasas.relative_to(config.RAIZ)}")


if __name__ == "__main__":
    main()
