# Churn Telco Irán: guía día a día (ajustada)

Octubre 28, 2026 · Ianis y Juanes

## Qué cambió

Esta versión reemplaza la guía del 10 de octubre: el trabajo en el repositorio no había empezado y **la presentación es el viernes 13 de noviembre**. Quedan 15 días, así que las cuatro semanas se comprimen en cuatro bloques:

| Bloque | Fechas | Qué sale | Reunión de PR |
|---|---|---|---|
| Arranque | jueves 29 oct | Repositorio en GitHub y los dos con `pytest` corriendo | (es la misma llamada) |
| 1 · Datos y relación | vie 30 oct – lun 2 nov | Base limpia y objetivo específico 1 | **lunes 2 nov (festivo)**, etiqueta `s1` |
| 2 · Caracterización y modelos | mar 3 – sáb 7 nov | Objetivo específico 2, modelos, primera priorización | **sábado 7 nov**, etiqueta `s2` |
| 3 · Cierre de cifras | dom 8 – mar 10 nov | Priorización final, interpretación, inicio del informe | **martes 10 nov**, etiqueta `s3` = cifras congeladas |
| 4 · Informe y presentación | mié 11 – vie 13 nov | Informe, diapositivas, ensayo | ensayo **jueves 12**, presentación **viernes 13** |

**Carga:** unas 10 sesiones de 2 a 3 horas por persona en 15 días, más las reuniones: unas 5 por semana en lugar de 3. Para que alcance, se recortaron las mejoras opcionales y el repositorio trae más cosas listas (ver abajo). Si el informe escrito tiene otra fecha, confírmenlo en el arranque.

### Qué cambió en el repositorio (28 de octubre)

- **Las pruebas ya están escritas** (`tests/test_*.py`), con las cifras de referencia. Ya no hay que crearlas en cada sesión. Al inicio `pytest -q` da **4 passed, 28 skipped**: las *skipped* son las de funciones que todavía tienen `raise NotImplementedError`. Cuando alguien implementa su función, sus pruebas empiezan a comprobar las cifras; si una falla, algo no coincide. Para ver qué falta: `pytest -q -rs`. Meta del martes 10: **0 skipped**.
- Cada función en `src/churn/` dice ahora qué columnas debe devolver y su cifra de referencia (sin cambiar las firmas acordadas). Se agregó `comparar_modelos()` en `modelos.py`.
- `config.py` trae, como valores provisionales, `COLUMNA_EDAD_A_QUITAR`, `VARIABLES_MODELO`, los conjuntos de sensibilidad, `PLIEGUES_CV`, `K_COSTOS` y `CAPACIDADES`. Se confirman en las reuniones.
- Los scripts ya encuentran el paquete solos: no hace falta fijar `PYTHONPATH`.
- `entrenar.py` acepta `--final --modelo <nombre>`.

### Quién es quién

| Persona | Letra | Rol | Archivos suyos |
|---|---|---|---|
| Ianis | I | Datos, caracterización y priorización | `scripts/preparar_datos.py`, `scripts/priorizar.py`, `src/churn/datos.py`, `src/churn/caracterizacion.py`, `src/churn/priorizacion.py`, notebooks `*_I.ipynb`, `docs/calidad_datos.md`, `docs/diccionario_datos.md` |
| Juanes | J | Repositorio, relación de variables y modelos | `.github/`, `scripts/entrenar.py`, `src/churn/relacion.py`, `src/churn/modelos.py`, `src/churn/evaluacion.py`, notebooks `*_J.ipynb`, `README.md` |
| Ambos | — | Se cambian **solo en la reunión** | `src/churn/config.py`, `docs/decisiones.md`, `docs/hallazgos.md`, `docs/contrato_predicciones.md`, `reports/informe_final.md` (cada quien sus secciones) |

Frente a la primera entrega:

- **Objetivo específico 1** (variables más relacionadas con el abandono) → Juanes, bloque 1; lo confirma con los modelos en el bloque 2.
- **Objetivo específico 2** (caracterizar a quienes abandonan frente a quienes permanecen) → Ianis, bloque 2.
- **Objetivo general** (predecir y apoyar la priorización) → Juanes construye el modelo (bloque 2) e Ianis lo convierte en una lista de prioridades (bloques 2 y 3).
- **Informe y presentación** → mitad y mitad (bloques 3 y 4).

La letra se usa en las ramas (`i/b1-datos`, `j/b2-modelos`) y en los notebooks.

### Rutina

1. **Al empezar cada bloque (5 min, por chat):** cada quien escribe qué sesiones hará y qué día.
2. **Durante el bloque:** trabajar solo en su rama y en sus archivos. Si necesitan algo del otro, usen el fixture o el contrato; no esperen.
3. **A mitad del bloque (5 min, por chat):** qué terminé, qué me falta, qué me bloquea. `git push` aunque no esté terminado.
4. **La víspera de la reunión, antes de las 20:00:** cada quien abre su PR.
5. **Reunión (1 a 1.5 h, en llamada):** cada quien comparte pantalla y muestra `pytest -q` y su resultado. El otro aprueba si se cumple el "Listo cuando". Se fusiona a `main`, se anotan las decisiones en `docs/decisiones.md`, se etiqueta (`git tag s1 && git push --tags`) y los dos hacen `git checkout main && git pull`.

### Cómo abrir un PR

```
git checkout main && git pull
git checkout -b i/b2-caracterizacion      # su letra / bloque-tema
# ... trabajar, guardar ...
git add src/churn/caracterizacion.py      # solo los archivos que tocaron, nunca git add .
git commit -m "caracterizacion: tabla de numéricas con Mann-Whitney"
git push -u origin i/b2-caracterizacion
# en GitHub: "Compare & pull request" y llenar la plantilla
```

En la reunión no se piden cambios de estilo; solo se bloquea un PR si algo no funciona, si una cifra no tiene respaldo o si toca archivos del otro.

### Palabras que se usan

- **Contrato:** el formato del archivo de predicciones que Juanes le entrega a Ianis (`docs/contrato_predicciones.md`): `fila_original`, `conjunto`, `churn_real`, `prob_churn`, `modelo`.
- **Fixture:** `data/processed/fixtures/predicciones_ejemplo.csv`, con el formato del contrato y un modelo simple de 3 variables, para que Ianis programe la priorización sin esperar. Sus cifras **no** van en el informe.
- **Base cruda / base limpia:** `data/raw/customer_churn.csv` (3150 filas, nunca se modifica) / `data/processed/clientes.csv` (lo genera el script de Ianis).
- **Partición:** la división fija entrenamiento/prueba en `data/processed/particion.csv`. Los dos usan la misma.
- **Cifras congeladas:** después de la reunión del martes 10 ningún número cambia; el informe se escribe sobre esas cifras.

---

## Arranque · jueves 29 de octubre

**Objetivo:** el repositorio en GitHub y los dos con el proyecto corriendo.

**Juanes · repositorio (45 min, antes de la llamada)**

- [ ] El repositorio ya está en GitHub (`juanesaacosta26/churn-iran`). Subir el commit del ajuste del 28 de octubre si aún no está: `git push`.
- [ ] Settings → Collaborators: confirmar que Ianis está invitada. Settings → Branches: proteger `main` (requerir PR, 1 aprobación y que pase el check "pruebas").
- [ ] Cambiar `@USUARIO_IANIS` y `@USUARIO_JUANES` en `.github/CODEOWNERS` por los usuarios reales.
- **Listo cuando:** la pestaña Actions muestra "pruebas" en verde.

**Los dos · llamada de arranque (1 h)**

- [ ] (10 min) Leer juntos esta sección.
- [ ] (15 min) Cada quien clona, crea su entorno e instala (ver README) y corre `pytest -q`: **4 passed, 28 skipped**.
- [ ] (10 min) Abrir `tests/conftest.py` y una prueba cualquiera para entender cómo funcionan las pruebas en espera.
- [ ] (15 min) Tomar las dos primeras decisiones de `docs/decisiones.md` (duplicados y edad) y anotarlas.
- [ ] (10 min) Confirmar con la profesora el tiempo de la presentación y si el informe escrito se entrega el mismo 13 (formato, plantilla, número de páginas).

---

## Bloque 1 · viernes 30 de octubre al lunes 2 de noviembre · Datos limpios y relación con el abandono

**Objetivo:** base limpia y documentada, y una primera respuesta al objetivo específico 1.

### Ianis

**Sesión 1 · datos limpios (2 h, viernes 30 o sábado 31)**

- [ ] En `scripts/preparar_datos.py`: contar las filas duplicadas exactas (todas las columnas menos `fila_original`; deben ser 300), quitarlas conservando la primera aparición, quitar `config.COLUMNA_EDAD_A_QUITAR` y guardar `clientes.csv` sin índice.
- [ ] En `src/churn/datos.py`, implementar `cargar_limpio()`.
- **Listo cuando:** `clientes.csv` tiene 2850 filas y 446 abandonos (15.6 %) y pasan las 5 pruebas de `test_preparar.py`.

**Sesión 2 · calidad, diccionario y distribuciones (2.5 h, domingo 1)**

- [ ] Que el mismo script escriba `docs/calidad_datos.md`: por columna mínimo, percentil 5, mediana, percentil 95, máximo, ceros y atípicos (1.5 × IQR); agregar los 107 clientes con `segundos_uso = 0` (¿cuántos abandonan?).
- [ ] Completar `docs/diccionario_datos.md` con los rangos reales.
- [ ] En `notebooks/01_calidad_datos_I.ipynb`: histogramas de las numéricas → `reports/figures/distribuciones.png`.
- [ ] Abrir el PR `i/b1-datos`.
- **Listo cuando:** `calidad_datos.md` se regenera solo al correr el script y el check "pruebas" está en verde.

### Juanes

**Sesión 1 · relación con el abandono (2 h, viernes 30 o sábado 31)**

- [ ] En `src/churn/relacion.py`: `correlacion_con_churn(df)` y `tasa_por_categoria(df, columna)`. Usar `cargar_crudo()` hasta que se fusione `cargar_limpio()`.
- [ ] Guardar `reports/tablas/relacion_churn.csv`.
- **Listo cuando:** el orden empieza con `quejas` (0.53), `estado` (0.50) y `frecuencia_llamadas` (−0.30) y pasan las 3 pruebas de `test_relacion.py` que usan la base cruda.

**Sesión 2 · redundancias y propuesta de variables (2.5 h, domingo 1)**

- [ ] `redundancias(df)`: pares con |r| ≥ 0.8 y VIF (`statsmodels`). Revisar `segundos_uso`–`frecuencia_llamadas` y `valor_cliente` contra las de uso.
- [ ] Mapa de calor → `reports/figures/correlaciones.png`.
- [ ] Escribir en `docs/decisiones.md` la propuesta: qué variables entran al modelo, qué hacer con `estado`, `quejas` y `valor_cliente`.
- [ ] `notebooks/03_relacion_variables_J.ipynb` con las tres gráficas más claras y dos hallazgos en `docs/hallazgos.md`, cada uno con su cifra.
- [ ] Abrir el PR `j/b1-relacion`.
- **Listo cuando:** la propuesta está escrita y el PR está en verde (la prueba de redundancias corre cuando ya se haya fusionado el PR de Ianis).

**Reunión 1 · lunes 2 de noviembre, festivo (1 h):** se fusiona primero el PR de Ianis y luego el de Juanes. Se decide qué variables entran al modelo, se actualiza `VARIABLES_MODELO` en `config.py` si cambia y se etiqueta `s1`. Juanes cambia `relacion.py` a `cargar_limpio()` en su siguiente rama.

---

## Bloque 2 · martes 3 al sábado 7 de noviembre · Caracterización, modelos y primera priorización

**Objetivo:** objetivo específico 2 con cifras y pruebas estadísticas; modelos comparados y modelo final elegido; priorización funcionando con el modelo base.

**Entregas entre los dos:** Juanes sube `predicciones_base.csv` a su rama **a más tardar el miércoles 4 en la noche** y `predicciones_final.csv` **a más tardar el sábado 7 al mediodía**.

### Ianis

**Sesión 1 · numéricas y categóricas (3 h, martes 3)**

- [ ] En `src/churn/caracterizacion.py`: `tabla_numericas(df)` (medianas, cuartiles, Mann-Whitney y delta de Cliff) y `tabla_categoricas(df)` (n, tasa, chi²; Fisher si hay celdas pequeñas).
- [ ] Guardar `caracterizacion_numericas.csv` y `caracterizacion_categoricas.csv` en `reports/tablas/`.
- **Listo cuando:** pasan las 8 pruebas de `test_caracterizacion.py` (segundos de uso 1256.5 contra 3596.5; con queja 82.6 % contra 9.8 %; no activo 47.5 % contra 5.6 %; contrato 2.6 % contra 16.8 %).

**Sesión 2 · figuras y hallazgos (2.5 h, miércoles 4)**

- [ ] Diagramas de caja por grupo (escala logarítmica en las de uso) y barras de tasa por categoría → `reports/figures/caracterizacion_*.png`.
- [ ] `notebooks/02_caracterizacion_I.ipynb` con la lectura de cada figura.
- [ ] Cinco hallazgos en `docs/hallazgos.md`, cada uno con cifra y figura.
- **Listo cuando:** los cinco hallazgos están escritos.

**Sesión 3 · deciles y capacidad (2.5 h, jueves 5 o viernes 6)**

- [ ] En `src/churn/priorizacion.py`: `tabla_deciles(pred)` y `capacidad(pred)`. Probar primero con el fixture y luego con `predicciones_base.csv` de Juanes (`git fetch` y `git checkout origin/j/b2-modelos -- data/processed/predicciones_base.csv`; no incluirlo en su commit).
- [ ] Completar la parte del bloque 2 de `scripts/priorizar.py`.
- [ ] Abrir el PR `i/b2-caracterizacion`.
- **Listo cuando:** con `predicciones_base.csv` el decil 1 captura 56 de 112 y existe la frase "contactando al 20 % de mayor riesgo se captura X %" (referencia: 76.8 %).

### Juanes

**Sesión 1 · partición, logística y métricas (3 h, martes 3)**

- [ ] En `src/churn/modelos.py`: `particion(df)` y `entrenar("logistica", X, y)` (`StandardScaler` + `LogisticRegression` en un `Pipeline`). En `evaluacion.py`: `metricas(y, prob, umbral)`.
- [ ] Completar `scripts/entrenar.py` y generar `predicciones_base.csv`. **Subirlo a la rama esa noche o el miércoles.**
- **Listo cuando:** 2137 en entrenamiento y 713 en prueba con 112 abandonos, AUC-ROC de la logística ≈ 0.933 y pasan las pruebas de partición, métricas, AUC y contrato.

**Sesión 2 · comparar modelos (2.5 h, miércoles 4 o jueves 5)**

- [ ] Agregar a `entrenar()`: árbol (profundidad 3–4) y bosque aleatorio. Boosting es **opcional**.
- [ ] `comparar_modelos()`: validación cruzada de 5 pliegues **solo sobre entrenamiento** → `reports/tablas/comparacion_modelos.csv`.
- [ ] Curvas ROC y precisión-recall de prueba → `reports/figures/`.
- **Listo cuando:** la tabla tiene los modelos con media y desviación y pasa `test_comparar_modelos`.

**Sesión 3 · ¿en qué medida? y modelo final (2.5 h, viernes 6)**

- [ ] Repetir el mejor modelo y la logística con `VARIABLES_MODELO`, `VARIABLES_SIN_ESTADO_QUEJAS` y `VARIABLES_SOLO_USO` → `reports/tablas/sensibilidad_variables.csv` (referencia: la logística sin `estado` ni `quejas` baja a ≈ 0.85).
- [ ] Proponer el modelo final con un criterio escrito (sugerido: AUC-PR y recall, desempatando por facilidad de explicar) y generar `predicciones_final.csv` con `python scripts/entrenar.py --final --modelo <nombre>`. **Subirlo antes del sábado al mediodía.**
- [ ] Dos líneas en `docs/hallazgos.md` sobre la sensibilidad.
- [ ] Abrir el PR `j/b2-modelos`.
- **Listo cuando:** la sensibilidad está en la tabla y `predicciones_final.csv` cumple el contrato.

**Reunión 2 · sábado 7 de noviembre (1.5 h):** se fusionan los dos PR y se etiqueta `s2`. Se decide el costo de equivocarse (un falso negativo cuesta k falsos positivos, probando k = 2, 5 y 10) y el modelo final. Se reparte el informe: Ianis secciones 1, 2, 4 y 6; Juanes 3, 5 y 7; la 8 y la 9 juntos.

---

## Bloque 3 · domingo 8 al martes 10 de noviembre · Cierre de cifras

**Objetivo:** priorización final, interpretación del modelo e inicio del informe. El martes las cifras se congelan.

### Ianis

**Sesión 1 · costos y perfil del grupo prioritario (2.5 h, domingo 8)**

- [ ] `costo_por_umbral(pred, costo_fn=k, costo_fp=1)` para cada k de `config.K_COSTOS`; figura del costo según el umbral y curva de ganancia acumulada.
- [ ] Con `tabla_numericas` y `tabla_categoricas`, comparar el 20 % de mayor riesgo contra el resto.
- [ ] Volver a correr todo con `predicciones_final.csv`; `notebooks/05_priorizacion_I.ipynb` con la tabla final para el equipo de retención.
- **Listo cuando:** las tablas y figuras de priorización usan `predicciones_final.csv` y pasan las 4 pruebas de `test_priorizacion.py`.

**Sesión 2 · informe, primera parte (2 h, lunes 9)**

- [ ] Secciones 1 (actualizar planteamiento, pregunta y objetivos desde `docs/primera_entrega.md`) y 2 (datos y calidad) en `reports/informe_final.md`.
- [ ] Abrir el PR `i/b3-cierre`.

### Juanes

**Sesión 1 · interpretar (2.5 h, domingo 8)**

- [ ] Razones de momios de la logística e importancia por permutación del modelo final → `reports/figures/importancia.png`.
- [ ] Dibujar el árbol → `reports/figures/arbol.png` (si no alcanza el tiempo, se corta).
- [ ] README final con las instrucciones para reproducir todo.
- **Listo cuando:** la figura de importancia existe y el README explica los scripts.

**Sesión 2 · informe, primera parte (2 h, lunes 9)**

- [ ] Sección 3 (metodología: partición, validación cruzada, variables y por qué, citando `docs/decisiones.md`).
- [ ] Abrir el PR `j/b3-cierre`.

**Reunión 3 · martes 10 de noviembre (1.5 h):** se fusionan los dos PR. Uno de los dos borra `data/processed/` (menos `fixtures/`), corre todo desde cero (`preparar_datos.py` → `entrenar.py` → `entrenar.py --final --modelo <nombre>` → `priorizar.py --predicciones data/processed/predicciones_final.csv`) y `pytest -q -rs`. Si las cifras coinciden y hay **0 skipped**, se etiqueta `s3` = **cifras congeladas**. Se completa `docs/hallazgos.md`.

**Si van atrasados**, lo indispensable es: base limpia, objetivo 1 (correlaciones), objetivo 2 (caracterización), logística y tablas de deciles y capacidad. Se cortan primero, en este orden: boosting, árbol dibujado, curva de costos por k, perfil del grupo prioritario, bosque aleatorio.

---

## Bloque 4 · miércoles 11 al viernes 13 de noviembre · Informe, presentación y entrega

**Objetivo:** escribir sobre cifras congeladas, sin código nuevo (solo correcciones). Los dos parten de `s3`.

### Miércoles 11

- [ ] **Ianis (2.5 h):** secciones 4 (caracterización) y 6 (priorización).
- [ ] **Juanes (2.5 h):** secciones 5 (relación y modelos) y 7 (falsos positivos, falsos negativos y privacidad).
- [ ] **Los dos (1 h, en llamada, en la noche):** secciones 8 (conclusiones: respuesta directa a la pregunta con dos o tres cifras) y 9 (limitaciones). Cada quien revisa las secciones del otro comparando cada número con `reports/tablas/` y comenta en el PR.
- **Listo cuando:** el informe está completo y cada cifra tiene respaldo.

### Jueves 12

- [ ] **Ianis (2 h):** sus diapositivas (contexto, pregunta, datos, caracterización, priorización; ver `presentacion/README.md`) y exportar el informe (`pandoc reports/informe_final.md -o informe_final.docx`) con formato APA 7.
- [ ] **Juanes (2 h):** sus diapositivas (relación, modelos, "¿en qué medida?", riesgos, referencias) y prueba de reproducibilidad: en una carpeta nueva clonar `main`, instalar, correr los scripts y `pytest -q`.
- [ ] **Los dos (1.5 h, en llamada) · cierre final:** ensayar la presentación cronometrada y recorrer esta lista:
  - [ ] `pytest -q` en verde en `main`, 0 skipped.
  - [ ] Cada cifra del informe y de las diapositivas coincide con `reports/tablas/`.
  - [ ] El informe responde la pregunta y los dos objetivos específicos.
  - [ ] Referencias en APA 7 (como mínimo las dos de la primera entrega).
  - [ ] Se etiqueta `v1.0`.

### Viernes 13 · presentación

- [ ] Presentar y subir el informe y las diapositivas por el canal que indique la profesora (y el enlace al repositorio si lo piden).
