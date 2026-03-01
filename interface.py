import streamlit as st
import pandas as pd
# Importando os modulos desenvolvidos por Emanuel e Josuel
from base_lexica import AnalisadorLexicoAFD
from sintaxe import AnalisadorSintatico
from modulo_matematico import ModuloMatematico

def configurar_pagina():
    """Configura o layout e o título da aba do navegador."""
    st.set_page_config(
        page_title="Tradutor de Lógica Proposicional - UFMA",
        page_icon="🎓",
        layout="wide"
    )

def renderizar_cabecalho():
    """Exibe o título e as instruções iniciais na tela."""
    st.title("🧠 Analisador Lógico Proposicional")
    st.markdown("""
    Este sistema converte sentenças em linguagem natural (Português) para fórmulas lógicas 
    e gera automaticamente a **Tabela-Verdade**.
    
    **Exemplos de entrada:**
    - *Se chove, então não saio*
    - *Estudo e trabalho, logo passo*
    - *Fico em casa ou vou ao cinema*
    """)
    st.divider()

def main():
    configurar_pagina()
    renderizar_cabecalho()