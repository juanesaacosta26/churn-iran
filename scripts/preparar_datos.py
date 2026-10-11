"""Genera data/processed/clientes.csv a partir del CSV original.

Dueña: Ianis (Semana 1). Correr con:  python scripts/preparar_datos.py
"""
from churn import config
from churn.datos import cargar_crudo


def main():
    df = cargar_crudo()
    # TODO 1: contar y quitar filas duplicadas exactas (sin contar fila_original)
    # TODO 2: aplicar la decisión sobre edad / grupo_edad (docs/decisiones.md)
    # TODO 3: revisar rangos raros y documentarlos en docs/calidad_datos.md
    # TODO 4: guardar en config.DATA_PROCESADA (index=False)
    raise NotImplementedError


if __name__ == "__main__":
    main()
