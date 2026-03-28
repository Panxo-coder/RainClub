import streamlit as st
import pandas as pd

# Configuración de Software Profesional
st.set_page_config(page_title="RainClub Enterprise V4.0", page_icon="💧", layout="wide")

# Estilo para evitar bloqueos y mejorar diseño
st.markdown('<html lang="es"></html>', unsafe_allow_html=True)

# --- BASE DE DATOS REGIONAL MAULE ---
comunas_maule = {
    "Provincia de Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
    "Provincia de Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
    "Provincia de Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
    "Provincia de Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
}

# --- ENCABEZADO ---
st.title("💧 RainClub Enterprise V4.0")
st.markdown("## Sistema Integral de Gestión Hídrica - Región del Maule")
st.write("---")

# --- PANEL LATERAL (INPUTS) ---
st.sidebar.header("📍 1. Ubicación y Entorno")
prov = st.sidebar.selectbox("Provincia", list(comunas_maule.keys()))
comu = st.sidebar.selectbox("Comuna", comunas_maule[prov])
entorno = st.sidebar.radio("Tipo de Entorno", ["Campo Abierto", "Invernadero Tecnificado", "Invernadero Casero"])

st.sidebar.header("🌱 2. Cultivo y Marco")
cat = st.sidebar.selectbox("Categoría", ["Frutales", "Hortalizas", "Viñedos", "Cereales"])
has = st.sidebar.number_input("Superficie (Hectáreas o m²)", min_value=0.1, value=1.0)
dist_h = st.sidebar.number_input("Distancia entre hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Distancia entre plantas (m)", value=2.0)

st.sidebar.header("⚙️ 3. Datos Técnicos")
sis = st.sidebar.selectbox("Sistema de Riego", ["Goteo", "Cinta de Riego", "Microaspersión", "Surco"])
caudal_emisor = st.sidebar.number_input("Caudal por emisor (Litros/Hora)", value=2.0)
emisores_por_planta = st.sidebar.number_input("N° emisores por planta", value=2)

# --- LÓGICA DE CÁLCULO PROFESIONAL ---
# Factores de corrección
factor_entorno = 0.7 if "Invernadero" in entorno else 1.0
etc_base = 5.5 * factor_entorno 

# Cálculos de Densidad
plantas_ha = 10000 / (dist_h * dist_p)
total_plantas = plantas_ha * has

# Cálculos de Agua
litros_planta_dia = etc_base 
litros_totales_dia = litros_planta_dia * total_plantas

# Cálculo de Tiempo (basado en emisores)
litros_hora_planta = caudal_emisor * emisores_por_planta
horas_riego = litros_planta_dia / litros_hora_planta
minutos_riego = horas_riego * 60

# --- PANTALLA PRINCIPAL (RESULTADOS) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Agua Total Proyecto", f"{litros_totales_dia:,.0f} L/día")
    st.caption(f"Cálculo para {int(total_plantas)} plantas en {comu}")

with col2:
    st.metric("Tiempo de Riego", f"{int(minutos_riego)} min")
    st.caption(f"Frecuencia sugerida: 1 vez al día")

with col3:
    st.metric("Dosis por Planta", f"{litros_planta_dia:.2f} L")
    st.caption(f"Eficiencia del sistema: {(0.95 if sis == 'Goteo' else 0.5)*100}%")

# --- MODELO DE NEGOCIO Y PAGOS (EL PITCH GANADOR) ---
st.write("---")
st.subheader("💼 Plan de Negocios RainClub")

tab1, tab2, tab3 = st.tabs(["💎 Funciones Premium vs Gratis", "💰 Pasarela de Pagos", "🚀 Impacto"])

with tab1:
    col_g, col_p = st.columns(2)
    with col_g:
        st.success("### **Plan Básico (Gratis)**")
        st.write("- Calculadora de riego ilimitada.")
        st.write("- Soporte para las 30 comunas del Maule.")
        st.write("- Guía de cultivos estacionales.")
        st.write("**Para:** Pequeños agricultores e huerteros.")
    with col_p:
        st.warning("### **Plan Premium ($15.000/mes)**")
        st.write("- **Alertas por SMS:** Aviso de heladas en tiempo real.")
        st.write("- **Sensores IoT:** Conexión directa a humedad de suelo.")
        st.write("- **Historial:** Gráficos de consumo mensual.")
        st.write("**Para:** Productores exportadores.")

with tab2:
    st.write("#### ¿A dónde va el dinero?")
    st.info("Los fondos se recaudan a través de la **Cooperativa RainClub Maule**, destinados al mantenimiento del servidor y a la donación de kits de riego para escuelas agrícolas de la región.")
    
    st.write("#### Métodos de Pago Aceptados:")
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.button("💳 WebPay / Débito")
    col_p2.button("📱 Mercado Pago")
    col_p3.button("🏦 Transferencia")

with tab3:
    st.write("#### ¿Por qué premiar este proyecto?")
    st.write("1. **Local:** Diseñado en el corazón del Maule (Linares/Yerbas Buenas).")
    st.write("2. **Social:** Los que tienen más (Premium) financian a los que tienen menos (Básico).")
    st.write("3. **Ecológico:** Ahorro proyectado de un 40% de agua en la región.")

st.info("RainClub Enterprise V4.0 - Software desarrollado para SabíaLab 2026.")
