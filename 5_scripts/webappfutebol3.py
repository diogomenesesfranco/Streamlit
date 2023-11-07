# importando as libraries

import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff


# Nome da aplicação
st.write(
    """
    **Futebol Wep App**
    
    """
)

# Criando uma side bar

st.sidebar.header('Escolha os times') # cabeçalho do sidebar


# Lendo arquivo de ações

def get_data():
    path = '../3_bases_upload/gols.csv'
    return pd.read_csv(path, sep=';')

def get_data2():
    path = '../2_bases_tratadas/futebol2.csv'
    return pd.read_csv(path, sep=';')

df = get_data()
df3 = get_data2()

df_data = df['anomes'].drop_duplicates()

min_data = min(df_data)
max_data = max(df_data)


indicador = ['temporal', 'específico']
escolha_do_indicador = st.sidebar.selectbox("Escolha o indicador", indicador)

total_gols = df3['away_team_goal_count'].sum()

if escolha_do_indicador == 'temporal':

    stock = df['home_team_name'].drop_duplicates()
    stock_choice = st.sidebar.selectbox("Escolha o time", stock)

    start_date = st.sidebar.text_input("Digite uma data de inicio:", min_data)

    end_date = st.sidebar.text_input("Digite uma data final:", max_data)

    start = int(start_date)
    end = int(end_date)


    if start > end:
        st.error('Data Final deve ser **MAIOR** que data inicial')

    df = df[(df['home_team_name'] == stock_choice) & ((df['anomes']) >= start) & ((df['anomes']) <= end)]

    df = df.set_index(df['anomes'].astype(str))

    #Criar grafico
    st.header('Time: ' + stock_choice.upper())
    st.write('Gols em casa')
    st.line_chart(df['gols'])

    st.write('Pontos por jogo em casa')
    st.line_chart(df['home_ppg'])


else:
    # como ver uma tabela
    

    top10 = df.groupby('home_team_name')['home_ppg'].count().sort_values(ascending=False).iloc[:10]
    top10 = list(top10.index)
    stock_choice = st.sidebar.selectbox("Escolha o time", top10)

   
    start_date = st.sidebar.text_input("Digite uma data de inicio:", min_data)

    end_date = st.sidebar.text_input("Digite uma data final:", max_data)

    start = int(start_date)
    end = int(end_date)

    if start > end:
        st.error('Data Final deve ser **MAIOR** que data inicial')

    df = df[(df['home_team_name'] == stock_choice) & ((df['anomes']) >= start) & ((df['anomes']) <= end)]

    df = df.set_index(df['anomes'].astype(str))

    df2 = df.copy()
    df2.anomes = (df2.anomes/100)
    df2.anomes = df2.anomes.astype(str)
    
    def grafico1(df):
        fig = px.scatter(df, x="anomes", y="gols", color='home_ppg',
                hover_name="home_team_name", size_max=60)
        return st.plotly_chart(fig)

    grafico1(df2)

    st.write('gols sofridos')
    st.area_chart(df3['away_team_goal_count'])
