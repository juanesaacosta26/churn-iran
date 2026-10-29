"""Genera data/processed/clientes.csv a partir del CSV original.

Dueña: Ianis (bloque 1). Correr con:  python scripts/preparar_datos.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # para no tener que fijar PYTHONPATH

from churn import config  # noqa: E402
from churn.datos import cargar_crudo  # noqa: E402


def main():
    df = cargar_crudo()
    # TODO 1: contar y quitar filas duplicadas exactas (sin contar fila_original); deben ser 300
    # TODO 2: quitar config.COLUMNA_EDAD_A_QUITAR (decisión del arranque, docs/decisiones.md)
    # TODO 3: revisar rangos raros y documentarlos en docs/calidad_datos.md
    # TODO 4: guardar en config.DATA_PROCESADA (index=False)
    raise NotImplementedError


if __name__ == "__main__":
    main()
