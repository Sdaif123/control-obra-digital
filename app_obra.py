import streamlit as st
import pandas as pd
import numpy as np

# Configuración básica
st.set_page_config(page_title="Control de Obra", layout="wide")

st.title("📊 Monitor de Control Integral")
st.write("Ingeniería de Control de Producción v5.0")

# Entradas en la barra lateral
st.sidebar.header("📥 Datos de Campo")
dia = st.sidebar.slider("Día de Obra", 1, 30, 10)
paneles = st.sidebar.number_input("Paneles hoy", value=2.0)
horas = st.sidebar.number_input("Horas cuadrilla", value=12.0)

# Cálculos sencillos
prod_real = horas / paneles if paneles > 0 else 0
ejes_x = np.arange(1, dia + 1)
datos_plan = ejes_x * 25000
datos_real = ejes_x * 23500

# Panel de métricas
c1, c2, c3 = st.columns(3)
c1.metric("Plazo (Paneles)", "-1.5 p")
c2.metric("Certificación", f"{datos_real[-1]:,.0f} €")
c3.metric("Eficiencia", f"{prod_real:.1f} h/p")

# Gráfico de avance
st.subheader("📈 Avance de Obra: Planificado vs Real")
df = pd.DataFrame({"Planificado": datos_plan, "Real": datos_real}, index=ejes_x)
st.line_chart(df)

if st.button("🚀 Generar Informe"):
    st.balloons()
    st.success("Informe enviado correctamente")
