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

def processar_sentenca(frase):
    """
    Função 'ponte' que conecta a interface com os módulos de processamento.
    Retorna os dados processados ou levanta um erro.
    """
    lexico = AnalisadorLexicoAFD()
    sintatico = AnalisadorSintatico()
    matematico = ModuloMatematico()

    # 1. Análise Léxica
    tokens = lexico.tokenizar(frase)
    
    # 2. Análise Sintática (Gera a fórmula e o mapa de variáveis)
    formula, variaveis_map = sintatico.parse(tokens)
    
    # 3. Processamento Matemático (Gera a Tabela Verdade)
    tabela, vars_encontradas, etapas = matematico.gerar_tabela_verdade(formula)
    
    return formula, variaveis_map, tabela, vars_encontradas, etapas

def main():
    configurar_pagina()
    renderizar_cabecalho()

    # --- ENTRADA DE DADOS ---
    col1, col2 = st.columns([3, 1])
    with col1:
        frase_usuario = st.text_input(
            "Digite sua frase lógica:", 
            placeholder="Ex: Se estudo e pratico, então aprendo"
        )
    with col2:
        st.write("##") # Espaçador para alinhar o botão
        botao_gerar = st.button("Gerar Tabela-Verdade", use_container_width=True)