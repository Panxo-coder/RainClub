import streamlit as st
import time

# Configuración de nivel Consultoría Agronómica
st.set_page_config(page_title="RainClub V25.0 - Agronomy Suite", page_icon="🚜", layout="wide")

# --- 1. INTELIGENCIA AGRONÓMICA (BASES DE DATOS) ---

# Fertilización recomendada por cultivo (N-P-K y Microelementos)
dict_nutricion = {
    "Cerezos": "Nitrógeno para crecimiento, Potasio en pinta. Calcio para evitar partiduras.",
    "Nogales": "Nitrógeno en primavera. Zinc y Boro para mejorar el llenado de la nuez.",
    "Paltos": "Nitrógeno moderado. Hierro y Magnesio para evitar clorosis en hojas.",
    "Maíz": "Urea (Nitrógeno) en V4-V6. Fósforo a la siembra para raíz fuerte.",
    "Papas": "Alto Potasio para calibre de tubérculo. Fósforo para inicio de estolones.",
    "Alfalfa": "Principalmente Fósforo y Azufre. No requiere mucho Nitrógeno (lo fija sola).",
    "Tomate": "Potasio para sabor y color. Calcio vital para evitar 'pudrición apical'.",
    "Pradera": "Nitrógeno tras cada pastoreo para rebrote rápido. Azufre para calidad de proteína."
}

# Tipos de Suelo y su capacidad de retención
dict_suelos = {
    "Arcilloso (Pesado)": {"retencion": "Alta", "drenaje": "Lento", "ajuste_riego": 0.8},
    "Franco (Ideal)": {"retencion": "Media-Alta", "drenaje": "Bueno", "ajuste_riego": 1.0},
    "Arenoso (Ligero)": {"retencion": "Baja", "drenaje": "Muy rápido", "ajuste_riego": 1.3},
    "Franco-Arcilloso": {"retencion": "Alta", "drenaje": "Moderado", "ajuste_riego": 0.9}
}

# --- 2. INTERFAZ Y NAVEGACIÓN ---
st.title("🚜 RainClub: Gestión Agronómica Integral")
st.markdown("##### Asesoría Técnica Automatizada para el Agricultor Chileno")
st.write("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📍 Configuración del Predio")
    reg = st.selectbox("Región", ["Maule", "Metropolitana", "O'Higgins", "Araucanía", "Coquimbo"])
    has = st.number_input("Hectáreas totales", min_value=0.1, value=1.0)
    
    st.divider()
    st.header("🌱 Información del Cultivo")
    es_inv = st.checkbox("Cultivo en Invernadero")
    tipo_cultivo = st.selectbox("Cultivo", list(dict_nutricion.keys()))
    
    st.divider()
    st.header("🧪 Edafología (Suelo)")
    suelo_sel = st.selectbox("Tipo de Suelo", list(dict_suelos.keys()))
    
    st.divider()
    st.header("💧 Sistema de Riego")
    sistema = st.selectbox("Método", ["Goteo", "Microaspersión", "Surcos", "Aspersión"])

# --- 3. LÓGICA DE MARCO DE PLANTACIÓN ---
# Si no es pradera, calculamos densidades
es_pradera = "Pradera" in tipo_cultivo or "Alfalfa" in tipo_cultivo

st.subheader(f"📋 Ficha Técnica: {tipo_cultivo}")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.info("### 📐 Marco de Plantación")
    if not es_pradera:
        d_h = st.number_input("Distancia Hileras (m)", value=4.0, step=0.5)
        d_p = st.number_input("Distancia Plantas (m)", value=2.0, step=0.5)
        densidad = (10000 / (d_h * d_p)) * has
        st.write(f"**Densidad:** {int(densidad)} plantas totales.")
    else:
        st.write("**Siembra:** Cobertura Total (Voleo/Líneas juntas).")
        st.write("**Dosis semilla:** 25-35 kg/ha aprox.")

with col_m2:
    st.info("### 🧪 Suelo y Nutrición")
    info_s = dict_suelos[suelo_sel]
    st.write(f"**Suelo:** {suelo_sel}")
    st.write(f"**Drenaje:** {info_s['drenaje']}")
    st.write(f"**Recomendación:** {dict_nutricion[tipo_cultivo]}")

with col_m3:
    st.info("### ⛅ Clima y Riego")
    et_base = 5.2 # Valor base Maule
    ajuste_suelo = info_s['ajuste_riego']
    etc = et_base * 1.1 * ajuste_suelo # Simplificado
    st.write(f"**Evapotranspiración:** {etc:.2f} mm/día")
    st.write(f"**Estado Tiempo:** Despejado / 24°C")

# --- 4. PLAN DE ACCIÓN DEL TÉCNICO (EL "QUE HACER") ---
st.write("---")
st.subheader("📅 Calendario de Actividades Mensual")

t1, t2, t3 = st.tabs(["💧 Riego y Agua", "💊 Fertilización", "🛡️ Sanidad y Poda"])

with t1:
    vol_dia = (etc / 0.9) * 10 * has
    st.metric("Volumen diario sugerido", f"{vol_dia:,.0f} Litros")
    st.write(f"**Frecuencia:** En suelo {suelo_sel}, se recomienda regar cada " + ("1 día" if "Arenoso" in suelo_sel else "3 días") + ".")

with t2:
    st.write(f"### Plan de Abonado para {tipo_cultivo}")
    st.success(f"**Fertilizantes sugeridos:** {dict_nutricion[tipo_cultivo]}")
    st.write("- **Fondo:** Aplicar Fósforo y Potasio antes de la brotación.")
    st.write("- **Mantención:** Nitrógeno fraccionado vía fertirriego.")

with t3:
    st.write("### Monitoreo Técnico")
    st.warning("⚠️ **Alerta:** Revisar presencia de Arañita Roja y Pulgones esta semana por altas temperaturas.")
    st.write("- Realizar poda de formación en ramas bajas.")
    st.write("- Revisar sellado de cortes con pasta podadora.")

# --- SECCIÓN PRO ---
st.write("---")
if st.button("💎 Generar Informe PDF Profesional (Versión Pro)"):
    st.toast("Generando reporte agronómico...")
    time.sleep(1)
    st.success("Informe generado con éxito. Suscríbete para descargar.")

st.caption("RainClub V25.0 - La Suite Agronómica más potente del Maule.")
