import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN TÉCNICA
st.set_page_config(page_title="Control Digital de Obra", layout="wide")

# 2. IDENTIFICACIÓN
st.title("📊 Monitor de Control Integral")
st.write("Estado de Producción y Ratios de Eficiencia")

# 3. ENTRADA DE DATOS (SIDEBAR)
st.sidebar.header("📥 Parte Diario")
dia_actual = st.sidebar.slider("Día de Obra", 1, 30, 10)
paneles_hoy = st.sidebar.number_input("Paneles ejecutados hoy", min_value=0.0, value=2.0)
horas_reales = st.sidebar.number_input("Horas totales cuadrilla hoy", min_value=0.1, value=12.0)
m3_hormigon = st.sidebar.number_input("M3 Hormigón (Real)", value=25.5)

# 4. LÓGICA DE CONTROL DE PLANIFICACIÓN
PLAN_DIARIO = 2.0 
desvio_unidades = paneles_hoy - PLAN_DIARIO
cumplimiento_pct = (paneles_hoy / PLAN_DIARIO) * 100 if PLAN_DIARIO > 0 else 0

# Lógica de Mano de Obra
ratio_h_p = horas_reales / paneles_hoy if paneles_hoy > 0 else 0
objetivo_h_p = 6.0
ahorro_horas = objetivo_h_p - ratio_h_p

# 5. DASHBOARD DE INDICADORES (CENTRO)
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Muestra los paneles, el desvío numérico y el % de cumplimiento
    st.metric("PANELES HOY", f"{paneles_hoy:.1f} p", delta=f"{desvio_unidades:+.1f} vs plan")
    st.write(f"**Cumplimiento: {cumplimiento_pct:.0f}%**")

with col2:
    # Eficiencia de mano de obra h/pan
    st.metric("EFICIENCIA M.O.", f"{ratio_h_p:.1f} h/p", delta=f"{ahorro_horas:.1f} h", delta_color="normal")

with col3:
    # Margen económico del hormigón
    margen_h = (25.0 - m3_hormigon) * 94.0
    st.metric("MARGEN HORMIGÓN", f"{margen_h:.2f} €")

with col4:
    # Valor de la producción acumulada
    total_cert = (dia_actual * 1.8 * 12500) 
    st.metric("CERTIFICACIÓN", f"{total_cert:,.2f} €")

# 6. GRÁFICA DE AVANCE
st.subheader("📈 Comparativa: Avance Real vs Planificado")
dias = np.arange(1, dia_actual + 1)
df_avance = pd.DataFrame({
    'Planificado': dias * PLAN_DIARIO * 12500,
    'Real': dias * 1.8 * 12500
}, index=dias)
st.line_chart(df_avance)
