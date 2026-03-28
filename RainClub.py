import streamlit as st
import random

# Configuración de Software Escala Nacional Jerárquico
st.set_page_config(page_title="RainClub Chile V12.0", page_icon="🇨🇱", layout="wide")

# --- BASE DE DATOS JERÁRQUICA NACIONAL ---
# Estructura: Región -> Provincia -> Comunas
chile_datos = {
    "Región del Maule": {
        "Provincias": {
            "Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
            "Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
            "Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
            "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
        },
        "Sugerencia": "Cerezos, Arándanos, Manzanos y Vides viníferas.",
        "ET_Base": 5.2
    },
    "Región de O'Higgins": {
        "Provincias": {
            "Cachapoal": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente"],
            "Colchagua": ["San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"],
            "Cardenal Caro": ["Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones"]
        },
        "Sugerencia": "Maíz, Frutales de carozo y Semilleros.",
        "ET_Base": 5.5
    },
    "Región Metropolitana": {
        "Provincias": {
            "Santiago": ["Santiago", "Cerrillos", "Maipú", "Pudahuel", "Quilicura"],
            "Chacabuco": ["Colina", "Lampa", "Tiltil"],
            "Maipo": ["San Bernardo", "Buin", "Paine", "Calera de Tango"],
            "Melipilla": ["Melipilla", "Curacaví", "María Pinto", "San Pedro"]
        },
        "Sugerencia": "Nogales, Hortalizas frescas y Uva de mesa.",
        "ET_Base": 5.8
    }
}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V12.0")
st.markdown("### Plataforma de Gestión Hídrica Nacional Inteligente")
st.write("---")

# --- PANEL LATERAL (JERARQUÍA DE UBICACIÓN) ---
st.sidebar.header("📍 Ubicación Geográfica")

# 1. Selección de Región
region_sel = st.sidebar.selectbox("Seleccione Región", list(chile_datos.keys()))

# 2. Selección de Provincia (basada en la Región)
provincias_dict = chile_datos[region_sel]["Provincias"]
provincia_sel = st.sidebar.selectbox("Seleccione Provincia", list(provincias_dict.keys()))

# 3. Selección de Comuna (basada en la Provincia)
comuna_sel = st.sidebar.selectbox("Seleccione Comuna", provincias_dict[provincia_sel])

st.sidebar.divider()
st.sidebar.header("🚜 Datos del Predio")
has = st.sidebar.number_input("Hectáreas totales", value=1.0)
dist_h = st.sidebar.number_input("Entre Hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Entre Plantas (m)", value=2.0)
sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo (95%)", "Microaspersión (85%)", "Tendida (50%)"])

# --- LÓGICA DE CÁLCULO ---
et_actual = chile_datos[region_sel]["ET_Base"]
eficiencia = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else 0.50)
plantas_total = (10000 / (dist_h * dist_p)) * has
litros_totales = (et_actual * plantas_total) / eficiencia
minutos_riego = (litros_totales / (1.5 * has * 60))

# --- RESULTADOS ---
st.subheader(f"📊 Reporte: {comuna_sel} ({provincia_sel}), {region_sel}")

col_info, col_res = st.columns([1, 2])

with col_info:
    st.info("💡 **Análisis de Factibilidad:**")
    st.write(f"En esta zona sugerimos: **{chile_datos[region_sel]['Sugerencia']}**")
    st.caption(f"Datos climáticos sincronizados con ET: {et_actual} mm/día")

with col_res:
    res1, res2, res3 = st.columns(3)
    res1.metric("Agua Diaria", f"{litros_totales:,.0f} L")
    res2.metric("Tiempo Riego", f"{int(minutos_riego)} min")
    res3.metric("Plantas", f"{int(plantas_total)} pl")

# --- MODELO DE NEGOCIO Y PAGOS ---
st.write("---")
tab1, tab2, tab3 = st.tabs(["💎 Planes", "💳 Pasarelas de Pago", "💰 Mi Comisión"])

with tab1:
    st.success("### **Plan Básico (Gratis)**: Acceso nacional completo.")
    st.warning("### **Plan Pro ($15.000/mes)**: Alertas WhatsApp y Sensores IoT.")

with tab2:
    st.write("#### Medios de Pago:")
    st.write("💳 Visa | Mastercard | WebPay | PayPal | Google Pay | Apple Pay | Mercado Pago")
    st.button("PAGAR SUSCRIPCIÓN")

with tab3:
    st.write("#### Transparencia de Ingresos:")
    st.
