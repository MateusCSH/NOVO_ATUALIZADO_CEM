
import pandas as pd
from datetime import datetime

def transformar_horas(df):
    
    v1 = df['Inicio']
    v2 = df['Fim']

    return v2 - v1

# Função para formatar timedelta como HH:MM
def format_timedelta(td):   #
    total_seconds = int(td.total_seconds()) #
    hours, remainder = divmod(total_seconds, 3600)  #
    minutes, _ = divmod(remainder, 60)  #
    return f"{hours:02}:{minutes:02}"   #


