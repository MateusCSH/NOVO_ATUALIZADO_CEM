import streamlit as st
import pandas as pd
from datetime import datetime as dt
from Notebook_aux import transformar_horas, format_timedelta
import plotly.graph_objects as go
from service.grap  import Quantidade_periodo
from service.aux_main2_usu_hrs_perio import graf, total_time, selec_peri



def cont_usuários():

    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)
    
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
            horas1, minutos1 = format_timedelta(total_sum) 
            qtd_pessoas = len(df['Nome'])

            st.markdown(f'<div class="sem_arquivo"> <span class="tex_info">QUANTIDADE DE HORAS</span> <span class = "com_arquivo">GERAL</span></div> ',unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="usuario"><span>HORAS ACUMULADAS</span><span class="value">{horas1}:{minutos1:02d} hrs</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="usuario"><span>QUANTIDADE DE PESSOAS</span><span class="value">{qtd_pessoas}</span></div>', unsafe_allow_html=True)


            
############ FAZENDO A PARTE DE MOTIVO ###################
            # MOTIVO -> ESTUDO
            h_estudo_E = df[df['Motivo'] == 'ESTUDO']           

            horas_por_motivo_E = transformar_horas(h_estudo_E)
            total_hrs_motivo_E = horas_por_motivo_E.sum()
            horas_motivo_E, minutos_motivo_E = format_timedelta(total_hrs_motivo_E)
            

            #Ctrl + del apaga os espaços até a frase
            
            # MOTIVO -> REUNIÃO
            h_estudo_R = df[df['Motivo'] == 'REUNIÃO']           

            horas_por_motivo_R = transformar_horas(h_estudo_R)
            total_hrs_motivo_R = horas_por_motivo_R.sum()
            horas_motivo_R, minutos_motivo_R = format_timedelta(total_hrs_motivo_R)

            # MOTIVO -> ENPRO-JR
            h_estudo_EJ = df[df['Motivo'] == 'ENPRO-JR']           

            horas_por_motivo_EJ = transformar_horas(h_estudo_EJ)
            total_hrs_motivo_EJ = horas_por_motivo_EJ.sum()
            horas_motivo_EJ, minutos_motivo_EJ = format_timedelta(total_hrs_motivo_EJ)

            # MOTIVO -> DINAMICA
            h_estudo_D = df[df['Motivo'] == 'DINAMICA']
            horas_por_motivo_D = transformar_horas(h_estudo_D)
            total_hrs_motivo_D = horas_por_motivo_D.sum()
            horas_motivo_D, minutos_motivo_D = format_timedelta(total_hrs_motivo_D)


            st.markdown(f'<div class="sem_arquivo"> <span class="tex_info">QUANTIDADE DE HORAS POR</span> <span class = "com_arquivo">MOTIVO</span></div> ',unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div class="usuario_motivo"><span class="tex_info">HORAS ESTUDO</span><span class="value_motivo">{horas_motivo_E}:{minutos_motivo_E:02d} hrs</span></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="usuario_motivo"><span class="tex_info">HORAS ENP_JUNIOR</span><span class="value_motivo">{horas_motivo_EJ}:{minutos_motivo_EJ:02d} hrs</span></div>', unsafe_allow_html=True)
            
            
            with col2:
                st.markdown(f'<div class="usuario_motivo"><span class="tex_info">HORAS REUNIÃO</span><span class="value_motivo">{horas_motivo_R}:{minutos_motivo_R:02d} hrs</span></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="usuario_motivo"><span class="tex_info">HORAS DINÂMICA</span><span class="value_motivo">{horas_motivo_D}:{minutos_motivo_D:02d} hrs</span></div>', unsafe_allow_html=True)
        
        
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

            


            Pessoas_periodo, Horas_periodo, top3 = st.tabs(['Quantidade de pessoas', 'Quantidade Horas por periodo', 'Top 3'])


            
           
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

                    # Convertendo e somando as horas somente do periodo desejado
                    horas = transformar_horas(df_perio)
                    total_hrs = horas.sum()
                    horas_periodo, minutos_periodo = format_timedelta(total_hrs) #VALORES EM STRING

                    # Convertendo e somando as horas de todo o dataframe
                    horas2 = transformar_horas(df)
                    total_hrs2 = horas2.sum()
                    

                    #TRANSFORMANDO VALORES PARA SEGUNDO!
                    porcentagem = (total_hrs.total_seconds() / 3600) / (total_hrs2.total_seconds() / 3600) * 100


                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f'<div class="usuario"><span>HORAS POR PERIODO</span><span class="value">{horas_periodo}:{minutos_periodo:02d} hrs</span></div>', unsafe_allow_html=True)
                    with col2:  
                        st.markdown(f'<div class="usuario"><span>PORCENTAGEM PERÍODO</span><span class="value">{porcentagem:.2f}% hrs</span></div>', unsafe_allow_html=True)


                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = porcentagem,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "PORCENTAGEM POR PERIODO"},
                        gauge={'axis': {'range': [None, 100]}}))

                    st.plotly_chart(fig)

                    
                    # MELHORIA
                    a = df
                    df['Diferença'] = df['Fim'] - df['Inicio']

                    periodos = df['Periodo'].unique()
                    seconds_1 = df.query("Periodo == @hrs_periodo")['Diferença'].dt.total_seconds()

                    hr_min = seconds_1.apply(lambda x: divmod(x, 3600))
                    df['Horas'] = hr_min.apply(lambda x: x[0])
                    df['Segundos Restantes'] = hr_min.apply(lambda x: x[1])

                    df['Minutos'] = df['Segundos Restantes'] // 60

                    total_horas = df['Horas'].sum()
                    total_minutos = df['Minutos'].sum()

                    total_horas += total_minutos // 60
                    total_minutos = total_minutos % 60
                    hrs_m = total_horas + float(total_minutos/10)

                    # Chamando funcão que paga as horas totais.
                    total_timer = total_time(a) 
                    porcent_peri = hrs_m / total_timer

                    op = st.selectbox('Selecione o periodo de comparação', options=df['Periodo'].unique())

                    comp = selec_peri(a, op)
                    porcent_comp = (hrs_m / comp) * 100 - 100


                    with st.expander("Comparação", icon="📊"):
                        col1, col2, col3 = st.columns(3)
                        with col2:
                            with st.container(border=True):
                                title = f"HORAS {hrs_periodo}"                            
                                st.metric(label=title, value=hrs_m, delta=f'{porcent_comp:.2f}%') 

                                resultado = f"⬆ {porcent_comp:.1f}%" if porcent_peri > 0 else f"⬇ {porcent_comp:.1f}%"
                                
                                st.markdown(resultado)              
                                
                        

                        graf(a)

                
                with top3:                  

                    lista = [p1, p2, p3, p4, p5]
                    lista2 = {
                        '1º PERIODO': p1,
                        '2º PERIODO': p2,
                        '3º PERIODO': p3,
                        '4º PERIODO': p4,
                        '5º PERIODO': p5,
                        '6º PERIODO': p6,
                        '7º PERIODO': p7,
                        '8º PERIODO': p8,
                        '9º PERIODO': p9,
                        '10º PERIODO': p10
                    }            

                    

                    list_ord = sorted(lista2.values(), reverse=True)
                    first = list_ord[0]
                    second = list_ord[1]
                    third = list_ord[2]

                    

                    primeira_maior_chave = [k for k, v in lista2.items() if v == first][0]
                    segundo_maior_chave = [k for k, v in lista2.items() if v == second][0]
                    terceiro_maior_chave = [k for k, v in lista2.items() if v == third][0]

                    st.markdown(f'<div class = "sem_arquivo"> <span> CLASSIFICAÇÃO POR </span> <span class = "com_arquivo">PERIODO</span></div>', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                            <div class="flex-container">
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-large"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{primeira_maior_chave}</span>
                                        <span>{first}</span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-group"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{segundo_maior_chave}</span>
                                        <span>{second} </span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-users"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{terceiro_maior_chave}</span>
                                        <span>{third} </span>
                                    </div>
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)

    


    else:
        st.markdown(f'<div class = "sem_arquivo"> <span>SEM ARQUIVO! SUBA A BASE DE DADOS PARA USUÁRIOS DO CEM</span> <span class = "com_valor">(FICHA DE ATENDIMENTO) <span></span> </div>', unsafe_allow_html=True)
        c = 'Browse files'
        st.markdown(f'<div class = "sem_arquivo"> <span>Para que consigamos mostrar o relatório necessita-se subir o arquivo em</span> <span class = "com_valor">{c} <span></span> </div>', unsafe_allow_html=True)
        st.markdown(f'<div class = "sem_arquivo"> <span>OBS: Este arquivo deve ser de "presença de usuários no CEM" em formato</span> <span class = "com_valor"> .CSV <span></span> </div>', unsafe_allow_html=True)

        

        st.toast('ESPERANDO ARQUIVO', icon='❗')
