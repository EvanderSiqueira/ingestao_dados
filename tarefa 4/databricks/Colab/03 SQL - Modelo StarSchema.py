# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo Star Schema em SQL

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Deletar** antes de subir no Github

# COMMAND ----------

from google.colab import drive
drive.mount('/content/drive')

# COMMAND ----------

!pip install -U pandasql

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 Importando csv como dataframe

# COMMAND ----------

# MAGIC %md
# MAGIC Carregando bibliotecas necessárias

# COMMAND ----------

import pandas as pd
import numpy as np
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())



# caminho para salvamento dos arquivos
caminho = '/content/drive/MyDrive/Colab Notebooks/dados/'

# COMMAND ----------

# MAGIC %md
# MAGIC Importando arquivos normalizados

# COMMAND ----------

df_consolidado = pd.read_csv(caminho + 'normalizadas/df_consolidado.csv', encoding='latin1')
df_lista_inst = pd.read_csv(caminho + 'normalizadas/df_lista_inst.csv', encoding='latin1')
df_reclamacoes = pd.read_csv(caminho + 'normalizadas/df_reclamações.csv', encoding='latin1')
df_tarifas = pd.read_csv(caminho + 'normalizadas/df_tarifas.csv', encoding='latin1')

# COMMAND ----------

df_lista_inst.columns

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 Usando SQL para fazer a modelagem Star Schema

# COMMAND ----------

# MAGIC %md
# MAGIC #### **df_reclamações** para **Fato Reclamações**
# MAGIC 
# MAGIC Não é necessário fazer nenhuma alteração pois a df_reclamações já está no formato que precisamos para subir no banco. Mas, vamos garantir que não tenha duplicados usando um Group By

# COMMAND ----------

# query
q = """
    select 
          fk_cnpj, 
          fk_calendario, 
          sum(quantidade_reclamacoes_reguladas_procedentes) as quantidade_reclamacoes_reguladas_procedentes,
          sum(quantidade_reclamacoes_reguladas_outras) as quantidade_reclamacoes_reguladas_outras,
          sum(quantidade_reclamacoes_nao_reguladas) as quantidade_reclamacoes_nao_reguladas, 
          sum(quantidade_total_reclamacoes) as quantidade_total_reclamacoes,
          sum(quantidade_total_clientes_ccs_e_scr) as quantidade_total_clientes_ccs_e_scr, 
          sum(quantidade_clientes_ccs) as quantidade_clientes_ccs,
          sum(quantidade_clientes_scr) as quantidade_clientes_scr
    from df_reclamacoes
    group by fk_cnpj, fk_calendario;
  """

# COMMAND ----------

# criando fato com SQL
fato_reclamacoes = pysqldf(q)

# COMMAND ----------

# MAGIC %md
# MAGIC A fato_reclamações só deve ter códigos presentes na dimensão de instituições

# COMMAND ----------

# query
q = """
    select fc.*
    from fato_reclamacoes fc
    inner join df_lista_inst li
    ON fc.fk_cnpj = li.cnpj;
 
  """

# COMMAND ----------

fato_reclamacoes = pysqldf(q)

# COMMAND ----------

# MAGIC %md
# MAGIC #### **df_tarifas** para **Fato Tarifas**
# MAGIC 
# MAGIC Não é necessário fazer nenhuma alteração pois a df_tarifas já está no formato que precisamos para subir no banco. Mas, vamos garantir que não tenha duplicados usando um Group By

# COMMAND ----------

df_tarifas.columns

# COMMAND ----------

# query
q = """
    SELECT 
         pk_tarifa,
         fk_calendario,
         fk_cnpj,
         descr_tarifa, 
         tipo_tarifa, 
         data_vigencia,
         valor_maximo, 
         tipo_valor, 
         periodicidade         
    FROM df_tarifas
    GROUP BY 
        pk_tarifa,
         fk_calendario,
         fk_cnpj,
         descr_tarifa, 
         tipo_tarifa, 
         data_vigencia,
         valor_maximo, 
         tipo_valor, 
         periodicidade;
  """

# COMMAND ----------

# criando fato com SQL
fato_tarifas = pysqldf(q)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Criando **Dim Calendario**
# MAGIC 
# MAGIC A tabela Calendario deriva das colunas `fk_calendar` das `Fato Reclamações` e `Fato Tarifas`. Assim, vamos unir ambas tabelas e obter apenas a coluna `pk_calendar`. 
# MAGIC 
# MAGIC Na sequência, criaremos as colunas `ano`, `trimestre`, `trimestre descr curta` e `trimestre descr longa`

# COMMAND ----------

# query
q = """
SELECT
    fk_calendario as pk_calendario,
    substr(fk_calendario, 1, 4) as ano,
    substr(fk_calendario, -1, 1) as trimestre,
    substr(fk_calendario, -1, 1) || 'º' as 'trimestre_descr_curta',
    substr(fk_calendario, -1, 1) || 'º Trimestre' as 'trimestre_descr_longa'
FROM
    (
        SELECT
            fk_calendario
        FROM
            (
                SELECT
                    fk_calendario
                FROM
                    df_tarifas
                UNION
                ALL
                SELECT
                    fk_calendario
                FROM
                    df_reclamacoes
            ) t
        GROUP BY
            fk_calendario
    ) a
  """

# COMMAND ----------

# criando dimensão com SQL
dim_calendario = pysqldf(q)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Criando **Dim Instituições**
# MAGIC 
# MAGIC A dimensão instituições é basicamente um left join com a tabela df_consolidados

# COMMAND ----------

# query
q = """
  SELECT li.cnpj as pk_cnpj, li.nome_instituicao, c.codigo_grupo, c.descr_grupo
  FROM df_lista_inst li
  LEFT JOIN df_consolidado c
  ON li.codigo_grupo = c.codigo_grupo;

  """

# COMMAND ----------

# criando dimensão com SQL
dim_instituicoes = pysqldf(q)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 Salvando bases modelagem Star Schema

# COMMAND ----------

fato_reclamacoes.to_csv(caminho + 'modeladas/fato_reclamacoes.csv', encoding='latin1', index= False)
fato_tarifas.to_csv(caminho + 'modeladas/fato_tarifas.csv', encoding='latin1', index= False)
dim_calendario.to_csv(caminho + 'modeladas/dim_calendario.csv', encoding='latin1', index= False)
dim_instituicoes.to_csv(caminho + 'modeladas/dim_instituicoes.csv', encoding='latin1', index= False)

# COMMAND ----------


