import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
        # Gráfico de distribuição das contas a pagar por fornecedor
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        df_fornecedor = pd.read_sql_query("SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor", conn)
        fig, ax = plt.subplots()
        ax.pie(df_fornecedor['total'], labels=df_fornecedor['fornecedor'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)
        
        # Status das contas a pagar e a receber
        st.subheader("Status das Contas a Pagar e Receber")
        df_status_pagar = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_pagar GROUP BY status", conn)
        df_status_receber = pd.read_sql_query("SELECT status, SUM(valor) as total FROM contas_receber GROUP BY status", conn)
        
        fig, ax = plt.subplots()
        ax.bar(df_status_pagar['status'], df_status_pagar['total'], label='Contas a Pagar', alpha=0.6)
        ax.bar(df_status_receber['status'], df_status_receber['total'], label='Contas a Receber', alpha=0.6)
        ax.set_ylabel("Valor Total")
        ax.set_title("Status das Contas a Pagar e Receber")
        ax.legend()
        st.pyplot(fig)
        
        # Top 5 clientes com maior receita
        st.subheader("Top 5 Clientes com Maior Receita")
        df_top_clientes = pd.read_sql_query("SELECT cliente, SUM(valor) as total FROM contas_receber GROUP BY cliente ORDER BY total DESC LIMIT 5", conn)
        st.dataframe(df_top_clientes)
        
        fig, ax = plt.subplots()
        ax.bar(df_top_clientes['cliente'], df_top_clientes['total'], color='green')
        ax.set_ylabel("Receita Total")
        ax.set_title("Top 5 Clientes com Maior Receita")
        st.pyplot(fig)
    
    conn.close()
    
if __name__ == "__main__":
    main()