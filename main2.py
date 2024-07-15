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




tipo = st.sidebar.selectbox('ESCOLHA O QUE DESEJA EFETUAR', options=['MONITOR','USUÁRIOS CEM'])

st.sidebar.markdown("""
    <div class="scroll">
        <div class="scroll_container">
            <div class="scroll_item"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-gVhOMXs1Rv5jChE2bdB3ptM5PZWVO-5Mdg&s" alt="mask1"></div>
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

            
            with col1:     
                st.markdown(f'<div class="metric"><span>HORAS ACUMULADAS</span><span class="value">{qtdhoras} hrs</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric"><span>HORAS MÁXIMA</span><span class="value">{qtd_hr_max} hrs</span></div>', unsafe_allow_html=True)

            with col3:
                st.markdown(f'<div class="metric"><span>MONITORES</span><span class="value">{qtdmoni}</span></div>', unsafe_allow_html=True)

        
            
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
                

                


    #--------------


        if op == 'Horas por situação':

            bar, inf, pizza = st.tabs(['BARRAS','INFORMAÇÕES','PIZZA'])
            
            with bar:

                st.markdown('<div class = "sem_arquivo"> <span>GRÁFICO DE HORAS POR</span> <span class = "com_valor">UTILIZAÇÃO</span> </div>', unsafe_allow_html=True)
                
                grap_plotly(df_select, 'Horas','Motivo')



            with inf:

                st.markdown(f'<div class ="sem_arquivo"><span>INFORMAÇÕES POR</span> <span class="com_valor">MOTIVO</span> </div>', unsafe_allow_html=True)
                st.subheader('',divider='rainbow')
                
                col1, col2, col3, col4 = st.columns(4)
                reun = df_select[df_select['Motivo'] == 'Reunião']['Horas'].sum()
                monin = df_select[df_select['Motivo'] == 'Monitoria']['Horas'].sum()
                aula = df_select[df_select['Motivo'] == 'Aula']['Horas'].sum()
                estu = df_select[df_select['Motivo'] == 'Estudos']['Horas'].sum()

                st.subheader('', divider='rainbow')

                with col1:              
                
                    st.markdown(f'<div class = "metric"> <span>Horas - reunião </span> <span class="value">{reun} hrs</span> </div>', unsafe_allow_html=True)

                with col2:

                    st.markdown(f'<div class = "metric"> <span>Horas - monitoria </span> <span class="value">{monin} hrs</span> </div>', unsafe_allow_html=True)


                with col3:

                    st.markdown(f'<div class = "metric"> <span>Horas - aula </span> <span class="value">{aula} hrs</span> </div>', unsafe_allow_html=True)


                with col4:           

                    st.markdown(f'<div class = "metric"> <span>Horas - estudo </span> <span class="value">{estu} hrs</span> </div>', unsafe_allow_html=True)




            with pizza:
        
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

                # CRIA TABELA COM .PIVOT
        
        #df_select = df[df['Nome']==name]

    else:

        c = 'Browse files'


        st.markdown(f'<div class = "sem_arquivo"> <span>Para que consigamos mostrar o relatório necessita-se subir o arquivo em</span> <span class = "com_valor">{c} <span></span> </div>', unsafe_allow_html=True)
        st.markdown(f'<div class = "sem_arquivo"> <span>OBS: Arquivo deve ser em formato</span> <span class = "com_valor"> .CSV <span></span> </div>', unsafe_allow_html=True)

        

        st.toast('ESPERANDO ARQUIVO', icon='❗')

        
        st.markdown(f'''<div class="box"> 
                    <i class="fa-solid fa-user"></i> 
                    <span>LUGAR</span>
                    <span>NOME ESPAÇO</span>
                    <button class = "social"> INSTAGRAM </button>
                    <div class="msg">www.site.com.br</div>
                    </div>  ''', unsafe_allow_html=True)        

else:
    cont_usuários()
