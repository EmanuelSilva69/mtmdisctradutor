import streamlit as st
import pandas as pd
# Importando os modulos desenvolvidos por Emanuel e Josuel
from base_lexica import AnalisadorLexicoAFD
from sintaxe import AnalisadorSintatico
from modulo_matematico import ModuloMatematico
import re

def configurar_pagina():
    """Configura o layout e o título da aba do navegador."""
    st.set_page_config(
        page_title="Tradutor de Lógica Proposicional - UFMA",
        page_icon="🎓",
        layout="wide"
    )

def renderizar_cabecalho():
    """Exibe o título e as instruções iniciais na tela."""
    st.title(" Analisador Lógico Proposicional")
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

    # Análise léxica
    tokens = lexico.tokenizar(frase)
    
    # Análise sintática (Gera a fórmula e o mapa de variáveis)
    formula, variaveis_map = sintatico.parse(tokens)
    
    # Processamento matemático (Gera a Tabela Verdade)
    tabela, vars_encontradas, etapas = matematico.gerar_tabela_verdade(formula)
    
    return formula, variaveis_map, tabela, vars_encontradas, etapas

def validar_proposicao(frase):
    """
    Validação semântica simples:
    """
    frase = frase.strip()

    if "?" in frase or "!" in frase:
        return False, "Não é uma proposição."

    return True, ""

def main():
    configurar_pagina()
    renderizar_cabecalho()

    with st.form(key="form_logica"):
        col1, col2 = st.columns([3, 1])
        with col1:
            frase_usuario = st.text_input(
                "Digite sua frase lógica:", 
                placeholder="Ex: Se estudo e pratico, então aprendo"
            )
        with col2:
            st.write("##") 
        
            botao_gerar = st.form_submit_button("Gerar Tabela-Verdade", use_container_width=True)

    if botao_gerar:
        if not frase_usuario.strip():
            st.warning("Por favor, digite uma frase antes de processar.")
            return
        
        valido, mensagem = validar_proposicao(frase_usuario)

        if not valido:
            st.error(mensagem)
            return
        
        # Limitação: Não suporta símbolos de Lógica de Predicados
        if re.search(r"[∀∃]", frase_usuario):
            st.warning("ALERTA: Este sistema suporta apenas Lógica Proposicional. Quantificadores formais (∀, ∃) não são suportados.")
            return
    
        # Não aceita parênteses manuais
        if "(" in frase_usuario or ")" in frase_usuario:
            st.warning("ALERTA: O sistema não aceita parênteses manuais. A precedência é definida automaticamente.")
            return
        # Filtro de caracteres e tamanho máximo
        if len(frase_usuario) > 200:
            st.error("AVISO: A frase deve conter no máximo 200 caracteres.")
            return

        if not re.match(r"^[A-Za-zÀ-ÿ\s,.]+$", frase_usuario):
            st.error("ALERTA: A frase contém caracteres inválidos.")
            return
        try:
            formula, vars_map, tabela, vars_list, etapas = processar_sentenca(frase_usuario)
            # Limite de variáveis
            if len(vars_list) > 6:
                st.error("ALERTA: O sistema permite no máximo 6 proposições distintas (limitação computacional).")
                return
            if len(vars_list) < 2:
                st.error("A Tabela-Verdade só pode ser gerada para fórmulas com pelo menos duas proposições.")
                return

            st.subheader("Análise Concluída")
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.info("**Mapeamento de Proposições:**")
                for termo, letra in vars_map.items():
                    st.write(f"🔹 **{letra}**: {termo}")

            with res_col2:
                st.success("**Fórmula Lógica Gerada:**")
                st.code(formula, language="text")

            st.divider()
            st.subheader("Tabela-Verdade")
            
            df = pd.DataFrame(tabela)
            
            # 2. Ordenar as colunas (Variáveis primeiro, depois etapas parciais)
            # Garantimos que a fórmula principal fique por último
            colunas_ordenadas = vars_list + [e for e in etapas if e not in vars_list and e != formula]
            if formula not in colunas_ordenadas:
                colunas_ordenadas.append(formula)
            
            # Filtra o dataframe pela ordem correta (caso falte alguma coluna, ignora erros)
            df = df[[c for c in colunas_ordenadas if c in df.columns]]
            
            # 3. Traduzindo True/False para V/F (usando o método atualizado .map)
            df_visual = df.map(lambda x: "V" if x else "F")
            
            # 4.  Pintar a última coluna para dar destaque ao resultado
            def pintar_fundo(val):
                if val == 'V': return 'background-color: rgba(144, 238, 144, 0.3); font-weight: bold;'
                if val == 'F': return 'background-color: rgba(255, 99, 71, 0.3); font-weight: bold;'
                return ''
            
            ultima_col = df_visual.columns[-1]
            tabela_estilizada = df_visual.style.map(pintar_fundo, subset=[ultima_col])
            
            # Exibindo a tabela formatada
            st.dataframe(tabela_estilizada, use_container_width=True)
            
            st.caption(f"A tabela possui {len(df)} combinações possíveis ($2^{len(vars_list)}$ linhas).")
            
            # Para a classificação semântica 
            resultado_final = df_visual.iloc[:, -1]

            if all(valor == "V" for valor in resultado_final):
                classificacao = "Tautologia"
            elif all(valor == "F" for valor in resultado_final):
                classificacao = "Contradição"
            else:
                classificacao = "Contingência"

            st.subheader("Classificação Lógica")
            st.success(f"A fórmula é uma **{classificacao}**.")

        except SyntaxError as se:
            st.error(f"**Erro de Sintaxe:** {se}")
            
        except Exception as e:
            st.error(f"**Erro Inesperado:** Não foi possível processar esta frase. Verifique a estrutura. (Detalhe: {e})")

# Ponto de entrada da aplicação
if __name__ == "__main__":
    main()
