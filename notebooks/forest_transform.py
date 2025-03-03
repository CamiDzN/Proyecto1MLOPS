import tensorflow as tf
import tensorflow_transform as tft
import forest_constants

# Extraer las constantes definidas
_NUMERIC_FEATURE_KEYS = forest_constants.NUMERIC_FEATURE_KEYS
_LABEL_KEY = forest_constants.LABEL_KEY
_BUCKET_FEATURE_KEYS = forest_constants.BUCKET_FEATURE_KEYS
_FEATURE_BUCKET_COUNT = forest_constants.FEATURE_BUCKET_COUNT
_transformed_name = forest_constants.transformed_name

def preprocessing_fn(inputs):
    """
    Función de callback para tf.transform que aplica transformaciones a las features.
    
    Args:
        inputs: Diccionario mapeando cada clave de feature a sus valores crudos.
    
    Returns:
        Diccionario mapeando las claves de las features transformadas a sus operaciones.
    """
    outputs = {}

    # 1. Escalar algunas features numéricas al rango [0, 1]
    for key in ['Elevation', 'Hillshade_9am', 'Hillshade_Noon']:
        outputs[_transformed_name(key)] = tft.scale_to_0_1(inputs[key])
    
    # 2. Escalar 'Slope' usando la normalización z-score
    outputs[_transformed_name('Slope')] = tft.scale_to_z_score(inputs['Slope'])
    
    # 3. Para las distancias, usamos scale_by_min_max
    for key in ['Horizontal_Distance_To_Hydrology', 
                'Vertical_Distance_To_Hydrology',
                'Horizontal_Distance_To_Roadways',
                'Horizontal_Distance_To_Fire_Points']:
        outputs[_transformed_name(key)] = tft.scale_by_min_max(inputs[key])
    
    # 4. Bucketización: además de normalizar, se crea una versión bucketizada de 'Slope'
    for key in _BUCKET_FEATURE_KEYS:
        outputs[_transformed_name(key) + '_bucketized'] = tft.bucketize(inputs[key],
                                                                        _FEATURE_BUCKET_COUNT[key])
    
    # 5. Convertir la etiqueta a un índice a través de un vocabulario.
    # Convertimos a string para obtener un vocabulario consistente.
    outputs[_transformed_name(_LABEL_KEY)] = tft.compute_and_apply_vocabulary(
                                                tf.as_string(inputs[_LABEL_KEY])
                                             )
    
    # 6. Ejemplo adicional: aplicar hashing a la etiqueta
    outputs[_transformed_name(_LABEL_KEY) + '_hashed'] = tft.hash_strings(
                                                            tf.as_string(inputs[_LABEL_KEY]),
                                                            hash_buckets=10
                                                         )
    
    return outputs

# Opcional: suprimir mensajes de advertencia de TensorFlow
tf.get_logger().setLevel('ERROR')
