# Riesgo de abandono (churn) — Telco iraní

Proyecto Integrador · Pensamiento Crítico II · Universidad Externado de Colombia
**Ianis Ramírez Cárdenas** y **Juan Esteban Acosta Morales** · Informe: 9 de noviembre de 2026 · Presentación: 13 de noviembre de 2026

> ¿En qué medida las características de uso, servicio y suscripción de los primeros 9 meses permiten
> identificar y predecir qué clientes abandonarán al mes 12, para priorizar acciones de retención?

**Bitácora de decisiones:** [`docs/decisiones.md`](docs/decisiones.md) · **Plan de trabajo:** [GUIA.md](GUIA.md)

## Resultados en una línea

Con las 10 variables del modelo, un **bosque aleatorio** alcanza al 91 % de los clientes que abandonan
llamando solo al 20 % de la base (AUC-PR 0.91 en 713 clientes de prueba; el azar da 0.16). La
**regresión logística bayesiana** explica el peso de cada variable con su incertidumbre: una queja
multiplica las *odds* de abandonar por unas 35 (IC 95 %: 20 a 62).

## Instalación (una vez)

```bash
git clone https://github.com/juanesaacosta26/churn-iran.git
cd churn-iran
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducir todo desde cero

Correr en este orden desde la carpeta del repositorio. Cada script lee lo que generó el anterior.

| # | Comando | Qué genera | Dueño |
|---|---|---|---|
| 1 | `python scripts/preparar_datos.py` | `data/processed/clientes.csv` (2850 clientes, sin duplicados) y `docs/calidad_datos.md` | Ianis |
| 2 | `python scripts/relacionar.py` | Objetivo específico 1: `relacion_churn.csv`, `tasa_por_categoria.csv`, `vif.csv`, `redundancias.csv`, `correlaciones.png` | Juanes |
| 3 | `python scripts/caracterizar.py` | Objetivo específico 2: `caracterizacion_numericas.csv`, `caracterizacion_categoricas.csv` | Ianis |
| 4 | `python scripts/entrenar.py` | Partición (`particion.csv`: 2137 entrenamiento, 713 prueba) y logística → `predicciones_base.csv`, `logistica_coeficientes.csv` | Juanes |
| 5 | `python scripts/bayes.py` | Logística bayesiana (≈ 3 min): `bayes_*.csv`, `bayes_*.png`, `predicciones_bayes.csv`. Prueba rápida: `--rapido` | Juanes |
| 6 | `python scripts/comparar.py` | 12 configuraciones en validación cruzada y en prueba, reglas R1/R2, criterios C1–C4: `comparacion_modelos.csv`, `metricas_prueba_todos.csv`, `criterios_avance2.json`, `curvas_roc_pr.png` | Juanes |
| 7 | `python scripts/entrenar.py --final --modelo bosque` | Modelo final → `predicciones_final.csv` | Juanes |
| 8 | `python scripts/interpretar.py` | Importancia por permutación del bosque y árbol dibujado: `importancia.png`, `arbol.png`, `importancia_permutacion.csv` | Juanes |
| 9 | `python scripts/priorizar.py --predicciones data/processed/predicciones_final.csv` | Priorización con el modelo final: `priorizacion_deciles.csv`, `priorizacion_capacidad.csv` | Ianis |
| 10 | `pytest -q -rs` | Verifica las cifras de referencia | Ambos |

Las tablas quedan en `reports/tablas/` y las figuras en `reports/figures/`. Todas las semillas son 42,
así que las cifras se repiten exactamente. La excepción es la logística bayesiana: por usar MCMC, en otro
computador sus cifras pueden variar en el segundo o tercer decimal (error de Monte Carlo), sin cambiar
ninguna conclusión.

**Versión en R (opcional):** `Rscript scripts/bayes_rstanarm.R` ajusta la misma logística bayesiana con
`rstanarm` para contrastar con la implementación en Python. Necesita los pasos 1 y 4.

## Estructura

```
churn-iran/
├── data/
│   ├── raw/customer_churn.csv  Base original UCI (no se modifica nunca)
│   └── processed/              Lo que generan los scripts (clientes, partición, predicciones)
├── src/churn/                  La lógica (funciones que se prueban)
│   ├── config.py               Rutas, semilla, variables del modelo y decisiones
│   ├── datos.py                Carga y limpieza                          (Ianis)
│   ├── caracterizacion.py      Objetivo específico 2                     (Ianis)
│   ├── priorizacion.py         Deciles, capacidad, umbral por costos     (Ianis)
│   ├── relacion.py             Objetivo específico 1                     (Juanes)
│   ├── modelos.py              Partición, modelos y comparación          (Juanes)
│   ├── bayes.py                Logística bayesiana (HMC, diagnósticos)   (Juanes)
│   └── evaluacion.py           Métricas                                  (Juanes)
├── scripts/                    Un script por paso (tabla de arriba)
├── notebooks/                  Lectura de resultados; sufijo _I = Ianis, _J = Juanes
├── tests/                      Pruebas (pytest) con las cifras de referencia
├── reports/                    figures/, tablas/ e informe_final.md
├── presentacion/               Diapositivas
└── docs/                       Decisiones, diccionario, calidad, hallazgos, resultados bayesianos y fuentes de las previas
```

## Documentos clave

- [`docs/decisiones.md`](docs/decisiones.md): cada decisión que cambia cifras, con fecha, razón y responsable.
- [`docs/hallazgos.md`](docs/hallazgos.md): hallazgos de la caracterización.
- [`docs/bayes_resultados.md`](docs/bayes_resultados.md): resultados completos de la logística bayesiana.
- [`docs/fuentes_previas.md`](docs/fuentes_previas.md): de dónde salen las previas y cómo se convirtieron.

## Reglas cortas

1. Cada quien trabaja en **su rama** y en **sus archivos**.
2. `data/raw/` no se toca. Todo lo procesado sale de un script.
3. La lógica va en `src/churn/`; los notebooks solo muestran.
4. Toda decisión que cambie cifras se anota en `docs/decisiones.md`.

Fuente de datos: Iranian Churn Dataset, UCI Machine Learning Repository (2020).
