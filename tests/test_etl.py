import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('vax',ROOT/'01_etl_analise.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def fixture():
 return pd.DataFrame({'country':['A','A','A','B'],'date':['2024-01-10','2024-01-01','2024-01-03','2024-01-01'],'total_vaccinations':[30,10,20,None],'people_vaccinated':[15,5,10,None],'people_fully_vaccinated':[5,1,2,None],'daily_vaccinations':[30,10,None,None]})
class TemporalContract(unittest.TestCase):
 def test_sort_calendar_window_and_missing_reports(self):
  df=m.transform(fixture());a=df[df.country=='A'];self.assertEqual(a.date.dt.day.tolist(),[1,3,10]);self.assertEqual(a.iloc[-1].avg_7d_daily_vaccinations,30)
  self.assertTrue(pd.isna(a.iloc[1].daily_vaccinations));self.assertTrue(pd.isna(df[df.country=='B'].iloc[0].avg_7d_daily_vaccinations))
 def test_duplicates_rejected(self):
  df=fixture()
  with self.assertRaisesRegex(ValueError,'duplicada'):m.transform(pd.concat([df,df.iloc[:1]]))
 def test_negative_metric_rejected(self):
  df=fixture();df.loc[0,'daily_vaccinations']=-1
  with self.assertRaises(ValueError):m.transform(df)
 def test_sql_load_reconciles_and_preserves_null(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);fixture().to_csv(root/'fixture.csv',index=False);r=m.run(root/'fixture.csv',root/'out')
   self.assertEqual(r['records'],4)
   with sqlite3.connect(root/'out/vaccination.db') as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM fato_vacinacao_diaria WHERE daily_vaccinations IS NULL').fetchone()[0],2)
if __name__=='__main__':unittest.main()
