# 💉 Data-Driven Public Health: Análise de Progresso de Vacinação Global (SQL & Python)

## 🎯 Missão do Projeto

Este projeto demonstra a capacidade de construir um mini **Pipeline de Dados (ETL)** e aplicar **Modelagem Dimensional** em um dataset de **Séries Temporais** (dados diários), transformando dados brutos de vacinação em insights acionáveis.

O projeto comprova as seguintes *hard skills* de nível Júnior/Pleno:
* Limpeza, padronização e manipulação de dados em **Python (Pandas)**.
* Conhecimento em **Modelagem Dimensional** (Star Schema) e consultas avançadas em **SQL**.
* Análise de **Séries Temporais** (cálculo de Média Móvel).

## 🛠️ Stack Tecnológico

* **Linguagens:** Python, SQL
* **Bibliotecas:** Pandas, Matplotlib, Seaborn
* **Skills:** ETL, Feature Engineering, Modelagem Dimensional (Star Schema)

## ⚙️ Processo e Arquitetura de Dados

O projeto seguiu três etapas cruciais para garantir a qualidade e a estrutura do dado:

1.  **Limpeza e Feature Engineering (Python):** Tratamento de valores nulos e padronização. Implementação de **Média Móvel de 7 Dias** nas doses diárias para suavizar o ruído de reporte (um requisito típico em análises de séries temporais).
2.  **Modelagem Dimensional (SQL):** Criação das tabelas **`dim_pais`** e **`fato_vacinacao_diaria`** e definição das chaves (primárias/estrangeiras), garantindo que a base de dados seja eficiente para consultas analíticas.
3.  **Análise Exploratória (EDA):** Identificação dos Top 5 países por volume total e visualização da tendência de vacinação (Média Móvel).

## 📊 Principais Insights

* **Ritmo de Vacinação:** A análise da **Média Móvel de 7 Dias** revela a tendência real do processo de vacinação, que é obscurecida pelas flutuações diárias de reporte.
* **Desigualdade Global:** A visualização dos **Top 5 Países em Doses Aplicadas** demonstra a concentração de vacinas em poucos países, servindo como base para discussões sobre equidade e logística.

---
