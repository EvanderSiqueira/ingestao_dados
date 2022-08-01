-- Criando o banco de dados analiseFinanceira ---------------------------------------------
CREATE DATABASE "analiseFinanceira"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Criando dimensões ---------------------------------------------------------------------

CREATE TABLE dim_calendario (
  pk_calendario INT NOT NULL,
  ano INT NOT NULL,
  trimestre INT NOT NULL,
  trimestre_descr_curta VARCHAR(255),
  trimestre_descr_longa VARCHAR(255),
  PRIMARY KEY (pk_calendario)
);

CREATE TABLE dim_instituicoes (
  pk_cnpj INT NOT NULL,
  nome_instituicao VARCHAR(255),
  codigo_grupo INT NOT NULL,
  descr_grupo VARCHAR(255),
  PRIMARY KEY (pk_cnpj)
);

-- Criando fatos ------------------------------------------------------------------------

CREATE TABLE fato_reclamacoes (
  fk_cnpj INT NOT NULL,
  fk_calendario INT NOT NULL,
  quantidade_reclamacoes_reguladas_procedentes DECIMAL NOT NULL,
  quantidade_reclamacoes_reguladas_outras DECIMAL NOT NULL,
  quantidade_reclamacoes_nao_reguladas DECIMAL NOT NULL,
  quantidade_total_reclamacoes DECIMAL NOT NULL,
  quantidade_total_clientes_ccs_e_scr DECIMAL NOT NULL,
  quantidade_clientes_ccs DECIMAL NOT NULL,
  quantidade_clientes_scr DECIMAL NOT NULL,
 
  PRIMARY KEY (fk_cnpj, fk_calendario),
  FOREIGN KEY (fk_cnpj)
      REFERENCES dim_instituicoes (pk_cnpj),
  FOREIGN KEY (fk_calendario)
      REFERENCES dim_calendario (pk_calendario)
);


CREATE TABLE fato_tarifas (
  pk_tarifa INT NOT NULL,
  fk_calendario INT NOT NULL,
  fk_cnpj INT NOT NULL,
  descr_tarifa VARCHAR(255),
  tipo_tarifa VARCHAR(50),
  data_vigencia DATE,
  valor_maximo DECIMAL,
  tipo_valor VARCHAR(255),
  periodicidade VARCHAR(255),

  PRIMARY KEY (pk_tarifa, fk_calendario, fk_cnpj),
  FOREIGN KEY (fk_cnpj)
      REFERENCES dim_instituicoes (pk_cnpj),
  FOREIGN KEY (fk_calendario)
      REFERENCES dim_calendario (pk_calendario)
);