# Detección de cambios en humedales del Chaco entre 2005 y 2025 mediante Machine Learning

## Problema

Los humedales constituyen ecosistemas de gran importancia ambiental y presentan cambios espaciales que pueden ser difíciles de detectar mediante relevamientos tradicionales. El problema principal es que el monitoreo de grandes extensiones mediante relevamientos de campo resulta costoso, lento y difícil de repetir periódicamente.
La solución puede ser de utilidad para investigadores, instituciones ambientales, organismos públicos y equipos técnicos que necesiten realizar seguimiento territorial de humedales y detectar zonas donde podrían haberse producido cambios.


## Objetivo

Desarrollar un modelo de clasificación supervisada para identificar coberturas terrestres, con especial interés en la clase Humedales, y analizar su persistencia, pérdida y ganancia entre los años 2005 y 2025.

## Datos

Se utilizaron imágenes Landsat disponibles en Google Earth Engine:

- Landsat 5 TM para el año 2005 (35O imagenes)
- Landsat 8 y Landsat 9 OLI para el año 2025 (716 imagenes)

Se emplearon las siguientes variables (Indices espectrales utilizando bandas de las imagenes satelitales):

- Blue
- Green
- Red
- NIR
- SWIR1
- SWIR2
- NDVI
- NDWI
- MNDWI

Las muestras de entrenamiento corresponden a siete clases de cobertura:

1. Bosque hidromórfico
2. Bosque xerofítico
3. Cuerpos de agua
4. Tierras manejadas
5. Sabanas con árboles y arbustales
6. Sabanas hidromórficas
7. Humedales

Para 2005 se utilizaron 1.185 muestras y para 2025 se utilizaron 1.195 muestras. Las muestras utilizadas fueron generadas en el proyecto Geoforpy con datos de INFONA mas datos obtenidos mediante interpretacion visual. Los conjuntos de cada año fueron procesados y entrenados de manera independiente.

## Modelo de aprendizaje supervisado para clasificación.

Machine Learning permite aprender estas relaciones a partir de muestras previamente clasificadas y posteriormente aplicar el modelo sobre grandes superficies.
Se compararon dos algoritmos:

- Logistic Regression: se utilizó como modelo base por ser simple, interpretable y eficiente. Permite evaluar hasta qué punto las clases pueden separarse mediante relaciones relativamente simples entre las bandas espectrales y los índices derivados.

- Random Forest: se seleccionó porque puede representar relaciones no lineales y complejas entre las variables espectrales, es robusto frente a ruido y variables correlacionadas, y suele presentar buen desempeño en problemas de clasificación de coberturas terrestres con imágenes satelitales.

La evaluación se realizó por separado para 2005 y 2025 utilizando un conjunto de entrenamiento del 70% y un conjunto de prueba del 30%.

Además de la exactitud global, se analizaron Precision, Recall y F1-score e Indice Kappa específicamente para la clase Humedales.


COMPARACIÓN DE MODELOS EXACTITUD
 Año   Modelo                 Accuracy_global   Kappa   
2005    Logistic Regression     0.5393          0.4424        
2005    Random Forest           0.6713          0.5859

2025    Logistic Regression     0.6797          0.5993      
2025    Random Forest           0.7270          0.6487

Se selecciono Random Forest ya que presento mejor desempeño como algoritmo final para ambos años.

El modelo final de cada año fue posteriormente reentrenado utilizando la totalidad de las muestras correspondientes a ese año.

## Resultados

La clasificación estimó:

- Humedales 2005: 359.087,11 ha
- Humedales 2025: 362.217,77 ha
- Persistencia: 28.179,09 ha
- Pérdida detectada: 330.908,02 ha
- Ganancia detectada: 334.038,67 ha
- Cambio neto: +3.130,66 ha

En términos porcentuales:

- Persistencia: 7,85%
- Pérdida detectada: 92,15%
- Ganancia detectada: 93,02%
- Cambio neto: +0,87%

## Estimación de ROI

El uso de clasificación automática mediante imágenes satelitales puede reducir costos asociados al monitoreo extensivo de humedales, principalmente al disminuir la necesidad de campañas de campo generalizadas y orientar las verificaciones hacia zonas prioritarias.

Se plantean tres escenarios ilustrativos:

| Escenario | Reducción estimada del trabajo de campo | Impacto esperado |
| Conservador | 20 % | Reducción limitada de traslados, viáticos y horas técnicas |
| Intermedio | 40 % | Disminución significativa de campañas y priorización de zonas |
| Favorable | 60 % | Monitoreo remoto rutinario con campañas de campo focalizadas |


## Limitaciones del trabajo

- La cantidad de muestras de la clase Humedales es considerablemente menor que la de algunas otras clases utilizadas, se requiere cubrir todo el area de estudio para mejorar el desempeño.
- Los modelos alcanzaron una exactitud moderada para la clase Humedales.


## Mejoras futuras

1. **Incrementar las muestras de entrenamiento de Humedales**, procurando una mejor distribución espacial y representación de diferentes tipos de ambientes húmedos.

2. **Evaluar ventanas temporales equivalentes**, por ejemplo utilizando imágenes correspondientes a la misma estación del año para reducir diferencias asociadas a estacionalidad e inundaciones temporales.

3. **Incorporar nuevas variables**, como índices adicionales, topografía, precipitación o frecuencia histórica de inundación.


## Archivos principales

- `notebook_final.ipynb`: procesamiento, entrenamiento, evaluación y análisis.
- `model.pkl`: modelos Random Forest finales de 2005 y 2025.
- `datos_muestra.csv`: muestra de 100 registros utilizada como archivo reducido de entrega.