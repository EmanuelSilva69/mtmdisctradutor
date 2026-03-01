import itertools
import re

class ModuloMatematico:
    def __init__(self):
        self.operadores_map = {'∧': ' and ', '∨': ' or ', '¬': ' not '}

    def extrair_subexpressoes_automaticas(self, formula):
        etapas = []
        # 1. Negações simples
        negacoes = re.findall(r'¬[A-Z]', formula)
        etapas.extend(negacoes)

        # 2. Busca o primeiro par de operação (P ∧ Q)
        
        primeira_op = re.findall(r'(?:¬?[A-Z]\s[∧∨]\s¬?[A-Z])', formula)
        for op in primeira_op:
            etapas.append(f"({op})")

        # 3. Fórmula Final 
        formula_limpa = formula.strip()
        if not (formula_limpa.startswith('(') and formula_limpa.endswith(')')):
            etapas.append(f"({formula_limpa})")
        else:
            etapas.append(formula_limpa)

        return sorted(list(set(e for e in etapas if e)), key=len)

    def avaliar(self, exp, contexto):
        try:
            # 1. Se a expressão for uma implicação, tratamos como (not A or B)
            if '→' in exp:
                partes = exp.split('→')
                # Remove parênteses externos das partes para não bugar o split
                ant = partes[0].strip().strip('()')
                cons = partes[1].strip().strip('()')
                # A mágica da lógica: A -> B é o mesmo que (not A or B)
                exp_python = f"(not ({ant}) or ({cons}))"
            else:
                exp_python = exp

            # 2. Traduz os símbolos para operadores do Python
            for simb, op in self.operadores_map.items():
                exp_python = exp_python.replace(simb, op)
            
            # 3. Avalia no contexto das variáveis (V/F)
            return bool(eval(exp_python, {"__builtins__": None}, contexto))
        except Exception as e:
            
            return False

    def gerar_tabela_verdade(self, formula):
        variaveis = sorted(list(set(re.findall(r'\b[P-Z]\b', formula))))
        etapas = self.extrair_subexpressoes_automaticas(formula)
        
        combinacoes = list(itertools.product([True, False], repeat=len(variaveis)))
        tabela_completa = []
        
        for combo in combinacoes:
            linha_contexto = dict(zip(variaveis, combo))
            # Calcula cada etapa e guarda no contexto da linha
            for etapa in etapas:
                if etapa not in variaveis:
                    resultado = self.avaliar(etapa, linha_contexto)
                    linha_contexto[etapa] = resultado
            tabela_completa.append(linha_contexto)
            
        return tabela_completa, variaveis, etapas

    def imprimir_tabela(self, tabela, variaveis, etapas):
        colunas = variaveis + [e for e in etapas if e not in variaveis]
        larguras = {col: max(len(col), 5) for col in colunas}
        
        header = " | ".join(col.center(larguras[col]) for col in colunas)
        print(header)
        print("-" * len(header))
        
        for linha in tabela:
            print(" | ".join(("V" if linha.get(col) else "F").center(larguras[col]) for col in colunas))