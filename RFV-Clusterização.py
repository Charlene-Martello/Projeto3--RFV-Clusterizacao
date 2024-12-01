import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from datetime import datetime
from io import BytesIO
from mpl_toolkits.mplot3d import Axes3D

# Configurações do Streamlit
st.set_page_config(page_title="Análise de Clusters RFV", layout="wide")
st.write("Para iniciar a análise, suba o arquivo na caixa ao lado.")

# Função para carregar e processar os dados
@st.cache_data
def carregar_dataframe(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, infer_datetime_format=True, parse_dates=['DiaCompra'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def carregar_dados(df):
    dia_atual = datetime(2021, 12, 9)
    # Calcular recência
    df_recencia = df.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
    df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
    df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
    # Calcular frequência
    df_frequencia = df.groupby('ID_cliente').size().reset_index(name='Frequencia')
    # Calcular valor total
    df_valor = df.groupby('ID_cliente')['ValorTotal'].sum().reset_index()
    df_valor.columns = ['ID_cliente', 'Valor']
    # Combinar as métricas
    df_rfv = df_recencia.merge(df_frequencia, on='ID_cliente').merge(df_valor, on='ID_cliente')
    return df_rfv.set_index('ID_cliente')

# Função para padronizar os dados
def padronizar_dados(df, colunas):
    scaler = StandardScaler()
    df_padronizado = pd.DataFrame(scaler.fit_transform(df[colunas]), columns=colunas, index=df.index)
    return df_padronizado

# Função para plotar o método do cotovelo
def plotar_cotovelo(df_padronizado, max_clusters=15):
    inertia_values = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df_padronizado)
        inertia_values.append(kmeans.inertia_)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, max_clusters + 1), inertia_values, 'bo-', markersize=8)
    ax.set_xlabel('Número de Clusters (k)')
    ax.set_ylabel('Soma das Distâncias Quadradas (Inércia)')
    ax.set_title('Método do Cotovelo')
    ax.grid()
    return fig

# Função para calcular e plotar a silhueta
def calcular_silhueta(df_padronizado, max_clusters=15):
    silhouette_scores = []
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(df_padronizado)
        score = silhouette_score(df_padronizado, labels)
        silhouette_scores.append(score)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
    ax.set_xlabel('Número de Clusters')
    ax.set_ylabel('Pontuação da Silhueta')
    ax.set_title('Pontuação da Silhueta')
    ax.grid()
    return fig, silhouette_scores

# Função para plotar clusters em 3D
def plotar_clusters_3d(df_padronizado, labels, colunas):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df_padronizado[colunas[0]], df_padronizado[colunas[1]], df_padronizado[colunas[2]], c=labels, cmap='viridis')
    ax.set_xlabel(colunas[0])
    ax.set_ylabel(colunas[1])
    ax.set_zlabel(colunas[2])
    return fig

# Interface Streamlit
st.title("Análise de Clusters RFV")
st.sidebar.header("Configurações Da Página")
st.sidebar.image("clust.jpg")
caminho_arquivo = st.sidebar.file_uploader("Carregue o arquivo CSV:", type=['csv'])

if caminho_arquivo:
    # Carregar dados brutos
    df = carregar_dataframe(caminho_arquivo)
    if df is not None:
        st.write("### Dados Brutos:")
        st.write(df.head())

        # Gerar dados RFV
        df_rfv = carregar_dados(df)
        st.write("### Dados RFV (Recência, Frequência e Valor):")
        st.write(df_rfv.head())

        # Padronizar os dados
        variaveis_rfv = ['Recencia', 'Frequencia', 'Valor']
        df_rfv_padronizado = padronizar_dados(df_rfv, variaveis_rfv)
        st.write("### Dados Padronizados:")
        st.write(df_rfv_padronizado.head())

        # Método do Cotovelo
        st.write("### Método do Cotovelo")
        max_clusters = st.sidebar.slider("Máximo de clusters", 5, 20, 15)
        fig_cotovelo = plotar_cotovelo(df_rfv_padronizado, max_clusters)
        st.pyplot(fig_cotovelo)

        # Método da Silhueta
        st.write("### Método da Silhueta")
        fig_silhueta, silhouette_scores = calcular_silhueta(df_rfv_padronizado, max_clusters)
        melhor_k = silhouette_scores.index(max(silhouette_scores)) + 2
        st.pyplot(fig_silhueta)
        st.write(f"**Melhor número de clusters (Silhueta):** {melhor_k}")

        
    # Clusterização com KMeans
        n_clusters = st.sidebar.slider("Número de clusters", 2, 10, melhor_k)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(df_rfv_padronizado)

        # Adicionar os clusters ao DataFrame padronizado
        df_rfv_padronizado['Cluster'] = labels  # Adiciona a coluna Cluster

        
        # Visualização em 3D
        st.write("### Visualização dos Clusters em 3D")
        fig_3d = plotar_clusters_3d(df_rfv_padronizado, labels, variaveis_rfv)
        st.pyplot(fig_3d)
        
        # Tabela cruzada com média das variáveis por cluster
        st.write("### Tabela Cruzada")
        tabela_crosstab = df_rfv_padronizado.groupby('Cluster')[variaveis_rfv].mean()

        # Adicionando o tamanho de cada cluster
        tamanho_clusters = df_rfv_padronizado['Cluster'].value_counts().sort_index()
        tabela_crosstab['Count'] = tamanho_clusters
        # Formatando a tabela para exibir o separador de milhar no padrão brasileiro
        tabela_crosstab['Count'] = tabela_crosstab['Count'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
        st.write(tabela_crosstab)


        # Interpretação da Tabela Cruzada
        st.write("### Interpretação da Tabela Cruzada")

        if n_clusters == 2:
            st.write("Em termos de interpretação, sabemos que uma **recência menor** indica clientes que realizaram compras mais recentemente, o que é desejável. Por outro lado, **frequência** e **valor** maiores refletem clientes mais ativos e com maior gasto total, características também desejáveis.")
            st.write("Com base nesses critérios, podemos concluir que:")
            st.write("- **Grupo 0:** Clientes menos engajados, com menor frequência e menor valor de compras.")
            st.write("- **Grupo 1:** Clientes enganjados, com boa frequência e valor. Para esses cliente iremos enviar cupons de desconto e criar campanhas de fidelização, afim de fortalecer ainda mais esse relacionamento.")
            st.write("Abaixo está o data frame com identificação do cliente e ação de marketing a ser tomada com base no grupo a que ele pertence.")

        elif n_clusters == 3:
            st.write("Em termos de interpretação, sabemos que uma **recência menor** indica clientes que realizaram compras mais recentemente, o que é desejável. Por outro lado, **frequência** e **valor** maiores refletem clientes mais ativos e com maior gasto total, características também desejáveis.")
            st.write("Com base nesses critérios, podemos concluir que:")
            st.write("- **Grupo 0:** Clientes menos engajados, com menor frequência e menor valor de compras.")
            st.write("- **Grupo 1:** Clientes moderadamente engajados, que estão em um meio termo em termos de frequência e valor, esses são os que tentaremos aproximar enviando cupons de desconto.")
            st.write("- **Grupo 2:** Clientes altamente engajados, com baixa recência, alta frequência e alto valor, sendo os ideais para fornecer indicação e receber amostras grátis de novos produtos e cupons de desconto .")
            st.write("Abaixo está o data frame com identificação do cliente e ação de marketing a ser tomada com base no grupo a que ele pertence.")

        elif n_clusters == 4:
            st.write("Em termos de interpretação, sabemos que uma **recência menor** indica clientes que realizaram compras mais recentemente, o que é desejável. Por outro lado, **frequência** e **valor** maiores refletem clientes mais ativos e com maior gasto total, características também desejáveis.")
            st.write("Com base nesses critérios, podemos concluir que:")
            st.write("- **Grupo 0:** Clientes menos engajados, com menor frequência e menor valor de compras.")
            st.write("- **Grupo 1:** Clientes engajados, que estão em um meio termo em termos de frequência e valor, esses são os que tentaremos aproximar enviando cupons de desconto.")
            st.write("- **Grupo 2:** Clientes altamente engajados, com baixa recência, alta frequência e alto valor, sendo os ideais para fornecer indicação e receber amostras grátis de novos produtos e cupons de desconto .")
            st.write("- **Grupo 3:** Clientes com baixíssimo enganjamento e valor gasto.")
            st.write("Abaixo está o data frame com identificação do cliente e ação de marketing a ser tomada com base no grupo a que ele pertence.")

        else:
            st.write("De acordo com as métricas utilizadas para avaliar a qualidade da segmentação, um número maior que 4 clusters não parece ser adequado para nossos dados, a seleção está permitida apenas para visualização. Procure escolher um número menor de segmentos.")

        # Verificar se o número de clusters é até 4 antes de adicionar ações de marketing
        if n_clusters <= 4:
            # Dicionário de ações de marketing
            dict_acoes = {
                0: 'Churn! Clientes que gastaram bem pouco e fizeram poucas compras, não realizar ações com esses clientes por enquanto.',
                1: 'Enviar e-mails com novos produtos, criar campanhas de fidelização e enviar cupons de desconto para aumentar e/ou manter a frequência de compras.',
                2: 'Enviar cupons de desconto, pedir para indicar nosso produto para algum amigo e ao lançar um novo produto, enviar amostras grátis.',
                3: 'Churn! Clientes que gastaram bem pouco e fizeram poucas compras, não realizar ações com esses clientes por enquanto.',
            }

            # Adicionar coluna de ação de marketing
            df_rfv_padronizado['Ação de Marketing'] = df_rfv_padronizado['Cluster'].map(dict_acoes)

            # Exibir tabela com clusters e ações de marketing
            st.write("### Dados Padronizados e Ação de Marketing:")
            st.write(df_rfv_padronizado[['Recencia', 'Frequencia', 'Valor', 'Ação de Marketing']])

            # Criar o arquivo .xlsx com a tabela e fornecer o botão de download
            df_xlsx = to_excel(df_rfv_padronizado[['Recencia', 'Frequencia', 'Valor', 'Ação de Marketing']])
            st.download_button(label='Download da tabela acima no formato .xlsx',
                            data=df_xlsx,
                            file_name='RFV_Com_Acoes_Marketing.xlsx')

        else:
            st.write("A segmentação com mais de 4 clusters não será realizada para ações de marketing, a fim preservar a qualidade dos agrupamentos.")
