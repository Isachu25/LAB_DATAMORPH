import streamlit as st
import pandas as pd
import json

# Configuración de la página
st.set_page_config(page_title="DataMorph JSON", layout="wide")
st.title("DataMorph: De NoSQL (JSON) a SQL (Tabular)")

# --- Paso A: El Editor y el Visor ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Entrada NoSQL (JSON Flexible)")
    # JSON de ejemplo inicial con personas diferentes (Esquema Dinámico)
    default_json = """[
  {"id": 1, "nombre": "Ana", "edad": 28},
  {"id": 2, "nombre": "Beto", "ciudad": "Madrid"},
  {"id": 3, "nombre": "Carla", "hobbies": ["Ciclismo", "Lectura"]}
]"""
    json_input = st.text_area("Pega tu JSON aquí:", value=default_json, height=300)

with col2:
    st.subheader("2. Vista SQL (Tabla Rígida)")
    
    # --- Paso C: Gestión de Errores (Robustez) ---
    try:
        # Convertir texto a objeto Python
        data_object = json.loads(json_input)
        
        # Normalizar: La magia que aplana el JSON a una tabla
        df = pd.json_normalize(data_object)
        
        st.dataframe(df, use_container_width=True)

        # --- Paso B: Analítica de Esquema ---
        st.divider()
        st.write("### 📊 Analítica del Esquema Detectado")
        
        # Listar columnas detectadas
        cols = df.columns.tolist()
        st.write(f"**Columnas detectadas:** {', '.join(cols)}")
        
        # Contar valores nulos (NaN)
        total_nulls = df.isnull().sum().sum()
        st.metric(label="Total Valores Nulos (NaN)", value=total_nulls)
        
        if total_nulls > 0:
            st.warning(
                f"⚠️ ¡Atención! Se han detectado {total_nulls} huecos vacíos. "
                "En SQL esto desperdicia espacio (almacenando NULLs). "
                "En NoSQL es normal y eficiente (Sparse Data)."
            )
            
    except json.JSONDecodeError:
        st.error("❌ Error de Formato: El texto introducido no es un JSON válido. Revisa las comas y corchetes.")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado: {e}")

# --- Paso C: Explicación Teórica ---
with st.expander("ℹ️ ¿Qué está pasando aquí? (Teoría SQL vs NoSQL)"):
    st.markdown("""
    * **SQL (Esquema Fijo):** Es como una cárcel[cite: 4]. Si la columna no existe, no puedes guardar el dato.
    * **NoSQL (Esquema Flexible):** Es dinámico[cite: 5]. Si llega un campo nuevo, se guarda sin afectar a los demás.
    * **Schema-on-Read:** Aquí guardamos el JSON tal cual y definimos la estructura solo al leerlo con Pandas[cite: 144].
    """)
