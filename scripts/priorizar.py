"""Tablas y figuras de priorización a partir de un archivo de predicciones.

Dueña: Ianis (bloques 2 y 3).
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churn import config
from churn.priorizacion import tabla_deciles, capacidad


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--predicciones",
        default=str(config.FIXTURE_PREDICCIONES)
    )
    args = p.parse_args()

    # Leer las predicciones.
    pred = pd.read_csv(args.predicciones)

    # Generar las tablas de priorización.
    deciles = tabla_deciles(pred)
    tabla_capacidad = capacidad(pred, config.CAPACIDADES)

    # Crear la carpeta de resultados si no existe.
    config.TABLAS.mkdir(parents=True, exist_ok=True)

    # Guardar las tablas.
    deciles.to_csv(
        config.TABLAS / "priorizacion_deciles.csv",
        index=False
    )

    tabla_capacidad.to_csv(
        config.TABLAS / "priorizacion_capacidad.csv",
        index=False
    )

    print("\nTabla de deciles:")
    print(deciles.to_string(index=False))

    print("\nTabla de capacidad:")
    print(tabla_capacidad.to_string(index=False))

    print("\nTablas guardadas correctamente en reports/tablas/")


if __name__ == "__main__":
    main()