import streamlit as st
import time

# Configuración Pro
st.set_page_config(page_title="RainClub V18.0 - Greenhouse Edition", page_icon="🏠", layout="wide")

# --- BASES DE DATOS DE CULTIVOS ---
cultivos_aire_libre = {
    "-- Frutales --": 1.0, "Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Manzanos": 1.0, "Vides": 0.85, "Arándanos": 0.9,
    "-- Extensivos --": 1.0, "Maíz": 1.2, "Trigo": 1.0, "Papas": 1.1,
    "-- Forrajes --": 1.0, "Pradera Natural": 0.9, "Alfalfa": 1.15
}

cultivos_invernadero = {
    "-- Hortalizas --": 1.0, "Tomate Invernadero": 1.15, "Pimiento / Morrón": 1.1, "Pepino": 1.1, "Melón": 1.0, "Sandía": 1.0,
    "-- Flores --": 1.0, "Rosas": 0.9, "Claveles": 0.85, "Lilium": 0.9,
    "-- Verdes --": 1.0, "Lechuga Hidropónica": 1.0, "Espinaca": 1.0, "Frutilla Invernadero": 0.95
}

# --- BASE DE DATOS REGIONAL ---
chile_agro = {
    "Región del Maule": {"ET": 5.2}, "Región Metropolitana": {"ET": 5.8}, "Región de O'Higgins": {"ET": 5.5}
}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V18.0")
st.markdown("#### Gestión de Riego: Aire Libre e Invernaderos Tecnificados")
st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("📍 1. Ubicación")
reg_sel = st.sidebar.selectbox("Región", list(chile_agro.keys()))

st.sidebar.divider()
st.sidebar.header("🏠 2. Tipo de Instalación")
# BOTÓN CLAVE: Cambia toda la lógica de la App
es_invernadero = st.sidebar.checkbox("¿Cultiva en Invernadero?")

st.sidebar.divider()
st.sidebar.header("🌱 3. Selección de Cultivo")

if es_invernadero:
    st.sidebar.warning("🛠️ Modo Invernadero Activo")
    lista_actual = cultivos_invernadero
else:
    lista_actual = cultivos_aire_libre

cultivo_usuario = st.sidebar.selectbox("¿Qué tiene plantado?", list(lista_actual.keys()))
kc_actual = lista_actual[cultivo_usuario]

st.sidebar.divider()
st.sidebar.header("🚜 4. Parámetros")
has = st.sidebar.number_input("Superficie (Hectáreas)", min_value=0.01, value=1.0, step=0.1)

# Lógica de Marco de Plantación
es_cobertura_total = "Pradera" in cultivo_usuario or "Alfalfa" in cultivo_usuario or "Hidropónica" in cultivo_usuario

if not es_cobertura_total:
    dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=3.0 if es_invernadero else 4.0)
    dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=0.5 if es_invernadero else 2.0)
    pl_total = (10000 / (dist_h * dist_p)) * has
else:
    pl_total = 1

sistema = st.sidebar.selectbox("Riego", ["Goteo", "Microaspersión", "Nebulización (Invernadero)"])

# --- LÓGICA DE CÁLCULO ---
et_base = chile_agro[reg_sel]["ET"]
# En invernadero la ET es menor (un 70% de la exterior aprox) pero el Kc es mayor por la intensidad
etc_final = (et_base * 0.7 * kc_actual) if es_invernadero else (et_base * kc_actual)

efi = 0.95 if "Goteo" in sistema or "Nebulización" in sistema else 0.85
vol_m3 = (etc_final / efi) * 10 * has
l_dia = vol_m3 * 1000
min_riego = (vol_m3 / (2.5 * has)) * 60 # Caudal más alto en invernaderos

# --- RESULTADOS ---
st.subheader(f"📊 Reporte: {cultivo_usuario} " + ("(Ambiente Controlado)" if es_invernadero else "(Aire Libre)"))

if "--" in cultivo_usuario:
    st.error("Por favor, seleccione un cultivo específico.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Agua Diaria", f"{l_dia:,.0f} L")
    c2.metric("Tiempo Riego", f"{int(min_riego)} min")
    c3.metric("Kc Ajustado", f"{kc_actual}")
    c4.metric("Tipo", "Invernadero" if es_invernadero else "Cielo Abierto")

# --- SECCIÓN PRO ---
st.write("---")
col_pro, col_pago = st.columns(2)
with col_pro:
    st.info("### 💎 Beneficios Pro")
    if st.button("🔔 Simular Alerta de Humedad"):
        st.toast("Verificando sensores del invernadero...")
        time.sleep(1)
        st.success(f"✅ Alerta: Nivel de humedad óptimo para su {cultivo_usuario}.")
with col_pago:
    st.warning("### 💳 Suscripción")
    st.write("Costo: $15.000/mes. 40% de comisión para el desarrollador.")
    st.button("Activar RainClub Pro")

st.info("RainClub V18.0 - La App más versátil para el agro chileno.")
