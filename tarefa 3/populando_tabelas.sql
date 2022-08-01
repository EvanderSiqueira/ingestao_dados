-- populando dim_calendario -------------------------------------------------
COPY dim_calendario(pk_calendario, ano, trimestre, trimestre_descr_curta, trimestre_descr_longa)
FROM 'C:\Users\Public\modeladas\dim_calendario.csv' ENCODING 'LATIN1'
DELIMITER ',' CSV HEADER;

-- populando dim_instituicoes -------------------------------------------------
COPY dim_instituicoes(pk_cnpj, nome_instituicao, codigo_grupo, descr_grupo)
FROM 'C:\Users\Public\modeladas\dim_instituicoes.csv' ENCODING 'LATIN1'
DELIMITER ',' CSV HEADER;

-- populando fato fato_reclamacoes -------------------------------------------------
COPY fato_reclamacoes(fk_cnpj, fk_calendario, quantidade_reclamacoes_reguladas_procedentes, quantidade_reclamacoes_reguladas_outras, quantidade_reclamacoes_nao_reguladas, quantidade_total_reclamacoes, quantidade_total_clientes_ccs_e_scr, quantidade_clientes_ccs, quantidade_clientes_scr)
FROM 'C:\Users\Public\modeladas\fato_reclamacoes.csv' ENCODING 'LATIN1'
DELIMITER ',' CSV HEADER;

-- populando fato fato_tarifas -------------------------------------------------
COPY fato_tarifas(pk_tarifa, fk_calendario, fk_cnpj, descr_tarifa, tipo_tarifa, data_vigencia, valor_maximo, tipo_valor, periodicidade)
FROM 'C:\Users\Public\modeladas\fato_tarifas.csv' ENCODING 'LATIN1'
DELIMITER ',' CSV HEADER;