from pandas._config.config import options
from pandas.core.arrays.boolean import coerce_to_array
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import altair as alt

def main():
    st.title("Интерактивный отчет")
    df = pd.read_csv(os.path.join("data_oleg_report", "dataset.csv"), parse_dates=True, index_col="Date")
    cols = st.sidebar.multiselect("Выберите столбцы для визуализации", options=df.columns[1:])
    visual = st.sidebar.selectbox("Выберите библиотеку визуализации", ["Vega", "Plotly"])
    unique_years = df.index.year.unique()
    years = st.sidebar.select_slider("Выберите год для визуализации",options = unique_years)
    years_end = st.sidebar.select_slider("Выберите год окончания для визуализация",options = unique_years)
    df_chart = df.loc[str(years):str(years_end)]
    if st.sidebar.button("Привести все значения к диапазону [0;1]"):
        df_chart = (df_chart - df_chart.min()) / (df_chart.max() - df_chart.min())
    if visual in "Vega":
        st.write(f"График за все года до {years}")
        st.line_chart(df_chart[cols])
    elif visual in "Plotly":
        st.plotly_chart(
            px.line(data_frame=df_chart, y=cols)
        )
    with st.beta_expander("Статистика"):   
        st.markdown("Общая статистика")
        stats = df_chart[cols].describe()
        st.dataframe(stats)
        st.markdown("Матрица кореляции Пирсона")
        corr_matrix = df_chart[cols].corr()
        st.dataframe(corr_matrix)
    

    

if __name__ == "__main__":
    main()