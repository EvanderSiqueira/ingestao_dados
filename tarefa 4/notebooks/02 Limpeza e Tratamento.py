# Databricks notebook source
# MAGIC %md
# MAGIC # Limpeza e tratamento dos dados

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Deletar** antes de subir no Github

# COMMAND ----------

from google.colab import drive
drive.mount('/content/drive')

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 Importando csv como dataframe

# COMMAND ----------

# MAGIC %md
# MAGIC Carregando bibliotecas necessárias

# COMMAND ----------

import pandas as pd
import numpy as np

# caminho para salvamento dos arquivos
caminho = '/content/drive/MyDrive/Colab Notebooks/dados/'

# COMMAND ----------

# MAGIC %md
# MAGIC Carregando as bases brutas extraídas

# COMMAND ----------

df_consolidado = pd.read_csv(caminho + '/df_consolidado.csv', encoding='latin1')
df_lista_inst = pd.read_csv(caminho + '/df_lista_inst.csv', encoding='latin1')
df_reclamações = pd.read_csv(caminho + '/df_reclamações.csv', encoding='latin1')
df_tarifas = pd.read_csv(caminho + '/df_tarifas.csv', encoding='latin1')

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 Data Wrangling

# COMMAND ----------

# MAGIC %md
# MAGIC #### Limpando o ``` df_consolidado```

# COMMAND ----------

df_consolidado_normal = df_consolidado.copy()

# COMMAND ----------

# MAGIC %md
# MAGIC Deletando colunas desnecessárias e renomeando

# COMMAND ----------

# deletando colunas desnecessárias
df_consolidado_normal.drop(['Unnamed: 0'], axis=1, inplace=True)

# Listando nomes atuais
print(df_consolidado_normal.columns)

# Renomeando
novos_nomes_colunas = {'Codigo': 'codigo_grupo', 'Nome': 'descr_grupo'}
df_consolidado_normal.rename(columns=novos_nomes_colunas, inplace=True)
df_consolidado_normal.head(2)

# COMMAND ----------

# removendo duplicadas
df_consolidado_normal.drop_duplicates(subset=['codigo_grupo'], inplace=True)
df_consolidado_normal.head(2)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Limpando o ``` df_lista_inst```

# COMMAND ----------

df_lista_inst_normal = df_lista_inst.copy()

# COMMAND ----------

# MAGIC %md
# MAGIC Deletando colunas desnecessárias e renomeando

# COMMAND ----------

# deletando colunas desnecessárias
df_lista_inst_normal.drop(['Unnamed: 0'], axis=1, inplace=True)

# Listando nomes atuais
print(df_lista_inst_normal.columns)

# Renomeando
novos_nomes_colunas = {'Cnpj': 'cnpj', 'Nome': 'nome_instituicao', 'CodigoGrupo': 'codigo_grupo'}
df_lista_inst_normal.rename(columns=novos_nomes_colunas, inplace=True)
df_lista_inst_normal.head(2)

# COMMAND ----------

# removendo duplicadas
df_lista_inst_normal.drop_duplicates(subset=['cnpj'], inplace=True)
df_lista_inst_normal.head(2)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Limpando o ``` df_reclamações```

# COMMAND ----------

df_reclamações_normal = df_reclamações.copy()

# COMMAND ----------

# MAGIC %md
# MAGIC Criando chave ``` fk_calendario```

# COMMAND ----------

df_reclamações_normal['fk_calendario'] = df_reclamações_normal['Ano'].map(str) + df_reclamações_normal['Trimestre'].str.replace('º', '')

# COMMAND ----------

# MAGIC %md
# MAGIC Deletando colunas desnecessárias e renomeando

# COMMAND ----------

# deletando colunas desnecessárias
df_reclamações_normal.drop(['Ano', 'Trimestre', 'Unnamed: 14', 'Unnamed: 0', 'Instituição financeira', 'Índice', 'Categoria', 'Tipo'], axis=1, inplace=True)

# Renomeando
novos_nomes_colunas = {
    'CNPJ IF': 'fk_cnpj', 
    'Quantidade de reclamações reguladas procedentes': 'quantidade_reclamacoes_reguladas_procedentes', 
    'Quantidade de reclamações reguladas - outras': 'quantidade_reclamacoes_reguladas_outras',
    'Quantidade de reclamações não reguladas': 'quantidade_reclamacoes_nao_reguladas',
    'Quantidade total de reclamações': 'quantidade_total_reclamacoes',
    'Quantidade total de clientes  CCS e SCR': 'quantidade_total_clientes_ccs_e_scr',
    'Quantidade de clientes  CCS': 'quantidade_clientes_ccs',
    'Quantidade de clientes  SCR': 'quantidade_clientes_scr'
    }

df_reclamações_normal.rename(columns=novos_nomes_colunas, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC Mantendo apenas linhas com CNPJ

# COMMAND ----------

# Substituindo vazios por NaN
df_reclamações_normal.fk_cnpj.replace(" ", float("NaN"), inplace=True)

# Deletando NaN
df_reclamações_normal.dropna(subset = ['fk_cnpj'], inplace=True)


# COMMAND ----------

# removendo duplicadas
df_reclamações_normal.drop_duplicates(subset=['fk_cnpj'], inplace=True)
df_reclamações_normal.head(2)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Limpando o ``` df_tarifas```

# COMMAND ----------

df_tarifas_normal = df_tarifas.copy()

# COMMAND ----------

# deletando colunas desnecessárias
df_tarifas_normal.drop(['Unnamed: 0'], axis=1, inplace=True)

# Listando nomes atuais
print(df_tarifas_normal.columns)

# Renomeando
novos_nomes_colunas = {
    'CodigoServico': 'pk_tarifa',
    'CNPJ':'fk_cnpj',
    'Servico': 'descr_tarifa', 
    'Unidade': 'tipo_tarifa',
    'DataVigencia': 'data_vigencia',
    'ValorMaximo': 'valor_maximo',
    'TipoValor': 'tipo_valor',
    'Periodicidade': 'periodicidade'
    }
df_tarifas_normal.rename(columns=novos_nomes_colunas, inplace=True)
df_tarifas_normal.head(2)

# COMMAND ----------

# MAGIC %md
# MAGIC Criando chave ``` fk_calendario```

# COMMAND ----------

# Garantindo data_vigencia como data
df_tarifas_normal['data_vigencia'] = df_tarifas_normal['data_vigencia'].astype('datetime64[ns]')

# Criando chave
df_tarifas_normal['fk_calendario'] = df_tarifas_normal.data_vigencia.dt.year.map(str) + df_tarifas_normal.data_vigencia.dt.quarter.map(str)

# COMMAND ----------

# removendo duplicadas
df_tarifas_normal.drop_duplicates(subset=['pk_tarifa'], inplace=True)
df_tarifas_normal.head(2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 Salvando dados tratados

# COMMAND ----------

# refazendo cópias

df_consolidado = df_consolidado_normal.copy()
df_lista_inst = df_lista_inst_normal.copy()
df_reclamações = df_reclamações_normal.copy()
df_tarifas = df_tarifas_normal.copy()

# COMMAND ----------

df_tarifas.to_csv(caminho + 'normalizadas/df_tarifas.csv', encoding='latin1', index=False)
df_lista_inst.to_csv(caminho + 'normalizadas/df_lista_inst.csv', encoding='latin1', index=False)
df_consolidado.to_csv(caminho + 'normalizadas/df_consolidado.csv', encoding='latin1', index=False)
df_reclamações.to_csv(caminho + 'normalizadas/df_reclamações.csv', encoding='latin1', index=False)
