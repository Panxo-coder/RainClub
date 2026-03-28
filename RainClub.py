import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="RainClub - Maule", page_icon="💧")

# Estilo para evitar que Chrome intente traducir y se bloquee
st.markdown('<html lang="es"></html>', unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("💧 RainClub: Inteligencia Hídrica")
st.subheader("Optimización de riego para la Región del Maule")
st.write("Proyecto para la competencia **SabíaLab 2026**")

# --- ENTRADA DE DATOS (Panel Lateral) ---
st.sidebar.header("Configuración del Predio")
comuna = st.sidebar.selectbox("Seleccione Comuna", ["Linares", "Yerbas Buenas", "Longaví"])
cultivo = st.sidebar.selectbox("Tipo de Cultivo", ["Cerezos", "Arándanos", "Manzanos"])
hectareas = st.sidebar.number_input("Cantidad de Hectáreas", min_value=0.1, value=1.0)
sistema_riego = st.sidebar.radio("Sistema de Riego", ["Goteo (Eficiencia 95%)", "Tendida (Eficiencia 50%)"])

# --- LÓGICA DE CÁLCULO ---
# Datos simulados basados en clima actual de la zona
evapotranspiracion = 4.5  # mm/día promedio en marzo para el Maule
eficiencia = 0.95 if "Goteo" in sistema_riego else 0.50
agua_necesaria = (evapotranspiracion * hectareas) / eficiencia

# --- VISUALIZACIÓN DE RESULTADOS ---
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Agua Requerida (m³/día)", value=f"{agua_necesaria:.2f}")
    st.info(f"📍 Ubicación: {comuna}")

with col2:
    ahorro = "Máximo" if eficiencia > 0.9 else "Bajo"
    st.metric(label="Nivel de Eficiencia", value=ahorro)
    st.success(f"🌱 Cultivo: {cultivo}")

# --- MODELO DE NEGOCIO (Para el Jurado) ---
st.divider()
st.write("### 📊 Modelo de Negocio: RainClub")
col_a, col_b = st.columns(2)

with col_a:
    st.write("**Plan Básico (Gratis)**")
    st.write("- Cálculo de riego diario")
    st.write("- Soporte para 1 predio")
    st.write("- Ideal para pequeños agricultores")

with col_b:
    st.write("**Plan Pro ($15.000/mes)**")
    st.write("- Alertas por SMS/WhatsApp")
    st.write("- Sensores IoT integrados")
    st.write("- **Financia el acceso gratuito al agro local**")

st.info("💡 RainClub utiliza un modelo Freemium para democratizar la tecnología en el campo chileno.")
