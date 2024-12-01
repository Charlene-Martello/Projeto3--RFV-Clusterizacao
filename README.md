# **Projeto: Análise de Clusters RFV**

Este projeto tem como objetivo analisar e segmentar clientes com base no modelo RFV (Recência, Frequência e Valor) utilizando técnicas de aprendizado não supervisionado, especificamente o algoritmo **K-Means**, para identificar diferentes perfis de clientes e definir estratégias de marketing personalizadas.

## **Funcionalidades do Projeto**

- **Carregamento de Dados:** Permite carregar arquivos CSV contendo informações de transações dos clientes.
- **Tratamento dos Dados:** Converte os dados transacionais no formato RFV (Recência, Frequência e Valor).
- **Padronização:** Os dados são padronizados para melhorar a performance e precisão da clusterização.
- **Método do Cotovelo:** Avalia o número ideal de clusters baseado na soma das distâncias quadradas (inércia).
- **Análise da Silhueta:** Calcula a pontuação de silhueta para determinar a qualidade da clusterização.
- **Visualização 3D:** Gráfico interativo que exibe os clusters em 3D com base nas dimensões RFV.
- **Tabela Cruzada:** Exibe a média das variáveis RFV por cluster e o tamanho de cada cluster.
- **Sugestões de Ações de Marketing:** Recomenda estratégias baseadas no perfil dos clusters.
- **Exportação dos Resultados:** Permite o download da tabela de resultados no formato Excel (.xlsx).

---

## **Tecnologias Utilizadas**

- **Linguagem:** Python
- **Bibliotecas Principais:**
  - **Pandas:** Manipulação e análise de dados.
  - **Matplotlib/Seaborn:** Visualização de dados.
  - **Scikit-learn:** Algoritmos de aprendizado de máquina (K-Means, StandardScaler, Silhouette Score).
  - **Streamlit:** Criação de interface interativa para o projeto.
- **Outras:** `mpl_toolkits.mplot3d` para visualizações tridimensionais.

---

## **Como Utilizar**

1. **Carregar Arquivo:**
   - No menu lateral do aplicativo Streamlit, clique no botão **"Browse files"** para selecionar e carregar o arquivo CSV disponível neste repositório.

2. **Visualizar os Dados:**
   - Após carregar o arquivo, você verá duas tabelas:
     - **Dados Brutos:** Exibe os dados originais carregados.
     - **Dados RFV:** Mostra as métricas RFV (Recência, Frequência e Valor) calculadas para cada cliente.

3. **Análise de Clusterização:**
   - Utilize o **método do cotovelo** para avaliar o número ideal de clusters:
     - No menu lateral, ajuste o número máximo de clusters para análise (valor padrão: 15).
     - Visualize o gráfico para identificar o ponto de inflexão.
   - Analise a **pontuação da silhueta** para determinar a qualidade da clusterização:
     - O gráfico exibirá as pontuações para diferentes números de clusters.
     - O número ideal de clusters será destacado com base na melhor pontuação.

4. **Clusterização com K-Means:**
   - No menu lateral, selecione o número de clusters desejado (com base nas análises anteriores).
   - Visualize os clusters no gráfico 3D interativo, usando as métricas RFV.

5. **Tabela de Resultados:**
   - Explore a tabela que mostra:
     - **Médias das métricas RFV** por cluster.
     - **Tamanho de cada cluster.**
     - Estratégias sugeridas de marketing para cada grupo.
   - Baixe os resultados no formato Excel clicando no botão **"Download da tabela acima no formato .xlsx"**.
**obs**: A análise da tabela é em relação ao csv disponibilizado nesse repositório. 
