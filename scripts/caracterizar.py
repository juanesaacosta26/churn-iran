
from pathlib import Path

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
