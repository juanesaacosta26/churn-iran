
"""Tablas y figuras de priorización a partir de un archivo de predicciones.

Dueña: Ianis (bloques 2 y 3).
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Agregar la carpeta src a la ruta para encontrar el paquete churn.
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

# Importar módulos del proyecto.
from churn import config
from churn.datos import cargar_limpio
from churn.priorizacion import (
    tabla_deciles,
    capacidad,
    costo_por_umbral,
    comparar_grupo_prioritario
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

    # Cargar las características de los clientes.
    clientes = cargar_limpio()

    # Comparar el 20 % de mayor riesgo frente al resto.
    (
        tabla_prioritarios,
        tabla_categorias_prioritarios
    ) = comparar_grupo_prioritario(
        pred,
        clientes,
        proporcion=0.20
    )

    # Generar las tablas generales de priorización.
    deciles = tabla_deciles(pred)
    tabla_capacidad = capacidad(
        pred,
        config.CAPACIDADES
    )

    # Calcular costos para cada escenario.
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

    # Crear carpetas de resultados.
    config.FIGURAS.mkdir(
        parents=True,
        exist_ok=True
    )

    config.TABLAS.mkdir(
        parents=True,
        exist_ok=True
    )

    # Gráfica del costo según el umbral.
    plt.figure(figsize=(9, 5))

    for k, grupo in tabla_costos.groupby("k"):
        plt.plot(
            grupo["umbral"],
            grupo["costo"],
            marker="o",
            label=f"k = {k}"
        )

    plt.xlabel("Umbral de decisión")
    plt.ylabel("Costo total")
    plt.title("Costo total según el umbral de decisión")
    plt.legend(title="Costo por falso negativo")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        config.FIGURAS / "priorizacion_costos_umbral.png",
        dpi=150
    )

    plt.close()

    # Curva de ganancia acumulada.
    plt.figure(figsize=(9, 5))

    plt.plot(
        deciles["decil"],
        deciles["pct_acumulado"],
        marker="o",
        label="Modelo"
    )

    # Línea de referencia: selección aleatoria.
    plt.plot(
        [1, 10],
        [10, 100],
        linestyle="--",
        label="Selección aleatoria"
    )

    plt.xlabel("Deciles de clientes (mayor a menor riesgo)")
    plt.ylabel("Porcentaje acumulado de abandonos capturados")
    plt.title("Curva de ganancia acumulada")
    plt.xticks(range(1, 11))
    plt.ylim(0, 105)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        config.FIGURAS / "ganancia_acumulada.png",
        dpi=150
    )

    plt.close()

    # Guardar tablas generales.
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

    # Guardar tablas del perfil de clientes prioritarios.
    tabla_prioritarios.to_csv(
        config.TABLAS / "perfil_prioritarios_numericas.csv",
        index=False
    )

    tabla_categorias_prioritarios.to_csv(
        config.TABLAS / "perfil_prioritarios_categoricas.csv",
        index=False
    )

    # Mostrar resultados.
    print("\nTabla de deciles:")
    print(deciles.to_string(index=False))

    print("\nTabla de capacidad:")
    print(tabla_capacidad.to_string(index=False))

    print("\nTabla de costos por umbral:")
    print(tabla_costos.to_string(index=False))

    print("\nPerfil numérico: 20 % de mayor riesgo frente al resto")
    print(tabla_prioritarios.to_string(index=False))

    print("\nPerfil categórico: 20 % de mayor riesgo frente al resto")
    print(tabla_categorias_prioritarios.to_string(index=False))

    print("\nTablas guardadas correctamente en reports/tablas/")
    print("\nGráficas guardadas correctamente en reports/figures/")


if __name__ == "__main__":
    main()
