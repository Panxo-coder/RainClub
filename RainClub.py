import streamlit as st
import time

# Configuración de Software de Nivel Empresarial
st.set_page_config(page_title="RainClub Chile V15.0", page_icon="🇨🇱", layout="wide")

# --- BASE DE DATOS NACIONAL JERÁRQUICA (16 REGIONES) ---
chile_agro = {
    "Región del Maule": {
        "Provincias": {
            "Linares": ["Linares", "Yerbas Buenas", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"],
            "Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael"],
            "Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
            "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"]
        },
        "Sugerencia": "Cerezos, Arándanos, Manzanos y Avellano Europeo.", "ET": 5.2
    },
    "Región Metropolitana": {
        "Provincias": {
            "Santiago": ["Santiago", "Maipú", "Pudahuel", "Quilicura", "Lampa"],
            "Maipo": ["San Bernardo", "Buin", "Paine", "Calera de Tango"],
            "Melipilla": ["Melipilla", "Curacaví", "María Pinto", "San Pedro"]
        },
        "Sugerencia": "Nogales, Uva de Mesa, Hortalizas y Alfalfa.", "ET": 5.8
    },
    "Región de O'Higgins": {
        "Provincias": {
            "Cachapoal": ["Rancagua", "Rengo", "Requínoa", "Machalí", "Doñihue"],
            "Colchagua": ["San Fernando", "Santa Cruz", "Chimbarongo", "Nancagua"],
            "Cardenal Caro": ["Pichilemu", "Litueche", "Marchigüe"]
        },
        "Sugerencia": "Maíz, Cerezos, Ciruelos y Vides de exportación.", "ET": 5.5
    }
    # Nota: Se pueden seguir agregando las 16 regiones con esta misma estructura
}

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("💧 RainClub Chile V15.0")
st.markdown("#### Inteligencia Hídrica Nacional para el Agricultor Moderno")
st.write("---")

# --- PANEL LATERAL (CONTROL DE MANDO) ---
st.sidebar.header("📍 Ubicación del Predio")
reg_sel = st.sidebar.selectbox("Región", list(chile_agro.keys()))
prov_dict = chile_agro[reg_sel]["Provincias"]
prov_sel = st.sidebar.selectbox("Provincia", list(prov_dict.keys()))
comu_sel = st.sidebar.selectbox("Comuna", prov_dict[prov_sel])

st.sidebar.divider()
st.sidebar.header("⚙️ Centro de Alertas Pro")
if st.sidebar.button("🔔 Probar Alerta WhatsApp"):
    with st.sidebar:
        with st.status("Sincronizando con Agromet...", expanded=True) as status:
            time.sleep(1.2)
            st.write(f"🛰️ Analizando sensores en {comu_sel}...")
            time.sleep(1.2)
            st.write("⚠️ Detectada baja de presión en sector 2.")
            time.sleep(1)
            status.update(label="✅ Notificación Enviada", state="complete", expanded=False)
    st.sidebar.success(f"📱 Mensaje: 'RainClub: Revisar válvula en {comu_sel}.'")

# --- CÁLCULOS TÉCNICOS ---
st.sidebar.divider()
st.sidebar.header("🚜 Datos Técnicos")
has = st.sidebar.number_input("Hectáreas", min_value=0.1, value=1.0, step=0.1)
dist_h = st.sidebar.number_input("Marco: Entre Hileras (m)", value=4.0)
dist_p = st.sidebar.number_input("Marco: Sobre Hilera (m)", value=2.0)
sistema = st.sidebar.selectbox("Sistema de Riego", ["Goteo (95% Eficiencia)", "Microaspersión (85%)", "Tendida (50%)"])

# Cálculo de lógica agropecuaria
et_val = chile_agro[reg_sel]["ET"]
efi = 0.95 if "Goteo" in sistema else (0.85 if "Micro" in sistema else 0.50)
pl_ha = 10000 / (dist_h * dist_p)
total_pl = pl_ha * has
l_dia = (et_val * total_pl) / efi
min_riego = (l_dia / (1.5 * has * 60))

# --- RESULTADOS PRINCIPALES ---
st.subheader(f"📊 Reporte Operativo: {comu_sel}, {prov_sel}")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Agua Diaria", f"{l_dia:,.0f} L", help="Litros totales necesarios para el predio hoy.")
with c2:
    st.metric("Tiempo de Riego", f"{int(min_riego)} min", help="Tiempo sugerido para reponer la humedad del suelo.")
with c3:
    st.metric("Población", f"{int(total_pl)} pl", help="Cantidad total de plantas según el marco de plantación.")
with c4:
    st.metric("Evapotranspiración", f"{et_val} mm", delta="Agromet", help="Dato climático de la estación más cercana.")

# --- SECCIÓN ESTRATÉGICA (SABIALAB) ---
st.write("---")
tab1, tab2, tab3, tab4 = st.tabs(["💡 Factibilidad", "💎 Planes", "💳 Pagos", "📱 Instalar"])

with tab1:
    st.info(f"### Análisis de Cultivo para {reg_sel}")
    st.write(f"Según las condiciones climáticas y de suelo, los cultivos más factibles son: **{chile_agro[reg_sel]['Sugerencia']}**")
    st.write("Este análisis ayuda a reducir el riesgo de inversión para nuevos productores.")

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("### Plan Básico (Gratis)")
        st.write("- Calculadora nacional FAO-56.")
        st.write("- Sugerencias de cultivo por región.")
        st.write("- Acceso a bases de datos históricas.")
    with col_b:
        st.warning("### Plan Pro ($15.000/mes)")
        st.write("- **Alertas WhatsApp en tiempo real.**")
        st.write("- Conexión a Sensores IoT de humedad.")
        st.write("- **40% de Comisión para el Creador ($6.000).**")

with tab3:
    st.write("#### Pasarela de Pagos Segura (Simulación)")
    st.write("Aceptamos todas las tarjetas de crédito, débito y billeteras digitales.")
    st.markdown("💳 **Visa | Mastercard | WebPay | PayPal | Mercado Pago | MACH**")
    if st.button("🚀 Probar Suscripción Pro"):
        st.toast("Conectando con pasarela de pago...")
        time.sleep(2)
        st.success("¡Pago Procesado! RainClub Pro activado con éxito.")

with tab4:
    st.write("### ¿Cómo descargar RainClub?")
    st.write("Nuestra app es una **PWA (Progressive Web App)**. No gasta espacio y es muy segura.")
    st.markdown("""
    1. Abre este link en tu celular (Chrome o Safari).
    2. Toca el botón de **'Compartir'** o los **tres puntos** arriba.
    3. Selecciona **'Agregar a la pantalla de inicio'**.
    4. ¡Listo! Ya tienes el icono de RainClub junto a tus otras apps.
    """)

st.write("---")
st.caption("RainClub V15.0 - Tecnología Chilena para el Ahorro de Agua. SabíaLab 2026.")
