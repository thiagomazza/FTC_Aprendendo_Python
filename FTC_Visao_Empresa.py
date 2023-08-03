# Importando bibliotecas
import pandas as pd
import re
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff
from PIL import Image

# Lendo do Arquivo
df = pd.read_csv( 'FTC_Aprendendo_Python/train.csv' )

############################
#### Limpando base #########
############################

# Remover spaco da string
for i in range( len( df ) ):
  df.loc[i, 'ID'] = df.loc[i, 'ID'].strip()
  df.loc[i, 'Delivery_person_ID'] = df.loc[i, 'Delivery_person_ID'].strip()

# Excluir as linhas com a idade dos entregadores vazia
# ( Conceitos de seleção condicional )
linhas_vazias = df['Delivery_person_Age'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['Road_traffic_density'] != 'NaN '
df = df.loc[linhas_vazias, :]
linhas_vazias = df['City'] != 'NaN '
df = df.loc[linhas_vazias, :]

# Conversao de texto/categoria/string para numeros inteiros
df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )

# Conversao de texto/categoria/strings para numeros decimais
df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )

# Conversao de texto para data
df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

#
linhas_vazias = df['multiple_deliveries'] != 'NaN '
df = df.loc[linhas_vazias, :]
df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )

# Comando para remover o texto de números
df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
df.loc[:, 'Type_of_order'] = df.loc[:, 'Type_of_order'].str.strip()
df.loc[:, 'Type_of_vehicle'] = df.loc[:, 'Type_of_vehicle'].str.strip()
df.loc[:, 'City'] = df.loc[:, 'City'].str.strip()

##########################################################################################

# Define título e tamanho ocupado na página
st.set_page_config(page_title="Goodreads Analysis App", layout="wide")


with st.sidebar:
    image = Image.open('FTC_Aprendendo_Python/Logo_2.png')
    st.image(image)
    ## Teste

# Montagem Layout com dados
tab1, tab2, tab3 = st.tabs(['Quantidade Pedidos','Pedidos por Tipo Trafego  / Cidade','Pedidos x Entregador' ])

with tab1:
    col1, col2 = st.columns((2, 2))
    with col1:
        #1. Quantidade de pedidos por dia.
        st.markdown('#### Qtde de Pedidos Dia')
        colunas = ['ID', 'Order_Date']
        df_pedidos_dia = df.loc[:, colunas].groupby( ['Order_Date'] ).count().reset_index()
        fig = px.bar( df_pedidos_dia, x='Order_Date', y='ID')
        st.plotly_chart(fig, use_container_width=True)        

    with col2:
        # Criando as semanas e adicionando no Dataframe
        df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )
        #2. Quantidade de pedidos por semana.    
        st.markdown('#### Qtde de Pedidos Semana')
        colunas = ['week_of_year', 'ID']
        df_pedidos_semana = df.loc[:, colunas].groupby( ['week_of_year'] ).count().reset_index()
        fig = px.bar( df_pedidos_semana, x='week_of_year', y='ID')
        st.plotly_chart(fig, use_container_width=True)        

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        #3. Distribuição dos pedidos por tipo de tráfego.
        st.markdown('#### Pedidos x Tipo Tráfego')
        colunas = ['ID', 'Road_traffic_density']
        df_pedidos_dia = df.loc[:, colunas].groupby( ['Road_traffic_density'] ).count().reset_index()
        st.dataframe(df_pedidos_dia, width = 300, height=200)  
    with col2:  
        #4. Comparação do volume de pedidos por cidade e tipo de tráfego.
        st.markdown('#### Pedidos x Tráfego x Cidade')
        colunas = ['ID', 'Road_traffic_density', 'City']
        df_pedidos_dia = df.loc[:, colunas].groupby( ['Road_traffic_density', 'City'] ).count().reset_index()
        st.dataframe(df_pedidos_dia, width = 400, height=300)  

with tab3:
    #5. A quantidade de pedidos por entregador por semana.
    st.markdown('#### Pedidos x Entregador x Semana')
    colunas = ['week_of_year', 'Delivery_person_ID', 'ID']
    df_pedidos_dia = df.loc[:, colunas].groupby( ['week_of_year', 'Delivery_person_ID'] ).count().reset_index()
    st.dataframe(df_pedidos_dia, width = 450, height=400)  
