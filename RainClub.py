import streamlit as st
import time

# Configuración de Ingeniería Agronómica Superior
st.set_page_config(page_title="RainClub V26.0 - Master Agro", page_icon="🚜", layout="wide")

# --- 1. BASES DE DATOS TÉCNICAS ---
# Kc (Coeficiente de cultivo)
dict_cultivos = {
    "Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Manzanos": 1.0, "Vides": 0.85,
    "Maíz": 1.2, "Alfalfa": 1.15, "Papas": 1.1, "Tomates": 1.15, "Praderas": 1.0
}

# Tipos de Suelo (Capacidad de Retención de Humedad)
dict_suelos = {
    "Suelo Arenoso (Ligero)": {"frecuencia": 1, "retencion": 0.7, "desc": "Baja retención. Requiere riegos cortos y frecuentes."},
    "Suelo Franco (Ideal)": {"frecuencia": 3, "retencion": 1.0, "desc": "Equilibrio perfecto. Riegos cada 3 días aprox."},
    "Suelo Arcilloso (Pesado)": {"frecuencia": 5, "retencion": 1.3, "desc": "Mucha retención. Riegos abundantes pero distanciados."}
}

# Nutrición Base
dict_nutricion = {
    "Cerezos": "Fósforo al inicio, Potasio en maduración y Calcio para la firmeza.",
    "Nogales": "Zinc y Nitrógeno para el llenado del fruto.",
    "Alfalfa": "Fósforo y Potasio. El Nitrógeno es bajo (lo fija el cultivo).",
    "Maíz": "Urea (Nitrógeno) en etapas V4 y V6."
}

# --- 2. INTERFAZ ---
st.title("🚜 RainClub: Consultoría Técnica Integral")
st.markdown("##### Del Maule para el mundo - Inteligencia Agronómica V26.0")
st.write("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📍 1. Localización y Suelo")
    comuna = st.text_input("Comuna / Sector", "Linares")
    tipo_suelo = st.selectbox("Seleccione su tipo de suelo", list(dict_suelos.keys()))
    
    st.divider()
    st.header("🌱 2. Información del Cultivo")
    cultivo_sel = st.selectbox("Cultivo", list(dict_cultivos.keys()))
    has = st.number_input("Superficie (Hectáreas)", min_value=0.1, value=1.0)
    
    st.divider()
    st.header("💧 3. Sistema de Riego")
    sistema = st.selectbox("Método de Riego", ["Goteo (95% Efic.)", "Microaspersión (85% Efic.)", "Aspersión (75% Efic.)", "Surcos (50% Efic.)"])

# --- 3. LÓGICA DE INGENIERÍA DE RIEGO (CORREGIDA) ---
et_base = 5.5 # ET0 promedio zona central en verano
kc = dict_cultivos[cultivo_sel]
suelo_info = dict_suelos[tipo_suelo]

# Cálculo de Necesidad Neta (mm/día)
necesidad_mm_dia = et_base * kc

# Frecuencia según suelo
dias_frecuencia = suelo_info["frecuencia"]

# Agua total a reponer en el ciclo de riego (mm)
lamina_a_reponer = necesidad_mm_dia * dias_frecuencia

# Eficiencia según sistema
efi = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else 0.50)

# Volumen Total en Litros para la superficie
litros_totales_ciclo = (lamina_a_reponer / efi) * 10 * has * 1000

# CORRECCIÓN DE HORAS: Caudal promedio real por sistema (L/hora/ha)
# Un sistema de goteo suele entregar entre 40,000 y 60,000 L/hora por hectárea
caudal_hora_ha = 45000 if "Goteo" in sistema else (80000 if "Micro" in sistema else 150000)
horas_riego_total = litros_totales_ciclo / (caudal_hora_ha * has)

# --- 4. VISUALIZACIÓN DE RESULTADOS ---
st.subheader(f"📋 Diagnóstico Técnico para {cultivo_sel} en {comuna}")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Frecuencia de Riego", f"Cada {dias_frecuencia} días")
    st.write(f"**Nota Suelo:** {suelo_info['desc']}")
with c2:
    st.metric("Litros por Turno", f"{litros_totales_ciclo:,.0f} L")
    st.write(f"**Superficie:** {has} Hectáreas")
with c3:
    # Mostramos minutos si es menos de una hora, o horas si es más
    if horas_riego_total < 1:
        st.metric("Tiempo de Riego", f"{int(horas_riego_total * 60)} min")
    else:
        st.metric("Tiempo de Riego", f"{horas_riego_total:.1f} Horas")
    st.write(f"**Eficiencia:** {int(efi*100)}% ({sistema})")

# --- 5. CALENDARIO Y RECOMENDACIONES ---
st.write("---")
col_info, col_cal = st.columns([1, 2])

with col_info:
    st.info("### 💊 Plan de Nutrición")
    st.write(dict_nutricion.get(cultivo_sel, "Aplicar fertilización base N-P-K según análisis de suelo."))
    
    st.warning("### 🛡️ Sanidad Vegetal")
    st.write("- Revisar envés de las hojas por posibles ácaros.")
    st.write("- Aplicar fungicida preventivo si la humedad relativa sube del 70%.")

with col_cal:
    st.success("### 📅 Calendario Próximos 7 Días")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for d in dias:
        # Lógica simple: si el día es múltiplo de la frecuencia, se riega
        indice = dias.index(d)
        if indice % dias_frecuencia == 0:
            st.write(f"✅ **{d}:** Toca Riego ({int(horas_riego_total*60)} min)")
        else:
            st.write(f"⚪ **{d}:** Descanso (Suelo con humedad)")

# --- MODO PREMIUM ---
st.write("---")
if st.button("💎 Activar RainClub PRO (Gestión 360°)"):
    st.balloons()
    st.write("### 🎁 Beneficios Pro Activados (Simulación):")
    st.write("- Conexión directa a Estaciones Meteorológicas AGROMET.")
    st.write("- Registro de aplicaciones de agroquímicos (SAG).")
    st.write("- Predicción de cosecha y rentabilidad.")
