# Primera entrega (17 de septiembre de 2026) — resumen

**Riesgo de abandono de clientes en una empresa de telecomunicaciones iraní**
Ianis Ramírez Cárdenas · Juan Esteban Acosta Morales — Pensamiento Crítico II, Universidad Externado de Colombia.
Docente: Ghislaine Tibaire Murzi Sifontes. El documento completo está en el proyecto (`Primera Entrega del Proyecto Integrador - IRC - PC2.docx`).

## Pregunta
¿En qué medida las características de uso, servicio y suscripción observadas durante los primeros nueve meses
permiten identificar y predecir qué clientes presentan mayor riesgo de abandono al finalizar los doce meses,
para así apoyar la priorización de acciones de retención durante la brecha de planificación de tres meses?

## Objetivo general
Analizar la medida en que las características observadas de uso, servicios y suscripción de los clientes durante
los primeros nueve meses permiten identificar cuáles presentan mayor riesgo de churn al finalizar los doce meses,
con el propósito de apoyar la priorización de clientes para posibles acciones de retención.

## Objetivos específicos → dónde se trabajan en el repositorio
1. Identificar las características de comportamiento con mayor relación con el abandono → `src/churn/relacion.py` (Juanes, bloque 1) y modelos (Juanes, bloque 2).
2. Caracterizar el comportamiento según la condición final de abandono → `src/churn/caracterizacion.py` (Ianis, bloque 2).
3. (Objetivo general) Predecir y apoyar la priorización → `src/churn/modelos.py` (Juanes, bloque 2) y `src/churn/priorizacion.py` (Ianis, bloques 2 y 3).

## Alcance y limitaciones (recordatorio)
- 3150 clientes, unidad de análisis = cliente; no se incorporan variables externas.
- No se evalúan estrategias de retención ni se afirma causalidad: se evalúa capacidad de identificar y predecir.
- Riesgos: falsos positivos (recursos mal usados) y falsos negativos (oportunidad perdida); privacidad de datos.

## Referencias
- Arai, K., Fujikawa, I., Nakagawa, Y., Momozaki, R., & Ogawa, S. (2023). Churn customer estimation method based on LightGBM for improving sales. *IJACSA, 14*(2), 119–125.
- Iranian Churn [Dataset]. (2020). UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
