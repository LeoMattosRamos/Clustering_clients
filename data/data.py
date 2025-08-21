

#%%

import pandas as pd
import numpy as np
import sqlalchemy


#%%


# Configurações
num_linhas = 200000
num_clientes = 5000
np.random.seed(42)

# Criar IDs e idade dos clientes
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

# Criar viés de compra por cliente
viés_clientes = {}
for cid in clientes_ids:
    # Cada cliente tem uma distribuição aleatória de preferência por categoria
    probs = np.random.dirichlet(np.ones(len(categorias)), size=1)[0]
    viés_clientes[cid] = dict(zip(categorias, probs))

# Gerar histórico de compras
clientes = np.random.choice(clientes_ids, size=num_linhas)

datas = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2023-01-01").value // 10**9,
        pd.Timestamp("2025-08-10").value // 10**9,
        num_linhas
    ),
    unit='s'
)

categorias_escolhidas = []
produtos_escolhidos = []
valor_venda = []

for cid in clientes:
    # Escolher categoria baseada no viés do cliente
    probs = list(viés_clientes[cid].values())
    categoria = np.random.choice(categorias, p=probs)
    categorias_escolhidas.append(categoria)
    
    # Escolher produto aleatório dentro da categoria
    produto = np.random.choice(produtos_por_categoria[categoria])
    produtos_escolhidos.append(produto)
    
    # Gerar valor da venda
    if categoria == 'Eletronicos':
        valor_venda.append(round(np.random.uniform(200, 4000), 2))
    elif categoria == 'Roupas':
        valor_venda.append(round(np.random.uniform(30, 500), 2))
    elif categoria == 'Alimentos':
        valor_venda.append(round(np.random.uniform(5, 100), 2))
    elif categoria == 'Brinquedos':
        valor_venda.append(round(np.random.uniform(20, 300), 2))
    elif categoria == 'Livros':
        valor_venda.append(round(np.random.uniform(15, 200), 2))

# Criar DataFrame
df = pd.DataFrame({
    "ID_cliente": clientes,
    "idade": [mapa_idade[cid] for cid in clientes],
    "data": datas,
    "produto": produtos_escolhidos,
    "categoria_produto": categorias_escolhidas,
    "valor_venda": valor_venda
})

# Ordenar e resetar índice
df.sort_values(by=["ID_cliente", "data"], inplace=True)
df.reset_index(drop=True, inplace=True)
df["data"] = df["data"].dt.date


con = sqlalchemy.create_engine("sqlite:///database.db")

create_table = df.to_sql("Vendas", con, if_exists="replace", index=False)
