# Riesgo de abandono (churn) — Telco iraní

Proyecto Integrador · Pensamiento Crítico II · Universidad Externado de Colombia
**Ianis Ramírez Cárdenas** y **Juan Esteban Acosta Morales** · Entrega final: inicios de noviembre de 2026

> ¿En qué medida las características de uso, servicio y suscripción de los primeros 9 meses permiten
> identificar y predecir qué clientes abandonarán al mes 12, para priorizar acciones de retención?

**Plan de trabajo semana a semana: [GUIA.md](GUIA.md)** ← empezar aquí.

## Estructura

```
churn-iran/
├── GUIA.md                     Plan semana a semana, quién hace qué
├── data/
│   ├── raw/customer_churn.csv  Base original UCI (no se modifica nunca)
│   └── processed/              Lo que generan los scripts (clientes.csv, particion.csv, predicciones_*.csv)
│       └── fixtures/           Archivos de ejemplo para trabajar sin esperar al otro
├── src/churn/                  La lógica (funciones que se prueban)
│   ├── config.py               Rutas, semilla, nombres de columnas      (ambos, solo en reunión)
│   ├── datos.py                Carga y limpieza                          (Ianis)
│   ├── caracterizacion.py      Objetivo específico 2                     (Ianis)
│   ├── priorizacion.py         Deciles, lift, umbral por costos          (Ianis)
│   ├── relacion.py             Objetivo específico 1                     (Juanes)
│   ├── modelos.py              Partición y modelos                       (Juanes)
│   └── evaluacion.py           Métricas y curvas                         (Juanes)
├── scripts/                    Lo que se corre: preparar_datos.py (Ianis), entrenar.py (Juanes)
├── notebooks/                  Exploración y gráficas; sufijo _I = Ianis, _J = Juanes
├── tests/                      Pruebas (pytest)
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
pytest -q          # deben pasar las 4 pruebas de datos crudos
```

## Correr todo (cuando esté terminado)

```bash
python scripts/preparar_datos.py   # data/processed/clientes.csv
python scripts/entrenar.py         # data/processed/predicciones_final.csv
pytest -q
```

Los scripts necesitan ver el paquete: en Mac/Linux `export PYTHONPATH=src`; en Windows (PowerShell) `$env:PYTHONPATH="src"`.

## Reglas cortas

1. Cada quien trabaja en **su rama** y en **sus archivos** (tabla "Quién es quién" en GUIA.md).
2. `data/raw/` no se toca. Todo lo procesado sale de un script.
3. La lógica va en `src/churn/`; los notebooks solo muestran.
4. Una vez por semana (sábado) se hace la reunión de PR: se revisan, se fusionan a `main` y se etiqueta la semana.
5. Toda decisión que cambie cifras se anota en `docs/decisiones.md`.

Fuente de datos: Iranian Churn Dataset, UCI Machine Learning Repository (2020).
