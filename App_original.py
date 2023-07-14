import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import json

df = pd.read_csv('dados_discentes_comp_titulados_apenas.csv')

st.markdown('#### Explorando egressos de pós graduação da área de computação :nerd_face:')
st.markdown(""":mortar_board: Este projeto explora dados de egressos de pós-graduação da CAPES utilizando o Streamlit.""")
st.markdown(":open_book: O objetivo é demonstrar a funcionalidade do Streamlit com dados reais na disciplina de Estágio à Docência do mestrado da UNIRIO.")
st.markdown('---')

grau_academico = df['DS_GRAU_ACADEMICO_DISCENTE'].unique().tolist()
regiao = df['NM_REGIAO'].unique().tolist()

st.sidebar.markdown("### Filtre os egressos da pós de computação")
selecao_grau_academico = st.sidebar.multiselect('Filtre pelo grau acadêmico:', grau_academico, default=grau_academico)
selecao_regiao = st.sidebar.multiselect('Filtre pela região:', regiao, default=regiao)

st.sidebar.markdown("""
    <p style='font-size: 10px;'>
    Os dados utilizados neste projeto são de acesso público e foram obtidos através do portal de dados abertos da CAPES. 
    Estes dados são disponibilizados pela CAPES para promover a transparência e permitir a análise e a pesquisa acadêmica. 
    Para acessar diretamente esses dados, visite o portal de 
    <a href='https://dadosabertos.capes.gov.br/'>dados abertos da CAPES</a>.
    </p>
    """, unsafe_allow_html=True)

filtered_df = df[(df['NM_REGIAO'].isin(selecao_regiao) & (df['DS_GRAU_ACADEMICO_DISCENTE'].isin(selecao_grau_academico)))]


st.markdown('##### Quantos egressos da computação estamos tendo? :student:')


# Pré-processamento dos dados
grouped_df = filtered_df.groupby(['AN_BASE', 'NM_REGIAO']).size().reset_index(name='counts')

# Criando uma tabela dinâmica para o gráfico de barras empilhado
pivot_df = grouped_df.pivot(index='AN_BASE', columns='NM_REGIAO', values='counts').fillna(0)

# Normalizando as contagens para obter porcentagens
pivot_df_percentage = pivot_df.divide(pivot_df.sum(axis=1), axis=0) * 100

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Botão de rádio para alternar entre os gráficos
tipo_grafico = st.radio('Escolha o tipo de gráfico:', ('Valores absolutos', 'Porcentagem'))

if tipo_grafico == 'Porcentagem':
    # Gráfico de barras empilhadas com porcentagens
    pivot_df_percentage.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Porcentagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})
else:
    # Gráfico de barras empilhadas com valores absolutos
    pivot_df.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())

# E explorando universidades?

# Botão de expansão para a seleção de universidade
expander = st.expander("Deseja investigar alguma universidade em específico?")

# Lista de universidades
universidades = filtered_df['NM_ENTIDADE_ENSINO'].unique().tolist()

# Caixa de seleção para escolher uma universidade
universidade_selecionada = expander.selectbox('Selecione uma universidade:', universidades)

# Filtrando o dataframe para a universidade selecionada
df_universidade = filtered_df[filtered_df['NM_ENTIDADE_ENSINO'] == universidade_selecionada]

# Agrupando os dados por ano
grouped_df = df_universidade.groupby('AN_BASE').size().reset_index(name='counts')

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

with expander:
    # Gráfico de linhas para a universidade selecionada
    plt.figure(figsize=(15, 8))
    line_plot = sns.lineplot(x='AN_BASE', y='counts', data=grouped_df, linewidth=2.5)
    line_plot.set(xlabel='Ano', ylabel='Contagem')
    line_plot.set_ylim(bottom=0)  # Define o limite inferior do eixo y como 0
    plt.title('Gráfico de linha de contagem de egressos por ano para ' + universidade_selecionada, fontsize=14)

    # Para exibir o gráfico no Streamlit
    st.pyplot(plt.gcf())
st.markdown('---')
st.markdown('##### Qual dependência administrativa dos egressos? :bar_chart:')

# Pré-processamento dos dados
grouped_df_dep = filtered_df.groupby(['AN_BASE', 'DS_DEPENDENCIA_ADMINISTRATIVA']).size().reset_index(name='counts')

# Criando uma tabela dinâmica para o gráfico de barras empilhado
pivot_df_dep = grouped_df_dep.pivot(index='AN_BASE', columns='DS_DEPENDENCIA_ADMINISTRATIVA', values='counts').fillna(0)

# Normalizando as contagens para obter porcentagens
pivot_df_percentage_dep = pivot_df_dep.divide(pivot_df_dep.sum(axis=1), axis=0) * 100

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Botão de rádio para alternar entre os gráficos
tipo_grafico_selecionado_dep = st.radio('Escolha o tipo de gráfico a ser exibido:  ', ('Valores absolutos', 'Porcentagem'))

if tipo_grafico_selecionado_dep == 'Porcentagem':
    # Gráfico de barras empilhadas com porcentagens
    pivot_df_percentage_dep.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Porcentagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})
else:
    # Gráfico de barras empilhadas com valores absolutos
    pivot_df_dep.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())


st.markdown('---')
st.markdown('##### Qual a distribuição dos egressos de acordo com o status jurídico de suas instituições? :bar_chart:')

# Pré-processamento dos dados
grouped_df_jur = filtered_df.groupby(['AN_BASE', 'CS_STATUS_JURIDICO']).size().reset_index(name='counts')

# Criando uma tabela dinâmica para o gráfico de barras empilhado
pivot_df_jur = grouped_df_jur.pivot(index='AN_BASE', columns='CS_STATUS_JURIDICO', values='counts').fillna(0)

# Normalizando as contagens para obter porcentagens
pivot_df_percentage_jur = pivot_df_jur.divide(pivot_df_jur.sum(axis=1), axis=0) * 100

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Botão de rádio para alternar entre os gráficos
tipo_grafico_selecionado_jur = st.radio('Escolha o tipo de gráfico a ser exibido:   ', ('Valores absolutos', 'Porcentagem'))

if tipo_grafico_selecionado_jur == 'Porcentagem':
    # Gráfico de barras empilhadas com porcentagens
    pivot_df_percentage_jur.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Porcentagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})
else:
    # Gráfico de barras empilhadas com valores absolutos
    pivot_df_jur.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())

st.markdown('---')
st.markdown('##### Qual a idade dos nossos egressos de computação? :runner:')

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Configurando tamanho da figura
plt.figure(figsize=(15, 8))

# Botão de rádio para escolher se deseja visualizar outliers
show_outliers = st.radio('Deseja visualizar outliers?', ('Sim', 'Não'))

# Criando o boxplot
box_plot = sns.boxplot(x='AN_BASE', y='IDADE_APROX_DISCENTE', data=filtered_df, showfliers = (show_outliers == 'Sim'), color="#2a9d8f")
box_plot.set(xlabel='Ano', ylabel='Idade Aproximada')
plt.title('Distribuição das idades aproximadas dos egressos de computação por ano', fontsize=14)

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())

# Criando um painel expansível
expander_idade = st.expander("Deseja investigar a idade dos egressos de uma universidade específica?")

# Caixa de seleção para escolher uma universidade
universidade_selecionada_idade = expander_idade.selectbox('Selecione uma universidade abaixo:', universidades)

# Filtrando o dataframe para a universidade selecionada
df_universidade_idade = filtered_df[filtered_df['NM_ENTIDADE_ENSINO'] == universidade_selecionada_idade]

# Configurando tamanho da figura
plt.figure(figsize=(15, 8))

# Criando o boxplot para a universidade selecionada
box_plot = sns.boxplot(x='AN_BASE', y='IDADE_APROX_DISCENTE', data=df_universidade_idade, showfliers = (show_outliers == 'Sim'), color="#2a9d8f")
box_plot.set(xlabel='Ano', ylabel='Idade Aproximada')
plt.title('Distribuição das idades aproximadas dos egressos de computação por ano para ' + universidade_selecionada_idade, fontsize=14)

# Para exibir o gráfico no Streamlit
expander_idade.pyplot(plt.gcf())

st.markdown('---')
st.markdown('##### Quantos meses demora até a titulação dos egressos de computação? :alarm_clock:')

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Configurando tamanho da figura
plt.figure(figsize=(15, 8))

# Botão de rádio para escolher se deseja visualizar outliers
show_outliers_tempo = st.radio('Deseja visualizar os outliers?', ('Sim', 'Não'))

# Criando o boxplot
box_plot = sns.boxplot(x='AN_BASE', y='QT_MES_TITULACAO', data=filtered_df, showfliers = (show_outliers_tempo == 'Sim'), color="#2a9d8f")
box_plot.set(xlabel='Ano', ylabel='Meses até titulação')
box_plot.set_ylim(bottom=0)
plt.title('Distribuição do tempo dos egressos de computação por ano até a titulação', fontsize=14)

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())

# Criando um painel expansível
expander_tempo = st.expander("Deseja investigar o tempo até a titulação egressos de uma universidade específica?")

# Caixa de seleção para escolher uma universidade
universidade_selecionada_tempo = expander_tempo.selectbox('Selecione uma universidade da lista:', universidades)

# Filtrando o dataframe para a universidade selecionada
df_universidade_tempo = filtered_df[filtered_df['NM_ENTIDADE_ENSINO'] == universidade_selecionada_tempo]

# Configurando tamanho da figura
plt.figure(figsize=(15, 8))

# Criando o boxplot para a universidade selecionada
box_plot_uni = sns.boxplot(x='AN_BASE', y='QT_MES_TITULACAO', data=df_universidade_tempo, showfliers = (show_outliers_tempo == 'Sim'), color="#2a9d8f")
box_plot_uni.set(xlabel='Ano', ylabel='Meses até titulação')
box_plot_uni.set_ylim(bottom=0)
plt.title('Distribuição do tempo até a titulação dos egressos de computação por ano para ' + universidade_selecionada_tempo, fontsize=14)

# Para exibir o gráfico no Streamlit
expander_tempo.pyplot(plt.gcf())

st.markdown('---')
st.markdown('##### Quantos egressos existem de acordo com a nota CAPES do programa? :bar_chart:')

# Pré-processamento dos dados
grouped_df_programa = filtered_df.groupby(['AN_BASE', 'CD_CONCEITO_PROGRAMA']).size().reset_index(name='counts')

# Criando uma tabela dinâmica para o gráfico de barras empilhado
pivot_df_programa = grouped_df_programa.pivot(index='AN_BASE', columns='CD_CONCEITO_PROGRAMA', values='counts').fillna(0)

# Normalizando as contagens para obter porcentagens
pivot_df_percentage_programa = pivot_df_programa.divide(pivot_df_programa.sum(axis=1), axis=0) * 100

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Botão de rádio para alternar entre os gráficos
tipo_grafico_selecionado_programa = st.radio('Escolha o tipo de gráfico a ser exibido:', ('Valores absolutos', 'Porcentagem'))

if tipo_grafico_selecionado_programa == 'Porcentagem':
    # Gráfico de barras empilhadas com porcentagens
    pivot_df_percentage_programa.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Porcentagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})
else:
    # Gráfico de barras empilhadas com valores absolutos
    pivot_df_programa.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())


st.markdown('---')
st.markdown('##### Qual a participação de estrangeiros nos egressos? :airplane:')


# Pré-processamento dos dados
grouped_df_nacionalidade = filtered_df.groupby(['AN_BASE', 'DS_TIPO_NACIONALIDADE_DISCENTE']).size().reset_index(name='counts')

# Criando uma tabela dinâmica para o gráfico de barras empilhado
pivot_df_nacionalidade = grouped_df_nacionalidade.pivot(index='AN_BASE', columns='DS_TIPO_NACIONALIDADE_DISCENTE', values='counts').fillna(0)

# Normalizando as contagens para obter porcentagens
pivot_df_percentage_nacionalidade = pivot_df_nacionalidade.divide(pivot_df_nacionalidade.sum(axis=1), axis=0) * 100

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

# Botão de rádio para alternar entre os gráficos
tipo_grafico_nacionalidade = st.radio('Escolha o tipo de gráfico :', ('Valores absolutos', 'Porcentagem'))

if tipo_grafico_nacionalidade == 'Porcentagem':
    # Gráfico de barras empilhadas com porcentagens
    pivot_df_percentage_nacionalidade.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Porcentagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})
else:
    # Gráfico de barras empilhadas com valores absolutos
    pivot_df_nacionalidade.plot(kind='bar', stacked=True, figsize=(15, 8), edgecolor="0.2")
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.title('Gráfico de barras empilhadas de contagem de egressos por ano e região', fontsize=14)
    plt.legend(loc='lower right', prop={'size': 10})

# Para exibir o gráfico no Streamlit
st.pyplot(plt.gcf())

# E explorando universidades?

# Botão de expansão para a seleção de universidade
expander_nacionalidade = st.expander("Deseja investigar alguma universidade em específico?")

# Lista de universidades
universidades = filtered_df['NM_ENTIDADE_ENSINO'].unique().tolist()

# Caixa de seleção para escolher uma universidade
universidade_selecionada_nacionalidade = expander_nacionalidade.selectbox('Selecione uma universidade :', universidades)

# Filtrando o dataframe para a universidade selecionada
df_universidade_nacionalidade = filtered_df[(filtered_df['NM_ENTIDADE_ENSINO'] == universidade_selecionada_nacionalidade) & (filtered_df['DS_TIPO_NACIONALIDADE_DISCENTE'] == 'ESTRANGEIRO')]



# Agrupando os dados por ano
grouped_df_nacionalidade = df_universidade_nacionalidade.groupby('AN_BASE').size().reset_index(name='counts')

# Definindo um tema e inicializando uma figura
sns.set_theme(style="whitegrid")

with expander_nacionalidade:
    # Gráfico de linhas para a universidade selecionada
    plt.figure(figsize=(15, 8))
    line_plot_nacionalidade = sns.lineplot(x='AN_BASE', y='counts', data=grouped_df_nacionalidade, linewidth=2.5)
    line_plot.set(xlabel='Ano', ylabel='Contagem')
    line_plot.set_ylim(bottom=0)  # Define o limite inferior do eixo y como 0
    plt.title('Gráfico de linha de contagem de egressos por ano para ' + universidade_selecionada_nacionalidade, fontsize=14)

    # Para exibir o gráfico no Streamlit
    st.pyplot(plt.gcf())

st.markdown('---')
st.markdown('##### Que tal explorar um pouco mais os dados brutos? :airplane:')

filtered_df[['AN_BASE', 'NM_GRANDE_AREA_CONHECIMENTO',
       'CD_AREA_AVALIACAO', 'NM_AREA_AVALIACAO', 'CD_ENTIDADE_CAPES',
       'CD_ENTIDADE_EMEC', 'SG_ENTIDADE_ENSINO', 'NM_ENTIDADE_ENSINO',
       'CS_STATUS_JURIDICO', 'DS_DEPENDENCIA_ADMINISTRATIVA',
       'NM_MODALIDADE_PROGRAMA', 'NM_GRAU_PROGRAMA', 'CD_PROGRAMA_IES',
       'NM_PROGRAMA_IES', 'NM_REGIAO', 'SG_UF_PROGRAMA',
       'NM_MUNICIPIO_PROGRAMA_IES', 'CD_CONCEITO_PROGRAMA',
       'CD_CONCEITO_CURSO', 'ID_PESSOA', 'TP_DOCUMENTO_DISCENTE',
       'NR_DOCUMENTO_DISCENTE', 'NM_DISCENTE',
       'NM_PAIS_NACIONALIDADE_DISCENTE', 'DS_TIPO_NACIONALIDADE_DISCENTE',
       'AN_NASCIMENTO_DISCENTE', 'DS_FAIXA_ETARIA',
       'DS_GRAU_ACADEMICO_DISCENTE', 'ST_INGRESSANTE', 'NM_SITUACAO_DISCENTE',
       'DT_MATRICULA_DISCENTE', 'DT_SITUACAO_DISCENTE', 'QT_MES_TITULACAO',
       'NM_TESE_DISSERTACAO', 'NM_ORIENTADOR', 'ID_ADD_FOTO_PROGRAMA',
       'ID_ADD_FOTO_PROGRAMA_IES', 'NM_ORIENTADOR_PRINCIPAL', 'PCPF', 'CHK',
       'ANO_MATRICULA_DISCENTE', 'IDADE_APROX_DISCENTE']]

st.markdown('##### Quer explorar mais? Que tal baixar os dados?')

csv = filtered_df.to_csv(index=False)
csv_bytes = csv.encode()

# Use a função st.download_button() para baixar o dataframe como um arquivo csv
st.download_button(
    label="Baixar dados como CSV",
    data=csv_bytes,
    file_name="dados_filtrados.csv",
    mime="text/csv",
)
