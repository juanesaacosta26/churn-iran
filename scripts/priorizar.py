"""Tablas y figuras de priorización a partir de un archivo de predicciones.

Dueña: Ianis (bloques 2 y 3).
Correr con:  python scripts/priorizar.py --predicciones data/processed/predicciones_final.csv
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

from churn import config  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--predicciones", default=str(config.FIXTURE_PREDICCIONES))
    args = p.parse_args()
    # TODO bloque 2: leer args.predicciones -> tabla_deciles, capacidad -> reports/tablas/
    # TODO bloque 3: costo_por_umbral para cada k de config.K_COSTOS -> tabla y figura
    raise NotImplementedError


if __name__ == "__main__":
    main()
