
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churn import config
from churn.datos import cargar_crudo


def main():

    # 1. Cargar los datos originales
    df = cargar_crudo()

    print("Dimensiones originales:", df.shape)

    # 2. Identificar duplicados sin tener en cuenta fila_original
    columnas_comparar = df.columns.drop("fila_original")

    duplicados = df.duplicated(
        subset=columnas_comparar
    ).sum()

    print("Duplicados encontrados:", duplicados)

    # 3. Eliminar duplicados, conservando la primera aparición
    df = df.drop_duplicates(
        subset=columnas_comparar,
        keep="first"
    )

    # 4. Eliminar la columna definida en config.py
    df = df.drop(columns=[config.COLUMNA_EDAD_A_QUITAR])

    # 5. Mostrar las dimensiones finales
    print("Dimensiones después de limpiar:", df.shape)

    # 6. Crear la carpeta de destino si no existe
    config.DATA_PROCESADA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Guardar los datos procesados
    df.to_csv(config.DATA_PROCESADA, index=False)

    print("Archivo guardado en:", config.DATA_PROCESADA)


if __name__ == "__main__":
    main()

