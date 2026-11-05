# Vacinação | Tratamento temporal e carga SQLite

**Python · pandas · SQL · Modelagem dimensional**

Como transformar registros por país e data em uma base analítica sem confundir ausência de reporte com zero?

## Implementação

1. Valida colunas, chaves, datas e domínios das métricas.
2. Rejeita duplicidades país/data.
3. Ordena as observações e calcula média móvel de **sete dias corridos**, usando janela temporal.
4. Preserva nulos de reporte; não os converte em zero.
5. Carrega dimensão e fato em SQLite e reconcilia a quantidade de registros e as referências.
6. Exporta CSV tratado, máximos acumulados por país e relatório de validação.

## Executar

Ambiente de testes: Python 3.12.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python 01_etl_analise.py
# Outra entrada:
python 01_etl_analise.py --input caminho/base.csv --output artifacts
```

A entrada padrão continua sendo `data/country_vaccinations.csv`, já existente no repositório. As saídas ficam em `artifacts/`; o banco e o CSV tratado não são versionados.

## O que foi validado

Quatro testes locais passaram com uma **fixture sintética de quatro registros e dois países**, criada apenas para testar o comportamento. Conferem ordenação, intervalo com lacunas, nulos, duplicidade, métrica negativa e persistência SQL.

**O CSV original de 17 MB não foi executado nesta revisão:** o conector não entregou seu conteúdo. Os testes controlados não substituem essa execução. Não se publicam números de países, doses ou desempenho como se tivessem sido calculados na base completa.

## Decisões e limites

O SQL agora usa SQLite e é carregado pelo Python, substituindo a modelagem separada com dialeto incompatível. A construção do banco ocorre em temporário antes da substituição.

A média móvel usa as observações reportadas na janela, preservando o fato de que pode haver dias sem reporte. Ela não estima os valores ausentes. O máximo acumulado não necessariamente corresponde ao dado mais recente quando há revisões para baixo.

Países e agregados territoriais precisam ser diferenciados antes de somar volumes. A origem e licença do CSV ainda precisam de documentação; o projeto não oferece recomendação de saúde pública.

Evolução implementada com assistência de IA. A CI confere o contrato em fixtures e, em separado, tenta a execução da base original; consulte o resultado da execução do workflow antes de declarar a validação completa.

[Portfólio](https://github.com/llfaraco)
