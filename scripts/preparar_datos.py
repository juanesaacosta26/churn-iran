
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd

from churn import config
from churn.datos import cargar_crudo


def generar_informe_calidad(df):
    """Genera el informe de calidad de la base procesada."""

    # Excluir fila_original porque es un identificador.
    columnas_numericas = [
        columna
        for columna in df.select_dtypes(include="number").columns
        if columna != "fila_original"
    ]

    resultados = []

    # Calcular las estadísticas de cada variable numérica.
    for columna in columnas_numericas:
        serie = df[columna]

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        atipicos = (
            (serie < limite_inferior) |
            (serie > limite_superior)
        ).sum()

        resultados.append({
            "Variable": columna,
            "Mínimo": serie.min(),
            "Percentil 5": serie.quantile(0.05),
            "Mediana": serie.median(),
            "Percentil 95": serie.quantile(0.95),
            "Máximo": serie.max(),
            "Cantidad de ceros": (serie == 0).sum(),
            "Valores atípicos": atipicos
        })

    tabla = pd.DataFrame(resultados)

    # Analizar los clientes que no registraron segundos de uso.
    clientes_cero_uso = df[df["segundos_uso"] == 0]
    cantidad_cero_uso = len(clientes_cero_uso)
    abandonos_cero_uso = (clientes_cero_uso["churn"] == 1).sum()

    if cantidad_cero_uso > 0:
        porcentaje_abandono = (
            abandonos_cero_uso / cantidad_cero_uso
        ) * 100
    else:
        porcentaje_abandono = 0

    # Crear el contenido del documento.
    contenido = [
        "# Calidad de los datos",
        "",
        "## Resumen de la base procesada",
        "",
        f"- Total de clientes: {len(df)}.",
        f"- Total de variables: {len(df.columns)}.",
        f"- Valores faltantes: {df.isna().sum().sum()}.",
        f"- Registros duplicados: {df.duplicated(subset=[c for c in df.columns if c != 'fila_original']).sum()}.",
        "",
        "## Estadísticas por variable numérica",
        "",
        "Los valores atípicos se identificaron utilizando el criterio de 1.5 × IQR.",
        "",
        tabla.to_markdown(index=False),
        "",
        "## Clientes con cero segundos de uso",
        "",
        f"- Clientes con segundos_uso = 0: {cantidad_cero_uso}.",
        f"- De ellos, clientes que abandonaron: {abandonos_cero_uso}.",
        f"- Porcentaje de abandono en este grupo: {porcentaje_abandono:.2f}%.",
        "",
        "## Interpretación",
        "",
        (
            f"De los {cantidad_cero_uso} clientes que no registraron segundos "
            f"de uso, {abandonos_cero_uso} abandonaron el servicio, lo que "
            f"representa el {porcentaje_abandono:.2f}% de este grupo. "
            "Esto indica que más de la mitad de los clientes sin uso "
            "registrado terminaron abandonando. Por esta razón, la variable "
            "`segundos_uso` puede ser una señal importante para identificar "
            "clientes que podrían estar en riesgo de abandono. Sin embargo, "
            "este resultado muestra una relación entre las variables y no "
            "significa que la falta de uso sea necesariamente la causa "
            "del abandono."
            if cantidad_cero_uso > 0
            else "No hay clientes con cero segundos de uso para realizar esta interpretación."
        ),
        ""
    ]

    # Guardar el informe en docs/calidad_datos.md.
    ruta_documento = (
        Path(__file__).resolve().parents[1] /
        "docs" /
        "calidad_datos.md"
    )

    ruta_documento.parent.mkdir(parents=True, exist_ok=True)

    ruta_documento.write_text(
        "\n".join(contenido),
        encoding="utf-8"
    )

    print("Informe de calidad guardado en:", ruta_documento)


def main():

    # 1. Cargar los datos originales.
    df = cargar_crudo()

    print("Dimensiones originales:", df.shape)

    # 2. Identificar duplicados sin tener en cuenta fila_original.
    columnas_comparar = df.columns.drop("fila_original")

    duplicados = df.duplicated(
        subset=columnas_comparar
    ).sum()

    print("Duplicados encontrados:", duplicados)

    # 3. Eliminar duplicados, conservando la primera aparición.
    df = df.drop_duplicates(
        subset=columnas_comparar,
        keep="first"
    )

    # 4. Eliminar la columna definida en config.py.
    df = df.drop(columns=[config.COLUMNA_EDAD_A_QUITAR])

    # 5. Mostrar las dimensiones finales.
    print("Dimensiones después de limpiar:", df.shape)

    # 6. Crear la carpeta de destino si no existe.
    config.DATA_PROCESADA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Guardar los datos procesados.
    df.to_csv(config.DATA_PROCESADA, index=False)

    print("Archivo guardado en:", config.DATA_PROCESADA)

    # 8. Generar automáticamente el informe de calidad.
    generar_informe_calidad(df)


if __name__ == "__main__":
    main()
