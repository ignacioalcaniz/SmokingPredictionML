
# Smoking Prediction — Machine Learning

**Diplomatura en Inteligencia Artificial — Universidad de Palermo**  
**Trabajo Práctico 2 — Módulo 2**  
**Docente:** Martín Jaureguy

## 1. Descripción del proyecto

Este proyecto desarrolla un sistema de aprendizaje automático para predecir el hábito de fumar a partir de características demográficas y mediciones clínicas.

Se trata de un problema de clasificación binaria cuya variable objetivo es `smoking`:

- `0`: no fumador.
- `1`: fumador.

El objetivo principal es maximizar el **F1-score de la clase positiva (1)** y generar predicciones para un conjunto de datos sin etiqueta.

## 2. Dataset

Se utilizaron dos archivos originales:

| Archivo | Registros | Descripción |
|---|---:|---|
| `smoking_prediction.xlsx` | 50.000 | Datos etiquetados |
| `smoking_prediction_entrega.xlsx` | 5.692 | Datos sin etiqueta |

El conjunto etiquetado contiene 27 columnas, incluyendo `ID` y `smoking`. El conjunto de predicción contiene las mismas variables predictoras, pero no incluye la variable objetivo.

Se utilizaron 25 variables predictoras, excluyendo `ID`.

### Distribución de clases

| Clase | Registros | Porcentaje |
|---|---:|---:|
| No fumadores (0) | 31.671 | 63,34 % |
| Fumadores (1) | 18.329 | 36,66 % |

La distribución presenta un desequilibrio moderado, por lo que se priorizó el F1-score sobre la exactitud global.

## 3. Estructura del proyecto

```text
SmokingPredictionML/
├── data/
│   ├── raw/
│   │   ├── smoking_prediction.xlsx
│   │   └── smoking_prediction_entrega.xlsx
│   └── processed/
│       ├── train_clean.csv
│       ├── predict_clean.csv
│       └── smoking_predictions.csv
├── models/
│   ├── smoking_model.joblib
│   └── model_metadata.json
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_predictions.ipynb
├── src/
│   └── preprocessing.py
├── requirements.txt
└── README.md
```

## 4. Metodología

### 4.1. Análisis exploratorio

Se examinaron:

- Dimensiones y estructura de los datasets.
- Valores faltantes y duplicados.
- Distribución de la variable objetivo.
- Estadísticas descriptivas de las variables clínicas.
- Diferencias entre fumadores y no fumadores.

### 4.2. Calidad y reconstrucción de datos

Durante la exploración se identificó que 18 columnas numéricas habían sido interpretadas mediante representaciones de tiempo de Excel.

Se desarrolló una función de reconstrucción diferenciada para variables enteras y decimales, disponible en `src/preprocessing.py`.

La transformación se aplicó a ambos datasets. Se verificó que el módulo reproduce exactamente los archivos CSV procesados utilizados en el proyecto.

Esta reconstrucción se basa en los patrones observados y en la plausibilidad de las mediciones recuperadas; no fue contrastada con una fuente independiente.

### 4.3. Preparación para el modelado

Los datos etiquetados se dividieron mediante muestreo estratificado:

| Conjunto | Registros | Proporción |
|---|---:|---:|
| Entrenamiento | 30.000 | 60 % |
| Validación | 10.000 | 20 % |
| Prueba | 10.000 | 20 % |

Se utilizó `random_state=42` para favorecer la reproducibilidad.

El preprocesamiento incluyó:

- Estandarización de variables numéricas mediante `StandardScaler`.
- Codificación de variables categóricas mediante `OneHotEncoder`.
- Integración del preprocesamiento y el clasificador mediante `Pipeline`.

El preprocesamiento se ajustó exclusivamente sobre los datos de entrenamiento durante la evaluación.

### 4.4. Modelos evaluados

Se compararon:

1. Regresión logística con variables demográficas.
2. Regresión logística con todas las variables.
3. Random Forest con variables demográficas.
4. Random Forest con todas las variables.

Los umbrales de decisión se optimizaron sobre el conjunto de validación utilizando el F1-score de la clase positiva.

El conjunto de prueba se reservó para una única evaluación final.

## 5. Resultados experimentales

### Comparación de modelos

| Modelo | Variables | Mejor umbral | F1 validación |
|---|---|---:|---:|
| Regresión logística | Demográficas | 0.48 | 0.7030 |
| Regresión logística | Todas | 0.39 | 0.7076 |
| Random Forest | Demográficas | 0.28 | 0.7033 |
| **Random Forest** | **Todas** | **0.41** | **0.7368** |

Random Forest con todas las variables obtuvo el mejor resultado de validación.

### Evaluación final

El modelo seleccionado se evaluó sobre 10.000 registros independientes.

| Métrica | Resultado |
|---|---:|
| **F1-score clase 1** | **0.7415** |
| Precision clase 1 | 0.6407 |
| Recall clase 1 | 0.8800 |
| Accuracy | 0.7751 |

**Matriz de confusión:**

| | Predicción 0 | Predicción 1 |
|---|---:|---:|
| Real 0 | 4.525 | 1.809 |
| Real 1 | 440 | 3.226 |

El modelo identificó correctamente al 88 % de los fumadores del conjunto de prueba, aunque produjo una cantidad considerable de falsos positivos.

## 6. Insights principales

### Insight 1 — La calidad de los datos condiciona el modelado

**Evidencia:** `01_data_understanding.ipynb`, celdas 4–6.

Se identificaron 18 variables afectadas por representaciones de tiempo de Excel. Su reconstrucción permitió trabajar con mediciones numéricas plausibles.

**Conclusión:** El análisis de calidad de datos fue una etapa esencial antes del entrenamiento.

### Insight 2 — Existen asociaciones entre indicadores clínicos y tabaquismo

**Evidencia:** `01_data_understanding.ipynb`, celdas 8–9.

Las medianas de Gtp fueron 21 para no fumadores y 37 para fumadores. En triglicéridos fueron 96 y 132, respectivamente.

También se observaron diferencias en HDL y hemoglobina.

**Conclusión:** Existen asociaciones descriptivas entre ciertas mediciones clínicas y la variable objetivo, sin que esto implique causalidad.

### Insight 3 — Las variables clínicas mejoran la capacidad predictiva

**Evidencia:** `02_model_training.ipynb`, celda 9.

Al comparar dos modelos Random Forest, el F1-score aumentó de 0.7033 con variables demográficas a 0.7368 con todas las variables.

La mejora absoluta fue de 0.0335 puntos.

**Conclusión:** Los indicadores clínicos aportaron información predictiva adicional en el conjunto de validación.

### Insight 4 — El algoritmo y el umbral son decisiones relevantes

**Evidencia:** `02_model_training.ipynb`, celdas 5, 6 y 8.

La regresión logística completa pasó de F1 = 0.6578 a F1 = 0.7076 al ajustar el umbral de 0.50 a 0.39.

Random Forest completo alcanzó F1 = 0.7368 con un umbral de 0.41.

**Conclusión:** Tanto la selección del algoritmo como la optimización del umbral influyeron en el rendimiento.

### Insight 5 — El modelo prioriza la detección de fumadores

**Evidencia:** `02_model_training.ipynb`, celda 10.

El modelo obtuvo un recall de 0.8800, con 3.226 verdaderos positivos y 440 falsos negativos.

Sin embargo, generó 1.809 falsos positivos.

**Conclusión:** Existe un compromiso entre identificar una mayor proporción de fumadores y evitar clasificaciones positivas incorrectas.

## 7. Predicciones finales

Una vez seleccionado y evaluado el modelo, se entrenó una versión definitiva utilizando los 50.000 registros etiquetados.

Se guardó el pipeline completo junto con el umbral de clasificación de 0.41.

El modelo se aplicó a los 5.692 registros sin etiqueta.

| Predicción | Cantidad |
|---|---:|
| Fumador (1) | 2.260 |
| No fumador (0) | 3.432 |
| **Total** | **5.692** |

**Archivo generado:** `data/processed/smoking_predictions.csv`

El archivo contiene:

- `ID`: identificador original del registro.
- `smoking_prediction`: predicción binaria (0 o 1).

Estas cantidades corresponden a predicciones y no a etiquetas reales verificadas.

## 8. Instalación y reproducción

### Requisitos

- Python 3.11.
- Dependencias especificadas en `requirements.txt`.

### Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd SmokingPredictionML
```

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

### Ejecución

Con los archivos originales disponibles en `data/raw/`, ejecutar las notebooks en este orden:

1. `notebooks/01_data_understanding.ipynb`: exploración, reconstrucción y generación de datos procesados.
2. `notebooks/02_model_training.ipynb`: entrenamiento, comparación, evaluación y guardado del modelo.
3. `notebooks/03_predictions.ipynb`: carga del modelo y generación del archivo de predicciones.

Las notebooks utilizan rutas relativas y deben ejecutarse desde el directorio `notebooks/`.

El módulo `src/preprocessing.py` contiene la función de reconstrucción de mediciones y permite reproducir el procesamiento aplicado a los archivos originales.

## 9. Limitaciones

- La reconstrucción de las mediciones se infirió a partir de patrones observados en los archivos originales.
- El modelo presenta falsos positivos y falsos negativos.
- La evaluación se realizó sobre una partición independiente del mismo dataset, sin validación externa.
- Los resultados representan asociaciones predictivas, no relaciones causales.
- El sistema no debe utilizarse como herramienta de diagnóstico clínico.

## 10. Conclusión

El proyecto permitió desarrollar un flujo completo de aprendizaje automático para clasificación binaria, desde el análisis de calidad de datos hasta la generación de predicciones.

La comparación experimental respaldó la utilidad de incorporar variables clínicas y utilizar Random Forest para este problema.

El mejor modelo obtuvo un **F1-score de 0.7415 en el conjunto de prueba independiente**.

Finalmente, se entrenó una versión definitiva con los 50.000 registros etiquetados y se generaron las 5.692 predicciones solicitadas.

El trabajo demuestra la importancia de combinar calidad de datos, comparación experimental, evaluación rigurosa y reproducibilidad para construir soluciones de aprendizaje automático.
