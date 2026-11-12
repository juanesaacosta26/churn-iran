# Predicción del riesgo de abandono de clientes en una telco iraní con regresión logística bayesiana

**Ianis Ramírez Cárdenas** y **Juan Esteban Acosta Morales**
Proyecto Integrador · Estadística Bayesiana y Pensamiento Crítico II · Universidad Externado de Colombia · Noviembre de 2026

📄 **[Informe final (PDF)](reports/informe_final.pdf)**

> **Pregunta de investigación.** ¿En qué medida las características de uso, servicio y suscripción de los
> primeros nueve meses permiten identificar y predecir qué clientes abandonarán al mes doce, y cuáles son
> las variables que más pesan, para priorizar acciones de retención?

## Resultados principales

| | Cifra | Fuente |
|---|---|---|
| Base de trabajo | 2850 clientes únicos (se quitaron 300 duplicados exactos), 446 abandonos (15.6 %) | `docs/calidad_datos.md` |
| Partición | 2137 entrenamiento / 713 prueba (112 abandonos), estratificada, semilla 42 | `data/processed/particion.csv` |
| Señal más fuerte | Una queja multiplica las *odds* de abandonar por **35.3** (IC de credibilidad 95 %: 20.4 a 62.0); P(OR > 10) ≈ 1 | `reports/tablas/bayes_vs_clasica_coeficientes.csv` |
| Segunda señal | Estado no activo: OR **3.28** (2.12 a 5.11), cerca del 4.3 publicado en Corea | ídem |
| Sin efecto | Edad (OR 0.99 por 10 años) y plan (OR 0.83): sus intervalos contienen el 1 | ídem |
| Logística bayesiana vs. clásica | AUC-ROC 0.929 y 0.930; AUC-PR 0.765 y 0.766 (azar = 0.157) | `reports/tablas/bayes_vs_clasica_metricas.csv` |
| Convergencia (HMC) | 4 cadenas × 2000 muestras, R̂ ≤ 1.003, n_eff mínimo 4392, 0 divergencias | `reports/tablas/bayes_diagnosticos.csv` |
| Modelo para priorizar | Bosque aleatorio: AUC-PR **0.907**; contactando al **20 %** de mayor riesgo se encuentra el **91.1 %** de los abandonos | `reports/tablas/priorizacion_capacidad.csv` |
| Sin queja ni estado | La logística conserva AUC-PR 0.46 (casi 3 veces el azar); el bosque, 0.80 | `reports/tablas/bayes_variantes.csv`, `sensibilidad_variables.csv` |

**En una frase:** los nueve meses de uso anticipan bien el abandono; la logística bayesiana explica *qué pesa y con
cuánta incertidumbre* y el bosque aleatorio *ordena a quién llamar primero*. El efecto de la queja es mucho mayor que
el de la literatura (OR ≈ 1.7), lo que sugiere que pudo registrarse cerca del abandono (posible fuga de información).

## Datos

Iranian Churn Dataset (Keramati et al., 2014), [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset):
3150 registros de clientes de un operador iraní, 13 variables de los primeros nueve meses y el estado de abandono al
mes doce. El archivo original está en `data/raw/customer_churn.csv` y no se modifica. Diccionario en
[`docs/diccionario_datos.md`](docs/diccionario_datos.md).

## Método

1. **Limpieza:** se quitan 300 duplicados exactos y las variables redundantes `grupo_edad`, `valor_cliente`
   (VIF 53) y `frecuencia_llamadas` (r = 0.95 con `segundos_uso`). Quedan 10 predictores, todos con VIF ≤ 2.3.
2. **Modelo principal:** regresión logística bayesiana
   `Y ~ Bernoulli(π)`, `logit(π) = β0 + Σ βj xj`, con **previas de la literatura** descontadas (*power priors*) para
   estado y queja (Ahn et al., 2006) y antigüedad (operador del Reino Unido, 2016), y N(0, 2.5) para el resto.
   Se compara con una previa débilmente informativa (la de `rstanarm`).
3. **Estimación:** Monte Carlo hamiltoniano implementado con numpy (Laplace y Metropolis se probaron y descartaron).
4. **Validación:** chequeo predictivo posterior, sensibilidad a la previa (desviaciones × 0.5, 2 y 4), WAIC para
   modelos con menos variables y evaluación única en prueba.
5. **Comparación:** logística clásica (máxima verosimilitud), árbol, bosque aleatorio y boosting con validación
   cruzada de 5 pliegues, y dos reglas simples (R1: quien se quejó; R2: queja o no activo).
6. **Priorización:** deciles, capacidad de contacto (10, 20 y 30 %), costos de error y auditoría de errores por
   subgrupo.

Todas las decisiones que cambian cifras, con su razón, están en [`docs/decisiones.md`](docs/decisiones.md).

## Reproducir los resultados

```bash
git clone https://github.com/juanesaacosta26/churn-iran.git
cd churn-iran
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Correr en este orden desde la carpeta del repositorio (cada script lee lo que generó el anterior):

| # | Comando | Qué genera |
|---|---|---|
| 1 | `python scripts/preparar_datos.py` | `data/processed/clientes.csv` (2850 clientes) y `docs/calidad_datos.md` |
| 2 | `python scripts/relacionar.py` | Relación de cada variable con el abandono, VIF y redundancias, `correlaciones.png` |
| 3 | `python scripts/caracterizar.py` | Comparación de quienes abandonan frente a quienes permanecen |
| 4 | `python scripts/entrenar.py` | Partición y logística → `predicciones_base.csv` |
| 5 | `python scripts/bayes.py` | Logística bayesiana (≈ 2–3 min; prueba rápida con `--rapido`): `bayes_*.csv`, `bayes_*.png`, `predicciones_bayes.csv` |
| 6 | `python scripts/comparar.py` | 12 configuraciones en validación cruzada y prueba, reglas R1/R2, criterios C1–C4, `curvas_roc_pr.png` |
| 7 | `python scripts/entrenar.py --final --modelo bosque` | Modelo final → `predicciones_final.csv` |
| 8 | `python scripts/interpretar.py` | Importancia por permutación y árbol dibujado |
| 9 | `python scripts/priorizar.py --predicciones data/processed/predicciones_final.csv` | Deciles, capacidad, costos, perfil del grupo prioritario y errores por subgrupo |
| 10 | `pytest -q -rs` | Verifica las cifras de referencia (37 pruebas) |

Las tablas quedan en `reports/tablas/` y las figuras en `reports/figures/`. Todas las semillas son 42, así que las
cifras se repiten exactamente; la excepción es la logística bayesiana, cuyas cifras pueden variar en el segundo o
tercer decimal entre computadores (error de Monte Carlo) sin cambiar ninguna conclusión.

**Versión en R (opcional):** `Rscript scripts/bayes_rstanarm.R` ajusta la misma logística bayesiana con `rstanarm`
(necesita los pasos 1 y 4).

## Estructura

```
churn-iran/
├── data/
│   ├── raw/customer_churn.csv   Base original UCI (no se modifica)
│   └── processed/               Base limpia, partición y predicciones (salen de los scripts)
├── src/churn/                   Lógica del proyecto (funciones con pruebas)
│   ├── config.py                Rutas, semilla y variables del modelo
│   ├── datos.py                 Carga y limpieza
│   ├── relacion.py              Relación de cada variable con el abandono
│   ├── caracterizacion.py       Quienes abandonan frente a quienes permanecen
│   ├── modelos.py               Partición, modelos y comparación
│   ├── bayes.py                 Logística bayesiana (previas, HMC, diagnósticos)
│   ├── evaluacion.py            Métricas
│   └── priorizacion.py          Deciles, capacidad, costos y errores por subgrupo
├── scripts/                     Un script por paso (tabla de arriba)
├── notebooks/                   Lectura comentada de los resultados (01 a 05)
├── tests/                       Pruebas con las cifras de referencia
├── reports/
│   ├── informe_final.pdf        Informe final
│   ├── figures/                 Figuras
│   └── tablas/                  Tablas
└── docs/                        Decisiones, diccionario, calidad, hallazgos, resultados bayesianos y fuentes de las previas
```

## Documentación

- [`reports/informe_final.pdf`](reports/informe_final.pdf): informe final (artículo).
- [`docs/bayes_resultados.md`](docs/bayes_resultados.md): resultados completos de la logística bayesiana.
- [`docs/fuentes_previas.md`](docs/fuentes_previas.md): de dónde salen las previas y cómo se convirtieron.
- [`docs/hallazgos.md`](docs/hallazgos.md): hallazgos de la caracterización y la priorización.
- [`docs/decisiones.md`](docs/decisiones.md): bitácora de decisiones.
- [`docs/calidad_datos.md`](docs/calidad_datos.md) y [`docs/diccionario_datos.md`](docs/diccionario_datos.md): calidad y variables.
- [`docs/contrato_predicciones.md`](docs/contrato_predicciones.md): formato de los archivos de predicciones.

## Limitaciones

Las conclusiones son predictivas, no causales. No se sabe cuándo se registraron la queja y el estado; si fue cerca del
mes doce, serían casi el resultado, por eso se reportan los modelos sin ellas. Los datos son de un solo operador, un
año y solo voz y SMS, e incluyen solo clientes con al menos tres meses de antigüedad (sesgo de supervivencia).

## Referencia

Ramírez Cárdenas, I. y Acosta Morales, J. E. (2026). *Predicción del riesgo de abandono de clientes en una empresa de
telecomunicaciones iraní mediante regresión logística bayesiana*. Universidad Externado de Colombia.
