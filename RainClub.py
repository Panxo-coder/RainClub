import streamlit as st
import time

# Configuración de Software de Clase Mundial
st.set_page_config(page_title="RainClub Chile V17.0", page_icon="🇨🇱", layout="wide")

# --- BASE DE DATOS EXTENSA DE CULTIVOS (Kc) ---
# Clasificados por categoría para orden técnico
dict_cultivos = {
    "-- Frutales Mayores --": 1.0,
    "Cerezos": 1.1,
    "Nogales": 1.05,
    "Paltos": 0.85,
    "Cítricos (Limón/Naranja/Mandarina)": 0.75,
    "Manzanos": 1.0,
    "Perales": 1.0,
    "Olivos": 0.7,
    "Vides de Mesa": 0.85,
    "Vides para Vinificación": 0.75,
    "Almendros": 0.9,
    "-- Berries y Frutales Menores --": 1.0,
    "Arándanos": 0.9,
    "Frambuesas": 0.95,
    "Frutillas": 0.85,
    "Moras / Zarzaparrilla": 0.9,
    "-- Hortalizas y Cultivos Anuales --": 1.0,
    "Tomates": 1.05,
    "Lechugas": 1.0,
    "Cebollas": 1.0,
    "Papas": 1.1,
    "Maíz": 1.2,
    "Remolacha": 1.15,
    "Trigo / Cebada": 1.0,
    "-- Forrajes y Praderas (Siembra Directa) --": 1.0,
    "Praderas Naturales": 0.9,
    "Praderas de Trébol/Ballica": 1.05,
    "Alfalfa": 1.15
}

# --- BASE DE DATOS REGIONAL ---
chile_agro = {
    "Región del Maule": {"Provincias": {"Linares": ["Linares", "Yerbas Buenas", "Longaví"], "Talca": ["Talca", "San Clemente"]}, "ET": 5.2},
    "Región Metropolitana": {"Provincias": {"Santiago": ["Santiago", "Maipú"], "Maipo": ["Buin", "Paine"]}, "ET": 5.8},
    "Región de O'Higgins": {"Provincias": {"Cachapoal": ["Rancagua", "Rengo"], "Colchagua": ["San Fernando", "Santa Cruz"]}, "ET": 5.5}
}

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V17.0")
st.markdown("#### Catálogo Nacional de Cultivos y Gestión de Precisión")
st.write("---")

# --- PANEL LATERAL (CONFIGURACIÓN) ---
st.sidebar.header("📍 1. Ubicación")
reg_sel = st.sidebar.selectbox("Región", list(chile_agro.keys()))
prov_sel = st.sidebar.selectbox("Provincia", list(chile_agro[reg_sel]["Provincias"].keys()))
comu_sel = st.sidebar.selectbox("Comuna", chile_agro[reg_sel]["Provincias"][prov_sel])

st.sidebar.divider()
st.sidebar.header("🌱 2. Selección de Cultivo")
cultivo_usuario = st.sidebar.selectbox("¿Qué tiene plantado?", list(dict_cultivos.keys()))
kc_actual = dict_cultivos[cultivo_usuario]

st.sidebar.divider()
st.sidebar.header("🚜 3. Parámetros del Predio")
has = st.sidebar.number_input("Superficie Total (Hectáreas)", min_value=0.1, value=1.0)

# --- LÓGICA DE INTERFAZ INTELIGENTE ---
# Si es pradera o forraje, no pedimos marco de plantación
es_pradera = "Pradera" in cultivo_usuario or "Alfalfa" in cultivo_usuario

if not es_pradera:
    dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=4.0)
    dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=2.0)
    pl_total = (10000 / (dist_h * dist_p)) * has
else:
    st.sidebar.info("💡 Cultivo de cobertura total. Cálculo basado en superficie.")
    pl_total = 1 # Para las praderas el cálculo se hace por superficie, no por individuo

sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo (95%)", "Microaspersión (85%)", "Aspersión (75%)", "Tendida/Inundación (50%)"])

# --- LÓGICA DE CÁLCULO FAO-56 ---
et_base = chile_agro[reg_sel]["ET"]
etc_ajustada = et_base * kc_actual 
efi = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else (0.75 if "Aspersión" in sistema else 0.50))

# Cálculo de volumen: m3 = (Lámina / Eficiencia) * Superficie
# 1 mm = 10 m3 por hectárea
volumen_m3 = (etc_ajustada / efi) * 10 * has
litros_totales = volumen_m3 * 1000

# Tiempo estimado de riego (Asumiendo caudal estándar de 2.0 m3/hr por hectárea)
minutos_riego = (volumen_m3 / (2.0 * has)) * 60

# --- RESULTADOS ---
st.subheader(f"📊 Reporte Técnico: {cultivo_usuario}")
if "--" in cultivo_usuario:
    st.warning("Seleccione un cultivo válido del listado.")
else:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Agua Necesaria", f"{litros_totales:,.0f} L/día")
    with c2:
        st.metric("Tiempo Estimado", f"{int(minutos_riego)} min")
    with c3:
        if es_pradera:
            st.metric("Cobertura", "100%", delta="Siembra Directa")
        else:
            st.metric("Población", f"{int(pl_total)} pl")
    with c4:
        st.metric("Kc Aplicado", f"{kc_actual}")

# --- SECCIÓN ESTRATÉGICA ---
st.write("---")
t1, t2, t3 = st.tabs(["💎 Plan Pro", "💳 Suscripción", "📱 App Móvil"])

with t1:
    st.write("### Servicios Avanzados")
    if st.button("🔔 Simular Alerta de Riego"):
        st.toast("Calculando balance hídrico...")
        time.sleep(1)
        st.success(f"✅ Notificación enviada: 'Hora de regar su {cultivo_usuario} en {comu_sel}.'")

with t2:
    st.write("#### Activar Cuenta Pro")
    st.button("💳 Pagar $15.000 / mes")
    st.caption("Comisión para el desarrollador: 40% del valor neto.")

with t3:
    st.info("Para usar como App: Abre el menú de tu navegador y selecciona 'Agregar a pantalla de inicio'.")

st.info("RainClub V17.0 - La plataforma más completa de riego en Chile.")
