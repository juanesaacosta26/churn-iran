"""Configuración compartida. Solo se cambia en la reunión semanal (cierre de semana)."""
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
