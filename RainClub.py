import streamlit as st
import time

# Configuración de Software de Nivel Profesional
st.set_page_config(page_title="RainClub Chile V22.0", page_icon="💧", layout="wide")

# --- 1. BASE DE DATOS NACIONAL COMPLETA (16 REGIONES) ---
chile_full = {
    "Arica y Parinacota": {"ET": 6.8, "Provincias": {"Arica": ["Arica", "Camarones"], "Parinacota": ["Putre", "General Lagos"]}},
    "Tarapacá": {"ET": 6.5, "Provincias": {"Iquique": ["Iquique", "Alto Hospicio"], "Tamarugal": ["Pozo Almonte", "Pica", "Huara"]}},
    "Antofagasta": {"ET": 6.2, "Provincias": {"Antofagasta": ["Antofagasta", "Taltal"], "El Loa": ["Calama", "San Pedro de Atacama"], "Tocopilla": ["Tocopilla", "María Elena"]}},
    "Atacama": {"ET": 6.0, "Provincias": {"Copiapó": ["Copiapó", "Caldera", "Tierra Amarilla"], "Huasco": ["Vallenar", "Freirina", "Huasco", "Alto del Carmen"], "Chañaral": ["Chañaral", "Diego de Almagro"]}},
    "Coquimbo": {"ET": 5.8, "Provincias": {"Elqui": ["La Serena", "Coquimbo", "Andacollo", "Vicuña"], "Limarí": ["Ovalle", "Combarbalá", "Monte Patria", "Punitaqui"], "Choapa": ["Illapel", "Canela", "Los Vilos", "Salamanca"]}},
    "Valparaíso": {"ET": 5.5, "Provincias": {"Valparaíso": ["Valparaíso", "Viña del Mar", "Casablanca"], "Quillota": ["Quillota", "La Cruz", "Nogales"], "San Felipe": ["San Felipe", "Llay-Llay", "Putaendo"], "Los Andes": ["Los Andes", "Calle Larga", "San Esteban"], "Petorca": ["La Ligua", "Cabildo", "Zapallar"], "San Antonio": ["San Antonio", "Algarrobo", "Cartagena"], "Marga Marga": ["Quilpué", "Villa Alemana", "Limache"]}},
    "Metropolitana": {"ET": 5.6, "Provincias": {"Santiago": ["Santiago", "Maipú", "Pudahuel", "Quilicura"], "Maipo": ["San Bernardo", "Buin", "Paine", "Calera de Tango"], "Melipilla": ["Melipilla", "Curacaví", "María Pinto", "Alhué"], "Chacabuco": ["Colina", "Lampa", "Tiltil"], "Cordillera": ["Puente Alto", "Pirque", "San José de Maipo"], "Talagante": ["Talagante", "Isla de Maipo", "El Monte", "Peñaflor"]}},
    "O'Higgins": {"ET": 5.4, "Provincias": {"Cachapoal": ["Rancagua", "Machalí", "Rengo", "Requínoa", "Doñihue", "Coinco", "Coltauco", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "San Vicente"], "Colchagua": ["San Fernando", "Chimbarongo", "Santa Cruz", "Chépica", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque"], "Cardenal Caro": ["Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones"]}},
    "Maule": {"ET": 5.2, "Provincias": {"Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"], "Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"], "Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"], "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]}},
    "Ñuble": {"ET": 4.8, "Provincias": {"Diguillín": ["Chillán", "Bulnes", "Chillán Viejo", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay"], "Itata": ["Quirihue", "Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Ránquil", "Treguaco"], "Punilla": ["San Carlos", "Coihueco", "Ñiquén", "San Fabián", "San Nicolás"]}},
    "Biobío": {"ET": 4.5, "Provincias": {"Concepción": ["Concepción", "Talcahuano", "Coronel", "Chiguayante", "Florida", "Hualpén", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Tomé"], "Biobío": ["Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"], "Arauco": ["Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa"]}},
    "La Araucanía": {"ET": 4.0, "Provincias": {"Cautín": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol"], "Malleco": ["Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]}},
    "Los Ríos": {"ET": 3.5, "Provincias": {"Valdivia": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli"], "Ranco": ["La Unión", "Futrono", "Lago Ranco", "Río Bueno"]}},
    "Los Lagos": {"ET": 3.2, "Provincias": {"Llanquihue": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas"], "Osorno": ["Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo"], "Chiloé": ["Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao"], "Palena": ["Chaitén", "Futaleufú", "Hualaihué", "Palena"]}},
    "Aysén": {"ET": 2.5, "Provincias": {"Coyhaique": ["Coyhaique", "Lago Verde"], "Aysén": ["Aysén", "Cisnes", "Guaitecas"], "General Carrera": ["Chile Chico", "Río Ibáñez"], "Capitán Prat": ["Cochrane", "O'Higgins", "Tortel"]}},
    "Magallanes": {"ET": 2.0, "Provincias": {"Magallanes": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio"], "Última Esperanza": ["Puerto Natales", "Torres del Paine"], "Tierra del Fuego": ["Porvenir", "Primavera", "Timaukel"], "Antártica Chilena": ["Cabo de Hornos", "Antártica"]}}
}

# --- 2. CATÁLOGOS TÉCNICOS ---
dict_riego = {
    "-- Tecnificado --": 0.95, "Goteo": 0.95, "Goteo Subsuperficial": 0.98, "Microaspersión": 0.85, "Microjets": 0.85, "Nebulización": 0.90, "Hidroponía": 0.98,
    "-- Aspersión --": 0.80, "Pivote Central": 0.85, "Aspersión Fija": 0.75, "Aspersión Móvil": 0.70, "Cañón": 0.65,
    "-- Superficie --": 0.50, "Surcos c/ Mangas": 0.65, "Surcos Tradicional": 0.45, "Inundación Controlada": 0.50, "Tendida": 0.35
}

cultivos_aire = {
    "-- Frutales --": 1.0, "Cerezos": 1.1, "Nogales": 1.05, "Paltos": 0.85, "Manzanos": 1.0, "Vides": 0.85, "Olivos": 0.7, "Arándanos": 0.9,
    "-- Anuales --": 1.0, "Maíz": 1.2, "Trigo": 1.0, "Papas": 1.1, "Remolacha": 1.15,
    "-- Praderas --": 1.0, "Pradera Mixta": 1.05, "Alfalfa": 1.15, "Trebol": 1.0
}

cultivos_inv = {
    "-- Hortalizas --": 1.0, "Tomate": 1.15, "Pimiento": 1.1, "Pepino": 1.1, "Melón": 1.0,
    "-- Flores --": 1.0, "Rosas": 0.9, "Claveles": 0.85, "Lilium": 0.9,
    "-- Berries --": 1.0, "Frutilla Invernadero": 0.95, "Arándano en Maceta": 0.85
}

# --- 3. INTERFAZ ---
st.title("💧 RainClub Chile V22.0")
st.markdown("#### Gestión Nacional: Aire Libre, Invernaderos y Sistemas Globales")
st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("📍 1. Localización")
reg_sel = st.sidebar.selectbox("Región", list(chile_full.keys()))
prov_sel = st.sidebar.selectbox("Provincia", list(chile_full[reg_sel]["Provincias"].keys()))
comu_sel = st.sidebar.selectbox("Comuna", chile_full[reg_sel]["Provincias"][prov_sel])

st.sidebar.divider()
st.sidebar.header("🏠 2. Entorno")
es_inv = st.sidebar.checkbox("¿Es Cultivo en Invernadero?")

st.sidebar.divider()
st.sidebar.header("🌱 3. Cultivo y Riego")
lista_c = cultivos_inv if es_inv else cultivos_aire
cultivo_sel = st.sidebar.selectbox("¿Qué tiene plantado?", list(lista_c.keys()))
sistema_sel = st.sidebar.selectbox("Sistema de Riego", list(dict_riego.keys()))

st.sidebar.divider()
st.sidebar.header("🚜 4. Parámetros")
has = st.sidebar.number_input("Hectáreas (ha)", min_value=0.01, value=1.0)
es_cobertura = any(x in cultivo_sel for x in ["Pradera", "Alfalfa", "Hidropónica", "Trebol"])

if not es_cobertura and not "--" in cultivo_sel:
    dist_h = st.sidebar.number_input("Distancia Hileras (m)", value=4.0 if not es_inv else 1.0)
    dist_p = st.sidebar.number_input("Distancia Plantas (m)", value=2.0 if not es_inv else 0.5)
    pl_total = (10000 / (dist_h * dist_p)) * has
else:
    pl_total = 1

# --- CÁLCULOS ---
et_base = chile_full[reg_sel]["ET"]
kc = lista_c[cultivo_sel]
efi = dict_riego[sistema_sel]
# Ajuste Invernadero: Menor ET pero Kc intensivo
etc = (et_base * 0.75 * kc) if es_inv else (et_base * kc)
vol_m3 = (etc / efi) * 10 * has
litros = vol_m3 * 1000
minutos = (vol_m3 / (3.0 * has)) * 60 # Caudal referencial

# --- RESULTADOS (MODO GRATIS) ---
st.subheader(f"📊 Reporte Operativo: {comu_sel}")
if "--" in cultivo_sel or "--" in sistema_sel:
    st.info("Seleccione cultivo y riego para ver resultados.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Agua Diaria", f"{litros:,.0f} L")
    c2.metric("Tiempo Riego", f"{int(minutos)} min")
    c3.metric("Eficiencia", f"{int(efi*100)}%")
    c4.metric("Consumo Kc", f"{kc}")

# --- SECCIÓN PRO (NEGOCIO) ---
st.write("---")
t_pro, t_pago = st.tabs(["💎 Funciones Pro", "💳 Suscripción"])

with t_pro:
    st.write("### Beneficios Premium ($15.000/mes)")
    st.markdown("- **Alertas WhatsApp:** 'Hola, es hora de regar tu " + cultivo_sel + "'.")
    st.markdown("- **Sensores IoT:** Humedad de suelo en tiempo real.")
    if st.button("🔔 Probar Simulación de Alerta"):
        st.toast("Verificando clima en " + comu_sel)
        time.sleep(1)
        st.success("✅ Alerta enviada: 'RainClub: Riesgo de helada en su sector'.")

with t_pago:
    st.write("#### Activar RainClub Pro")
    st.button("💳 Ir a Pago Seguro")
    st.info("Modelo: 40% de comisión para el creador ($6.000 por usuario).")

st.info("RainClub V22.0 - Tecnología del Maule. SabíaLab 2026.")
