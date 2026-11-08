
"""Tablas y figuras de priorización a partir de un archivo de predicciones.

Dueña: Ianis (bloques 2 y 3).
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churn import config
from churn.priorizacion import (
    tabla_deciles,
    capacidad,
    costo_por_umbral
)


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

    # Calcular costos para cada escenario de k.
    resultados_costos = []

    for k in config.K_COSTOS:
        tabla = costo_por_umbral(
            pred,
            costo_fn=k,
            costo_fp=1
        )
        tabla.insert(0, "k", k)
        resultados_costos.append(tabla)

    tabla_costos = pd.concat(
        resultados_costos,
        ignore_index=True
    )

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

    tabla_costos.to_csv(
        config.TABLAS / "priorizacion_costos.csv",
        index=False
    )

    # Mostrar resultados.
    print("\nTabla de deciles:")
    print(deciles.to_string(index=False))

    print("\nTabla de capacidad:")
    print(tabla_capacidad.to_string(index=False))

    print("\nTabla de costos por umbral:")
    print(tabla_costos.to_string(index=False))

    print("\nTablas guardadas correctamente en reports/tablas/")


if __name__ == "__main__":
    main()
