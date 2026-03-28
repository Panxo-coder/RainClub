import streamlit as st
import time

# Configuración de Ingeniería Agrícola
st.set_page_config(page_title="RainClub V19.0 - Master Irrigation", page_icon="💧", layout="wide")

# --- BASE DE DATOS DE SISTEMAS DE RIEGO (Eficiencia Real) ---
dict_riego = {
    "-- Sistemas de Alta Eficiencia (Tecnificados) --": 0.95,
    "Riego por Goteo (Estándar)": 0.95,
    "Riego por Goteo Subsuperficial": 0.98,
    "Microaspersión": 0.85,
    "Microjets": 0.85,
    "Nebulización (Invernaderos)": 0.90,
    "-- Sistemas de Aspersión --": 0.80,
    "Aspersión Fija": 0.75,
    "Aspersión Móvil (Carros)": 0.70,
    "Pivote Central": 0.85,
    "Side Roll (Ala de riego)": 0.80,
    "-- Sistemas de Superficie (Tradicionales) --": 0.50,
    "Riego por Surcos (Bien nivelado)": 0.60,
    "Riego por Surcos (Tradicional)": 0.45,
    "Riego por Tendida (Inundación)": 0.35,
    "Riego por Bordes / Tazas": 0.55,
    "Riego por Califas": 0.50
}

# --- BASES DE DATOS DE CULTIVOS ---
cultivos_aire_libre = {
    "Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Manzanos": 1.0, "Vides": 0.85, "Arándanos": 0.9,
    "Maíz": 1.2, "Trigo": 1.0, "Papas": 1.1, "Pradera Natural": 0.9, "Alfalfa": 1.15, "Olivos": 0.7
}

cultivos_invernadero = {
    "Tomate Invernadero": 1.15, "Pimiento / Morrón": 1.1, "Pepino": 1.1, "Rosas": 0.9, 
    "Lechuga Hidropónica": 1.0, "Frutilla Invernadero": 0.95
}

# --- BASE DE DATOS REGIONAL ---
chile_agro = {"Región del Maule": {"ET": 5.2}, "Región Metropolitana": {"ET": 5.8}, "Región de O'Higgins": {"ET": 5.5}}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V19.0")
st.markdown("#### Plataforma Global de Gestión Hídrica y Eficiencia de Riego")
st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("📍 1. Ubicación")
reg_sel = st.sidebar.selectbox("Región", list(chile_agro.keys()))

st.sidebar.divider()
st.sidebar.header("🏠 2. Instalación")
es_invernadero = st.sidebar.checkbox("¿Cultiva en Invernadero?")

st.sidebar.divider()
st.sidebar.header("🌱 3. Selección de Cultivo")
lista_actual = cultivos_invernadero if es_invernadero else cultivos_aire_libre
cultivo_usuario = st.sidebar.selectbox("Cultivo", list(lista_actual.keys()))
kc_actual = lista_actual[cultivo_usuario]

st.sidebar.divider()
st.sidebar.header("💦 4. Sistema de Riego")
# AQUÍ ESTÁ EL CATÁLOGO MAESTRO QUE PEDISTE
sistema_sel = st.sidebar.selectbox("Tipo de Riego Utilizado", list(dict_riego.keys()))
efi_sel = dict_riego[sistema_sel]

st.sidebar.divider()
st.sidebar.header("🚜 5. Parámetros")
has = st.sidebar.number_input("Superficie (Hectáreas)", min_value=0.01, value=1.0, step=0.1)

# Lógica de población
es_cobertura_total = "Pradera" in cultivo_usuario or "Alfalfa" in cultivo_usuario or "Hidropónica" in cultivo_usuario
if not es_cobertura_total:
    dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=4.0)
    dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=2.0)
    pl_total = (10000 / (dist_h * dist_p)) * has
else:
    pl_total = 1

# --- CÁLCULO DE INGENIERÍA ---
et_base = chile_agro[reg_sel]["ET"]
etc_final = (et_base * 0.7 * kc_actual) if es_invernadero else (et_base * kc_actual)

# La eficiencia castiga o premia el volumen final
# Un riego por tendida (35%) requiere casi 3 veces más agua que un goteo (95%)
vol_m3 = (etc_final / efi_sel) * 10 * has
l_dia = vol_m3 * 1000
# Tiempo de riego referencial según el sistema
caudal_ref = 2.0 if efi_sel > 0.8 else (5.0 if efi_sel > 0.6 else 15.0)
min_riego = (vol_m3 / (caudal_ref * has)) * 60

# --- RESULTADOS ---
st.subheader(f"📊 Análisis Técnico: {cultivo_usuario} vía {sistema_sel}")

if "--" in sistema_sel:
    st.error("Seleccione un sistema de riego válido.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Agua Necesaria", f"{l_dia:,.0f} L/día")
    c2.metric("Tiempo Estimado", f"{int(min_riego)} min")
    c3.metric("Eficiencia", f"{int(efi_sel*100)}%", delta="Sistema" if efi_sel > 0.8 else "Baja", delta_color="normal")
