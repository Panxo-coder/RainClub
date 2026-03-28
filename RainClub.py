import streamlit as st
import time

# Configuración de Software Profesional
st.set_page_config(page_title="RainClub Chile V16.0", page_icon="🇨🇱", layout="wide")

# --- BASE DE DATOS DE CULTIVOS Y SUS COEFICIENTES (Kc) ---
# El Kc ajusta el riego según el tipo de planta
dict_cultivos = {
    "Cerezos": 1.1,
    "Nogales": 1.05,
    "Uva de Mesa": 0.85,
    "Arándanos": 0.9,
    "Manzanos": 1.0,
    "Cítricos (Limón/Naranja)": 0.75,
    "Paltos": 0.85,
    "Hortalizas (Tomate/Lechuga)": 1.05,
    "Alfalfa / Praderas": 1.15,
    "Maíz": 1.2
}

# --- BASE DE DATOS REGIONAL ---
chile_agro = {
    "Región del Maule": {
        "Provincias": {
            "Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
            "Talca": ["Talca", "Constitución", "San Clemente", "Maule", "San Rafael"],
            "Curicó": ["Curicó", "Molina", "Teno", "Romeral", "Sagrada Familia"],
            "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
        },
        "Sugerencia": "Cerezos y Arándanos", "ET": 5.2
    },
    "Región Metropolitana": {
        "Provincias": {
            "Santiago": ["Santiago", "Maipú", "Pudahuel", "Lampa"],
            "Maipo": ["San Bernardo", "Buin", "Paine"],
            "Melipilla": ["Melipilla", "Curacaví"]
        },
        "Sugerencia": "Nogales y Uva de Mesa", "ET": 5.8
    },
    "Región de O'Higgins": {
        "Provincias": {
            "Cachapoal": ["Rancagua", "Rengo", "Requínoa"],
            "Colchagua": ["San Fernando", "Santa Cruz", "Chimbarongo"]
        },
        "Sugerencia": "Maíz y Frutales de carozo", "ET": 5.5
    }
}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V16.0")
st.markdown("#### Gestión Hídrica Personalizada por Cultivo")
st.write("---")

# --- PANEL LATERAL (CONFIGURACIÓN) ---
st.sidebar.header("📍 1. Ubicación")
reg_sel = st.sidebar.selectbox("Región", list(chile_agro.keys()))
prov_sel = st.sidebar.selectbox("Provincia", list(chile_agro[reg_sel]["Provincias"].keys()))
comu_sel = st.sidebar.selectbox("Comuna", chile_agro[reg_sel]["Provincias"][prov_sel])

st.sidebar.divider()
st.sidebar.header("🌱 2. Mi Cultivo")
# AQUÍ ESTÁ LO QUE PEDISTE: El agricultor elige su cultivo
cultivo_usuario = st.sidebar.selectbox("¿Qué cultivo tiene en su predio?", list(dict_cultivos.keys()))
kc_actual = dict_cultivos[cultivo_usuario]

st.sidebar.divider()
st.sidebar.header("🚜 3. Datos Técnicos")
has = st.sidebar.number_input("Hectáreas totales", min_value=0.1, value=1.0)
dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=2.0)
sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo (95%)", "Microaspersión (85%)", "Tendida (50%)"])

# --- LÓGICA DE CÁLCULO (FÓRMULA FAO-56 REAL) ---
et_base = chile_agro[reg_sel]["ET"]
# La fórmula real es: ETc = ETo * Kc
etc_ajustada = et_base * kc_actual 
efi = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else 0.50)
pl_total = (10000 / (dist_h * dist_p)) * has
l_dia = (etc_ajustada * pl_total) / efi
min_riego = (l_dia / (1.5 * has * 60))

# --- RESULTADOS ---
st.subheader(f"📊 Reporte para {cultivo_usuario} en {comu_sel}")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Agua Diaria", f"{l_dia:,.0f} L")
    st.caption(f"Ajustado por Kc: {kc_actual}")
with c2:
    st.metric("Tiempo Riego", f"{int(min_riego)} min")
with c3:
    st.metric("Plantas", f"{int(pl_total)} pl")
with c4:
    st.metric("Evapotranspiración", f"{et_base} mm", delta="Base Agromet")

# --- SECCIÓN ESTRATÉGICA ---
st.write("---")
t1, t2, t3 = st.tabs(["💎 Planes y Alertas", "💳 Pagos", "📱 Instalación"])

with t1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("### Sugerencia de Expertos")
        st.write(f"Para la zona de {reg_sel}, además de {cultivo_usuario}, es muy factible plantar: **{chile_agro[reg_sel]['Sugerencia']}**.")
    with col_b:
        st.warning("### Plan Pro ($15.000/mes)")
        if st.button("🔔 Probar Alerta WhatsApp"):
            st.toast(f"Enviando alerta de riego para {cultivo_usuario}...")
            time.sleep(1)
            st.success("✅ Mensaje enviado al agricultor.")

with t2:
    st.write("#### Pasarela Segura")
    st.write("Visa | Mastercard | WebPay | PayPal | Mercado Pago")
    st.button("Activar Suscripción Pro")

with t3:
    st.write("### RainClub en tu celular")
    st.write("Usa la opción 'Agregar a pantalla de inicio' en tu navegador para instalar.")

st.info("RainClub V16.0 - Desarrollado para SabíaLab 2026.")
