import streamlit as st
import random

# Configuración de Software Escala Nacional
st.set_page_config(page_title="RainClub Chile V11.0", page_icon="🇨🇱", layout="wide")

# --- BASE DE DATOS NACIONAL (ZONIFICACIÓN) ---
zonas_chile = {
    "Norte Grande (Arica a Antofagasta)": {
        "comunas": ["Arica", "Iquique", "Antofagasta", "Calama", "Pica"],
        "sugerencia": "Limones, Olivos, Quínoa y hortalizas bajo malla.",
        "et_base": 6.5
    },
    "Norte Chico (Atacama a Coquimbo)": {
        "comunas": ["Copiapó", "Vallenar", "La Serena", "Coquimbo", "Ovalle", "Vicuña"],
        "sugerencia": "Uva de mesa, Cítricos, Nogales y Pisco.",
        "et_base": 5.8
    },
    "Zona Central (Valparaíso a Maule)": {
        "comunas": ["Santiago", "Rancagua", "Talca", "Linares", "Curicó", "Yerbas Buenas", "Quillota"],
        "sugerencia": "Cerezos, Arándanos, Vides viníferas y Frutales de carozo.",
        "et_base": 5.2
    },
    "Zona Sur (Ñuble a Los Lagos)": {
        "comunas": ["Chillán", "Concepción", "Temuco", "Valdivia", "Osorno", "Puerto Montt"],
        "sugerencia": "Avellano Europeo, Frambuesas, Lechería y Praderas.",
        "et_base": 3.5
    },
    "Zona Austral (Aysén a Magallanes)": {
        "comunas": ["Coyhaique", "Punta Arenas", "Puerto Natales"],
        "sugerencia": "Calafate, Invernaderos tecnificados y ganadería ovina.",
        "et_base": 2.1
    }
}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V11.0: Inteligencia Agrícola Nacional")
st.markdown("### El Futuro del Riego desde Arica a Magallanes")
st.write("---")

# --- PANEL LATERAL (CONTROL NACIONAL) ---
st.sidebar.header("🗺️ Selección Geográfica")
zona_sel = st.sidebar.selectbox("Zona de Chile", list(zonas_chile.keys()))
comuna_sel = st.sidebar.selectbox("Comuna", zonas_chile[zona_sel]["comunas"])

st.sidebar.divider()
st.sidebar.header("🚜 Datos del Predio")
has = st.sidebar.number_input("Hectáreas", min_value=0.1, value=1.0)
dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=2.0)
sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo (95%)", "Microaspersión (85%)", "Aspersión (75%)", "Tendida (50%)"])

# --- LÓGICA DE INTELIGENCIA ---
et_actual = zonas_chile[zona_sel]["et_base"]
eficiencia = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else 0.50)
plantas_total = (10000 / (dist_h * dist_p)) * has
litros_totales = (et_actual * plantas_total) / eficiencia
minutos_riego = (litros_totales / (1.5 * has * 60))

# --- PANTALLA DE RESULTADOS ---
st.subheader(f"📍 Reporte para {comuna_sel} - {zona_sel}")

col_sug, col_calc = st.columns([1, 2])

with col_sug:
    st.info("💡 **Sugerencia de Cultivo Factible:**")
    st.write(zonas_chile[zona_sel]["sugerencia"])
    st.warning("⚠️ Análisis basado en disponibilidad hídrica regional.")

with col_calc:
    c1, c2, c3 = st.columns(3)
    c1.metric("Agua Diaria", f"{litros_totales:,.0f} L")
    c2.metric("Tiempo Riego", f"{int(minutos_riego)} min")
    c3.metric("Plantas", f"{int(plantas_total)} pl")

# --- MODELO DE NEGOCIO NACIONAL (TU GANANCIA) ---
st.write("---")
tab1, tab2, tab3 = st.tabs(["💰 Planes Nacionales", "💳 Pasarela Global", "🛰️ Red Nacional Agromet"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("### **Plan Básico (Gratis)**")
        st.write("- Sugerencias de cultivo por zona.")
        st.write("- Calculadora nacional para las 16 regiones.")
        st.write("**Impacto:** Digitalizar el pequeño agro chileno.")
    with col_b:
        st.warning("### **Plan Pro-Empresarial ($15.000/mes)**")
        st.write("- Alertas críticas nacionales (MeteoChile/Agromet).")
        st.write("- Análisis de rentabilidad por cultivo.")
        st.write("- **40% de Comisión para el Desarrollador ($6.000).**")

with tab2:
    st.write("#### Medios de Pago Globales habilitados:")
    st.write("Visa, Mastercard, PayPal, Apple Pay, Google Pay, Mercado Pago, WebPay (Chile).")
    st.button("💳 SUSCRIBIRME A RAINCLUB PRO")

with tab3:
    st.info("RainClub Chile utiliza una red de +200 estaciones meteorológicas simuladas para el Pitch, listas para conexión vía API oficial.")

st.info("RainClub Chile V11.0 - Un proyecto de Impacto Nacional desarrollado para SabíaLab 2026.")
