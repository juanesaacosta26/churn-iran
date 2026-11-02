"""Genera las tablas del objetivo específico 1 (relación de cada variable con el abandono).

Dueño: Juanes (bloque 1). Correr con:  python scripts/relacionar.py

Salidas:
- reports/tablas/relacion_churn.csv        correlación de cada predictor con churn
- reports/tablas/tasa_por_categoria.csv    tasa de churn por nivel de cada variable categórica
- reports/tablas/redundancias.csv          pares de predictores con |r| >= 0.8 y su VIF
- reports/tablas/vif.csv                   VIF de cada predictor
- reports/figures/correlaciones.png        mapa de calor de correlaciones entre predictores

Usa la base limpia si ya existe (data/processed/clientes.csv y cargar_limpio() implementada);
si no, usa la base cruda y lo avisa. Después de la reunión 1 se usará siempre la limpia.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

import matplotlib  # noqa: E402

matplotlib.use("Agg")  # dibuja sin abrir ventanas (sirve en la terminal y en GitHub Actions)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_crudo, cargar_limpio  # noqa: E402
from churn.relacion import (  # noqa: E402
    _predictores,
    correlacion_con_churn,
    redundancias,
    tasa_por_categoria,
    vif_por_variable,
)


def cargar_base():
    """Devuelve (df, nombre_de_la_base). Prefiere la limpia; si no está lista, la cruda."""
    try:
        return cargar_limpio(), "limpia"
    except (NotImplementedError, FileNotFoundError):
        print("Aviso: la base limpia aún no está disponible; se usa la base cruda (3150 filas).")
        return cargar_crudo(), "cruda"


def sin_edad_redundante(df):
    """Quita config.COLUMNA_EDAD_A_QUITAR si sigue en la base (decisión del arranque).

    La base limpia ya no la trae; la cruda sí, y con ella edad y grupo_edad aparecerían
    como el par más redundante, lo que ya se sabe y tapa los pares que interesan.
    """
    return df.drop(columns=[config.COLUMNA_EDAD_A_QUITAR], errors="ignore")


def mapa_de_calor(df, ruta):
    """Guarda el mapa de calor de correlaciones (Pearson) entre predictores.

    Solo el triángulo inferior (la matriz es simétrica), escala de -1 a 1 centrada en 0,
    y el valor escrito en cada celda para leerlo sin adivinar el color.
    """
    predictores = _predictores(df)
    corr = df[predictores].astype(float).corr()
    mascara = np.triu(np.ones_like(corr, dtype=bool), k=0)  # sin la diagonal (siempre 1)
    datos = corr.mask(mascara)

    fig, ax = plt.subplots(figsize=(9, 7.5))
    im = ax.imshow(datos, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(predictores)), predictores, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(predictores)), predictores, fontsize=9)
    for i in range(len(predictores)):
        for j in range(i):
            v = corr.iat[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(v) >= 0.6 else "black")
    for borde in ax.spines.values():
        borde.set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="Correlación de Pearson")
    ax.set_title("Dos pares de variables casi repiten la misma información\n"
                 "segundos_uso–frecuencia_llamadas y frecuencia_sms–valor_cliente (|r| ≥ 0,9)",
                 fontsize=11, loc="left")
    fig.tight_layout()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


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

    base_red = sin_edad_redundante(df)
    red = redundancias(base_red)
    red.insert(0, "base", base)
    ruta_red = config.TABLAS / "redundancias.csv"
    red.to_csv(ruta_red, index=False)

    vif = vif_por_variable(base_red).rename_axis("variable").reset_index()
    vif.insert(0, "base", base)
    ruta_vif = config.TABLAS / "vif.csv"
    vif.to_csv(ruta_vif, index=False)

    ruta_fig = config.FIGURAS / "correlaciones.png"
    mapa_de_calor(base_red, ruta_fig)

    print(f"Base usada: {base} ({len(df)} filas, tasa de churn {df[config.OBJETIVO].mean():.3f})")
    print("\nTres variables más relacionadas con el abandono:")
    print(corr.head(3)[["variable", "pearson_pb", "spearman"]].round(3).to_string(index=False))
    print(f"\nGuardado: {ruta_corr.relative_to(config.RAIZ)}")
    print("\nPares redundantes (|r| >= 0.8):")
    print(red[["var_1", "var_2", "r", "vif_1", "vif_2"]].round(2).to_string(index=False))
    for ruta in (ruta_tasas, ruta_red, ruta_vif, ruta_fig):
        print(f"Guardado: {ruta.relative_to(config.RAIZ)}")


if __name__ == "__main__":
    main()
