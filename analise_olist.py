import pandas as pd

# Carregando o arquivo de pedidos da pasta archive
df_orders = pd.read_csv("archive/olist_orders_dataset.csv")

# Mostrando as 5 primeiras linhas para conferir se leu direito
print(df_orders.head())

import pandas as pd

# 1. Carregar os pedidos
df_orders = pd.read_csv("archive/olist_orders_dataset.csv")

# 2. Carregar os itens dos pedidos
df_items = pd.read_csv("archive/olist_order_items_dataset.csv")

# 3. Calcular o Faturamento Total (somando a coluna 'price')
faturamento_total = df_items['price'].sum()

print(f"Faturamento Total: R$ {faturamento_total:,.2f}")

# 4. Total de Pedidos únicos
total_pedidos = df_orders['order_id'].nunique()

# 5. Frete Total
freight_total = df_items['freight_value'].sum()

# 6. Ticket Médio (Faturamento / Total de Pedidos)
ticket_medio = faturamento_total / total_pedidos

print(f"Total de Pedidos: {total_pedidos:,}")
print(f"Frete Total: R$ {freight_total:,.2f}")
print(f"Ticket Médio: R$ {ticket_medio:,.2f}")