-- #############################################
-- PROJETO ANALYTICS: MODELAGEM DIMENSIONAL DE VACINAÇÃO GLOBAL
-- Objetivo: Criar um Star Schema (Modelo Dimensional) para análise de Séries Temporais.
-- #############################################

-- O script simula a criação das tabelas em um Data Warehouse (DW)
-- (Usando sintaxe compatível com MySQL/PostgreSQL para demonstração de conceitos)

-- 1. CRIAÇÃO DA TABELA DE DIMENSÃO (dim_pais)
-- Armazena dados descritivos dos países (atributos).

CREATE TABLE dim_pais (
    pais_sk INT PRIMARY KEY AUTO_INCREMENT, -- Chave Sub-rogada (Melhor Prática)
    country VARCHAR(100) NOT NULL UNIQUE, 
    iso_code VARCHAR(10) NOT NULL,
    source_name VARCHAR(255),
    source_website VARCHAR(255),
    vaccines_used VARCHAR(255) 
);

-- 2. CRIAÇÃO DA TABELA DE FATO (fato_vacinacao_diaria)
-- Armazena as métricas diárias (Series Temporais) e chaves estrangeiras.

CREATE TABLE fato_vacinacao_diaria (
    date DATE NOT NULL, 
    pais_fk INT NOT NULL, -- Chave estrangeira para dim_pais
    total_vaccinations BIGINT,
    people_vaccinated BIGINT,
    people_fully_vaccinated BIGINT,
    daily_vaccinations BIGINT,
    avg_7d_daily_vaccinations DECIMAL(18, 2), -- Média Móvel (Importado do Python)
    FOREIGN KEY (pais_fk) REFERENCES dim_pais(pais_sk),
    PRIMARY KEY (date, pais_fk) -- Chave Composta (data + país)
);

-- 3. QUERY DE AGREGAÇÃO AVANÇADA (NÍVEL PLENO)
-- Objetivo: Identificar o ritmo médio de vacinação (doses diárias) para os 10 países que mais vacinaram.
-- A função AVG com CASE demonstra domínio em SQL ao excluir dias com reporte zero do cálculo da média.

SELECT
    dp.country,
    -- Pega o total final de doses (último registro)
    MAX(fv.total_vaccinations) AS Total_Doses_Aplicadas_Final,
    -- Calcula a Média Diária de Vacinação (excluindo dias com 0 registro para ser mais preciso)
    AVG(CASE 
            WHEN fv.daily_vaccinations > 0 THEN fv.daily_vaccinations 
            ELSE NULL 
        END) AS Media_Doses_Diarias_Reportadas
FROM
    fato_vacinacao_diaria fv
JOIN
    dim_pais dp ON fv.pais_fk = dp.pais_sk
GROUP BY
    dp.country
ORDER BY
    Total_Doses_Aplicadas_Final DESC 
LIMIT 10;

-- FIM DO SCRIPT DE MODELAGEM
