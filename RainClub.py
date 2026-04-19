import streamlit as st
import time

# Configuración de Software Agronómico Profesional
st.set_page_config(page_title="AgroMind 360 - Gestión Integral", page_icon="🚜", layout="wide")

# --- 1. BASE DE DATOS GEOGRÁFICA (PROTEGIDA) ---
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

# --- 2. CONFIGURACIÓN TÉCNICA ---
dict_riego = {"Goteo": 0.95, "Microaspersión": 0.85, "Aspersión": 0.75, "Surcos": 0.50}
caudal_diseno = {"Goteo": 45000, "Microaspersión": 75000, "Aspersión": 120000, "Surcos": 180000}

cultivos_aire = {"Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Vides": 0.85, "Maíz": 1.2, "Alfalfa": 1.15, "Papas": 1.1, "Pradera": 1.05}
cultivos_inv = {"Tomate": 1.15, "Pimiento": 1.1, "Pepino": 1.1, "Rosas": 0.9, "Lechuga Hidropónica": 1.0}

dict_suelos = {
    "Suelo Arenoso": {"frecuencia": 1, "desc": "Textura gruesa. Riegos diarios cortos para evitar lixiviación."},
    "Suelo Franco": {"frecuencia": 3, "desc": "Textura ideal. Capacidad de retención equilibrada."},
    "Suelo Arcilloso": {"frecuencia": 5, "desc": "Textura fina. Alta retención, evitar saturación de raíces."}
}

# --- 3. INTERFAZ ---
st.title("🚜 AgroMind 360")
st.markdown("#### Inteligencia Agronómica Integral para el Productor del Futuro")
st.write("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📍 Localización")
    reg_sel = st.selectbox("Región", list(chile_full.keys()))
    prov_sel = st.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
