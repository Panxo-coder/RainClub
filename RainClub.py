import streamlit as st
import pandas as pd

# Configuración Enterprise
st.set_page_config(page_title="RainClub Business V5.0", page_icon="💧", layout="wide")

# Estilo para evitar bloqueos
st.markdown('<html lang="es"></html>', unsafe_allow_html=True)

# --- BASE DE DATOS REGIONAL MAULE ---
comunas_maule = {
    "Provincia de Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
    "Provincia de Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
    "Provincia de Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
    "Provincia de Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
}

# --- ENCABEZADO ---
st.title("💧 RainClub Enterprise V5.0")
st.markdown("## Gestión Hídrica y Rentabilidad Agrícola")
st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("📍 1. Ubicación")
prov = st.sidebar.selectbox("Provincia", list(comunas_maule.keys()))
comu = st.sidebar.selectbox("Comuna", comunas_maule[prov])
entorno = st.sidebar.radio("Entorno", ["Campo Abierto", "Invernadero Tecnificado"])

st.sidebar.header("🌱 2. Parámetros Técnicos")
has = st.sidebar.number_input("Hectáreas totales", min_value=0.1, value=1.0)
dist_h = st.sidebar.number_input("Entre hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Entre plantas (m)", value=2.0)
caudal = st.sidebar.number_input("Caudal Emisor (L/H)", value=2.0)
emisores = st.sidebar.number_input("Emisores por planta", value=2)

# --- LÓGICA DE CÁLCULO ---
etc = 5.5 if entorno == "Campo Abierto" else 3.8
plantas_ha = 10000 / (dist_h * dist_p)
total_plantas = plantas_ha * has
litros_planta = etc
litros_totales = litros_planta * total_plantas
minutos_riego = (litros_planta / (caudal * emisores)) * 60

# --- RESULTADOS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Agua Total", f"{litros_totales:,.0f} L/día")
with col2:
    st.metric("Tiempo de Riego", f"{int(minutos_riego)} min")
with col3:
    st.metric("Dosis Diaria", f"{litros_planta:.1f} L/planta")

# --- MODELO ECONÓMICO Y PAGOS (TU GANANCIA) ---
st.write("---")
st.subheader("💼 Modelo de Negocio y Estructura de Ingresos")

tab1, tab2 = st.tabs(["💰 Planes y Comisiones", "💳 Pasarela de Pago"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("### **Plan Basic (Suscripción Gratuita)**")
        st.write("- Financiado por publicidad de empresas de riego locales.")
        st.write("- Cálculo básico para pequeños agricultores del Maule.")
    with col_b:
        st.warning("### **Plan Pro ($15.000 / mes)**")
        st.write("- Monitoreo satelital y alertas premium.")
        st.write("- **Distribución del Pago:**")
        st.info("**60%** Mantenimiento y Servidores | **40% Utilidad del Desarrollador**")
        st.write("*(Esta comisión directa permite la innovación constante de la App)*")

with tab2:
    st.write("#### ¿Cómo se paga?")
    st.write("Utilizamos **Fintoc** o **WebPay** para depósitos automáticos.")
    
    # Simulación de botones de pago
    st.markdown("""
    | Plan | Precio | Acción |
    | :--- | :--- | :--- |
    | Mensual | $15.000 | [Pagar con WebPay] |
    | Anual (20% OFF) | $144.000 | [Pagar con Transferencia] |
    """)
    
    st.info(f"Los ingresos de **{comu}** se centralizan en la cuenta de administración de RainClub, donde el desarrollador recibe su porcentaje por propiedad intelectual.")

st.info("RainClub V5.0 - Desarrollado por Alumno de Liceo Agropecuario para SabíaLab 2026.")
