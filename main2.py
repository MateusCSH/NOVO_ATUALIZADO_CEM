import pandas as pd
import streamlit as st
import plotly.express as px
from service.grap import grap_bar
from service.grap import view_img #NEW_IMG
from service.grapplotly import grap_plotly
from service.piegrap import pie_grap
import plotly.graph_objects as go
from main2_Parte2_usuários import cont_usuários #PARTE DE USUÁRIOS





st.set_page_config(page_title='Dashboard CEM', layout='wide')

with open("styles3.css", 'r', encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Para usar ícones Font Awesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)



tipo = st.sidebar.selectbox('ESCOLHA O QUE DESEJA EFETUAR', options=['MONITOR','USUÁRIOS CEM'])

st.sidebar.markdown("""
    <div class="scroll">
        <div class="croll_container">
            <div class="eng_p"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTikPGflZbccXzUNha-7M-5ZpfizmvK8vwpIw&s" alt=""></div>
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
                    ('Horas por Monitor','Horas por situação', 'Comparação'),
                    index=None,
                    placeholder="Selecione a opção")

        st.write('Sua opção:', op)

        if op == 'Horas por Monitor':

            inf, melhor_de_3 = st.tabs(['INFO. GERAL','HALL DOS MONITORES'])

            with inf:
                view_img()
                # Usei reset_index() para transformar a série em um DataFrame, já que resultante do groupby não e um Dataframe.
                df_gb = df_select.groupby('Nome')['Horas'].sum().reset_index()
                #grap_bar(df_select,'Nome', 'Horas')
                grap_plotly(df_gb, 'Horas', 'Nome')
    
    
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
                st.markdown(f'<div class="sem_arquivo"> <span>PARTICIPAÇÃO PERCENTUAL POR</span> <span class = "com_arquivo">MONITOR</span></div> ',unsafe_allow_html=True)
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
    
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",    #gráfico de gauge (ou medidor) + número
                        value=porcentagem,
                        title={'text': "Percentual de Horas em relação ao total"},
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
                df_bg_st = df.groupby('Motivo')['Horas'].sum().reset_index()
                grap_plotly(df_bg_st, 'Horas','Motivo')

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

                st.markdown(f'<div class ="sem_arquivo"><span>INFORMAÇÕES HORAS POR</span> <span class="com_valor">MOTIVO</span> </div>', unsafe_allow_html=True)
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

        if op == 'Comparação':
            
            c1, c2 = st.columns(2)
            with c1:
                dtf3 = st.file_uploader('Mês anterior', type=['csv'])
            with c2:
                dtf4 = st.file_uploader('Mês atual', type=['csv'])
            
            if dtf3 and dtf4:

                df3 = pd.read_csv(dtf3, header=None, sep=',').drop(0).drop(columns=0)
                df3.columns = ['Nome', 'Horas', 'Motivo']
                df3['Horas'] = df3['Horas'].astype(int)

                df4 = pd.read_csv(dtf4, header=None, sep=',').drop(0).drop(columns=0)
                df4.columns = ['Nome', 'Horas', 'Motivo']
                df4['Horas'] = df4['Horas'].astype(int)

                dataframework = {
                    'Nome': ['M4S3', 'M5S2'],
                    'Horas': [df3['Horas'].sum(), df4['Horas'].sum()]
                }

                st.text(dataframework)


                # Criando o gráfico de barras agrupadas
                fig = px.bar(data_frame=dataframework, 
                            x='Nome', 
                            y='Horas', 
                            text='Horas',  # Adiciona rótulos de dados
                            color='Nome',  # Altera a cor das barras
                            color_discrete_sequence=['#636EFA', '#EF553B'],  # Cores personalizadas
                            title='Comparação entre Dois DataFrames')


                fig.update_traces(textfont_size=16, textfont_color='white')

                # Removendo grades de fundo
                fig.update_layout(
                    xaxis=dict(showgrid=False),  # Remove grades do eixo X
                    yaxis=dict(showgrid=False),

                    xaxis_tickfont_size=14,  # Remove grades do eixo Y
                    yaxis_tickfont_size=14,  # Aumenta o tamanho dos rótulos do eixo Y
                    legend_font_size=14,  # Aumenta o tamanho da fonte da legenda
                    xaxis_title_font_size=18,  # Aumenta o tamanho do rótulo do eixo X
                    yaxis_title_font_size=18,  # Aumenta o tamanho do rótulo do eixo Y
                    
                )

                # Exibindo o gráfico no Streamlit
                st.plotly_chart(fig)
                print('a')


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
