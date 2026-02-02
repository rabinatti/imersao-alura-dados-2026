import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Imersão Alura",
    page_icon="💻",
    layout="wide",
)

# Base da dados
df = pd.read_csv("https://raw.githubusercontent.com/rabinatti/imersao-alura-dados-2026/refs/heads/main/dados-imersao-final.csv")

# Limpeza em dados nulos (dado nulo devido a conversão de países no formato ISO2 para ISO3)
df['localizacao_iso3'] = df['localizacao_iso3'].fillna('XKX')

# Sidebar
st.sidebar.header("🔍 Filtros")

# Filtros

# Ano
anos_existentes = sorted(df['ano'].unique())
ano_selecionado = st.sidebar.multiselect('Ano', anos_existentes, default=anos_existentes)

# Senioridade
senioridades_existentes = sorted(df['senioridade'].unique())
senioridade_selecionado = st.sidebar.multiselect('Senioridade', senioridades_existentes, default=senioridades_existentes)

# Remoto
remotos_existentes = sorted(df['remoto'].unique())
remoto_selecionado = st.sidebar.multiselect('Remoto', remotos_existentes, default=remotos_existentes)

# Contrato
contratos_existentes = sorted(df['contrato'].unique())
contrato_selecionado = st.sidebar.multiselect('Contrato', contratos_existentes, default=contratos_existentes)

# Tamanho da Empresa
tamanhos_existentes = sorted(df['tamanho_empresa'].unique())
tamanho_selecionado = st.sidebar.multiselect('Tamanho da Empresa', tamanhos_existentes, default=tamanhos_existentes)

# País da Empresa
paises_existentes = sorted(df['localizacao_iso3'].unique())
pais_selecionado = st.sidebar.multiselect('Local da Empresa', paises_existentes, default=['BRA', 'USA'])

# Filtragem no Dataframe
df_filtrado = df[
    (df['ano'].isin(ano_selecionado)) &
    (df['senioridade'].isin(senioridade_selecionado)) &
    (df['remoto'].isin(remoto_selecionado)) &
    (df['contrato'].isin(contrato_selecionado)) &
    (df['tamanho_empresa'].isin(tamanho_selecionado)) &
    (df['localizacao_iso3'].isin(pais_selecionado))
]

# Título
st.title("💻 Imersão Alura - Análise Salarial de Profissionais de TI")
st.markdown("Análise dos salários dos profissionais de TI ao redor do mundo.")

# Métricas Principais
if not df_filtrado.empty:
    salario_medio = df_filtrado['salario_usd'].mean()
    salario_maximo = df_filtrado['salario_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio = 0
    salario_maximo = 0
    total_registros = 0
    cargo_mais_frequente = "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio em USD", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo em USD", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros}")
col4.metric("Cargo Mais Frequente", f"{cargo_mais_frequente}")

st.markdown("---")

# Gráficos
st.subheader("📊 Gráficos")

col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['salario_usd'].mean().nlargest(10).sort_values(ascending=False).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos com o maior salário",
            labels={'cargo': 'Cargo', 'salario_usd': 'Salário Médio em USD'},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para ser exibido, tente mudar os filtros")

with col_graph2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_usd',
            nbins=30,
            title="Distribuição dos Salários",
            labels={'salario_usd': 'Salário em USD', 'count': 'Número de Profissionais'},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        grafico_hist.update_layout(
            title_x=0.1,
            yaxis_title='Número de Profissionais',
        )
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para ser exibido, tente mudar os filtros")

col_graph3, col_graph4 = st.columns(2)

with col_graph3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['Tipo de trabalho', 'quantidade']

        grafico_remoto = px.pie(
            remoto_contagem,
            names = 'Tipo de trabalho',
            values = 'quantidade',
            title="Distribuição entre trabalho remoto e presencial",
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para ser exibido, tente mudar os filtros")

with col_graph4:
    if not df_filtrado.empty:
        media_salario_pais = df_filtrado.groupby('localizacao_iso3')['salario_usd'].mean().reset_index()
        grafico_paises = px.choropleth(
            media_salario_pais,
            locations='localizacao_iso3',
            color='salario_usd',
            color_continuous_scale='orrd',
            title="Média Salarial por País",
            labels={'localizacao_iso3': 'País', 'salario_usd': 'Salário Médio em USD'},
        )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para ser exibido, tente mudar os filtros")

st.markdown("---")

st.subheader("Tabela de dados")
st.dataframe(df_filtrado)
