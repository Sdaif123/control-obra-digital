import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Control Digital de Obra", layout="wide")

# 2. TÍTULOS
st.title("📊 Monitor de Control Integral: Producción y Ratios")
st.subheader("Ingeniería de Control de Producción v5.1")

# 3. SIDEBAR (ENTRADAS)
st.sidebar.header("📥 Parte Diario de Obra")
dia_actual = st.sidebar.slider("Día de Obra", 1, 30, 10)

st.sidebar.subheader("🚀 Producción")
paneles_hoy = st.sidebar.number_input("Paneles ejecutados hoy", min_value=0.1, value=2.0)

st.sidebar.subheader("👷 Mano de Obra")
horas_reales = st.sidebar.number_input("Horas totales cuadrilla hoy", min_value=0.1, value=12.0)

st.sidebar.subheader("🧱 Materiales")
m3_hormigon = st.sidebar.number_input("M3 Hormigón (Real)", value=25.5)

# 4. LÓGICA DE CÁLCULO
ratio_eficiencia = horas_reales / paneles_hoy
dias = np.arange(1, dia_actual + 1)
plan_previsto = dias * 2.0 * 12500 
cert_real = dias * 1.8 * 12500 + np.random.normal(0, 3000, len(dias))

df_plan = pd.DataFrame({
    'Día': dias,
    'Planificado': plan_previsto,
    'Real Ejecutado': cert_real
}).set_index('Día')

# 5. DASHBOARD (MÉTRICAS) - AHORA CON 4 COLUMNAS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Paneles Hoy", f"{paneles_hoy:.1f} p")

with col2:
    st.metric("Certificación Acum.", f"{cert_real[-1]:,.2f} €")

with col3:
    # Ratio Eficiencia h/pan
    objetivo = 6.0
    desviacion = objetivo - ratio_eficiencia
    st.metric("Eficiencia M.O.", f"{ratio_eficiencia:.1f} h/pan", delta=f"{desviacion:.1f} h", delta_color="normal")

with col4:
    margen_h = (25.0 - m3_hormigon) * 94.0
    st.metric("Margen Hormigón", f"{margen_h:.2f} €", delta=f"{margen_h:.2f}")

# 6. GRÁFICA
st.subheader("📈 Curva de Avance: Planificado vs Real")
st.line_chart(df_plan)

if st.button("🚀 Generar Informe de Producción"):
    st.success("Informe generado con éxito.")
    st.balloons()
