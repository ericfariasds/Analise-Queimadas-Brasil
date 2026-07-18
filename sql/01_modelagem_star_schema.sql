USE db_queimadas;

-- DIMENSÃO SATÉLITE
CREATE TABLE dim_satelite (
	id_satelite INT AUTO_INCREMENT PRIMARY KEY,
    nome_satelite VARCHAR(100)
);
INSERT INTO dim_satelite (nome_satelite)
SELECT DISTINCT satelite
FROM staging_queimadas
WHERE satelite IS NOT NULL;

-- DIMENSÃO LOCAL
CREATE TABLE dim_local (
	id_local INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(100),
    estado VARCHAR(100),
    municipio VARCHAR(150),
    bioma VARCHAR(100)
);
INSERT INTO dim_local (pais, estado, municipio, bioma)
SELECT DISTINCT pais, estado, municipio, bioma
FROM staging_queimadas
WHERE estado IS NOT NULL;

-- TABELA FATO
CREATE TABLE fato_queimadas (
    id_fato INT AUTO_INCREMENT PRIMARY KEY,
    id_satelite INT,
    id_local INT,
    data_hora DATETIME,
    ano INT,
    mes INT,
    dia INT,
    dias_sem_chuva FLOAT,
    precipitacao FLOAT,
    risco_fogo FLOAT,
    frp FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (id_satelite) REFERENCES dim_satelite(id_satelite),
    FOREIGN KEY (id_local) REFERENCES dim_local(id_local)
);
INSERT INTO fato_queimadas (
    id_satelite, id_local, data_hora, ano, mes, dia, 
    dias_sem_chuva, precipitacao, risco_fogo, frp, latitude, longitude
)
SELECT 
    ds.id_satelite,
    dl.id_local,
    sq.data_hora,
    sq.ano,
    sq.mes,
    sq.dia,
    sq.dias_sem_chuva,
    sq.precipitacao,
    sq.risco_fogo,
    sq.frp,
    sq.latitude,
    sq.longitude
FROM staging_queimadas sq
LEFT JOIN dim_satelite ds ON sq.satelite = ds.nome_satelite
LEFT JOIN dim_local dl ON sq.pais = dl.pais 
                       AND sq.estado = dl.estado 
                       AND sq.municipio = dl.municipio 
                       AND sq.bioma = dl.bioma;
                       