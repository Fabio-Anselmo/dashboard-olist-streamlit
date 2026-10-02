# 📊 Dashboard de Análise de E-Commerce (Olist)

Painel interativo desenvolvido em **Python** utilizando **Streamlit** e **Pandas**, com o objetivo de analisar os principais indicadores de desempenho (KPIs) e o comportamento geográfico de vendas com base na base de dados pública de e-commerce da **Olist**.

---

## 🚀 Funcionalidades do Painel
* **Indicadores Principais (KPIs):** Faturamento Total, Total de Pedidos, Frete Total e Ticket Médio dinâmicos.
* **Filtros Avançados (Sidebar):** 
  * Filtragem por **Status do Pedido** (com tradução completa para o português).
  * Filtragem por **Estado do Cliente (UF)** (com nomes completos e normalização de dados).
* **Análise Geográfica:** Visualização interativa da distribuição de pedidos por estado do Brasil.
* **Proteção de Interface:** Mecanismo integrado para garantir estabilidade visual e evitar problemas de tradução automática do navegador em métricas críticas.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas
* **Python** (Linguagem principal)
* **Streamlit** (Criação da interface web e componentes interativos)
* **Pandas** (Manipulação, limpeza, cruzamento e tratamento de bases de dados)

---

## 📂 Estrutura do Repositório
```text
├── archive/                  # Pasta contendo os datasets originais da Olist (CSV)
├── app.py                    # Código principal da aplicação Streamlit
├── .gitignore                # Arquivos ignorados pelo controle de versão
└── README.md                 # Documentação do projeto
