# Archivo de constantes para el dataset Forest Cover Type

# Lista de características numéricas que se transformarán
NUMERIC_FEATURE_KEYS = [
    'Elevation',
    'Slope',
    'Horizontal_Distance_To_Hydrology',
    'Vertical_Distance_To_Hydrology',
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am',
    'Hillshade_Noon',
    'Horizontal_Distance_To_Fire_Points'
]

# La etiqueta a predecir
LABEL_KEY = 'Cover_Type'

# Características que queremos bucketizar (por ejemplo, 'Slope')
BUCKET_FEATURE_KEYS = ['Slope']

# Número de buckets para cada característica a bucketizar
FEATURE_BUCKET_COUNT = {'Slope': 5}

# Función de utilidad para renombrar las features transformadas
def transformed_name(key):
    return key + '_xf'
