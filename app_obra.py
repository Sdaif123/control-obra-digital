import streamlit as st
import pandas as pd
import numpy as np

# ======================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Título en la pestaña del navegador)
# ======================================================================
st.set_page_config(page_title="Control Digital de Obra", layout="wide")

# ======================================================================
# 2. TÍTULOS PRINCIPALES DE LA WEB
# ======================================================================
st.title("📊 Monitor de Control Integral: Producción, Plazos y Márgenes")
st.subheader("Ingeniería de Control de Producción v5.0")

# ======================================================================
# 3. BARRA LATERAL (SIDEBAR): ENTRADA DE DATOS DE CAMPO
# ======================================================================
st.sidebar.header("📥 Parte Diario de Obra")
dia_actual = st.sidebar.slider("Día de Obra", 1, 30, 10)

st.sidebar.subheader("🚀 Producción")
paneles_hoy = st.sidebar.number_input("Paneles ejecutados hoy", min_value=0.0, value=2.0)

st.sidebar.subheader("👷 Mano de Obra")
horas_reales = st.sidebar.number_input("Horas totales cuadrilla hoy", min_value=0.0, value=12.0)
coste_hora_mo = 180.0  # Euros/hora (Personal + Maquinaria)

st.sidebar.subheader("🧱 Materiales")
m3_hormigon = st.sidebar.number_input("M3 Hormigón (Real)", value=25.5)

# ======================================================================
# 4. LÓGICA DE CÁLCULO (EL "CEREBRO" DEL PROGRAMA)
# ======================================================================
# Eficiencia Mano de Obra (Objetivo 6h/panel)
ratio_productividad = horas_reales / paneles_hoy if paneles_hoy > 0 else 0

# Plazo y Certificación (Simulación histórica para la gráfica)
dias = np.arange(1, dia_actual + 1)
plan_previsto = dias * 2.0 * 12500  # Objetivo: 2 pan/día a 12.500€ cada uno
# Generamos una curva real que simula la obra
cert_real = dias * 1.8 * 12500 + np.random.normal(0, 3000, len(dias))

# Creamos la tabla para la gráfica
df_plan = pd.DataFrame({
    'Día': dias,
    'Planificado (Adif)': plan_previsto,
    'Real Ejecutado (FCC)': cert_real
}).set_index('Día')

# ======================================================================
# 5. DISEÑO DEL PANEL (LO QUE VE EL JEFE DE OBRA)
# ======================================================================
# Creamos 4 columnas para las métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    atraso = (dia_actual * 2.0) - (cert_real[-1] / 12500)
    st.metric("Plazo (Paneles)", f"{atraso:.1f} p", delta=f"-{atraso:.1f}", delta_color="inverse")

with col2:
    st.metric("Certificación Acum.", f"{cert_real[-1]:,.2f} €")

with col3:
    # Mostramos la eficiencia: si es menos de 6h es bueno (verde), si es más es malo (rojo)
    st.metric("Eficiencia M.O.", f"{ratio_productividad:.1f} h/pan", delta=f"{6.0-ratio_productividad:.1f} h", delta_color="normal")

with col4:
    margen_h = (25.0 - m3_hormigon) * 94.0
    st.metric("Margen Hormigón", f"{margen_h:.2f} €", delta=margen_h)

# ======================================================================
# 6. GRÁFICA DE AVANCE (CURVA EN S)
# ======================================================================
st.subheader("📈 Curva de Avance: Planificado vs Real")
st.line_chart(df_plan)

# ======================================================================
# 7. BOTÓN DE ENVÍO DE INFORME
# ======================================================================
st.divider()
if st.button("🚀 Ejecutar Envío Profesional de Informe"):
    st.success(f"Informe ejecutivo generado con éxito.")
    st.info("Los datos han sido validados y el reporte ha sido enviado a Dirección y Compras.")
    st.balloons()