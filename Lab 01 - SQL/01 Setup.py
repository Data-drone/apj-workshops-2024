# Databricks notebook source
import os

current_user_id = (
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
)
#datasets_location = f"/FileStore/tmp/{current_user_id}/datasets/"

catalog = "workspace"
database_name = current_user_id.split("@")[0].replace(".", "_")
datasets_location = f'/Volumes/{catalog}/{database_name}/datasets'


# Create catalog (instructor only)
# spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog};")
# spark.sql(f"GRANT USE CATALOG ON CATALOG {catalog} to `{current_user_id}`")
# spark.sql(f"GRANT CREATE SCHEMA ON CATALOG {catalog} to `{current_user_id}`")
spark.sql(f"USE CATALOG {catalog};")

# Create database
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name};")
spark.sql(f"USE {database_name}")

# Create Volume
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{database_name}.datasets")

# COMMAND ----------

import os
import requests


def replace_in_files(directory, old_word, new_word):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".sql"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    file_contents = file.read()

                # Replace the target string
                file_contents = file_contents.replace(old_word, new_word)

                # Write the file out again
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_contents)
                print(f"Updated file: {file_path}")


directory_path = f"/Workspace/Users/{current_user_id}/apj-workshops-2024"
replace_in_files(directory_path, "catalog.database", f"{catalog}.{database_name}")
replace_in_files(directory_path, "email_address", current_user_id)

# COMMAND ----------

working_dir = "/".join(os.getcwd().split("/")[0:5])
git_datasets_location = f"{working_dir}/Datasets/SQL Lab"
git_permalinks = 'https://github.com/Data-drone/apj-workshops-2024/blob/e02468bf183113c9dfdef740d6283f19a202c7d6/Datasets/SQL%20Lab/'


dbutils.fs.mkdirs(f'{datasets_location}/SQL_Lab/')

sample_datasets = [
    "dim_customer",
    "dim_locations",
    "dim_products",
    "fact_apj_sale_items",
    "fact_apj_sales",
]


for sample_data in sample_datasets:
    dbutils.fs.rm(f"{datasets_location}/SQL_Lab/{sample_data}.csv.gz")
    response = requests.get(f'https://github.com/Data-drone/apj-workshops-2024/raw/e02468bf183113c9dfdef740d6283f19a202c7d6/Datasets/SQL%20Lab/{sample_data}.csv.gz')
    response.raise_for_status()
    file_path = f'{datasets_location}/SQL_Lab/{sample_data}.csv.gz'

    # Write the content of the response to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)

# COMMAND ----------

dbutils.fs.ls(f"{datasets_location}/SQL_Lab/")


# COMMAND ----------

# MAGIC %md
# MAGIC ###GET the DATABASE NAME below
# MAGIC You should use this throughout the lab

# COMMAND ----------

print(f"Use this catalog.database name through out the lab: {catalog}.{database_name}")

# COMMAND ----------

table_name = "dim_customer"
sample_file = f"{table_name}.csv.gz"
file_path = f'{datasets_location}/SQL_Lab/{table_name}.csv.gz'
#spark.conf.set("sampledata.path", f"dbfs:{datasets_location}SQL_Lab/{sample_file}")
#spark.conf.set("table.name", table_name)
spark.sql(f"DROP TABLE IF EXISTS `{table_name}`")

df = spark.read.option("header", "true") \
    .option("compression", "gzip") \
    .csv(file_path)

df.write.saveAsTable(f'{catalog}.{database_name}.{table_name}')


# COMMAND ----------

table_name = "dim_locations"
sample_file = f"{table_name}.csv.gz"
file_path = f'{datasets_location}/SQL_Lab/{table_name}.csv.gz'

spark.sql(f"DROP TABLE IF EXISTS `{table_name}`")

df = spark.read.option("header", "true") \
    .option("compression", "gzip") \
    .csv(file_path)

df.write.saveAsTable(f'{catalog}.{database_name}.{table_name}')


# COMMAND ----------

table_name = "dim_products"
sample_file = f"{table_name}.csv.gz"
file_path = f'{datasets_location}/SQL_Lab/{table_name}.csv.gz'

spark.sql(f"DROP TABLE IF EXISTS `{table_name}`")

df = spark.read.option("header", "true") \
    .option("compression", "gzip") \
    .csv(file_path)

df.write.saveAsTable(f'{catalog}.{database_name}.{table_name}')


# COMMAND ----------

table_name = "fact_apj_sales"
sample_file = f"{table_name}.csv.gz"
file_path = f'{datasets_location}/SQL_Lab/{table_name}.csv.gz'

spark.sql(f"DROP TABLE IF EXISTS `{table_name}`")

df = spark.read.option("header", "true") \
    .option("compression", "gzip") \
    .csv(file_path)

df.write.saveAsTable(f'{catalog}.{database_name}.{table_name}')

# COMMAND ----------

table_name = "fact_apj_sale_items"
sample_file = f"{table_name}.csv.gz"
file_path = f'{datasets_location}/SQL_Lab/{table_name}.csv.gz'

spark.sql(f"DROP TABLE IF EXISTS `{table_name}`")

df = spark.read.option("header", "true") \
    .option("compression", "gzip") \
    .csv(file_path)

df.write.saveAsTable(f'{catalog}.{database_name}.{table_name}')

# COMMAND ----------

# MAGIC %sql
# MAGIC /*store_data, json*/
# MAGIC CREATE
# MAGIC OR REPLACE TABLE store_data_json AS
# MAGIC SELECT
# MAGIC   1 AS id,
# MAGIC   '{
# MAGIC    "store":{
# MAGIC       "fruit": [
# MAGIC         {"weight":8,"type":"apple"},
# MAGIC         {"weight":9,"type":"pear"}
# MAGIC       ],
# MAGIC       "basket":[
# MAGIC         [1,2,{"b":"y","a":"x"}],
# MAGIC         [3,4],
# MAGIC         [5,6]
# MAGIC       ],
# MAGIC       "book":[
# MAGIC         {
# MAGIC           "author":"Nigel Rees",
# MAGIC           "title":"Sayings of the Century",
# MAGIC           "category":"reference",
# MAGIC           "price":8.95
# MAGIC         },
# MAGIC         {
# MAGIC           "author":"Herman Melville",
# MAGIC           "title":"Moby Dick",
# MAGIC           "category":"fiction",
# MAGIC           "price":8.99,
# MAGIC           "isbn":"0-553-21311-3"
# MAGIC         },
# MAGIC         {
# MAGIC           "author":"J. R. R. Tolkien",
# MAGIC           "title":"The Lord of the Rings",
# MAGIC           "category":"fiction",
# MAGIC           "reader":[
# MAGIC             {"age":25,"name":"bob"},
# MAGIC             {"age":26,"name":"jack"}
# MAGIC           ],
# MAGIC           "price":22.99,
# MAGIC           "isbn":"0-395-19395-8"
# MAGIC         }
# MAGIC       ],
# MAGIC       "bicycle":{
# MAGIC         "price":19.95,
# MAGIC         "color":"red"
# MAGIC       }
# MAGIC     },
# MAGIC     "owner":"amy",
# MAGIC     "zip code":"94025",
# MAGIC     "fb:testid":"1234"
# MAGIC  }' as raw;
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   store_data_json;

# COMMAND ----------

print(f"Use this catalog.database name through out the lab: {catalog}.{database_name}")
