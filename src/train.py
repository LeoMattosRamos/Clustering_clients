#%%

import pandas as pd
import sqlalchemy
from sklearn import cluster
from sklearn import metrics
from sklearn import pipeline
from sklearn import preprocessing
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn
import mlflow

# Conexao com mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")

#Setando Experimento
mlflow.set_experiment(experiment_id= "804881385784189289")

con = sqlalchemy.create_engine("sqlite:///../data/database.db")

def import_query(path):
    with open(path) as open_file:
        return(open_file.read())
    
query = import_query("../src/features.products.sql")

df = pd.read_sql(query, con)

X = df[df.columns[3:]] 



#%% 
# Verificando melhor valor de clusters para features de produtos

for k in range(2,10):
    model = cluster.KMeans(random_state=42, n_clusters= k)
    pipe = pipeline.Pipeline(
    steps= [
        ("Scaler", preprocessing.StandardScaler()),
        ("model", model)
    ]
)
    labels = pipe.fit_predict(X)
    X_scaled = pipe.named_steps["Scaler"].transform(X)
    score = metrics.silhouette_score(X_scaled, labels)
    print(f"k={k} ---> silhouete: {score}")


#%%
with mlflow.start_run(run_name="Kmeans_Products"):

    mlflow.sklearn.autolog()

    kmeans_model = cluster.KMeans(random_state=42, n_clusters= 4)

    pipe_model = pipeline.Pipeline(
        steps= [
            ("Scaler", preprocessing.StandardScaler()),
            ("model", kmeans_model)
        ]
    )

    train_model = pipe_model.fit(X)
    labels = train_model.predict(X)

x_label = X.copy()
x_label["LABEL"] = labels


seaborn.heatmap(x_label.groupby("LABEL").mean(), cmap= "YlGnBu")
plt.show()

x_label.groupby("LABEL").mean()

dc_produtos = {
    0: "Brinquedos_Lovers",
    1: "Livros&Food",
    2: "Tech_Lovers",
    3: "Moda_Lovers"
}




#%%
# Aplicando arvore para entender features mais importantes 

clf = tree.DecisionTreeClassifier(random_state=42)

clf.fit(X, labels)


features_importances = pd.Series(clf.feature_importances_, index=df.columns[2:].tolist())

features_importances.sort_values(ascending=False)



#%% 
# Agora para as features de RFV 

query_rfv = import_query("../src/featuresRFV.sql")

df_rfv = pd.read_sql(query_rfv,con)

X_rfv = df_rfv.drop(columns=["ID_cliente", "Dt_ref", "idade","Idade_base", "Frequencia"])



#%%

for k in range(2,10):
    model = cluster.KMeans(random_state=42, n_clusters= k)
    pipe = pipeline.Pipeline(
    steps= [
        ("Scaler", preprocessing.StandardScaler()),
        ("model", model)
    ]
)
    labels = pipe.fit_predict(X_rfv)
    X_scaled = pipe.named_steps["Scaler"].transform(X_rfv )
    score = metrics.silhouette_score(X_scaled, labels)
    print(f"k={k} ---> silhouete: {score}")


#%%

with mlflow.start_run(run_name="Kmeans_RFV"):

    mlflow.sklearn.autolog()

    kmeans_model = cluster.KMeans(random_state=42, n_clusters= 4)

    pipe_model = pipeline.Pipeline(
        steps= [
            ("Scaler", preprocessing.StandardScaler()),
            ("model", kmeans_model)
        ]
    )

    train_model = pipe_model.fit(X_rfv)
    labels = train_model.predict(X_rfv)

x_label = X_rfv.copy()
x_label["LABEL"] = labels


seaborn.heatmap(x_label.groupby("LABEL").mean(), cmap= "YlGnBu")
plt.show()

x_label.groupby("LABEL").mean()

dic_rfv = {0: "01-Frequentes de Baixo Valor",
       1: "03-VIPs/Alta Receita",
       2: "02-Frequentes de Alto Valor",
       3:"04-Risco churn"}




#%%
# Outra forma seria verificar dist das features de RFV em relacao a base -> podemos fazer cluster personalizados na nossa base nesse caso

query2 = import_query("../src/featuresRFV.sql")

df2 = pd.read_sql(query2,con)

colunas = df2.columns[1:].tolist()

for i in colunas:
    df_recencia = df2[i].sort_values().reset_index()
    df_recencia["unit"] = 1
    df_recencia["acum"] = df_recencia["unit"].cumsum()
    df_recencia["pct_acumulado"] = df_recencia["acum"]/df_recencia["acum"].max()

    plt.plot(df_recencia[i], df_recencia["pct_acumulado"])
    plt.grid(True)
    plt.xlabel(f"{i}")
    plt.ylabel("Pct acum base")
    plt.show()



