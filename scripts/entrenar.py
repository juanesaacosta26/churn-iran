"""Entrena los modelos y escribe las predicciones con el formato del contrato.

Dueño: Juanes (bloque 2). Correr con:
    python scripts/entrenar.py                          # logística -> predicciones_base.csv
    python scripts/entrenar.py --final --modelo bosque  # modelo elegido -> predicciones_final.csv
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

from churn import config  # noqa: E402,F401


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--final", action="store_true", help="escribe predicciones_final.csv")
    p.add_argument("--modelo", default="logistica", help="nombre para modelos.entrenar()")
    args = p.parse_args()
    # TODO bloque 2, sesión 1: partición -> logística -> predicciones_base.csv
    # TODO bloque 2, sesiones 2-3: comparar modelos -> modelo final -> predicciones_final.csv
    raise NotImplementedError


if __name__ == "__main__":
    main()
