"""Modelos predictivos. Dueño: Juanes (bloque 2)."""
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from churn import config


def particion(df: pd.DataFrame, guardar: bool = False) -> pd.DataFrame:
    """Divide en entrenamiento/prueba estratificado por churn (config.PROPORCION_PRUEBA,
    config.SEMILLA). Devuelve DataFrame [fila_original, conjunto]; con guardar=True lo
    escribe en config.PARTICION para que ambos usen la MISMA división.

    Referencia: 2137 en entrenamiento, 713 en prueba, 112 abandonos en prueba.
    """
    ent, pru = train_test_split(
        df["fila_original"],
        test_size=config.PROPORCION_PRUEBA,
        stratify=df[config.OBJETIVO],
        random_state=config.SEMILLA,
    )
    part = pd.concat([
        pd.DataFrame({"fila_original": ent, "conjunto": "entrenamiento"}),
        pd.DataFrame({"fila_original": pru, "conjunto": "prueba"}),
    ]).sort_values("fila_original").reset_index(drop=True)
    if guardar:
        config.PARTICION.parent.mkdir(parents=True, exist_ok=True)
        part.to_csv(config.PARTICION, index=False)
    return part


def separar(df: pd.DataFrame, part: pd.DataFrame | None = None):
    """Devuelve (entrenamiento, prueba) a partir de la partición."""
    if part is None:
        part = particion(df)
    conj = df["fila_original"].map(part.set_index("fila_original")["conjunto"])
    return df[conj == "entrenamiento"].copy(), df[conj == "prueba"].copy()


def _nuevo(nombre: str):
    s = config.SEMILLA
    if nombre == "logistica":
        return Pipeline([
            ("escala", StandardScaler()),
            ("modelo", LogisticRegression(max_iter=2000)),
        ])
    if nombre == "arbol":
        return DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, random_state=s)
    if nombre == "bosque":
        return RandomForestClassifier(n_estimators=500, min_samples_leaf=5, random_state=s, n_jobs=-1)
    if nombre == "boosting":
        return GradientBoostingClassifier(random_state=s)
    raise ValueError(f"modelo desconocido: {nombre}")


def entrenar(nombre: str, X: pd.DataFrame, y: pd.Series):
    """Devuelve un modelo de sklearn ajustado. nombre ∈ {"logistica", "arbol",
    "bosque", "boosting"}. "boosting" es opcional.

    Referencia: la logística con config.VARIABLES_MODELO da AUC-ROC ≈ 0.933 en prueba.
    """
    return _nuevo(nombre).fit(X, y)


def comparar_modelos(X: pd.DataFrame, y: pd.Series, nombres: list) -> pd.DataFrame:
    """Validación cruzada estratificada (config.PLIEGUES_CV) SOLO sobre entrenamiento.

    Columnas: modelo, auc_roc_media, auc_roc_desv, auc_pr_media, auc_pr_desv,
    recall_media, recall_desv.
    """
    cv = StratifiedKFold(n_splits=config.PLIEGUES_CV, shuffle=True, random_state=config.SEMILLA)
    filas = []
    for nombre in nombres:
        r = cross_validate(_nuevo(nombre), X, y, cv=cv,
                           scoring={"auc_roc": "roc_auc", "auc_pr": "average_precision", "recall": "recall"})
        fila = {"modelo": nombre}
        for m in ("auc_roc", "auc_pr", "recall"):
            fila[f"{m}_media"] = r[f"test_{m}"].mean()
            fila[f"{m}_desv"] = r[f"test_{m}"].std(ddof=1)
        filas.append(fila)
    return pd.DataFrame(filas)
