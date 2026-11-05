"""Tratamento temporal preservando ausência, com carga SQLite e reconciliação."""
import argparse
import json
import sqlite3
import tempfile
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
METRICS=['total_vaccinations','people_vaccinated','people_fully_vaccinated','daily_vaccinations']

def transform(df):
    df=df.copy();df.columns=df.columns.str.lower().str.strip().str.replace(' ','_')
    if not {'country','date',*METRICS}.issubset(df.columns):raise ValueError('Colunas obrigatórias ausentes')
    if df.empty or df[['country','date']].isna().any().any():raise ValueError('Base vazia ou chave ausente')
    df['date']=pd.to_datetime(df['date'],errors='raise')
    if df.duplicated(['country','date']).any():raise ValueError('Chave país/data duplicada')
    for column in METRICS:
        df[column]=pd.to_numeric(df[column],errors='raise')
        valid=df[column].dropna()
        if (valid<0).any() or not valid.lt(float('inf')).all():raise ValueError('Métrica fora do domínio: '+column)
    df=df.sort_values(['country','date']).reset_index(drop=True)
    df['avg_7d_daily_vaccinations']=float('nan')
    for _,group in df.groupby('country',sort=False):
        # Janela temporal real: não confundir sete registros com sete dias.
        rolled=group.set_index('date')['daily_vaccinations'].rolling('7D',min_periods=1).mean()
        df.loc[group.index,'avg_7d_daily_vaccinations']=rolled.to_numpy()
    return df

def run(input_path=ROOT/'data/country_vaccinations.csv',output=ROOT/'artifacts'):
    df=transform(pd.read_csv(input_path));output=Path(output);output.mkdir(parents=True,exist_ok=True)
    dimension=df[['country']].drop_duplicates().reset_index(drop=True);dimension.insert(0,'pais_sk',range(1,len(dimension)+1))
    if 'iso_code' in df:
        iso=df[['country','iso_code']].dropna().drop_duplicates()
        if iso.country.duplicated().any():raise ValueError('País com ISO inconsistente')
        dimension=dimension.merge(iso,on='country',how='left')
    else:dimension['iso_code']=None
    fact=df.merge(dimension[['pais_sk','country']],on='country',validate='many_to_one')
    fact['date']=fact['date'].dt.strftime('%Y-%m-%d');fact=fact.rename(columns={'pais_sk':'pais_fk'})[['date','pais_fk',*METRICS,'avg_7d_daily_vaccinations']]
    with tempfile.TemporaryDirectory(dir=output) as temp:
        path=Path(temp)/'vaccination.db'
        with sqlite3.connect(path) as db:
            db.executescript((ROOT/'02_modelagem_sql.sql').read_text())
            dimension.to_sql('dim_pais',db,if_exists='append',index=False);fact.to_sql('fato_vacinacao_diaria',db,if_exists='append',index=False)
            count=db.execute('SELECT COUNT(*) FROM fato_vacinacao_diaria').fetchone()[0]
            if count!=len(df) or db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Reconciliação falhou')
            aggregate=pd.read_sql_query('SELECT country, MAX(total_vaccinations) total_acumulado_maximo FROM fato_vacinacao_diaria JOIN dim_pais ON pais_fk=pais_sk GROUP BY country ORDER BY total_acumulado_maximo DESC',db)
        path.replace(output/'vaccination.db')
    df.to_csv(output/'tabela_limpa_vacinacao.csv',index=False);aggregate.to_csv(output/'totais_por_pais.csv',index=False)
    result={'input':str(input_path),'records':len(df),'countries':len(dimension),'period_start':df.date.min().date().isoformat(),'period_end':df.date.max().date().isoformat(),'missing_daily_reports':int(df.daily_vaccinations.isna().sum()),'checks':{'unique_country_date':True,'row_count_reconciled':True,'foreign_keys':True},'scope':'Máximos acumulados não devem ser somados entre países e agregados territoriais sem definir o universo.'}
    (output/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=ROOT/'data/country_vaccinations.csv');p.add_argument('--output',type=Path,default=ROOT/'artifacts');a=p.parse_args();run(a.input,a.output)
