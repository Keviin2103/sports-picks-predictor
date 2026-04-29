# streamlit_app.py
import streamlit as st
import pandas as pd
from src.predictions import crear_picks_del_dia

st.set_page_config(page_title="Sports Picks Predictor", layout="wide")
st.title("🎯 Sports Picks Predictor")
st.subheader("Predicciones diarias - Fútbol • MLB • NBA • NHL")

if st.button("🔄 Generar Picks del Día"):
    with st.spinner("Descargando datos y generando picks..."):
        crear_picks_del_dia()
        df = pd.read_csv("data/picks_hoy.csv")
        st.success(f"✅ {len(df)} picks generados")
        st.dataframe(df, use_container_width=True)
else:
    st.info("Presiona el botón para generar los picks de hoy")