import streamlit as st
import time

# Configuración de Software Agronómico Profesional
st.set_page_config(page_title="RainClub V28.0 - Full Master", page_icon="💧", layout="wide")

# --- 1. BASE DE DATOS NACIONAL COMPLETA (PROTEGIDA) ---
chile_full = {
    "Arica y Parinacota": {"ET": 6.8, "Provincias": {"Arica": ["Arica", "Camarones"], "Parinacota": ["Putre", "General Lagos"]}},
    "Tarapacá": {"ET": 6.5, "Provincias": {"Iquique": ["Iquique", "Alto Hospicio"], "Tamarugal": ["Pica", "Huara"]}},
    "Antofagasta": {"ET": 6.2, "Provincias": {"Antofagasta": ["Taltal"], "El Loa": ["Calama", "San Pedro"]}},
    "Atacama": {"ET": 6.0, "Provincias": {"Copiapó": ["Caldera"], "Huasco": ["Vallenar", "Huasco"]}},
    "Coquimbo": {"ET": 5.8, "Provincias": {"Elqui": ["La Serena", "Vicuña"], "Limarí": ["Ovalle"], "Choapa": ["Illapel"]}},
    "Valparaíso": {"ET": 5.4, "Provincias": {"Valparaíso": ["Casablanca"], "Quillota": ["Quillota"], "San Felipe": ["San Felipe"]}},
    "Metropolitana": {"ET": 5.6, "Provincias": {"Santiago": ["Maipú", "Pudahuel"], "Maipo": ["Buin", "Paine"], "Chacabuco": ["Colina", "Lampa"]}},
    "O'Higgins": {"ET": 5.4, "Provincias": {"Cachapoal": ["Rancagua", "Rengo"], "Colchagua": ["San Fernando", "Santa Cruz"], "Cardenal Caro": ["Pichilemu"]}},
    "Maule": {"ET": 5.2, "Provincias": {"Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"], "Talca": ["Talca", "Maule", "San Clemente"], "Curicó": ["Curicó", "Molina", "Teno"], "Cauquenes": ["Cauquenes", "Chanco"]}},
    "Ñuble": {"ET": 4.8, "Provincias": {"Diguillín": ["Chillán", "Bulnes"], "Itata": ["Quirihue"], "Punilla": ["San Carlos"]}},
    "Biobío": {"ET": 4.5, "Provincias": {"Concepción": ["Coronel"], "Biobío": ["Los Ángeles"], "Arauco": ["Cañete"]}},
    "La Araucanía": {"ET": 4.0, "Provincias": {"Cautín": ["Temuco", "Villarrica"], "Malleco": ["Angol", "Victoria"]}},
    "Los Ríos": {"ET": 3.5, "Provincias": {"Valdivia": ["Valdivia"], "Ranco": ["La Unión"]}},
    "Los Lagos": {"ET": 3.2, "Provincias": {"Llanquihue": ["Puerto Varas"], "Osorno": ["Osorno"], "Chiloé": ["Castro"]}},
    "Aysén": {"ET": 2.5, "Provincias": {"Coyhaique": ["Coyhaique"], "Aysén": ["Aysén"]}},
    "Magallanes": {"ET": 2.0, "Provincias": {"Magallanes": ["Punta Arenas"], "Última Esperanza": ["Puerto Natales"]}}
}

# --- 2. DICCIONARIOS TÉCNICOS ---
dict_riego = {"Goteo": 0.95, "Microaspersión": 0.85, "Aspersión": 0.75, "Surcos": 0.50}
caudal_diseno = {"Goteo": 45000, "Microaspersión": 75000, "Aspersión": 120000, "Surcos": 180000}

cultivos_aire = {"Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Vides": 0.85, "Maíz": 1.2, "Alfalfa": 1.15, "Papas": 1.1, "Pradera": 1.05}
cultivos_inv = {"Tomate": 1.15, "Pimiento": 1.1, "Pepino": 1.1, "Rosas": 0.9, "Lechuga Hidropónica": 1.0}

dict_suelos = {
    "Suelo Arenoso": {"frecuencia": 1, "desc": "Baja retención. Riegos cortos cada 1 día."},
    "Suelo Franco": {"frecuencia": 3, "desc": "Ideal. Riegos cada 3 días."},
    "Suelo Arcilloso": {"frecuencia": 5, "desc": "Alta retención. Riegos cada 5 días."}
}

# --- 3. INTERFAZ ---
st.title("💧 RainClub Chile V28.0")
st.markdown("### Sistema de Gestión Agronómica e Hídrica Integral")
st.write("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📍 1. Ubicación Geográfica")
    reg_sel = st.selectbox("Región", list(chile_full.keys()))
    prov_sel = st.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
    comu_sel = st.selectbox("Comuna", chile_full[reg_sel]["Provincias"][prov_sel])
    
    st.divider()
    st.header("🧪 2. Tipo de Suelo")
    suelo_sel = st.selectbox("Textura del Suelo", list(dict_suelos.keys()))
    
    st.divider()
    st.header("🏠 3. Entorno y Cultivo")
    es_inv = st.checkbox("Cultivo en Invernadero")
    lista_c = cultivos_inv if es_inv else cultivos_aire
    cultivo_sel = st.selectbox("Cultivo", list(lista_c.keys()))
    has = st.number_input("Hectáreas (ha)", min_value=0.1, value=1.0)
    
    st.divider()
    st.header("💧 4. Sistema de Riego")
    sistema_sel = st.selectbox("Método de Riego", list(dict_riego.keys()))

# --- 4. LÓGICA DE INGENIERÍA ---
et_reg = chile_full[reg_sel]["ET"]
kc = lista_c[cultivo_sel]
frecuencia = dict_suelos[suelo_sel]["frecuencia"]
efi = dict_riego[sistema_sel]

# Cálculo de necesidad hídrica por turno (Ingeniería de Riego)
# Ajuste invernadero (menos evaporación directa)
etc = (et_reg * 0.75 * kc) if es_inv else (et_reg * kc)
lamina_turno = (etc * frecuencia) / efi
litros_turno = lamina_turno * 10 * has * 1000
horas_riego = litros_turno / (caudal_diseno[sistema_sel] * has)

# --- 5. RESULTADOS ---
st.subheader(f"📊 Reporte Técnico: {comu_sel}, {reg_sel}")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Frecuencia", f"Cada {frecuencia} días")
col2.metric("Litros por Turno", f"{litros_turno:,.0f} L")
col3.metric("Tiempo de Riego", f"{int(horas_riego*60)} min" if horas_riego < 1 else f"{horas_riego:.1f} Horas")
col4.metric("Consumo Kc", f"{kc}")

st.info(f"💡 **Recomendación del Técnico:** {dict_suelos[suelo_sel]['desc']}")

# --- 6. CALENDARIO Y NUTRICIÓN ---
st.write("---")
c_izq, c_der = st.columns([2, 1])

with c_izq:
    st.success("📅 Calendario Semanal de Riego")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d in enumerate(dias):
        if i % frecuencia == 0:
            st.write(f"✅ **{d}:** Toca Riego - Operar por **{int(horas_riego*60)} min**.")
        else:
            st.write(f"⚪ **{d}:** Descanso - Suelo con reserva.")

with c_der:
    st.warning("💊 Plan de Fertirriego")
    st.write(f"- **Cultivo:** {cultivo_sel}")
    if not es_inv:
        st.write("- **Marco sugerido:** Revisar densidad por hectárea.")
    st.write("- **Nota:** Aplicar Nitrógeno y Potasio según etapa de crecimiento.")

# --- MODO PRO ---
st.divider()
if st.button("💎 Activar Plan Pro Empresarial"):
    st.balloons()
    st.write("### Beneficios RainClub Pro ($15.000/mes)")
    st.write("- Alertas de Helada vía WhatsApp.")
    st.write("- Integración con sensores de humedad de suelo.")
    st.write("- Informe PDF para certificación Global GAP.")
