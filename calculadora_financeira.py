import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def calcular_parcelas(valor_total, numero_parcelas, taxa_juros_anual):
    taxa_juros_mensal = taxa_juros_anual / 12 / 100
    valor_parcela = valor_total * (taxa_juros_mensal / (1 - (1 + taxa_juros_mensal)**(-numero_parcelas)))
    juros_total = valor_parcela * numero_parcelas - valor_total
    return valor_parcela, juros_total

st.title('Calculadora de Financiamento')

valor_total = st.number_input('Valor total:', min_value=1, step=1)
numero_parcelas = st.number_input('Número de parcelas:', min_value=1, step=1, format='%d')
taxa_juros_anual = st.number_input('Taxa de juros anual (%):', min_value=1, step=1)
data_inicial = st.date_input('Data inicial do financiamento:')

if st.button('Calcular'):
    valor_parcela, juros_total = calcular_parcelas(valor_total, numero_parcelas, taxa_juros_anual)
    st.write(f'Valor de cada parcela: R$ {valor_parcela:.2f}')
    st.write(f'Total de juros pagos: R$ {juros_total:.2f}')

    df = pd.DataFrame({
        'Parcela': range(1, numero_parcelas + 1),
        'Valor Parcela': [valor_parcela] * numero_parcelas,
        'Juros': [valor_parcela * i - valor_total for i in range(1, numero_parcelas + 1)],
        'Saldo Devedor': [valor_total - valor_parcela * i for i in range(numero_parcelas)],
    })

    st.write(df)

    if st.button('Crie outro financiamento'):
        df.to_excel('resultados_financiamento.xlsx', index=False)
        st.success('Arquivo Excel gerado com sucesso!')