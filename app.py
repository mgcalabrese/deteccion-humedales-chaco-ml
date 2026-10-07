# ============================================================
# APP STREAMLIT - CLASIFICACIÓN DE COBERTURA
# Proyecto Final M7
# ============================================================

import os
import joblib
import pandas as pd
import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Clasificación de Humedales",
    page_icon="🌿",
    layout="centered"
)

RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
RUTA_MODELO = os.path.join(RUTA_PROYECTO, "model.pkl")
RUTA_MUESTRA = os.path.join(RUTA_PROYECTO, "datos_muestra.csv")

FEATURES = [
    "Blue",
    "Green",
    "Red",
    "NIR",
    "SWIR1",
    "SWIR2",
    "NDVI",
    "NDWI",
    "MNDWI"
]

CLASES = {
    1: "Bosque hidromórfico",
    2: "Bosque xerofítico",
    3: "Cuerpos de agua",
    4: "Tierras manejadas",
    5: "Sabanas con árboles y arbustales",
    6: "Sabanas hidromórficas",
    7: "Humedales"
}

# ============================================================
# CARGAR MODELOS Y DATOS
# ============================================================

@st.cache_resource
def cargar_modelos():
    return joblib.load(RUTA_MODELO)

@st.cache_data
def cargar_muestra():
    return pd.read_csv(RUTA_MUESTRA)

modelos = cargar_modelos()
datos = cargar_muestra()

# ============================================================
# TÍTULO
# ============================================================

st.title("🌿 Clasificación de coberturas del Chaco")

st.write(
    """
    Aplicación demostrativa del modelo Random Forest utilizado para
    clasificar coberturas terrestres en 2005 y 2025, con especial
    interés en la identificación de humedales.
    """
)

# ============================================================
# SELECCIÓN DE AÑO
# ============================================================

anio = st.selectbox(
    "Seleccionar modelo",
    ["2005", "2025"]
)

modelo = modelos[anio]

# ============================================================
# MODO DE ENTRADA
# ============================================================

modo = st.radio(
    "Forma de ingresar los datos",
    [
        "Usar un registro de datos_muestra.csv",
        "Ingresar valores manualmente"
    ]
)

# ============================================================
# OPCIÓN 1: REGISTRO REAL DE LA MUESTRA
# ============================================================

if modo == "Usar un registro de datos_muestra.csv":

    datos_anio = datos[datos["year"] == int(anio)].reset_index(drop=True)

    indice = st.selectbox(
        "Seleccionar registro",
        range(len(datos_anio)),
        format_func=lambda x: f"Registro {x + 1}"
    )

    fila = datos_anio.iloc[indice]

    st.subheader("Variables del registro")

    tabla = pd.DataFrame({
        "Variable": FEATURES,
        "Valor": [fila[col] for col in FEATURES]
    })

    st.dataframe(tabla, use_container_width=True)

    X = pd.DataFrame(
        [[fila[col] for col in FEATURES]],
        columns=FEATURES
    )

    clase_real = int(fila["Id"])

    st.write(
        f"**Clase real del registro:** "
        f"{clase_real} - {CLASES[clase_real]}"
    )

# ============================================================
# OPCIÓN 2: INGRESO MANUAL
# ============================================================

else:

    st.subheader("Ingresar variables espectrales")

    valores = {}

    for feature in FEATURES:
        valores[feature] = st.number_input(
            feature,
            value=0.0,
            format="%.6f"
        )

    X = pd.DataFrame([valores])

# ============================================================
# PREDICCIÓN
# ============================================================

st.divider()

if st.button("Realizar predicción", type="primary"):

    prediccion = int(modelo.predict(X)[0])

    st.subheader("Resultado")

    if prediccion == 7:
        st.success(
            f"Clase predicha: {prediccion} - {CLASES[prediccion]} 🌿"
        )
        st.write("El modelo identifica este registro como **Humedal**.")
    else:
        st.info(
            f"Clase predicha: {prediccion} - {CLASES[prediccion]}"
        )
        st.write("El modelo no identifica este registro como Humedal.")

    if hasattr(modelo, "predict_proba"):

        probabilidades = modelo.predict_proba(X)[0]

        clases_modelo = modelo.classes_

        df_prob = pd.DataFrame({
            "Clase": [
                f"{int(c)} - {CLASES[int(c)]}"
                for c in clases_modelo
            ],
            "Probabilidad": probabilidades
        })

        df_prob = df_prob.sort_values(
            "Probabilidad",
            ascending=False
        )

        st.subheader("Probabilidades por clase")

        st.dataframe(
            df_prob,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            df_prob.set_index("Clase")["Probabilidad"]
        )

# ============================================================
# INFORMACIÓN DEL PROYECTO
# ============================================================

st.divider()

st.caption(
    "Proyecto Final M7 | Clasificación de coberturas mediante "
    "Random Forest y datos Landsat."
)