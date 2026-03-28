import streamlit as st

# Configuración de Software de Alto Impacto
st.set_page_config(page_title="RainClub Evolution V7.0", page_icon="💧", layout="wide")

# Estilo para evitar bloqueos
st.markdown('<html lang="es"></html>', unsafe_allow_html=True)

# --- BASE DE DATOS REGIONAL ---
comunas_maule = {
    "Provincia de Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
    "Provincia de Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
    "Provincia de Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
    "Provincia de Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
}

# --- ENCABEZADO ---
st.title("💧 RainClub Evolution V7.0")
st.markdown("## La Herramienta Definitiva para el Agro del Maule")
st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("📍 Configuración Técnica")
prov = st.sidebar.selectbox("Provincia", list(comunas_maule.keys()))
comu = st.sidebar.selectbox("Comuna", comunas_maule[prov])
has = st.sidebar.number_input("Hectáreas", min_value=0.1, value=1.0)
dist_h = st.sidebar.number_input("Entre Hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Entre Plantas (m)", value=2.0)
sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo", "Microaspersión", "Aspersión", "Tendida"])

# --- LÓGICA DE CÁLCULO ---
plantas_total = (10000 / (dist_h * dist_p)) * has
litros_dia = 5.2 * plantas_total
minutos_estimados = (litros_dia / (1.5 * has * 60)) # Cálculo base

# --- RESULTADOS TÉCNICOS (GRATUITOS) ---
st.subheader(f"📊 Reporte de Riego para {comu}")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Agua Necesaria", f"{litros_dia:,.0f} L/día")
with c2:
    st.metric("Tiempo Estimado", f"{int(minutos_estimados)} min")
with c3:
    st.metric("Densidad", f"{int(plantas_total)} plantas")

# --- COMPARATIVA DE PLANES (ESTRATEGIA DE VENTAS) ---
st.write("---")
st.subheader("🚀 Elige el poder de tu Gestión")

col_free, col_pro = st.columns(2)

with col_free:
    st.success("### **Plan Campesino (Gratis)**")
    st.write("✅ **Cálculo de Litros y Minutos:** Precisión diaria.")
    st.write("✅ **Todas las Comunas:** Acceso total al Maule.")
    st.write("✅ **Soporte de Cultivos:** Base de datos completa.")
    st.write("✅ **Guía de Buenas Prácticas:** Consejos de ahorro.")
    st.button("Plan Actual Activo", disabled=True)

with col_pro:
    st.warning("### **Plan Pro-Empresarial ($15.000/mes)**")
    st.write("🌟 **Alertas WhatsApp:** Avisos de heladas y golpes de calor.")
    st.write("🌟 **Sensores en Vivo:** Conexión a humedad de suelo real.")
    st.write("🌟 **Historial de Riego:** Gráficos para certificar exportaciones.")
    st.write("🌟 **Soporte VIP:** Chat directo con expertos.")
    if st.button("🔥 MEJORAR A PLAN PRO"):
        st.balloons()

# --- PASARELA DE PAGOS TOTAL ---
st.write("---")
st.subheader("💳 Métodos de Pago Seguros")
st.write("Aceptamos todas las tarjetas y plataformas para tu comodidad:")

# Logos y métodos
st.markdown("""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
    <p style="font-size: 20px;"><b>Visa | Mastercard | WebPay | PayPal | Apple Pay | Google Pay | Mercado Pago | MACH</b></p>
    <p><i>El 40% de tu suscripción va directamente al fondo de innovación del desarrollador.</i></p>
</div>
""", unsafe_allow_html=True)

st.info("RainClub V7.0 - Uniendo tecnología y campo. Desarrollado para SabíaLab 2026.")
