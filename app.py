import streamlit as st
import pandas as pd
import re

st.title("MonitorSolo - Comparador simplificado para Lanzadera")

st.markdown("Sube un archivo de texto clínico (.txt) y otro CSV de CRF para ver si hay discrepancias.")

# Subida del texto clínico simulado
archivo_txt = st.file_uploader("📄 Subir texto clínico (.txt)", type="txt")

if archivo_txt:
    texto = archivo_txt.read().decode("utf-8")

    st.markdown("### Texto clínico cargado:")
    st.write(texto)

    # Extracción simple con regex
    def buscar(pat, texto):
        r = re.search(pat, texto, re.IGNORECASE)
        return r.group(0) if r else ""

    valores = {
        "HbA1c": buscar(r"HbA1c[:\s]*\d+(\.\d+)?%", texto),
        "Glucosa": buscar(r"glucosa.*?\d+.*?mg/dL", texto),
        "Presión_Arterial": buscar(r"presión.*?\d+/\d+", texto),
        "Peso": buscar(r"peso.*?\d+\s?kg", texto),
        "Creatinina": buscar(r"creatinina.*?\d+(\.\d+)?\s?mg/dL", texto),
        "eGFR": buscar(r"eGFR.*?\d+", texto),
        "Medicamento": buscar(r"metformina|sitagliptin|canagliflozin", texto),
    }

    df_ehr = pd.DataFrame([valores])
    st.markdown("### Datos extraídos (versión simplificada):")
    st.dataframe(df_ehr)

    archivo_crf = st.file_uploader("📄 Subir CRF (.csv)", type="csv")
    if archivo_crf:
        df_crf = pd.read_csv(archivo_crf)
        st.markdown("### Datos del CRF:")
        st.dataframe(df_crf)

        diferencias = []
        for campo in valores:
            val_ehr = str(valores[campo]).strip().lower()
            val_crf = str(df_crf.iloc[0].get(campo, "")).strip().lower()
            if val_ehr != val_crf:
                diferencias.append({
                    "Campo": campo,
                    "EHR extraído": valores[campo],
                    "CRF": df_crf.iloc[0].get(campo, "")
                })

        if diferencias:
            st.markdown("### ⚠️ Discrepancias detectadas:")
            st.dataframe(pd.DataFrame(diferencias))
        else:
            st.success("✅ Todos los campos coinciden.")