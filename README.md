# Pipeline de Machine Learning con TFX y ML Metadata

Este repositorio presenta un pipeline de Machine Learning robusto y reproducible utilizando TFX. Se muestra cómo preparar el dataset, aplicar transformaciones consistentes en el entrenamiento y servicio, y rastrear los artefactos generados a través del almacén de metadatos (ML Metadata). Además, se incluye la configuración para desplegar el entorno en un contenedor Docker mediante Docker Compose.

## Descripción

El pipeline construido en este proyecto abarca las siguientes etapas:

1. **Selección de Características:**  
   Se utilizó `SelectKBest` para reducir la dimensionalidad del dataset original, seleccionando 8 de las 11 características disponibles.  
   **Características seleccionadas:**
   - `Elevation`
   - `Slope`
   - `Horizontal_Distance_To_Hydrology`
   - `Vertical_Distance_To_Hydrology`
   - `Horizontal_Distance_To_Roadways`
   - `Hillshade_9am`
   - `Hillshade_Noon`
   - `Horizontal_Distance_To_Fire_Points`

   La salida se guarda en `../data/selected_dataset/selected.csv`.

2. **Creación del Contexto Interactivo e Ingesta de Datos:**  
   Se configuró un `InteractiveContext` que utiliza una base de datos SQLite localizada en `./pipeline_root/metadata.sqlite` para almacenar la metadata del pipeline.  
   Se ingestan los datos a través del componente `CsvExampleGen`.

3. **Generación de Estadísticas y Esquema:**  
   - **Estadísticas:** Utilizando `StatisticsGen` se obtienen métricas descriptivas del dataset.
   - **Inferencia del Esquema:** Con `SchemaGen` se infiere el esquema a partir de las estadísticas.
   - **Curación del Esquema:**  
     Se ajustaron manualmente los rangos de algunas características (por ejemplo, `Hillshade_9am`, `Hillshade_Noon`, `Slope` y `Cover_Type`) y se especificó que `Cover_Type` es categórica.  
     Además, se definieron entornos (TRAINING y SERVING) para asegurar que la variable objetivo no se incluya en los datos de servicio.

4. **Transformación de Datos:**  
   Se implementó un módulo de transformación (por ejemplo, `forest_transform.py`) que define la función `preprocessing_fn`. En dicha función se aplican diversas transformaciones utilizando TensorFlow Transform (tft):
   - **Escalado:**  
     - `tft.scale_to_0_1` para `Elevation`, `Hillshade_9am` y `Hillshade_Noon`.
     - `tft.scale_to_z_score` para `Slope`.
     - `tft.scale_by_min_max` para las distancias (por ejemplo, `Horizontal_Distance_To_Hydrology`).
   - **Bucketización:** Se aplicó `tft.bucketize` a `Slope`.
   - **Conversión de cadenas a índices:** Se utilizó `tft.compute_and_apply_vocabulary` para transformar la etiqueta `Cover_Type`.
   - **Hashing:** Se empleó `tft.hash_strings` como ejemplo adicional.

   El componente `Transform` genera un grafo de transformación que se aplica de manera consistente tanto en el entrenamiento como en la inferencia, generando datos transformados (TFRecords).

5. **Exploración del Almacén de Metadatos (ML Metadata):**  
   Se utiliza ML Metadata para rastrear y consultar los artefactos producidos en cada etapa del pipeline. Entre las consultas realizadas se incluyen:
   - Recuperar todos los tipos de artefactos registrados.
   - Listar, por ejemplo, los artefactos del tipo `Schema` (indicando el esquema inferido y el actualizado).
   - Rastrear las entradas utilizadas para generar un artifact particular (por ejemplo, un `TransformGraph`) mediante el uso de `get_events_by_artifact_ids()` y `get_events_by_execution_ids()`.
   - Consultar las propiedades (automáticas y personalizadas) de cada artifact generado.

## Despliegue del Contenedor

El entorno de desarrollo se despliega en un contenedor Docker para facilitar la configuración, la reproducción y el aislamiento del entorno de ejecución. A continuación se describe la configuración utilizada:

### Dockerfile

El archivo `Dockerfile` define el entorno de ejecución basado en `python:3.10` e instala las dependencias necesarias:


### Docker Compose

El archivo docker-compose.yml define el servicio jupyterlab y monta los volúmenes correspondientes para compartir los notebooks y los datos:


### Requirements.txt

Las dependencias necesarias se especifican en el archivo requirements.txt:

numpy
requests
tensorflow
tfx
google-api-python-client
protobuf
pandas
tensorflow-data-validation
scikit-learn
uvicorn
apache-beam
jupyterlab

### Estructura del Proyecto

├── data
│   ├── selected_dataset
│   │   └── selected.csv
│   └── serving_dataset
│       └── serving_data.csv
├── pipeline_root
│   ├── metadata.sqlite          # Almacén de ML Metadata
│   └── ...                      # Otros artefactos generados
├── forest_constants.py          # Constantes del proyecto
├── forest_transform.py          # Módulo de transformación (preprocessing_fn)
├── Dockerfile                   # Configuración para construir el contenedor
├── docker-compose.yml           # Orquestación del contenedor
├── requirements.txt             # Dependencias del proyecto
├── notebooks
│   └── Proyecto1.ipynb  # Notebook con la ejecución del pipeline
└── README.md

### Despliegue del Contenedor

Ubicate en la carpeta principal del repositorio y construye la imagen y despliega el contenedor

1. docker-compose build
2. docker-compose up
3. Accede a JupyterLab a través del navegador en la dirección (Agrega el token Generado) http://localhost:8888.


¡Gracias por revisar este proyecto!

#Equipo de Trabajo

-Camilo Diaz Granados Nobman
-Daniel Ruiz Carrillo
-Luis Fernandez Vargas - https://github.com/LuisCa-Cyber/MLOps_Talleres/





