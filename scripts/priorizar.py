"""Tablas y figuras de priorización a partir de un archivo de predicciones.

Dueña: Ianis (Semana 3).
Correr con:  python scripts/priorizar.py --predicciones data/processed/predicciones_final.csv
"""
import argparse

from churn import config


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--predicciones", default=str(config.FIXTURE_PREDICCIONES))
    args = p.parse_args()
    # TODO S3: leer args.predicciones -> tabla_deciles, capacidad, costo_por_umbral -> reports/tablas/
    raise NotImplementedError


if __name__ == "__main__":
    main()
