import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
 
# ---------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------------
st.set_page_config(page_title="Dashboard Olist - E-Commerce", layout="wide")
 
# Impede o tradutor automático do navegador de alterar o texto da página.
# (É ele que transforma "AM" em "Sou": a base de dados está correta.)
components.html(
    """
    <script>
    const d = window.parent.document;
    d.documentElement.setAttribute('translate', 'no');
    d.documentElement.classList.add('notranslate');
    if (!d.querySelector('meta[name="google"]')) {
        const m = d.createElement('meta');
        m.name = 'google';
        m.content = 'notranslate';
        d.head.appendChild(m);
    }
    </script>
    """,
    height=0,
)
 
st.title("📊 Dashboard de Análise de E-Commerce (Olist)")
st.markdown("Painel interativo com filtros dinâmicos na barra lateral e tratamento de dados.")
 
# ---------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------
TRADUCAO_STATUS = {
    'delivered': 'Entregue',
    'shipped': 'Enviado',
    'processing': 'Em Processamento',
    'invoiced': 'Faturado',
    'created': 'Criado',
    'approved': 'Aprovado',
    'canceled': 'Cancelado',
    'unavailable': 'Indisponível',
}
 
NOMES_UF = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins',
}
 
 
def formatar_uf(uf):
    """Mostra 'AM – Amazonas' no lugar da sigla solta (evita tradução automática)."""
    return uf if uf == 'Todos' else f"{uf} – {NOMES_UF.get(uf, uf)}"
 
 
# ---------------------------------------------------------------
# CARREGAMENTO E TRATAMENTO DOS DADOS (cacheado)
# ---------------------------------------------------------------
@st.cache_data
def carregar_dados():
    df_orders = pd.read_csv(
        "archive/olist_orders_dataset.csv",
        usecols=['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp'],
    )
    df_items = pd.read_csv(
        "archive/olist_order_items_dataset.csv",
        usecols=['order_id', 'price', 'freight_value'],
    )
    df_customers = pd.read_csv(
        "archive/olist_customers_dataset.csv",
        usecols=['customer_id', 'customer_state'],
    )
 
    # Traduz o status dos pedidos
    df_orders['status_pt'] = (
        df_orders['order_status'].map(TRADUCAO_STATUS).fillna(df_orders['order_status'])
    )
 
    # Cruza pedidos com clientes
    df = pd.merge(df_orders, df_customers, on='customer_id', how='left')
 
    # Padroniza a UF
    df['customer_state'] = df['customer_state'].astype(str).str.upper().str.strip()
 
    # Mantém apenas UFs válidas e informa quantas linhas foram descartadas
    invalidos = int((~df['customer_state'].isin(NOMES_UF.keys())).sum())
    df = df[df['customer_state'].isin(NOMES_UF.keys())]
 
    return df, df_items, invalidos
 
 
with st.spinner("Carregando e processando os dados da Olist..."):
    df_base, df_items, linhas_descartadas = carregar_dados()
 
if linhas_descartadas > 0:
    st.warning(f"{linhas_descartadas} pedido(s) com UF inválida foram descartados.")
 
# ---------------------------------------------------------------
# BARRA LATERAL E FILTROS
# ---------------------------------------------------------------
st.sidebar.header("🔍 Filtros Avançados")
 
status_disponiveis = ['Todos'] + sorted(df_base['status_pt'].dropna().unique())
status_selecionado = st.sidebar.selectbox("Filtrar por Status do Pedido", status_disponiveis)
 
estados_disponiveis = ['Todos'] + sorted(df_base['customer_state'].unique())
estado_selecionado = st.sidebar.selectbox(
    "Filtrar por Estado do Cliente (UF)",
    estados_disponiveis,
    format_func=formatar_uf,
)
 
# Aplica os filtros
df_filtrado = df_base
if status_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['status_pt'] == status_selecionado]
if estado_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['customer_state'] == estado_selecionado]
 
df_items_filtrado = df_items[df_items['order_id'].isin(df_filtrado['order_id'])]
 
# ---------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------
faturamento_total = df_items_filtrado['price'].sum()
freight_total = df_items_filtrado['freight_value'].sum()
total_pedidos = df_filtrado['order_id'].nunique()
ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0.0
 
st.subheader("📈 Indicadores de Desempenho")
st.markdown(
    f"*Filtros ativos — Status: **{status_selecionado}** | "
    f"Estado: **{formatar_uf(estado_selecionado)}***"
)
 
col1, col2, col3, col4 = st.columns(4)
 
with col1:
    st.metric(label="Faturamento Total", value=f"R$ {faturamento_total:,.2f}")
with col2:
    st.metric(label="Total de Pedidos", value=f"{total_pedidos:,}")
with col3:
    st.metric(label="Frete Total", value=f"R$ {freight_total:,.2f}")
with col4:
    st.markdown(
        '<p translate="no" style="font-size: 14px; color: rgb(163, 168, 184); '
        'margin-bottom: 0px;">Ticket Médio</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h3 translate="no" style="margin-top: 0px;">R$ {ticket_medio:,.2f}</h3>',
        unsafe_allow_html=True,
    )
 
st.divider()
 
# ---------------------------------------------------------------
# GRÁFICO E TABELA
# ---------------------------------------------------------------
col_esq, col_dir = st.columns(2)
 
with col_esq:
    st.subheader("📍 Distribuição de Pedidos")
    if total_pedidos == 0:
        st.warning("⚠️ Não há registros para os filtros selecionados.")
    elif estado_selecionado == 'Todos':
        top_estados = df_filtrado['customer_state'].value_counts().head(5)
        top_estados.index = [formatar_uf(uf) for uf in top_estados.index]
        st.bar_chart(top_estados)
    else:
        st.success(f"Estado selecionado: **{formatar_uf(estado_selecionado)}**")
        st.metric(
            label=f"Volume de Pedidos em {estado_selecionado}",
            value=f"{total_pedidos:,}",
        )
 
with col_dir:
    st.subheader("📋 Amostra dos Dados Filtrados")
    if total_pedidos > 0:
        st.dataframe(
            df_filtrado[['order_id', 'customer_state', 'status_pt', 'order_purchase_timestamp']].head(5),
            hide_index=True,
        )
    else:
        st.info("Nenhum dado encontrado para exibir na tabela.")