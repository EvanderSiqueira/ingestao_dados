# Databricks notebook source
# MAGIC %md
# MAGIC # Extração dos dados

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Deletar** antes de subir no Github

# COMMAND ----------

from google.colab import drive
drive.mount('/content/drive')

# COMMAND ----------

# MAGIC %md
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 Importando bibliotecas

# COMMAND ----------

# MAGIC %md
# MAGIC Carregando bibliotecas necessárias

# COMMAND ----------

import requests
import pandas as pd
from io import BytesIO

# COMMAND ----------

# MAGIC %md
# MAGIC Criando função para gerar os dados da APIs

# COMMAND ----------

# onde codigos é uma lista, url_base é uma string e tipo_url pode ser simples (sem filtros) ou composta (com filtros)
def gerarDataFrame(url_base, tipo_url, codigos, nova_coluna):
    
    df = pd.DataFrame()
    session = requests.Session()
    
    if tipo_url == "simples":
        r = session.get(url = url_base)
        df = df.append(pd.json_normalize(r.json(), record_path =['value']), ignore_index = True)
        df.reset_index(drop=True)
    else:
        for codigo in codigos:
            url_final = url_base + codigo + "'&$top=10000&$format=json"
            r = session.get(url = url_final)
            df_temp = pd.json_normalize(r.json(), record_path =['value'])
            df_temp[nova_coluna] = codigo
            df = df.append(df_temp)
    
    df.reset_index(drop=True)
    return df

# COMMAND ----------

# MAGIC %md
# MAGIC Função para gerar os arquivos CSV, semetre por semestre [desse link](https://dados.gov.br/dataset/ranking-de-instituicoes-por-indice-de-reclamacoes/resource/1831c634-9055-4687-8faa-be9c9b811912).

# COMMAND ----------

# gerar arquivos CSV
def gerarCSV(lista_anos, lista_trimestre):
  df = pd.DataFrame()
  session = requests.Session()

  for ano in lista_anos:
      for trimestre in lista_trimestre:
        url_base = 'https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano=' + str(ano) + '&periodicidade=TRIMESTRAL&periodo=' + str(trimestre) + '&tipo=Bancos+e+financeiras'
        
        r = session.get(url_base).content
        df = df.append(pd.read_csv(BytesIO(r), encoding='latin1', delimiter=';'))

  return df

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 Gerandos os dados

# COMMAND ----------

# MAGIC %md
# MAGIC URL dos dados da API e caminho salvamento

# COMMAND ----------

url_grupos_consolidados = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/GruposConsolidados?$top=10000&$format=json"
url_lista_instituicoes = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaInstituicoesDeGrupoConsolidado(CodigoGrupoConsolidado=@CodigoGrupoConsolidado)?@CodigoGrupoConsolidado='"
url_tarifas = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='F'&@CNPJ='"

# caminho para salvamento dos arquivos
caminho = '/content/drive/MyDrive/Colab Notebooks/dados/'

# COMMAND ----------

# MAGIC %md
# MAGIC Obtendo o dados dos Grupos Consolidados

# COMMAND ----------

df_consolidado = gerarDataFrame(url_grupos_consolidados, 'simples', [], '')

# COMMAND ----------

# MAGIC %md
# MAGIC Obtendo a lista de todas as Instituições com base no Grupo Consolidado (df_consolidado)

# COMMAND ----------

# lista dos códigos dos grupos
lista_codigo_grupo = df_consolidado.Codigo.tolist()

# COMMAND ----------

# obtendo lista de todas as instituições
df_lista_inst = gerarDataFrame(url_lista_instituicoes, 'composta', lista_codigo_grupo, 'CodigoGrupo')

# COMMAND ----------

# MAGIC %md
# MAGIC Obtendo lista de Tarifas para Pessoas Fisicas

# COMMAND ----------

# lista dos CNPJs das instituições
lista_cnpjs = df_lista_inst.Cnpj.tolist()

# COMMAND ----------

# obtendo lista de todas as tarifas (demora para processar tudo)
df_tarifas = gerarDataFrame(url_tarifas, 'composta', lista_cnpjs, 'CNPJ')

# COMMAND ----------

# MAGIC %md
# MAGIC Obtendo a lista de reclamações

# COMMAND ----------

# Criando a lista de anos e de trimestres
lista_anos = [2020, 2021]
lista_trimestre = [1, 2, 3, 4]

# COMMAND ----------

#obtendo lista de todas as reclamações dos anos e semestres acima
df_reclamações = gerarCSV(lista_anos, lista_trimestre)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 Salvando os dados em um diretório

# COMMAND ----------

df_tarifas.to_csv(caminho + '/df_tarifas.csv', encoding='latin1')
df_lista_inst.to_csv(caminho + '/df_lista_inst.csv', encoding='latin1')
df_consolidado.to_csv(caminho + '/df_consolidado.csv', encoding='latin1')
df_reclamações.to_csv(caminho + '/df_reclamações.csv', encoding='latin1')
