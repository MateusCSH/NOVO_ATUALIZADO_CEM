import pandas as pd
import plotly.express as px
from datetime import datetime
import streamlit as st

def graf(df):


    # Converter as colunas de data para datetime
    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df['Fim'] = pd.to_datetime(df['Fim'])

    # Calcular a diferença de tempo
    df['Diferença'] = df['Fim'] - df['Inicio']

    # Obter os períodos únicos
    periodos = df['Periodo'].unique()
    armazing = []

    for periodo in periodos:
        seconds_1 = df.query("Periodo == @periodo")['Diferença'].dt.total_seconds()
        total_seconds = seconds_1.sum()  # Somar os segundos para o período
        armazing.append(total_seconds)

    # Criar DataFrame com os tempos em segundos
    df3 = pd.DataFrame({'Periodo': periodos, 'Tempo em Segundos': armazing})

    # Calcular horas e minutos
    hr_min = df3['Tempo em Segundos'].apply(lambda x: divmod(x, 3600))
    df3['Horas'] = hr_min.apply(lambda x: x[0])  # Horas
    df3['Segundos Restantes'] = hr_min.apply(lambda x: x[1])  # Segundos restantes
    df3['Minutos'] = df3['Segundos Restantes'] // 60

    # Criar uma coluna formatada para exibir como 'Xh Ym'
    df3['Tempo Formatado'] = df3.apply(lambda x: f"{int(x['Horas'])}h {int(x['Minutos'])}m", axis=1)

    # Criar gráfico de barras
    fig = px.bar(df3, 
                x='Periodo', 
                y='Horas',  # Usar horas no eixo y
                title='Horas por Período',
                labels={'Horas': 'Tempo (horas)', 'Periodo': 'Período'},
                text='Tempo Formatado')  # Usando a coluna formatada

    # Exibir o gráfico
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(yaxis_title='Tempo (horas)', xaxis_title='Período')

    st.plotly_chart(fig)


def total_time(df):
    seconds_1 = df['Diferença'].dt.total_seconds()

    # Usando divmod para calcular horas e segundos restantes
    hr_min = seconds_1.apply(lambda x: divmod(x, 3600))

    # Separando horas e minutos em colunas diferentes
    df['Horas'] = hr_min.apply(lambda x: x[0])  # Horas
    df['Segundos Restantes'] = hr_min.apply(lambda x: x[1])  # Segundos restantes

    # Convertendo segundos restantes para minutos
    df['Minutos'] = df['Segundos Restantes'] // 60


    # Somando horas e minutos
    total_horas = df['Horas'].sum()
    total_minutos = df['Minutos'].sum()

    # Ajustando se os minutos ultrapassarem 60
    total_horas += total_minutos // 60  # Converte minutos em horas
    total_minutos = total_minutos % 60   # Resto dos minutos
    hrs_m = total_horas + float(total_minutos/10)
    st.write(f"Tempo total: {hrs_m} horas")
    return hrs_m


def selec_peri(df, x):
    seconds_1 = df.query("Periodo == @x")['Diferença'].dt.total_seconds()

    # Usando divmod para calcular horas e segundos restantes
    hr_min = seconds_1.apply(lambda x: divmod(x, 3600))

    # Separando horas e minutos em colunas diferentes
    df['Horas'] = hr_min.apply(lambda x: x[0])  # Horas
    df['Segundos Restantes'] = hr_min.apply(lambda x: x[1])  # Segundos restantes

    # Convertendo segundos restantes para minutos
    df['Minutos'] = df['Segundos Restantes'] // 60


    # Somando horas e minutos
    total_horas = df['Horas'].sum()
    total_minutos = df['Minutos'].sum()

    # Ajustando se os minutos ultrapassarem 60
    total_horas += total_minutos // 60  # Converte minutos em horas
    total_minutos = total_minutos % 60   # Resto dos minutos
    hrs_m = total_horas + float(total_minutos/10)
    return hrs_m
