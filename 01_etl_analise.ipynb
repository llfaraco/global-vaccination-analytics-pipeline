import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de visualização
sns.set_style("whitegrid")

# --------------------------------------------------------
# FASE 1: EXTRAÇÃO E LIMPEZA (ETL)
# --------------------------------------------------------

# Carregamento do dataset a partir da pasta 'data/'
try:
    # Esta linha exige que o arquivo country_vaccinations.csv esteja na pasta 'data/'
    df = pd.read_csv('data/country_vaccinations.csv')
except FileNotFoundError:
    print("ERRO CRÍTICO: O arquivo CSV 'country_vaccinations.csv' não foi encontrado na pasta 'data/'.")
    print("Verifique se o nome do arquivo e a estrutura de pastas estão corretos.")
    exit()

print("--- 1. Informações Iniciais e Limpeza ---")

# 1.1 Tratamento de Nulos: Preencher NaN nas colunas de métricas com 0 
metric_cols = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 
               'daily_vaccinations', 'daily_people_vaccinated']
df.loc[:, metric_cols] = df[metric_cols].fillna(0) # Uso de .loc para evitar SettingWithCopyWarning

# 1.2 Conversão de Tipos de Dados: Garantir que 'date' seja do tipo datetime
df.loc[:, 'date'] = pd.to_datetime(df['date'])

# 1.3 Padronização: Renomear Colunas para snake_case (melhor prática de engenharia)
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# --------------------------------------------------------
# FASE 2: FEATURE ENGINEERING (Séries Temporais)
# --------------------------------------------------------

# 2.1 Cálculo da Média Móvel de 7 Dias (Habilidade Pleno)
# Suaviza o ruído diário para encontrar a tendência real de vacinação.
df['avg_7d_daily_vaccinations'] = df.groupby('country')['daily_vaccinations'].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)

print("\n--- 2. Dataset após a Limpeza e Feature Engineering (Pronto para SQL) ---")
print(df.head())


# --------------------------------------------------------
# FASE 3: ANÁLISE EXPLORATÓRIA (EDA) E VISUALIZAÇÃO
# --------------------------------------------------------

# 3.1 Identificar os 5 Maiores Vacinadores (em Total de Doses)
df_top = df.groupby('country')['total_vaccinations'].max().reset_index()
df_top = df_top.sort_values(by='total_vaccinations', ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x='country', y='total_vaccinations', data=df_top, palette='Reds_d')
plt.title('Top 5 Países em Total de Doses Aplicadas')
plt.ylabel('Total de Doses (em bilhões)')
plt.xlabel('País')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top5_vacinacao.png') # Salva o gráfico


# 3.2 Análise de Tendência (Brasil)
df_brasil = df[df['country'] == 'Brazil'].copy()

plt.figure(figsize=(12, 6))
plt.plot(df_brasil['date'], df_brasil['daily_vaccinations'], label='Doses Diárias (Bruto)', alpha=0.5)
plt.plot(df_brasil['date'], df_brasil['avg_7d_daily_vaccinations'], label='Média Móvel 7 Dias', color='red', linewidth=2)
plt.title('Tendência de Vacinação Diária no Brasil (Média Móvel 7 Dias)')
plt.ylabel('Doses Diárias')
plt.xlabel('Data')
plt.legend()
plt.tight_layout()
plt.savefig('tendencia_brasil.png') # Salva o gráfico


# --------------------------------------------------------
# FASE 4: EXPORTAÇÃO PARA MODELAGEM SQL
# --------------------------------------------------------

# Salva o dataset limpo e enriquecido (com a Média Móvel)
df.to_csv('data/tabela_limpa_vacinacao.csv', index=False)

print("\nDataset final limpo exportado para 'data/tabela_limpa_vacinacao.csv', pronto para o script SQL.")
