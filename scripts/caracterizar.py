
"""Genera las tablas del objetivo específico 2 (caracterización de quienes abandonan frente a quienes permanecen).

Correr con:  python scripts/caracterizar.py

Salidas: reports/tablas/caracterizacion_numericas.csv y reports/tablas/caracterizacion_categoricas.csv
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

from churn.datos import cargar_limpio
from churn.caracterizacion import tabla_numericas, tabla_categoricas


def main():
    df = cargar_limpio()

    numericas = tabla_numericas(df)
    categoricas = tabla_categoricas(df)

    carpeta = Path("reports/tablas")
    carpeta.mkdir(parents=True, exist_ok=True)

    numericas.to_csv(
        carpeta / "caracterizacion_numericas.csv",
        index=False
    )

    categoricas.to_csv(
        carpeta / "caracterizacion_categoricas.csv",
        index=False
    )

    print("Tablas de caracterización generadas correctamente.")
    print(f"Variables numéricas: {len(numericas)}")
    print(f"Filas categóricas: {len(categoricas)}")


if __name__ == "__main__":
    main()
