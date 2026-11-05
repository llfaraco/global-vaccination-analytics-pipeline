# Vacinação global | Tratamento de dados e modelagem analítica

**Projeto de estudo · Python · pandas · SQL · Séries temporais**

## Pergunta analítica

Como organizar registros diários de vacinação para comparar volumes e observar a evolução no tempo?

## Implementação disponível

- `01_etl_analise.py`: leitura do CSV, preenchimento de nulos em métricas, conversão de data, padronização de nomes e cálculo de média móvel de sete registros por país.
- Geração de gráficos para os cinco maiores volumes acumulados e a série do Brasil.
- Exportação do resultado para `data/tabela_limpa_vacinacao.csv`.
- `02_modelagem_sql.sql`: dimensão de país, fato de vacinação diária e consulta de agregação.
- `data/country_vaccinations.csv`: arquivo de entrada disponível no repositório.

## Como executar a etapa Python

Na raiz do projeto, em um ambiente Python:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install pandas numpy matplotlib seaborn
python 01_etl_analise.py
```

O script prevê a criação de `top5_vacinacao.png`, `tendencia_brasil.png` e do CSV tratado. A execução não foi validada nesta revisão documental.

## Etapa SQL

O modelo é uma demonstração separada. O Python **não cria nem carrega automaticamente** as tabelas SQL. A definição usa `AUTO_INCREMENT`, próprio da família MySQL; precisa de adaptação para PostgreSQL.

## Limitações analíticas

- Ausência de informação é preenchida com zero no script atual; isso pode afetar médias e a interpretação de volumes.
- A janela móvel usa sete registros, não necessariamente sete dias corridos quando há lacunas.
- A ordenação temporal deve ser conferida antes de interpretar a média móvel.
- A origem e a licença do CSV precisam de documentação complementar antes de sua redistribuição.
- Comparações por volume absoluto não medem, por si só, cobertura vacinal ou desempenho de políticas públicas.

## Evolução

Documentar a fonte, revisar os critérios de qualidade e a ordenação temporal, automatizar a carga SQL e registrar resultados reproduzíveis. Este é um exercício técnico, sem uso operacional ou recomendação de saúde pública.

## Contato

[Lucas Faraco](https://www.linkedin.com/in/lucasrfaraco) · [E-mail](mailto:lucas.rfaraco@gmail.com) · [Perfil e portfólio](https://github.com/llfaraco)
