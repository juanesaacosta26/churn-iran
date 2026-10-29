# Riesgo de abandono (churn) — Telco iraní

Proyecto Integrador · Pensamiento Crítico II · Universidad Externado de Colombia
**Ianis Ramírez Cárdenas** y **Juan Esteban Acosta Morales** · **Presentación: viernes 13 de noviembre de 2026**

> ¿En qué medida las características de uso, servicio y suscripción de los primeros 9 meses permiten
> identificar y predecir qué clientes abandonarán al mes 12, para priorizar acciones de retención?

**Plan de trabajo día a día: [GUIA.md](GUIA.md)** ← empezar aquí.

## Estructura

```
churn-iran/
├── GUIA.md                     Plan por bloques hasta el 13 de noviembre, quién hace qué
├── data/
│   ├── raw/customer_churn.csv  Base original UCI (no se modifica nunca)
│   └── processed/              Lo que generan los scripts (clientes.csv, particion.csv, predicciones_*.csv)
│       └── fixtures/           Archivos de ejemplo para trabajar sin esperar al otro
├── src/churn/                  La lógica (funciones que se prueban)
│   ├── config.py               Rutas, semilla, columnas y decisiones      (ambos, solo en reunión)
│   ├── datos.py                Carga y limpieza                          (Ianis)
│   ├── caracterizacion.py      Objetivo específico 2                     (Ianis)
│   ├── priorizacion.py         Deciles, capacidad, umbral por costos     (Ianis)
│   ├── relacion.py             Objetivo específico 1                     (Juanes)
│   ├── modelos.py              Partición, modelos y comparación          (Juanes)
│   └── evaluacion.py           Métricas y curvas                         (Juanes)
├── scripts/                    preparar_datos.py y priorizar.py (Ianis), entrenar.py (Juanes)
├── notebooks/                  Exploración y gráficas; sufijo _I = Ianis, _J = Juanes
├── tests/                      Pruebas (pytest), ya escritas con las cifras de referencia
├── reports/                    figures/, tablas/ e informe_final.md
├── presentacion/               Diapositivas finales
└── docs/                       Diccionario, decisiones, contrato, hallazgos, primera entrega
```

## Instalación (una vez)

```bash
git clone https://github.com/<USUARIO>/churn-iran.git
cd churn-iran
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q          # al inicio: 4 passed, 28 skipped
```

Las pruebas *skipped* son las de funciones que todavía no están implementadas. Cada vez que alguien implementa la suya, sus pruebas empiezan a comprobar las cifras de referencia. Para ver qué falta: `pytest -q -rs`. Meta del martes 10 de noviembre: 0 skipped.

## Correr todo (cuando esté terminado)

```bash
python scripts/preparar_datos.py                       # data/processed/clientes.csv
python scripts/entrenar.py                             # predicciones_base.csv (logística)
python scripts/entrenar.py --final --modelo <nombre>   # predicciones_final.csv
python scripts/priorizar.py --predicciones data/processed/predicciones_final.csv
pytest -q
```

## Reglas cortas

1. Cada quien trabaja en **su rama** y en **sus archivos** (tabla "Quién es quién" en GUIA.md).
2. `data/raw/` no se toca. Todo lo procesado sale de un script.
3. La lógica va en `src/churn/`; los notebooks solo muestran.
4. Al cierre de cada bloque se hace la reunión de PR (lunes 2, sábado 7 y martes 10 de noviembre): se revisan, se fusionan a `main` y se etiqueta.
5. Toda decisión que cambie cifras se anota en `docs/decisiones.md`.

Fuente de datos: Iranian Churn Dataset, UCI Machine Learning Repository (2020).
