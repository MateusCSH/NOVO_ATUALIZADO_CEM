import streamlit as st
import pandas as pd
from datetime import datetime as dt
from Notebook_aux import transformar_horas, format_timedelta
import plotly.graph_objects as go
from service.grap  import Quantidade_periodo



def cont_usuários():

    up = st.sidebar.file_uploader('AQUIVO CSS USUÁRIO!', type='csv')

    if up is not None:
        df = pd.read_csv(up, header=None, sep=',').drop(0).drop(columns=0)
        df.columns = ['Nome', 'Matricula', 'Periodo','Inicio', 'Fim', 'Motivo']

        df['Nome'] = df['Nome'].astype(str)      
 


        df['Inicio'] = pd.to_datetime(df['Inicio'], format='%H:%M:%S')
        df['Fim'] = pd.to_datetime(df['Fim'], format='%H:%M:%S')
        # df['minuto'] = (df['Fim'] - df['Inicio']).dt.minute



        filtro = st.selectbox('FILTRO', options=['INFORMAÇÕES GERAIS','PERIODO'])



        if filtro == 'INFORMAÇÕES GERAIS':
            

            total = transformar_horas(df)
            total_sum = total.sum()
            Conversão_hrs = format_timedelta(total_sum)   # Retorna conversão h:m   
            qtd_pessoas = len(df['Nome'])


            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="usuario"><span>HORAS ACUMULADAS</span><span class="value">{Conversão_hrs} hrs</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="usuario"><span>QUANTIDADE DE PASSOAS</span><span class="value">{qtd_pessoas}</span></div>', unsafe_allow_html=True)


        
        p1=0; p2=0; p3=0; p4=0; p5=0
        p6=0; p7=0; p8=0; p9=0; p10=0;
        if filtro == 'PERIODO':
            for i in df.index:
                if df.loc[i,'Periodo'] == '1º PERIODO':
                    p1 += 1

                if df.loc[i,'Periodo'] == '2º PERIODO':
                    p2 += 1

                if df.loc[i,'Periodo'] == '3º PERIODO':
                    p3 += 1

                if df.loc[i,'Periodo'] == '4º PERIODO':
                    p4 += 1

                if df.loc[i,'Periodo'] == '5º PERIODO':
                    p5 += 1

                if df.loc[i,'Periodo'] == '6º PERIODO':
                    p6 += 1

                if df.loc[i,'Periodo'] == '7º PERIODO':
                    p7 += 1

                if df.loc[i,'Periodo'] == '8º PERIODO':
                    p8 += 1

                if df.loc[i,'Periodo'] == '9º PERIODO':
                    p9 += 1

                if df.loc[i, 'Periodo'] == '10º PERIODO':
                    p10 += 1

            


            Pessoas_periodo, Horas_periodo = st.tabs(['Quantidade de pessoas', 'Quantidade Horas por periodo'])
           
            with Pessoas_periodo:
                st.markdown(f'<div class="sem_arquivo"> <span>QUANTIDADE DE PESSOAS POR</span> <span class = "com_arquivo">PERIODO</span></div> ',unsafe_allow_html=True)

                col1, col2, col3, col4, col5= st.columns(5)
                with col1:
                    Quantidade_periodo(1, p1)
                    Quantidade_periodo(6, p6)
                with col2:
                    Quantidade_periodo(2, p2)
                    Quantidade_periodo(7, p7)
                with col3:
                    Quantidade_periodo(3, p3)
                    Quantidade_periodo(8, p8)
                with col4:
                    Quantidade_periodo(4, p4)
                    Quantidade_periodo(9, p9)
                with col5:
                    Quantidade_periodo(5, p5)
                    Quantidade_periodo(10, p10)
        

                selec_perio = st.selectbox('SELECIONE O PERIÓDO PARA FILTRO', options=df['Periodo'].unique())

                df_select_periodo = df.query(
                    'Periodo == @selec_perio'
                )
                
                soma_periodo = len(df_select_periodo)

                percent_peri = (soma_periodo/len(df['Periodo'])) * 100

                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = percent_peri,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "PORCENTAGEM POR PERIODO"},
                    gauge={'axis': {'range': [None, 100]}}))

                st.plotly_chart(fig)


                with Horas_periodo:
                    st.markdown(f'<div class="sem_arquivo"> <span>QUANTIDADE DE HORAS POR</span> <span class = "com_arquivo">PERIODO</span></div> ',unsafe_allow_html=True)

                    
                    hrs_periodo = st.selectbox('SELECIONE O PERIODO', options=df['Periodo'].unique())

                    df_perio = df.query(
                        'Periodo == @hrs_periodo'
                    )

                    horas = transformar_horas(df_perio)
                    total_hrs = horas.sum()
                    Conversão_hrs = format_timedelta(total_hrs) #VALORES EM STRING


                    horas2 = transformar_horas(df)
                    total_hrs2 = horas2.sum()
                    Conversão_hrs2 = format_timedelta(total_hrs2) #VALORES EM STRING

                    #TRANSFORMANDO VALORES PARA SEGUNDO!
                    porcentagem = (total_hrs.total_seconds() / 3600) / (total_hrs2.total_seconds() / 3600) * 100


                    print("total_hrs_perio:", total_hrs2)
                    print("total_hrs_total:", total_hrs)

                    porcentagem2 = (total_hrs / total_hrs2) * 100
                    print("Porcentagem:", porcentagem)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f'<div class="usuario"><span>HORAS POR PERIODO</span><span class="value">{Conversão_hrs} hrs</span></div>', unsafe_allow_html=True)
                    with col2:  
                        st.markdown(f'<div class="usuario"><span>PORCENTAGEM PERÍODO</span><span class="value">{porcentagem:.2f}% hrs</span></div>', unsafe_allow_html=True)


                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = porcentagem,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "PORCENTAGEM POR PERIODO"},
                        gauge={'axis': {'range': [None, 100]}}))

                    st.plotly_chart(fig)


    else:
        st.markdown(f'<div class = "sem_arquivo"> <span>SEM ARQUIVO! SUBA A BASE DE DADOS PARA USUÁRIOS DO CEM</span> <span class = "com_valor">(FICHA DE ATENDIMENTO) <span></span> </div>', unsafe_allow_html=True)
        c = 'Browse files'
        st.markdown(f'<div class = "sem_arquivo"> <span>Para que consigamos mostrar o relatório necessita-se subir o arquivo em</span> <span class = "com_valor">{c} <span></span> </div>', unsafe_allow_html=True)
        st.markdown(f'<div class = "sem_arquivo"> <span>OBS: Este arquivo deve ser de "presença de usuários no CEM" em formato</span> <span class = "com_valor"> .CSV <span></span> </div>', unsafe_allow_html=True)

        

        st.toast('ESPERANDO ARQUIVO', icon='❗')
