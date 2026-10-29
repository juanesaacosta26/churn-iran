"""Configuración compartida. Solo se cambia en la reunión de cierre de cada bloque."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATA_RAW = RAIZ / "data" / "raw" / "customer_churn.csv"
DATA_PROCESADA = RAIZ / "data" / "processed" / "clientes.csv"
PARTICION = RAIZ / "data" / "processed" / "particion.csv"
PREDICCIONES_BASE = RAIZ / "data" / "processed" / "predicciones_base.csv"
PREDICCIONES_FINAL = RAIZ / "data" / "processed" / "predicciones_final.csv"
FIXTURE_PREDICCIONES = RAIZ / "data" / "processed" / "fixtures" / "predicciones_ejemplo.csv"
FIGURAS = RAIZ / "reports" / "figures"
TABLAS = RAIZ / "reports" / "tablas"

SEMILLA = 42
PROPORCION_PRUEBA = 0.25

# Nombres originales del CSV (con espacios normalizados) -> nombres en español
COLUMNAS = {
    "Call Failure": "fallas_llamada",
    "Complains": "quejas",
    "Subscription Length": "meses_suscripcion",
    "Charge Amount": "nivel_cobro",
    "Seconds of Use": "segundos_uso",
    "Frequency of use": "frecuencia_llamadas",
    "Frequency of SMS": "frecuencia_sms",
    "Distinct Called Numbers": "numeros_distintos",
    "Age Group": "grupo_edad",
    "Tariff Plan": "plan_tarifa",
    "Status": "estado",
    "Age": "edad",
    "Customer Value": "valor_cliente",
    "Churn": "churn",
}

OBJETIVO = "churn"

# Grupos de variables según la pregunta de investigación (uso, servicio, suscripción)
USO = ["segundos_uso", "frecuencia_llamadas", "frecuencia_sms", "numeros_distintos"]
SERVICIO = ["fallas_llamada", "quejas"]
SUSCRIPCION = ["meses_suscripcion", "nivel_cobro", "plan_tarifa", "estado", "valor_cliente"]
DEMOGRAFIA = ["edad", "grupo_edad"]

NUMERICAS = USO + ["fallas_llamada", "meses_suscripcion", "valor_cliente", "edad"]
CATEGORICAS = ["quejas", "nivel_cobro", "plan_tarifa", "estado", "grupo_edad"]

ETIQUETAS = {
    "quejas": {0: "Sin queja", 1: "Con queja"},
    "plan_tarifa": {1: "Pago por uso", 2: "Contrato"},
    "estado": {1: "Activo", 2: "No activo"},
    "churn": {0: "Permanece", 1: "Abandona"},
}

# ---------------------------------------------------------------------------
# Agregado el 28 de octubre al ajustar el calendario. Valores PROVISIONALES:
# se confirman (o cambian) en las reuniones indicadas y se anota en docs/decisiones.md.

# Arranque (jue 29 oct): columna de edad que se quita (son la misma información).
COLUMNA_EDAD_A_QUITAR = "grupo_edad"

# Reunión 1 (lun 2 nov): variables del modelo, según la propuesta de Juanes.
# Provisional = todas menos grupo_edad.
VARIABLES_MODELO = SERVICIO + USO + SUSCRIPCION + ["edad"]
# Sensibilidad ("¿en qué medida?", bloque 2):
VARIABLES_SIN_ESTADO_QUEJAS = [v for v in VARIABLES_MODELO if v not in ("estado", "quejas")]
VARIABLES_SOLO_USO = USO + ["fallas_llamada"]

PLIEGUES_CV = 5

# Reunión 2 (sáb 7 nov): un falso negativo cuesta k veces un falso positivo.
K_COSTOS = [2, 5, 10]
# Fracción de clientes que el equipo de retención alcanza a contactar.
CAPACIDADES = (0.10, 0.20, 0.30)
