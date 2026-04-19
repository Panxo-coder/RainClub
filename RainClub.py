import streamlit as st
import time

# --- CONFIGURACIÓN DE NIVEL PROFESIONAL ---
st.set_page_config(page_title="AgroMind 360 - Gestión Integral", page_icon="🚜", layout="wide")

# --- 1. BASE DE DATOS GEOGRÁFICA COMPLETA (TODAS LAS REGIONES) ---
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

# --- 2. DICCIONARIOS TÉCNICOS DE CULTIVOS (MARCOS Y NUTRICIÓN) ---
# Aquí están integrados los datos que antes ocupaban muchas líneas separadas
cultivos_aire = {
    "Cerezos": {"kc": 1.1, "dist_h": 4.5, "dist_p": 2.5, "nut": "Calcio para firmeza y Potasio en pinta."},
    "Nogales": {"kc": 1.05, "dist_h": 7.0, "dist_p": 5.0, "nut": "Zinc y Nitrógeno para llenado de nuez."},
    "Paltos": {"kc": 0.85, "dist_h": 6.0, "dist_p": 4.0, "nut": "Hierro para evitar clorosis."},
    "Vides": {"kc": 0.85, "dist_h": 3.0, "dist_p": 1.5, "nut": "Magnesio y Potasio para azúcar."},
    "Maíz": {"kc": 1.2, "dist_h": 0.7, "dist_p": 0.2, "nut": "Urea (Nitrógeno) en etapas V4-V6."},
    "Alfalfa": {"kc": 1.15, "dist_h": 0.2, "dist_p": 0.1, "nut": "Fósforo y Azufre para proteína."},
    "Papas": {"kc": 1.1, "dist_h": 0.75, "dist_p": 0.3, "nut": "Potasio alto para calibre de tubérculo."},
    "Pradera": {"kc": 1.05, "dist_h": 0.1, "dist_p": 0.1, "nut": "Nitrógeno tras cada pastoreo."}
}

cultivos_inv = {
    "Tomate": {"kc": 1.15, "dist_h": 1.0, "dist_p": 0.4, "nut": "Calcio para evitar pudrición apical."},
    "Pimiento": {"kc": 1.1, "dist_h": 0.8, "dist_p": 0.3, "nut": "Potasio para grosor de pared."},
    "Pepino": {"kc": 1.1, "dist_h": 1.2, "dist_p": 0.5, "nut": "Nitrógeno constante y mucha agua."},
    "Lechuga Hidropónica": {"kc": 1.0, "dist_h": 0.25, "dist_p": 0.25, "nut": "Solución nutritiva balanceada."}
}

dict_suelos = {
    "Suelo Arenoso": {"frecuencia": 1, "desc": "Poca retención. Riegos diarios cortos para evitar lavado de nutrientes."},
    "Suelo Franco": {"frecuencia": 3, "desc": "Textura ideal. Retención equilibrada. Riego cada 3 días."},
    "Suelo Arcilloso": {"frecuencia": 5, "desc": "Alta retención. Riegos distanciados para evitar asfixia radicular."}
}

dict_riego = {"Goteo": 0.95, "Microaspersión": 0.85, "Aspersión": 0.75, "Surcos": 0.50}
caudal_diseno = {"Goteo": 45000, "Microaspersión": 75000, "Aspersión": 120000, "Surcos": 180000}

# --- 3. INTERFAZ Y NAVEGACIÓN ---
st.title("🚜 AgroMind 360")
st.markdown("#### Inteligencia Agronómica Integral | Maule - Chile")
st.write("---")

with st.sidebar:
    st.header("📍 1. Ubicación y Suelo")
    reg_sel = st.selectbox("Región", list(chile_full.keys()), index=8) # Default Maule
    prov_sel = st.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
    comu_sel = st.selectbox("Comuna", chile_full[reg_sel]["Provincias"][prov_sel])
    suelo_sel = st.selectbox("Tipo de Suelo", list(dict_suelos.keys()), index=1)
    
    st.divider()
    st.header("🌱 2. Cultivo y Superficie")
    es_inv = st.checkbox("Cultivo en Invernadero")
    lista_actual = cultivos_inv if es_inv else cultivos_aire
    cultivo_sel = st.selectbox("Especie", list(lista_actual.keys()))
    has = st.number_input("Hectáreas Totales (ha)", min_value=0.1, value=1.0, step=0.1)
    
    st.subheader("📐 Marco de Plantación")
    dist_h = st.number_input("Hileras (m)", value=lista_actual[cultivo_sel]["dist_h"], step=0.1)
    dist_p = st.number_input("Plantas (m)", value=lista_actual[cultivo_sel]["dist_p"], step=0.1)
    
    st.divider()
    st.header("💧 3. Sistema de Riego")
    sistema_sel = st.selectbox("Sistema", list(dict_riego.keys()))

# --- 4. LÓGICA DE INGENIERÍA ---
# Cálculo de Densidad de Plantación
densidad_ha = 10000 / (dist_h * dist_p)
total_plantas = densidad_ha * has

# Lógica de Riego
et_base = chile_full[reg_sel]["ET"]
kc = lista_actual[cultivo_sel]["kc"]
frecuencia = dict_suelos[suelo_sel]["frecuencia"]
efi = dict_riego[sistema_sel]

# ETc ajustada (Invernadero reduce 25% la demanda hídrica directa)
etc = (et_base * 0.75 * kc) if es_inv else (et_base * kc)

# Litros a reponer según el ciclo (Frecuencia)
lamina_turno = (etc * frecuencia) / efi
litros_turno = lamina_turno * 10 * has * 1000

# Tiempo de riego corregido (Caudal del sistema x ha)
horas_riego = litros_turno / (caudal_diseno[sistema_sel] * has)

# --- 5. VISUALIZACIÓN DE RESULTADOS ---
st.subheader(f"📊 Reporte Técnico AgroMind: {comu_sel}")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Población Total", f"{int(total_plantas):,} pl.")
c2.metric("Turno de Riego", f"{litros_turno:,.0f} L")
c3.metric("Tiempo / Turno", f"{int(horas_riego*60)} min" if horas_riego < 1 else f"{horas_riego:.1f} h")
c4.metric("Frecuencia", f"Cada {frecuencia} días")

# --- 6. CALENDARIO Y ASESORÍA ---
st.write("---")
col_cal, col_nut = st.columns([2, 1])

with col_cal:
    st.success("📅 Calendario Semanal de Riego")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, d in enumerate(dias):
        if i % frecuencia == 0:
            t_str = f"{int(horas_riego*60)} min" if horas_riego < 1 else f"{horas_riego:.1f} h"
            st.write(f"💧 **{d}:** Toca Riego - Operar sistema por **{t_str}**.")
        else:
            st.write(f"⚪ **{d}:** Descanso - Suelo con reserva de humedad.")

with col_nut:
    st.warning("💊 Nutrición y Sanidad")
    st.write(f"**Recomendación Específica:**")
    st.write(f"- {lista_actual[cultivo_sel]['nut']}")
    st.write(f"- Densidad calculada: {int(densidad_ha)} plantas por ha.")
    st.write(f"**Análisis de Suelo:** {dict_suelos[suelo_sel]['desc']}")

# --- BOTÓN DE NEGOCIO ---
st.divider()
if st.button("💎 Generar Ficha Técnica AgroMind PRO"):
    st.balloons()
    st.write("Generando documento PDF... Esta función requiere suscripción activa.")
