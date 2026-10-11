# Churn Telco Irán: guía semana a semana

Octubre 10, 2026 · Ianis y Juanes

## Cómo usar esta guía

Cada persona busca su nombre dentro de la semana en la que va y sigue las sesiones en orden, marcando las casillas. Al final de cada sesión debe poder mostrar lo que dice **"Listo cuando"**. Las cifras de "Listo cuando" se calcularon al armar el repositorio: si a ustedes les da algo distinto, no es necesariamente un error, pero hay que entender por qué y anotarlo en `docs/decisiones.md`.

**Fechas:** arranque = domingo 11 de octubre · reuniones de PR = sábados 17, 24 y 31 de octubre · ensayo y cierre = jueves 5 de noviembre · **entrega ≈ viernes 6 de noviembre** (ajusten a la fecha exacta que dé la profesora). Los lunes 12 de octubre y 2 de noviembre son festivos.

**Carga:** tres sesiones por semana de 2 a 3 horas cada una (unas 7–8 horas por persona por semana) más la reunión del sábado.

### Quién es quién

| Persona | Letra | Rol | Archivos suyos |
|---|---|---|---|
| Ianis | I | Datos, caracterización y priorización | `scripts/preparar_datos.py`, `scripts/priorizar.py`, `src/churn/datos.py`, `src/churn/caracterizacion.py`, `src/churn/priorizacion.py`, notebooks `*_I.ipynb`, `docs/calidad_datos.md`, `docs/diccionario_datos.md` |
| Juanes | J | Repositorio, relación de variables y modelos | `.github/`, `scripts/entrenar.py`, `src/churn/relacion.py`, `src/churn/modelos.py`, `src/churn/evaluacion.py`, notebooks `*_J.ipynb`, `README.md` |
| Ambos | — | Se cambian **solo en la reunión** | `src/churn/config.py`, `docs/decisiones.md`, `docs/hallazgos.md`, `docs/contrato_predicciones.md`, `reports/informe_final.md` (cada quien sus secciones) |

Cómo se reparte el proyecto frente a la primera entrega:

- **Objetivo específico 1** (variables más relacionadas con el abandono) → Juanes, semana 1, y lo confirma con los modelos en la semana 3.
- **Objetivo específico 2** (caracterizar a quienes abandonan frente a quienes permanecen) → Ianis, semana 2.
- **Objetivo general** (predecir y apoyar la priorización) → Juanes construye el modelo (semanas 2 y 3) e Ianis lo convierte en una lista de prioridades para el equipo de retención (semana 3).
- **Informe y presentación** → mitad y mitad (semana 4).

La letra se usa en las ramas (`i/s1-datos`, `j/s2-modelo-base`) y en los notebooks (`02_caracterizacion_I.ipynb`).

### Rutina de cada semana

1. **Lunes o martes (5 min, por chat):** cada quien escribe qué sesiones va a hacer esta semana, copiándolas de esta guía.
2. **Durante la semana:** trabajen solo en su rama y en sus archivos. Si necesitan algo del otro, usen el fixture o el contrato (ver abajo); no esperen.
3. **Miércoles (5 min, por chat):** tres líneas: qué terminé, qué me falta, qué me bloquea. Suban sus cambios a su rama aunque no estén terminados (`git push`).
4. **Viernes, antes de las 20:00:** cada quien abre su PR.
5. **Sábado, reunión semanal (1 a 1.5 h, en llamada):** cada quien comparte pantalla y muestra `pytest` en verde y su resultado. El otro aprueba si se cumple el "Listo cuando". Se fusiona a `main`, se toman las decisiones pendientes y se anotan en `docs/decisiones.md`, se etiqueta la semana (`s1`, `s2`…) y los dos hacen `git checkout main && git pull` para empezar la siguiente.

### Cómo abrir un PR (para los dos)

```
git checkout main && git pull
git checkout -b i/s2-caracterizacion      # su letra / semana-tema
# ... trabajar, guardar ...
git add src/churn/caracterizacion.py      # solo los archivos que tocaron, nunca git add .
git commit -m "caracterizacion: tabla de numéricas con Mann-Whitney"
git push -u origin i/s2-caracterizacion
# en GitHub: "Compare & pull request" y llenar la plantilla
```

En la reunión no se piden cambios de estilo; solo se bloquea un PR si algo no funciona, si una cifra no tiene respaldo o si toca archivos del otro.

### Palabras que se usan en la guía

- **Contrato:** el formato del archivo de predicciones que Juanes le entrega a Ianis (`docs/contrato_predicciones.md`): `fila_original`, `conjunto`, `churn_real`, `prob_churn`, `modelo`.
- **Fixture:** un archivo de ejemplo con el formato del contrato, ya creado en `data/processed/fixtures/predicciones_ejemplo.csv`, para que Ianis trabaje la priorización sin esperar el modelo. Sus cifras **no** van en el informe.
- **Base cruda / base limpia:** `data/raw/customer_churn.csv` (3150 filas, nunca se modifica) / `data/processed/clientes.csv` (lo genera el script de Ianis).
- **Partición:** la división fija entrenamiento/prueba en `data/processed/particion.csv`. Los dos usan la misma.
- **Cifras congeladas:** después del cierre de la semana 3 ningún número cambia; el informe se escribe sobre esas cifras.

---

## Semana 0 · domingo 11 de octubre · Arranque

**Objetivo:** el repositorio en GitHub, los dos con el proyecto corriendo en su computador.

**Juanes · subir el repositorio (1 h, antes de la llamada)**

- [ ] Crear en GitHub un repositorio **privado** llamado `churn-iran`, vacío (sin README).
- [ ] Descomprimir `churn-iran.zip`; ya trae git iniciado con un primer commit. Dentro de la carpeta: `git remote add origin https://github.com/<USUARIO>/churn-iran.git` y `git push -u origin main`.
- [ ] Settings → Collaborators: invitar a Ianis.
- [ ] Settings → Branches: proteger `main` (requerir PR, 1 aprobación y que pase el check "pruebas").
- [ ] Cambiar `@USUARIO_IANIS` y `@USUARIO_JUANES` en `.github/CODEOWNERS` por los usuarios reales.
- **Listo cuando:** la pestaña Actions muestra "pruebas" en verde.

**Los dos · reunión de arranque (1.5 h, en llamada)**

- [ ] (15 min) Leer juntos esta sección y el README.
- [ ] (20 min) Juanes comparte pantalla y recorre las carpetas; ubicar los archivos de cada uno en la tabla "Quién es quién".
- [ ] (20 min) Cada quien clona, crea su entorno (`python -m venv .venv`), instala `requirements.txt` y corre `pytest -q`: deben pasar 4 pruebas.
- [ ] (25 min) Tomar las dos primeras decisiones y anotarlas en `docs/decisiones.md`: ¿se quitan las 300 filas duplicadas? (sugerido: sí) y ¿se usa `edad` o `grupo_edad`? (son la misma información).
- [ ] (10 min) Confirmar la fecha exacta de entrega y si la profesora pide un formato (Word, PDF, plantilla, número de páginas, tiempo de presentación).

---

## Semana 1 · 12 al 17 de octubre · Datos limpios y relación con el abandono

**Objetivo de la semana:** una base limpia y documentada, y una primera respuesta al objetivo específico 1. Al cierre, cualquiera puede correr `python scripts/preparar_datos.py` y obtener `clientes.csv`.

### Ianis

**Sesión 1 · datos limpios (2.5 h)**

- [ ] En `scripts/preparar_datos.py`: contar las filas duplicadas exactas (comparando todas las columnas menos `fila_original`). Deben ser 300.
- [ ] Quitarlas conservando la primera aparición (según lo decidido el domingo).
- [ ] Quitar `grupo_edad` o `edad` (según lo decidido).
- [ ] Guardar `data/processed/clientes.csv` sin índice.
- **Listo cuando:** `clientes.csv` tiene 2850 filas y 446 clientes que abandonan (15.6 %).

**Sesión 2 · calidad de los datos (2.5 h)**

- [ ] Que el mismo script escriba `docs/calidad_datos.md`: por columna mínimo, percentil 5, mediana, percentil 95, máximo, número de ceros y número de atípicos (regla de 1.5 × IQR).
- [ ] Agregar los casos raros: los 107 clientes con `segundos_uso = 0` (¿cuántos abandonan?), y cualquier otro rango sospechoso.
- [ ] En `src/churn/datos.py`, implementar `cargar_limpio()`.
- [ ] Crear `tests/test_preparar.py`: 2850 filas, sin duplicados, `churn` solo 0 y 1, `fila_original` única.
- **Listo cuando:** `pytest -q` pasa y `calidad_datos.md` se regenera solo al correr el script.

**Sesión 3 · distribuciones y diccionario (2 h)**

- [ ] En `notebooks/01_calidad_datos_I.ipynb`: histograma de cada variable numérica; guardar `reports/figures/distribuciones.png`.
- [ ] Completar `docs/diccionario_datos.md` con los rangos reales.
- [ ] Abrir el PR `i/s1-datos`.
- **Listo cuando:** el PR está abierto y el check "pruebas" está en verde.

### Juanes

**Sesión 1 · relación con el abandono (2.5 h)**

- [ ] En `src/churn/relacion.py`, `correlacion_con_churn(df)`: correlación punto-biserial y de Spearman de cada predictor con `churn`, con su p-valor, ordenada por valor absoluto. Usar `cargar_crudo()` esta semana (en la semana 2 se cambia a `cargar_limpio()`).
- [ ] `tasa_por_categoria(df, columna)`: n y tasa de churn por nivel.
- [ ] Guardar `reports/tablas/relacion_churn.csv`.
- **Listo cuando:** en la base cruda el orden empieza con `quejas` (0.53), `estado` (0.50) y `frecuencia_llamadas` (0.30).

**Sesión 2 · redundancias (2.5 h)**

- [ ] `redundancias(df, umbral=0.8)`: pares de predictores con |r| ≥ 0.8 y el VIF de cada uno (`statsmodels`).
- [ ] Mapa de calor en `reports/figures/correlaciones.png`.
- [ ] Revisar en especial: `edad`–`grupo_edad`, `segundos_uso`–`frecuencia_llamadas` y `valor_cliente` contra las de uso.
- [ ] Escribir en `docs/decisiones.md` una propuesta: qué variables entran al modelo y qué hacer con `estado` y `quejas` (¿son señales tempranas o casi el resultado?).
- **Listo cuando:** la tabla de pares y VIF existe y la propuesta está escrita para discutirla el sábado.

**Sesión 3 · pruebas y notebook (2 h)**

- [ ] `tests/test_relacion.py`: `quejas` es la de mayor correlación; la tasa de churn con queja es mayor a 0.8 y sin queja menor a 0.11.
- [ ] `notebooks/03_relacion_variables_J.ipynb`: las tres gráficas más claras y un párrafo de lectura.
- [ ] Dos líneas en `docs/hallazgos.md`, cada una con su cifra.
- [ ] Abrir el PR `j/s1-relacion`.
- **Listo cuando:** el PR está abierto y en verde.

**Cierre de la semana 1 · sábado 17 (1 h):** se fusiona primero el PR de Ianis y luego el de Juanes. Se decide qué variables entran al modelo (propuesta de Juanes) y se anota. Se etiqueta `s1`.

---

## Semana 2 · 19 al 24 de octubre · Caracterización y modelo base

**Objetivo de la semana:** responder el objetivo específico 2 con cifras y pruebas estadísticas, y tener el primer modelo con su archivo de predicciones. Los dos parten de `main` con la etiqueta `s1` y usan `cargar_limpio()`.

### Ianis

**Sesión 1 · variables numéricas (2.5 h)**

- [ ] En `src/churn/caracterizacion.py`, `tabla_numericas(df)`: por variable, mediana, Q1 y Q3 de quienes abandonan y de quienes permanecen, p-valor de Mann-Whitney y tamaño del efecto (r = Z/√n o delta de Cliff).
- [ ] Ordenar por tamaño del efecto y guardar `reports/tablas/caracterizacion_numericas.csv`.
- **Listo cuando:** la mediana de `segundos_uso` es 1256.5 en quienes abandonan contra 3596.5 en quienes permanecen, y la de `frecuencia_llamadas` 29 contra 64.

**Sesión 2 · variables categóricas (2.5 h)**

- [ ] `tabla_categoricas(df)`: por variable y nivel, n, tasa de churn y p-valor de chi² (o Fisher si hay celdas pequeñas).
- [ ] Guardar `reports/tablas/caracterizacion_categoricas.csv`.
- **Listo cuando:** con queja 82.6 % contra 9.8 % sin queja; no activo 47.5 % contra 5.6 % activo; contrato 2.6 % contra 16.8 % pago por uso.

**Sesión 3 · figuras y hallazgos (2.5 h)**

- [ ] Diagramas de caja por grupo de churn (escala logarítmica para las de uso) y barras de tasa de churn por categoría; guardar en `reports/figures/caracterizacion_*.png`.
- [ ] `notebooks/02_caracterizacion_I.ipynb` con la lectura de las figuras.
- [ ] Cinco hallazgos en `docs/hallazgos.md`, cada uno con cifra y figura de respaldo.
- [ ] `tests/test_caracterizacion.py` con las cifras de las sesiones 1 y 2.
- [ ] Abrir el PR `i/s2-caracterizacion`.
- **Listo cuando:** los cinco hallazgos están escritos y el PR está en verde.

### Juanes

**Sesión 1 · partición y logística (2.5 h)**

- [ ] En `src/churn/modelos.py`, `particion(df)`: entrenamiento/prueba estratificado por `churn`, 25 % de prueba, semilla 42; guardar `data/processed/particion.csv`.
- [ ] `entrenar("logistica", X, y)`: `StandardScaler` + `LogisticRegression` en un `Pipeline`, con las variables acordadas el sábado.
- **Listo cuando:** 2137 clientes en entrenamiento y 713 en prueba, con 112 que abandonan en prueba.

**Sesión 2 · evaluación (2.5 h)**

- [ ] En `src/churn/evaluacion.py`, `metricas(y, prob, umbral)`: AUC-ROC, AUC-PR, recall, precisión, F1, falsos positivos y falsos negativos.
- [ ] Curva ROC y curva precisión-recall en `reports/figures/`.
- **Listo cuando:** la logística da un AUC-ROC cercano a 0.93 en prueba (como referencia, con todas las variables menos `grupo_edad` da 0.933).

**Sesión 3 · predicciones base (2.5 h)**

- [ ] `scripts/entrenar.py`: corre partición, logística y escribe `data/processed/predicciones_base.csv` con el formato del contrato.
- [ ] `tests/test_modelos.py`: la partición mantiene la proporción de churn, ningún cliente aparece en los dos conjuntos y el AUC de prueba es ≥ 0.90.
- [ ] Primera parte de `notebooks/04_modelos_J.ipynb`.
- [ ] Abrir el PR `j/s2-modelo-base`.
- **Listo cuando:** `predicciones_base.csv` tiene 713 filas y las columnas del contrato.

**Cierre de la semana 2 · sábado 24 (1 h):** se fusionan los dos PR y se etiqueta `s2`. Se decide **cuánto cuesta equivocarse**: en lugar de inventar pesos, se expresa como "un falso negativo cuesta k veces un falso positivo" y se acuerda probar k = 2, 5 y 10. Se anota en `config.py` y en `docs/decisiones.md`.

---

## Semana 3 · 26 al 31 de octubre · Comparación de modelos y priorización

**Objetivo de la semana:** responder "¿en qué medida?" (qué tan bien se predice y con qué variables) y convertir el modelo en una lista de prioridades para el equipo de retención. Al cierre, las cifras se congelan.

### Juanes

**Sesión 1 · comparar modelos (3 h)**

- [ ] Agregar a `entrenar()`: árbol de decisión (profundidad 3–4, para poder leerlo), bosque aleatorio y boosting (`HistGradientBoostingClassifier`; LightGBM opcional, como en Arai et al., 2023).
- [ ] Validación cruzada estratificada de 5 pliegues **solo sobre entrenamiento**: AUC-ROC, AUC-PR y recall, con media ± desviación.
- [ ] Guardar `reports/tablas/comparacion_modelos.csv`.
- **Listo cuando:** la tabla tiene los 4 modelos con media y desviación.

**Sesión 2 · ¿en qué medida? (2.5 h)**

- [ ] Repetir el mejor modelo y la logística con tres conjuntos de variables: (a) todas las acordadas, (b) sin `estado` ni `quejas`, (c) solo las de uso.
- [ ] Guardar `reports/tablas/sensibilidad_variables.csv` y escribir dos líneas en `docs/hallazgos.md`.
- **Listo cuando:** la tabla existe (referencia: la logística sin `estado` ni `quejas` baja a un AUC cercano a 0.85).

**Sesión 3 · interpretar y elegir (2.5 h)**

- [ ] Razones de momios (odds ratios) de la logística e importancia por permutación del mejor modelo; figura `reports/figures/importancia.png`.
- [ ] Dibujar el árbol en `reports/figures/arbol.png` (sirve para explicarle al equipo de retención reglas simples).
- [ ] Elegir el modelo final con un criterio escrito en `docs/decisiones.md` (sugerido: AUC-PR y recall, desempatando por facilidad de explicar).
- [ ] `scripts/entrenar.py` escribe `data/processed/predicciones_final.csv`. **Subirlo a la rama a más tardar el jueves** para que Ianis lo use.
- [ ] Abrir el PR `j/s3-modelos`.
- **Listo cuando:** el modelo final está elegido y su archivo de predicciones cumple el contrato.

### Ianis

**Sesión 1 · deciles de riesgo (2.5 h)**

- [ ] En `src/churn/priorizacion.py`, `tabla_deciles(pred)`: ordenar por `prob_churn`, partir en 10 deciles y calcular n, abandonos reales, tasa, lift y % acumulado de abandonos capturados.
- [ ] Probarlo con el fixture y luego con `predicciones_base.csv`.
- [ ] `scripts/priorizar.py --predicciones <archivo>` que escribe las tablas en `reports/tablas/`.
- **Listo cuando:** con `predicciones_base.csv`, el 10 % de mayor riesgo captura cerca de la mitad de quienes abandonan (referencia: 56 de 112).

**Sesión 2 · capacidad y costos (2.5 h)**

- [ ] `capacidad(pred)`: si el equipo solo puede contactar al 10 %, 20 % o 30 % de mayor riesgo, cuántos abandonos captura y con qué precisión.
- [ ] `costo_por_umbral(pred, costo_fn, costo_fp)` con k = 2, 5 y 10; figura del costo según el umbral y curva de ganancia acumulada.
- **Listo cuando:** existe la frase "contactando al 20 % de mayor riesgo se captura X % de quienes abandonan" (referencia con la logística base: unos 77 %).

**Sesión 3 · perfil del grupo prioritario (2.5 h)**

- [ ] Con las funciones de la semana 2, comparar el 20 % de mayor riesgo contra el resto.
- [ ] `notebooks/05_priorizacion_I.ipynb` con una tabla final pensada para el equipo de retención.
- [ ] `tests/test_priorizacion.py`: los deciles suman 713 y el % acumulado termina en 100 %.
- [ ] Volver a correr todo con `predicciones_final.csv` de Juanes.
- [ ] Abrir el PR `i/s3-priorizacion`.
- **Listo cuando:** las tablas y figuras usan `predicciones_final.csv`.

**Cierre de la semana 3 · sábado 31 (1.5 h):** se fusionan los dos PR. Uno de los dos borra `data/processed/`, corre todo desde cero (`preparar_datos.py` → `entrenar.py` → `priorizar.py`) y `pytest -q`. Si las cifras coinciden, se etiqueta `s3` = **cifras congeladas**. Se completa `docs/hallazgos.md` y se reparte la presentación.

**Si van atrasados:** lo indispensable es la base limpia, el objetivo 1 (correlaciones), el objetivo 2 (caracterización), la logística y la tabla de deciles. El boosting, la sensibilidad por costos y el árbol dibujado son mejoras: se cortan primero.

---

## Semana 4 · 3 al 6 de noviembre · Informe, presentación y entrega

**Objetivo de la semana:** escribir sobre cifras congeladas, sin código nuevo (solo correcciones). Los dos parten de `s3`.

### Ianis

**Sesión 1 · informe, primera parte (2.5 h, martes 3)**

- [ ] En `reports/informe_final.md`: sección 1 (actualizar planteamiento, pregunta y objetivos de la primera entrega), sección 2 (datos y calidad) y sección 4 (caracterización).
- **Listo cuando:** cada cifra de sus secciones está en `reports/tablas/` o en `docs/hallazgos.md`.

**Sesión 2 · informe, segunda parte (2.5 h, miércoles 4)**

- [ ] Sección 6 (priorización) y su parte de limitaciones.
- [ ] Revisar las secciones de Juanes: comparar cada número con las tablas y comentar en el PR.
- **Listo cuando:** sus secciones están completas y la revisión cruzada está hecha.

**Sesión 3 · presentación y formato (2.5 h, jueves 5)**

- [ ] Diapositivas: contexto y pregunta, datos, caracterización, priorización (la mitad).
- [ ] Exportar el informe a Word o PDF (`pandoc reports/informe_final.md -o informe_final.docx`) y darle el formato que pida la profesora (APA 7).
- **Listo cuando:** sus diapositivas y el documento exportado están en `presentacion/` y `reports/`.

### Juanes

**Sesión 1 · informe, primera parte (2.5 h, martes 3)**

- [ ] Sección 3 (metodología: partición, validación cruzada, variables y por qué, citando `docs/decisiones.md`) y sección 5 (relación y modelos).
- **Listo cuando:** cada cifra de sus secciones está en `reports/tablas/`.

**Sesión 2 · informe, segunda parte (2.5 h, miércoles 4)**

- [ ] Sección 7 (falsos positivos, falsos negativos y privacidad) y su parte de limitaciones.
- [ ] Revisar las secciones de Ianis como en su sesión 2.
- [ ] README final con instrucciones para reproducir todo.
- **Listo cuando:** sus secciones están completas y la revisión cruzada está hecha.

**Sesión 3 · presentación y reproducibilidad (2.5 h, jueves 5)**

- [ ] Diapositivas: modelos, "¿en qué medida?", riesgos y recomendación (la otra mitad).
- [ ] En una carpeta nueva: clonar `main`, instalar, correr los tres scripts y `pytest -q`.
- **Listo cuando:** el proyecto se reproduce desde cero en otro lugar sin errores.

### Los dos

- [ ] **Miércoles 4 (1 h, en llamada):** escribir juntos la sección 8 (conclusiones): una respuesta directa a la pregunta de investigación, con dos o tres cifras.
- [ ] **Jueves 5 (1.5 h, en llamada) · cierre final:** ensayar la presentación cronometrada, fusionar los últimos PR y recorrer esta lista:
  - [ ] `pytest -q` en verde en `main`.
  - [ ] Cada cifra del informe y de las diapositivas coincide con `reports/tablas/`.
  - [ ] El informe responde la pregunta y los dos objetivos específicos.
  - [ ] Referencias en APA 7 (como mínimo, las dos de la primera entrega).
  - [ ] Se etiqueta `v1.0`.
- [ ] **Viernes 6 · entrega:** subir el informe y la presentación por el canal que indique la profesora (y el enlace al repositorio si lo piden).
