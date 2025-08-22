

#%%

import pandas as pd
import numpy as np
import sqlalchemy


#%%



# Configurações
num_linhas = 200_000
num_clientes = 5000
np.random.seed(42)

# IDs e idade dos clientes
clientes_ids = np.arange(1000, 1000 + num_clientes)
idades = np.random.randint(18, 70, size=num_clientes)
mapa_idade = dict(zip(clientes_ids, idades))

# Categorias e produtos
categorias = ['Eletronicos', 'Roupas', 'Alimentos', 'Brinquedos', 'Livros']
produtos_por_categoria = {
    'Eletronicos': ['Smartphone', 'Laptop', 'Fone de ouvido', 'Smartwatch'],
    'Roupas': ['Camiseta', 'Calça', 'Tênis', 'Jaqueta'],
    'Alimentos': ['Arroz', 'Feijão', 'Leite', 'Chocolate'],
    'Brinquedos': ['Boneca', 'Carrinho', 'Quebra-cabeça', 'Lego'],
    'Livros': ['Romance', 'Autoajuda', 'Ficção', 'Didático']
}

# --- Segmentos de clientes
n_recorrentes = int(num_clientes * 0.3)
n_ocasionais = int(num_clientes * 0.5)
n_inativos = num_clientes - (n_recorrentes + n_ocasionais)

clientes_recorrentes = clientes_ids[:n_recorrentes]
clientes_ocasionais = clientes_ids[n_recorrentes:n_recorrentes+n_ocasionais]
clientes_inativos = clientes_ids[n_recorrentes+n_ocasionais:]

# --- Criar clientes para todas as linhas
clientes = np.random.choice(clientes_ids, size=num_linhas, replace=True)

# --- Datas
datas = []
for cid in clientes:
    # Últimos 12 meses ou antes
    if np.random.rand() < 0.6:  # 60% das compras nos últimos 12 meses
        # Últimos 12 meses (2024-08-11 a 2025-08-10)
        datas.append(pd.to_datetime(
            np.random.randint(pd.Timestamp("2024-08-11").value//10**9,
                              pd.Timestamp("2025-08-10").value//10**9),
            unit="s"
        ))
    else:
        # Antes dos 12 meses (2024-01-01 a 2024-08-10)
        datas.append(pd.to_datetime(
            np.random.randint(pd.Timestamp("2024-01-01").value//10**9,
                              pd.Timestamp("2024-08-10").value//10**9),
            unit="s"
        ))

# --- Categorias, produtos e valores
categorias_escolhidas = []
produtos_escolhidos = []
valor_venda = []

for i, cid in enumerate(clientes):
    categoria = np.random.choice(categorias)
    categorias_escolhidas.append(categoria)
    
    produto = np.random.choice(produtos_por_categoria[categoria])
    produtos_escolhidos.append(produto)
    
    data_compra = datas[i]
    # Diferenciação de perfil apenas nos últimos 12 meses
    if data_compra >= pd.Timestamp("2024-08-11"):
        if cid in clientes_recorrentes:
            base = 1.2
        elif cid in clientes_ocasionais:
            base = 1.0
        else:
            base = 0.8
    else:
        base = 1.0  # antes dos 12 meses, uniforme
    
    if categoria == 'Eletronicos':
        valor_venda.append(round(np.random.uniform(200, 4000)*base, 2))
    elif categoria == 'Roupas':
        valor_venda.append(round(np.random.uniform(30, 500)*base, 2))
    elif categoria == 'Alimentos':
        valor_venda.append(round(np.random.uniform(5, 100)*base, 2))
    elif categoria == 'Brinquedos':
        valor_venda.append(round(np.random.uniform(20, 300)*base, 2))
    elif categoria == 'Livros':
        valor_venda.append(round(np.random.uniform(15, 200)*base, 2))

# --- Criar DataFrame final
df = pd.DataFrame({
    "ID_cliente": clientes,
    "idade": [mapa_idade[cid] for cid in clientes],
    "data": datas,
    "produto": produtos_escolhidos,
    "categoria_produto": categorias_escolhidas,
    "valor_venda": valor_venda
})

# Ordenar
df.sort_values(by=["ID_cliente", "data"], inplace=True)
df.reset_index(drop=True, inplace=True)
df["data"] = df["data"].dt.date






#%%

con = sqlalchemy.create_engine("sqlite:///database.db")

create_table = df.to_sql("Vendas", con, if_exists="replace", index=False)
