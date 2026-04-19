import streamlit as st
import time

# --- CONFIGURACIÓN DE NIVEL PROFESIONAL ---
st.set_page_config(page_title="AgroMind 360 - Full Precision", page_icon="🚜", layout="wide")

# --- 1. BASE DE DATOS GEOGRÁFICA COMPLETA ---
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

# --- 2. DICCIONARIOS TÉCNICOS ---
dict_suelos = {
    "Arenoso": {"frec": 1, "desc": "Textura gruesa, drenaje excesivo. Riegos diarios cortos."},
    "Arenoso Franco": {"frec": 1, "desc": "Predomina arena, muy baja retención."},
    "Franco Arenoso": {"frec": 2, "desc": "Drenaje rápido, requiere riegos frecuentes."},
    "Franco": {"frec": 3, "desc": "Textura equilibrada, retención óptima. Ideal."},
    "Franco Limoso": {"frec": 3, "desc": "Buena retención, cuidado con la compactación."},
    "Limoso": {"frec": 4, "desc": "Retención alta, riesgo de costra superficial."},
    "Franco Arcillo Arenoso": {"frec": 4, "desc": "Retención moderada-alta."},
    "Franco Arcillo Limoso": {"frec": 4, "desc": "Retención alta, drenaje algo lento."},
    "Franco Arcilloso": {"frec": 4, "desc": "Buena capacidad de campo, riego distanciado."},
    "Arcillo Arenoso": {"frec": 5, "desc": "Mucha arcilla, drenaje lento."},
    "Arcillo Limoso": {"frec": 5, "desc": "Muy pesado, riesgo de encharcamiento."},
    "Arcilloso": {"frec": 5, "desc": "Textura muy fina, alta retención. Riegos espaciados."}
}

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
    "Pepino": {"kc": 1.1, "dist_h": 1.2, "dist_p": 0.5, "nut": "Nitrógeno constante."},
    "Lechuga": {"kc": 1.0, "dist_h": 0.25, "dist_p": 0.25, "nut": "Nutrición balanceada."}
}

dict_riego = {"Goteo": 0.95, "Microaspersión": 0.85, "Aspersión": 0.75, "Surcos": 0.50}
caudal_diseno = {"Goteo": 45000, "Microaspersión": 75000, "Aspersión": 120000, "Surcos": 180000}

# --- 3. INTERFAZ ---
st.title("🚜 AgroMind 360")
st.markdown("#### Consultoría Agropecuaria de Precisión | Maule - Chile")
st.write("---")

with st.sidebar:
    st.header("📍 1. Localización y Suelo")
    reg_sel = st.selectbox("Región", list(chile_full.keys()), index=8)
    prov_sel = st.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
    comu_sel = st.selectbox("Comuna", chile_full[reg_sel]["Provincias"][prov_sel])
    suelo_sel = st.selectbox("Subtipo de Suelo (Textura)", list(dict_suelos.keys()), index=3)
    
    st.divider()
    st.header("🌱 2. Cultivo y Superficie")
    es_inv = st.checkbox("Cultivo en Invernadero")
    lista_actual = cultivos_inv if es_inv else cultivos_aire
    cultivo_sel = st.selectbox("Especie", list(lista_actual.keys()))
    has = st.number_input("Hectáreas (ha)", min_value=0.1, value=1.0, step=0.1)
    
    st.subheader("📐 Marco de Plantación")
    dist_h = st.number_input("Hileras (m)", value=lista_actual[cultivo_sel]["dist_h"], step=0.1)
    dist_p = st.number_input("Plantas (m)", value=lista_actual[cultivo_sel]["dist_p"], step=0.1)
    
    st.divider()
    st.header("💧 3. Sistema de Riego")
    sistema_sel = st.selectbox("Sistema", list(dict_riego.keys()))

# --- 4. LÓGICA DE INGENIERÍA ---
densidad_ha = 10000 / (dist_h * dist_p)
total_plantas = densidad_ha * has

et_base = chile_full[reg_sel]["ET"]
kc = lista_actual[cultivo_sel]["kc"]
frecuencia = dict_suelos[suelo_sel]["frec"]
efi = dict_riego[sistema_sel]

etc = (et_base * 0.75 * kc) if es_inv else (et_base * kc)
lamina_turno = (etc * frecuencia) / efi
litros_turno = lamina_turno * 10 * has * 1000
horas_riego = litros_turno / (caudal_diseno[sistema_sel] * has)

# --- 5. RESULTADOS ---
st.subheader(f"📊 Reporte de Ingeniería AgroMind: {comu_sel}")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Población Total", f"{int(total_plantas):,} pl.")
c2.metric("Turno de Riego", f"{litros_turno:,.0f} L")
c3.metric("Tiempo / Turno", f"{int(horas_riego*60)} min" if horas_riego < 1 else f"{horas_riego:.1f} h")
c4.metric("Frecuencia", f"Cada {frecuencia} días")

# --- 6. CALENDARIO Y NUTRICIÓN ---
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
            st.write(f"⚪ **{d}:** Descanso - Suelo con reserva.")

with col_nut:
    st.warning("💊 Nutrición y Sanidad")
    st.write(f"**Manejo para {cultivo_sel}:**")
    st.write(f"- {lista_actual[cultivo_sel]['nut']}")
    st.write(f"- Densidad: {int(densidad_ha)} plantas/ha.")
    st.info(f"📍 **Textura:** {dict_suelos[suelo_sel]['desc']}")

st.divider()
if st.button("💎 Generar Ficha AgroMind PRO"):
    st.balloons()
    st.write("Generando informe... Disponible en versión Pro.")
