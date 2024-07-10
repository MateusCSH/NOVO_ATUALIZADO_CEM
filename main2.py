import pandas as pd
import streamlit as st
import plotly.express as px
from service.grap import grap_bar
from service.grap import view_img #NEW_IMG
from service.grapplotly import grap_plotly
from service.piegrap import pie_grap
import plotly.graph_objects as go
from main2_Parte2_usuários import cont_usuários #PARTE DE USUÁRIOS



#python -m venv venv
#.\venv\Scripts\activate
#pip freeze > .\requirements.txt
# pip install -r .\requirements.txt

# #import streamlit as st

# HTML_BANNER = """
#     <h1 style="color:red;">Olá, Mundo!</h1>
#     <p>Only Just an example.</p>
# """

# stc.html(HTML_BANNER)

st.set_page_config(page_title='Dashboard CEM')

with open("styles3.css", 'r', encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#https://www.youtube.com/watch?v=3Rp-ArQEmtA
#Como customizar aplicativos do Streamlit (Python) com CSS




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
            maxhoras = int(df_select['Horas'].max())
            qtdmoni = len(df_select['Nome'].unique())

            
            with col1:     
                st.markdown(f'<div class="metric"><span>HORAS ACUMULADAS</span><span class="value">{qtdhoras} hrs</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric"><span>HORAS MÁXIMA</span><span class="value">{maxhoras} hrs</span></div>', unsafe_allow_html=True)

            with col3:
                st.markdown(f'<div class="metric"><span>MONITORES</span><span class="value">{qtdmoni}</span></div>', unsafe_allow_html=True)

            #st.image('data:image/jpeg;base64,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')
        
            
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
                
                #st.dataframe(df_select2)

                


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


else:
    cont_usuários()
