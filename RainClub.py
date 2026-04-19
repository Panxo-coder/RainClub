import streamlit as st
import time

# Configuración de Software Agronómico Profesional
st.set_page_config(page_title="AgroMind 360 - Gestión Integral", page_icon="🚜", layout="wide")

# --- 1. BASE DE DATOS NACIONAL COMPLETA ---
chile_full = {
    "Arica y Parinacota": {"ET": 6.8, "Provincias": {"Arica": ["Arica", "Camarones"], "Parinacota": ["Putre", "General Lagos"]}},
    "Tarapacá": {"ET": 6.5, "Provincias": {"Iquique": ["Iquique", "Alto Hospicio"], "Tamarugal": ["Pica", "Huara"]}},
    "Antofagasta": {"ET": 6.2, "Provincias": {"Antofagasta": ["Antofagasta", "Taltal"], "El Loa": ["Calama", "San Pedro"]}},
    "Atacama": {"ET": 6.0, "Provincias": {"Copiapó": ["Copiapó", "Caldera"], "Huasco": ["Vallenar", "Huasco"]}},
    "Coquimbo": {"ET": 5.8, "Provincias": {"Elqui": ["La Serena", "Coquimbo", "Vicuña"], "Limarí": ["Ovalle", "Monte Patria"], "Choapa": ["Illapel", "Salamanca"]}},
    "Valparaíso": {"ET": 5.4, "Provincias": {"Valparaíso": ["Valparaíso", "Casablanca"], "Quillota": ["Quillota"], "San Felipe": ["San Felipe", "Putaendo"]}},
    "Metropolitana": {"ET": 5.6, "Provincias": {"Santiago": ["Santiago", "Maipú", "Pudahuel"], "Maipo": ["San Bernardo", "Buin", "Paine"], "Chacabuco": ["Colina", "Lampa"]}},
    "O'Higgins": {"ET": 5.4, "Provincias": {"Cachapoal": ["Rancagua", "Machalí", "Rengo"], "Colchagua": ["San Fernando", "Santa Cruz"], "Cardenal Caro": ["Pichilemu", "Marchigüe"]}},
    "Maule": {"ET": 5.2, "Provincias": {"Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"], "Talca": ["Talca", "Maule", "San Clemente"], "Curicó": ["Curicó", "Molina", "Teno"], "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]}},
    "Ñuble": {"ET": 4.8, "Provincias": {"Diguillín": ["Chillán", "Bulnes"], "Itata": ["Quirihue"], "Punilla": ["San Carlos"]}},
    "Biobío": {"ET": 4.5, "Provincias": {"Concepción": ["Concepción", "Coronel"], "Biobío": ["Los Ángeles"], "Arauco": ["Cañete"]}},
    "La Araucanía": {"ET": 4.0, "Provincias": {"Cautín": ["Temuco", "Villarrica", "Pucón"], "Malleco": ["Angol", "Victoria"]}},
    "Los Ríos": {"ET": 3.5, "Provincias": {"Valdivia": ["Valdivia"], "Ranco": ["La Unión"]}},
    "Los Lagos": {"ET": 3.2, "Provincias": {"Llanquihue": ["Puerto Montt", "Puerto Varas"], "Osorno": ["Osorno"], "Chiloé": ["Castro"]}},
    "Aysén": {"ET": 2.5, "Provincias": {"Coyhaique": ["Coyhaique"], "Aysén": ["Aysén"]}},
    "Magallanes": {"ET": 2.0, "Provincias": {"Magallanes": ["Punta Arenas"], "Última Esperanza": ["Puerto Natales"]}}
}

# --- 2. CONFIGURACIÓN TÉCNICA Y DICCIONARIOS ---
dict_riego = {"Goteo": 0.95, "Microaspersión": 0.85, "Aspersión": 0.75, "Surcos": 0.50}
caudal_diseno = {"Goteo": 45000, "Microaspersión": 75000, "Aspersión": 120000, "Surcos": 180000}

cultivos_aire = {
    "Cerezos": {"kc": 1.1, "nut": "Calcio para firmeza y Potasio en pinta."},
    "Nogales": {"kc": 1.05, "nut": "Zinc y Nitrógeno para llenado de nuez."},
    "Paltos": {"kc": 0.85, "nut": "Hierro para evitar clorosis."},
    "Vides": {"kc": 0.85, "nut": "Magnesio y Potasio para azúcar."},
    "Maíz": {"kc": 1.2, "nut": "Urea (Nitrógeno) en etapas V4-V6."},
    "Alfalfa": {"kc": 1.15, "nut": "Fósforo y Azufre para proteína."},
    "Papas": {"kc": 1.1, "nut": "Potasio alto para calibre de tubérculo."},
    "Pradera": {"kc": 1.05, "nut": "Nitrógeno tras cada pastoreo."}
}

cultivos_inv = {
    "Tomate": {"kc": 1.15, "nut": "Calcio para evitar pudrición apical."},
    "Pimiento": {"kc": 1.1, "nut": "Potasio para grosor de pared."},
    "Pepino": {"kc": 1.1, "nut": "Nitrógeno constante y mucha agua."},
    "Lechuga Hidropónica": {"kc": 1.0, "nut": "Solución nutritiva balanceada."}
}

dict_suelos = {
    "Suelo Arenoso": {"frecuencia": 1, "desc": "Textura gruesa. Poca retención. Riegos diarios cortos."},
    "Suelo Franco": {"frecuencia": 3, "desc": "Textura ideal. Retención equilibrada. Riego cada 3 días."},
    "Suelo Arcilloso": {"frecuencia": 5, "desc": "Textura fina. Alta retención. Riegos largos pero distanciados."}
}

# --- 3. INTERFAZ ---
st.title("🚜 AgroMind 360")
st.markdown("#### Inteligencia Agronómica Integral | Maule - Chile")
st.write("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📍 1. Ubicación")
    reg_sel = st.selectbox("Región", list(chile_full.keys()), index=8) # Default Maule
    prov_sel = st.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
    comu_sel = st.selectbox("Comuna", chile_full[reg_sel]["Provincias"][prov_sel])
    
    st.divider()
    st.header("🧪 2. Edafología")
    suelo_sel = st.selectbox("Tipo de Suelo", list(dict_suelos.keys()), index=1)
    
    st.divider()
    st.header("🌱 3. Manejo y Cultivo")
    es_inv = st.checkbox("Cultivo en Invernadero")
    lista_actual = cultivos_inv if es_inv else cultivos_aire
    cultivo_sel = st.selectbox("Especie", list(lista_actual.keys()))
    has = st.number_input("Hectáreas (ha)", min_value=0.1, value=1.0, step=0.1)
    
    st.divider()
    st.header("💧 4. Riego")
    sistema_sel = st.selectbox("Sistema de Riego", list(dict_riego.keys()))

# --- 4. LÓGICA DE INGENIERÍA ---
et_base = chile_full[reg_sel]["ET"]
kc = lista_actual[cultivo_sel]["kc"]
frecuencia = dict_suelos[suelo_sel]["frecuencia"]
efi = dict_riego[sistema_sel]

# Cálculo de Evapotranspiración Real (ETc)
# Si es invernadero, se reduce la ET base un 25% por falta de viento/radiación directa
etc = (et_base * 0.75 * kc) if es_inv else (et_base * kc)

# Agua a reponer por cada turno de riego (según frecuencia del suelo)
lamina_turno = (etc * frecuencia) / efi
litros_turno = lamina_turno * 10 * has * 1000

# Cálculo de horas (Corregido para no exceder el día)
# Caudal total disponible = Caudal ha * número de hectáreas
horas_riego = litros_turno / (caudal_diseno[sistema_sel] * has)

# --- 5. RESULTADOS PRINCIPALES ---
st.subheader(f"📊 Reporte AgroMind: {comu_sel}, {reg_sel}")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Frecuencia", f"Cada {frecuencia} días")
c2.metric("Agua por Turno", f"{litros_turno:,.0f} L")
if horas_riego < 1:
    c3.metric("Tiempo de Riego", f"{int(horas_riego*60)} min")
else:
    c3.metric("Tiempo de Riego", f"{horas_riego:.1f} Horas")
c4.metric("Kc (Coeficiente)", f"{kc}")

st.info(f"💡 **Nota Técnica del Suelo:** {dict_suelos[suelo_sel]['desc']}")

# --- 6. CALENDARIO Y ASESORÍA TÉCNICA ---
st.write("---")
col_cal, col_nut = st.columns([2, 1])

with col_cal:
    st.success("📅 Calendario Semanal Sugerido")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d in enumerate(dias):
        if i % frecuencia == 0:
            tiempo_str = f"{int(horas_riego*60)} min" if horas_riego < 1 else f"{horas_riego:.1f} h"
            st.write(f"💧 **{d}:** Toca Riego - Operar por **{tiempo_str}**.")
        else:
            st.write(f"⚪ **{d}:** Descanso - El suelo mantiene humedad.")

with col_nut:
    st.warning("💊 Nutrición y Sanidad")
    st.write(f"**Recomendación para {cultivo_sel}:**")
    st.write(f"- {lista_actual[cultivo_sel]['nut']}")
    st.write("- Monitorear presencia de plagas cada 3 días.")
    st.write("- Revisar uniformidad de los emisores de riego.")

# --- MODO PRO / NEGOCIO ---
st.divider()
if st.button("💎 Generar Informe Técnico PRO"):
    st.balloons()
    st.write("### 🚀 AgroMind PRO Activado")
    st.write("- Conexión con estaciones meteorológicas locales.")
    st.write("- Predicción de cosechas mediante IA.")
    st.write("- Gestión de costos y mano de obra.")
    st.caption("Suscripción disponible para el lanzamiento en SabíaLab.")
