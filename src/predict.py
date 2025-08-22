#%%

import pandas as pd
import mlflow
import sqlalchemy


# Conexao com mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")

# Conexao com banco de dados
con = sqlalchemy.create_engine("sqlite:///../data/database.db")

# Modelo features produtos

model_products = mlflow.sklearn.load_model("models:/Cluster_Products_Model/1")

features_products = model_products.feature_names_in_

def import_query(path):
    with open(path) as open_file:
        return(open_file.read())
    
query = import_query("../src/features.products.sql")

df_products = pd.read_sql(query, con)

df_products["Cluster_products"] = model_products.predict(df_products[features_products])

clusters_names = {
    0: "Brinquedos_Lovers",
    1: "Livros&Food",
    2: "Tech_Lovers",
    3: "Moda_Lovers"
}

df_products["Cluster_products"] = df_products["Cluster_products"].map(clusters_names)

df_products = df_products[["Dt_ref", "ID_cliente", "Cluster_products" ]]
df_products

#%%

# Modelo features RFV

model_rfv= mlflow.sklearn.load_model("models:/Cluster_RFV_Model/1")

features_rfv= model_rfv.feature_names_in_

query_rfv = import_query("../src/featuresRFV.sql")

df_rfv = pd.read_sql(query_rfv, con)

df_rfv["Cluster_rfv"] = model_rfv.predict(df_rfv[features_rfv])

clusters_rfv = {0: "01-Frequentes de Baixo Valor",
       1: "03-VIPs/Alta Receita",
       2: "02-Frequentes de Alto Valor",
       3:"04-Risco churn"}


df_rfv["Cluster_rfv"] = df_rfv["Cluster_rfv"].map(clusters_rfv)

df_rfv = df_rfv[["Dt_ref", "ID_cliente", "Cluster_rfv"]]

df_rfv

#%%

df_clusters = pd.merge(df_rfv, df_products, on="ID_cliente")
df_clusters = df_clusters.drop(columns="Dt_ref_y")
df_clusters["Cluster"] = df_clusters["Cluster_rfv"] + ":" + df_clusters["Cluster_products"]
df_clusters.drop(columns=["Cluster_rfv", "Cluster_products"], inplace=True)
df_clusters.rename(columns={"Dt_ref_x": "Dt_ref"}, inplace=True)


df_clusters.to_sql("Cluster_clients", con, if_exists="append")


