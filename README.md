



# Ingestão de Dados

## Tarefa 4

#### Requisitos

1. **Requerimento**

Implementar as mesmas atividades da tarefa 3 com as seguintes diferenças:
 - O processamento realizado com Python simples deve ser realizado na plataforma AWS EMR
 - As fontes de dados devem ser as seguintes:
	- Ranking de Instituições por Índice de Reclamações (Arquivos CSV)
	- Tarifas Bancárias - por Segmento e por Instituição (Dados em uma base de dados Relacional)
 - Camadas de Dados no AWS S3:
	 - RAW (Dados Crus)
	 - Trusted (Dados Tratados mas sem implementação de modelagem)
	 - Analytics (Modelado em Star Schema - Replicados em base de dados relacional)
	 - Camadas Trusted e Analytics devem ser mapeadas no AWS Glue Catalog
 - Implementar Airflow e DBT é opcional
 
2. **Microsoft Azure**

Para desenvolver esse projeto, utilizamos o serviço **Microsoft Azure**. Então, baseados na descrição acima, fizemos todas as tarefas nos [serviços equivalentes da plataforma](https://docs.microsoft.com/pt-br/azure/architecture/aws-professional/services), conforme tabela abaixo:

|  Serviço AWS | Serviço do Azure | Descrição |
|--|--|--|
|[Glue](https://aws.amazon.com/glue)  | [Data Factory](https://azure.microsoft.com/services/data-factory) |Processa e move dados entre diferentes dispositivos de computação e armazenamento, bem como fontes de dados locais, em intervalos específicos. Crie, agende, orquestre e gerencie pipelines de dados. |
| [Glue](https://aws.amazon.com/glue)| [Azure Purview](https://azure.microsoft.com/services/purview)|Um serviço unificado de governança de dados que ajuda você a gerenciar e controlar seus dados locais, multinuvem e de SaaS (software como serviço).
| [EMR](https://aws.amazon.com/emr) | [Databricks](https://azure.microsoft.com/services/databricks) | Plataforma de análise com base no Apache Spark.
|[Serviços de armazenamento simples (S3)](https://aws.amazon.com/s3/) | [Armazenamento de Blobs](https://docs.microsoft.com/pt-br/azure/storage/blobs/storage-blobs-introduction) | Serviço de armazenamento de objeto para casos de uso como aplicativos de nuvem, distribuição de conteúdo, backup, arquivamento, recuperação de desastre e análise de big data.
|  [RDS](https://aws.amazon.com/rds) | [Banco de Dados SQL](https://azure.microsoft.com/services/sql-database)  | Serviços gerenciados de banco de dados relacional em que a resiliência, a escala e a manutenção são tratadas principalmente pela plataforma Azure.




#### Resolução resumida do Projeto

Precisamos preparar os dados que estão disponíveis no site do Banco Central para serem consumidos por produtos analíticos, como **Power BI** e **Tableau**.  Esses dados estão disponíveis para análise no [site do banco](https://www.bcb.gov.br/estabilidadefinanceira/tarifas_bancarias).

Como comentado, vamos utilizar o Microsoft Azure na arquitetura de todo o fluxo de dados entre os dados da API/CSV para o banco SQL que vai ser consumido pelo time de analytics. Conforme demostrado abaixo:

<img src="tarefa 4/imagens/esquema de dados.png" />

Assim, temos:

 1. O processamento da Extração, Limpeza e Tratamento e Modelagem via Databricks;
 
 <img src="tarefa 4/imagens/databricks.png" />

 2. O resultado desse processamento sendo salvo em arquivos .csv no Azure Blob Storage, nas pastas raw, trusted e analytics;

 <img src="tarefa 4/imagens/blob storage.png" />


 3. Os dados da camada Analytics sendo carregados em um banco SQL com Data Factory.   

 <img src="tarefa 4/imagens/carregamento dos dados.png" />

 <img src="tarefa 4/imagens/sql.png" />

Com isso, todos os dados podem ser carregados pelo Power BI para que sejam feitas análises.

Nas pastas da tarefas, todos os recursos criados no Azure.

## Tarefa 5

Como já tínhamos realizado todo o trabalho na plataforma Azure até a visualização dos dados, resolvemos melhorar o código de processamento e tratamento dos dados, como também melhorar o Power BI.

 <img src="tarefa 5/imagens/novo_datawrangling_pyspark.png" />

Assim, refizemos todo o código que antes estava escrito em Python para PySpark aproveitando assim, melhor a capacidade do Databricks para o processamento dos dados.
Basicamente, alteramos o Data Factory para considerar esse novo Notebook e eliminamos a modelagem em SQL, desnecessária uma vez que já modelamos os dados também com PySpark.

 <img src="tarefa 5/imagens/pipeline_tarefa5.png" />

No fim, conectamos nosso arquivo Power BI ao banco SQL e ajustamos algumas coisas. A principal alteração foi na modelagem. Agora, usamos apenas Instituições Financeira, e não mais Conglomerados. 
Nas versões anteriores , tentamos usar os dados dos conglomerados, porém não achamos uma base correta para ligar as instituições dos conglomerados com a base de reclamações, por meio de um CNPJ.

 <img src="tarefa 5/imagens/powerbi.png" />
 <img src="tarefa 5/imagens/rnk_gov.png" />


Com isso, os números do Power BI batem exatamente com o dashboard do [Banco Central](https://www.bcb.gov.br/estabilidadefinanceira/rankingreclamacoes), para instituições financeira (não conglomerados).

