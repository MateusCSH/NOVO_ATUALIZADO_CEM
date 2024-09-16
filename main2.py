import pandas as pd
import streamlit as st
import plotly.express as px
from service.grap import grap_bar
from service.grap import view_img #NEW_IMG
from service.grapplotly import grap_plotly
from service.piegrap import pie_grap
import plotly.graph_objects as go
from main2_Parte2_usuários import cont_usuários #PARTE DE USUÁRIOS





st.set_page_config(page_title='Dashboard CEM')

with open("styles3.css", 'r', encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Para usar ícones Font Awesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)



tipo = st.sidebar.selectbox('ESCOLHA O QUE DESEJA EFETUAR', options=['MONITOR','USUÁRIOS CEM'])

st.sidebar.markdown("""
    <div class="scroll">
        <div class="scroll_container">
            <div class="scroll_item"><img src="data:image/jpeg;base64,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" alt="mask1"></div>
            </div>
    </div>
    """, unsafe_allow_html=True)

if tipo == 'MONITOR':
    up = st.sidebar.file_uploader('Suba o arquivo', type='csv')


    if up is not None:

        df = pd.read_csv(up, header=None, sep=',').drop(0).drop(columns=0)
        df.rename(columns={1:'Nome',2:'Horas',3:'Motivo'}, inplace=True)
        df['Horas'] = df['Horas'].astype(int)

        

        name = st.sidebar.multiselect('Selecione os monitores:',
                                    options=sorted(df['Nome'].unique()),
                                    default=sorted(df['Nome'].unique()),
                                    placeholder='Selecione o arquivo!')
        
        df_select = df.query(
            'Nome == @name'
        )
        #df_select = df[df['Nome']==name]

        op = st.selectbox('**Opção:**',
                    ('Horas por Monitor','Horas por situação'),
                    index=None,
                    placeholder="Selecione a opção")

        st.write('Sua opção:', op)

        if op == 'Horas por Monitor':

            inf, melhor_de_3 = st.tabs(['INFO. GERAL','HALL DOS MONITORES'])

            with inf:
                view_img()
                #grap_bar(df_select,'Nome', 'Horas')
                grap_plotly(df_select, 'Horas', 'Nome')
    
    
                st.info('Informações')
                st.subheader('',divider='rainbow')
                col1, col2, col3 = st.columns(3)
                qtdhoras = df_select['Horas'].sum()
                # maxhoras = int(df_select['Horas'].max())
                qtdmoni = len(df_select['Nome'].unique())
    
                pessoa_max_hr = df_select.groupby('Nome')['Horas'].sum().reset_index()
                max_hr = pessoa_max_hr.nlargest(1,'Horas')
                qtd_hr_max = max_hr['Horas'].iloc[0]

                

                # MÉDIA E DESVIO PADRÃO
                med = df_select['Horas'].mean()
                dvp = df_select['Horas'].std()

                # HRS MÍNIMA
                min_hr = pessoa_max_hr.nlargest(qtdmoni, 'Horas')
                qtd_hrs_min = min_hr['Horas'].iloc[qtdmoni-1]
                
    
                
                with col1:     
                    st.markdown(f'<div class="metric"><span>HORAS ACUMULADAS</span><span class="value">{qtdhoras} hrs</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric"><span>MÉDIA HORAS</span><span class="value">{med:.2f} hrs</span></div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f'<div class="metric"><span>HORAS MÁXIMA</span><span class="value">{qtd_hr_max} hrs</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric"><span>HORAS MÍNIMA</span><span class="value">{qtd_hrs_min} hrs</span></div>', unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f'<div class="metric"><span>MONITORES</span><span class="value">{qtdmoni}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric"><span>DESV. PADRÃO</span><span class="value">{dvp:.2f}</span></div>', unsafe_allow_html=True)
    
            
                
                st.text('')
                nome = st.selectbox('Escolha o monitor',
                                        (sorted(df['Nome'].unique())))            
        
    
        #-----------------------
                if nome:
                    df_select2 = df.query('Nome == @nome')
                    hrs_total = df['Horas'].sum()
                    hrs_selecionada = df_select2['Horas'].sum()
                    maxhoras = int(df_select2['Horas'].max())
                    porcentagem = (hrs_selecionada / hrs_total) * 100 if hrs_total != 0 else 0
    
                    col1, col2 = st.columns(2)
                    with col1:                
                        st.metric('Total Horas',hrs_selecionada,)
                    with col2:
                        st.metric('Máx horas',maxhoras,)
    
                    st.markdown(f'<div class="sem_arquivo"> <span>PARTICIPAÇÃO PERCENTUAL POR</span> <span class = "com_arquivo">MONITOR</span></div> ',unsafe_allow_html=True)
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",    #gráfico de gauge (ou medidor) + número
                        value=porcentagem,
                        title={'text': "Percentual de Horas [DF ORIGINAL]"},
                        gauge={'axis': {'range': [None, 100]}}, #Define as configurações do gauge. Nesse caso, estamos definindo a escala do gauge para ir de 0 a 100.
                        domain={'x': [0, 1], 'y': [0, 1]}   #Define a área do gráfico que será ocupada pelo gauge. Nesse caso, estamos definindo que o gauge ocupará toda a área do gráfico (x e y vão de 0 a 1).
                    ))
    
                    st.plotly_chart(fig)
                
            with melhor_de_3:

                    df_agrupado = df_select.groupby('Nome')['Horas'].sum().reset_index()
                    people = df_agrupado.nlargest(3,'Horas')
                    people_name = people['Nome'].iloc[0]
                    people_hrs = people['Horas'].iloc[0]
                    people_name2 = people['Nome'].iloc[1]
                    people_hrs2 = people['Horas'].iloc[1]
                    people_name3 = people['Nome'].iloc[2]
                    people_hrs3 = people['Horas'].iloc[2]

                    st.markdown(f'<div class="sem_arquivo"> <span>CLASSIFICAÇÃO</span> <span class = "com_valor">HORAS TOTAIS</span></div> ',unsafe_allow_html=True)

                    st.markdown(f'''
                            <div class="flex-container">
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-large"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people_name}</span>
                                        <span>{people_hrs} hrs</span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-group"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people_name2}</span>
                                        <span>{people_hrs2} hrs</span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-users"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people_name3}</span>
                                        <span>{people_hrs3} hrs</span>
                                    </div>
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)


                
                    # CAPTANDO OS 3 MAIORES MONITORES RELACIOANDO A HORAS DE MONITORIA ---> TROCAR DPS PAAR OUTRA
                    df_agrupado = df_select.query('Motivo == "Monitoria"').groupby('Nome')['Horas'].sum().reset_index()
                    people = df_agrupado.nlargest(3, 'Horas')


                    st.markdown(f'<div class="sem_arquivo"> <span>CLASSIFICAÇÃO POR HORAS DE </span> <span class = "com_valor">MONITORIA</span></div> ',unsafe_allow_html=True)

                    st.markdown(f'''
                            <div class="flex-container">
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-large"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people['Nome'].iloc[0]}</span>
                                        <span>{people["Horas"].iloc[0]} hrs</span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-user-group"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people['Nome'].iloc[1]}</span>
                                        <span>{people["Horas"].iloc[1]} hrs</span>
                                    </div>
                                </div>
                                <div class="flex-box">
                                    <div class="icon-container">
                                        <i class="fa-solid fa-users"></i>
                                    </div>
                                    <div class="text-container">
                                        <span>{people['Nome'].iloc[2]}</span>
                                        <span>{people["Horas"].iloc[2]} hrs</span>
                                    </div>
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)

        

    #--------------


        if op == 'Horas por situação':

            bar, inf = st.tabs(['GRÁFICOS','INFORMAÇÕES'])
            
            with bar:

                st.markdown('<div class = "sem_arquivo"> <span>GRÁFICO DE HORAS POR</span> <span class = "com_valor">UTILIZAÇÃO</span> </div>', unsafe_allow_html=True)
                
                grap_plotly(df_select, 'Horas','Motivo')

                ########################################

                st.subheader('',divider='rainbow')
                st.markdown(f'<div class = "sem_arquivo"> <span>PERCENTUAL POR CATEGORIA</span> <span class = "com_valor"> GRÁFICOS <span></span> </div>', unsafe_allow_html=True)


                titulo = 'Gráfico de porcentagem - horas por situação'
                pie_grap(df_select, 'Horas', 'Motivo', titulo)

                fig = px.bar(
                            df_select,
                            x='Nome', 
                            y='Horas', 
                            color='Motivo', 
                            barmode='group', 
                            title='Horas por Nome e Motivo',
                            text=None)

                st.plotly_chart(fig)


                st.subheader('',divider='rainbow')
                ##############################

            with inf:

                st.markdown(f'<div class ="sem_arquivo"><span>INFORMAÇÕES POR</span> <span class="com_valor">MOTIVO</span> </div>', unsafe_allow_html=True)
                st.subheader('',divider='rainbow')
                
                col1, col2, col3, col4 = st.columns(4)
                reun = df_select[df_select['Motivo'] == 'Reunião']['Horas'].sum()
                monin = df_select[df_select['Motivo'] == 'Monitoria']['Horas'].sum()
                aula = df_select[df_select['Motivo'] == 'Aula']['Horas'].sum()
                estu = df_select[df_select['Motivo'] == 'Estudos']['Horas'].sum()


                porcent_reun = (reun / (df_select['Horas'].sum())) * 100
                porcent_moni = (monin / (df_select['Horas'].sum())) * 100
                porcent_aula = (aula / (df_select['Horas'].sum())) * 100
                porcent_estu = (estu / (df_select['Horas'].sum())) * 100

                st.subheader('', divider='rainbow')

                with col1:              
                
                    st.markdown(f'<div class = "metric"> <span>Reunião </span> <span class="value">{reun} hrs</span> </div>', unsafe_allow_html=True)
                    st.markdown(f'<div class = "metric"> <span>Reunião </span> <span class="value">{porcent_reun:.2f} %</span> </div>', unsafe_allow_html=True)

                with col2:

                    st.markdown(f'<div class = "metric"> <span>Monitoria </span> <span class="value">{monin} hrs</span> </div>', unsafe_allow_html=True)
                    st.markdown(f'<div class = "metric"> <span>Monitoria </span> <span class="value">{porcent_moni:.2f} %</span> </div>', unsafe_allow_html=True)


                with col3:

                    st.markdown(f'<div class = "metric"> <span>Aula </span> <span class="value">{aula} hrs</span> </div>', unsafe_allow_html=True)
                    st.markdown(f'<div class = "metric"> <span>Aula </span> <span class="value">{porcent_aula:.2f} %</span> </div>', unsafe_allow_html=True)


                with col4:           

                    st.markdown(f'<div class = "metric"> <span>Estudo </span> <span class="value">{estu} hrs</span> </div>', unsafe_allow_html=True)
                    st.markdown(f'<div class = "metric"> <span>Estudo </span> <span class="value">{porcent_estu:.2f} %</span> </div>', unsafe_allow_html=True)



                # CRIA TABELA COM .PIVOT
        
        #df_select = df[df['Nome']==name]

    else:

        c = 'Browse files'


        st.markdown(f'<div class = "sem_arquivo"> <span>Para que consigamos mostrar o relatório necessita-se subir o arquivo em</span> <span class = "com_valor">{c} <span></span> </div>', unsafe_allow_html=True)
        st.markdown(f'<div class = "sem_arquivo"> <span>OBS: Arquivo deve ser em formato</span> <span class = "com_valor"> .CSV <span></span> </div>', unsafe_allow_html=True)

        

        st.toast('ESPERANDO ARQUIVO', icon='❗')

        
        st.markdown(f'''
                    <div class="box">
                    <i class="fa-solid fa-user"></i>
                    <span>NOME DO LUGAR</span>
                    <span>ESPAÇO</span>                    
                    <div class="msg">ACESSE NOSSO INSTA</div>
                    <span><a href="https://www.youtube.com" target="_blank">YouTube</a></span>
                    </div>
                    ''', unsafe_allow_html=True)        

else:
    cont_usuários()
