#%%


import pandas as pd


#%%

import pandas as pd
import numpy as np

# Configurações
num_linhas = 50000
num_clientes = 2000  # cada cliente terá várias compras
np.random.seed(42)

# Gerar IDs de clientes
clientes = np.random.choice(range(1000, 1000 + num_clientes), size=num_linhas)

# Gerar datas aleatórias nos últimos 2 anos
datas = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2023-01-01").value // 10**9,
        pd.Timestamp("2025-01-01").value // 10**9,
        num_linhas
    ),
    unit='s'
)

# Produtos e categorias
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Brinquedos', 'Livros']
produtos_por_categoria = {
    'Eletrônicos': ['Smartphone', 'Laptop', 'Fone de ouvido', 'Smartwatch'],
    'Roupas': ['Camiseta', 'Calça', 'Tênis', 'Jaqueta'],
    'Alimentos': ['Arroz', 'Feijão', 'Leite', 'Chocolate'],
    'Brinquedos': ['Boneca', 'Carrinho', 'Quebra-cabeça', 'Lego'],
    'Livros': ['Romance', 'Autoajuda', 'Ficção', 'Didático']
}

# Escolher categorias aleatórias
categoria_produto = np.random.choice(categorias, size=num_linhas)

# Escolher produto correspondente à categoria
produto = [np.random.choice(produtos_por_categoria[cat]) for cat in categoria_produto]

# Gerar valor de venda aleatório por produto
valor_venda = []
for cat in categoria_produto:
    if cat == 'Eletrônicos':
        valor_venda.append(round(np.random.uniform(100, 2000), 2))
    elif cat == 'Roupas':
        valor_venda.append(round(np.random.uniform(20, 300), 2))
    elif cat == 'Alimentos':
        valor_venda.append(round(np.random.uniform(5, 50), 2))
    elif cat == 'Brinquedos':
        valor_venda.append(round(np.random.uniform(10, 200), 2))
    elif cat == 'Livros':
        valor_venda.append(round(np.random.uniform(10, 150), 2))

# Criar DataFrame
df = pd.DataFrame({
    "ID_cliente": clientes,
    "data": datas,
    "produto": produto,
    "categoria_produto": categoria_produto,
    "valor_venda": valor_venda
})

# Ordenar por cliente e data (opcional)
df.sort_values(by=["ID_cliente", "data"], inplace=True)
df.reset_index(drop=True, inplace=True)

df
