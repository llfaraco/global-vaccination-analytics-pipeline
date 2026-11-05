PRAGMA foreign_keys=ON;
CREATE TABLE dim_pais (pais_sk INTEGER PRIMARY KEY, country TEXT NOT NULL UNIQUE, iso_code TEXT);
CREATE TABLE fato_vacinacao_diaria (
 date TEXT NOT NULL, pais_fk INTEGER NOT NULL REFERENCES dim_pais(pais_sk),
 total_vaccinations REAL, people_vaccinated REAL, people_fully_vaccinated REAL,
 daily_vaccinations REAL, avg_7d_daily_vaccinations REAL,
 PRIMARY KEY(date,pais_fk)
);
