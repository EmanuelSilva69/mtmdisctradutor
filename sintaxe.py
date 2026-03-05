# uma Máquina de Estados Finitos com Alternância, o estado da máquina é controlado pela variável 'estado', 
# que alterna entre 'ESPERANDO_TERMO' e 'ESPERANDO_OPERADOR' conforme processamos os tokens.

class AnalisadorSintatico:
    def __init__(self):

        '''
        Mapeamento dos tokens para os símbolos lógicos matemáticos
        '''
        self.simbolos = {
            'TOKEN_E': '∧',
            'TOKEN_OU': '∨',
            'TOKEN_NAO': '¬',
            'TOKEN_ENTAO': '→'
        }

    def alocar_variavel(self, texto):
        '''
        Garante que a mesma palavra sempre receba a mesma letra. 
        Ex: se 'chove' apareceu duas vezes, ambas serão 'P'.
        '''
        if texto not in self.variaveis_map:
            self.variaveis_map[texto] = chr(self.letra_atual)
            self.letra_atual += 1
        return self.variaveis_map[texto]

    def parse(self, tokens):
        '''Dicionário para guardar o mapeamento 
        (ex: {'chove': 'P', 'venta': 'Q'}) -> só serve pra deixar a fórmula mais legível, não é obrigatório para o processo lógico em si
        '''
        self.variaveis_map = {}
        self.letra_atual = 80 
    
        formula_tokens = []
        dentro_de_se = False
        ultima_variavel_texto = ""
        estado = 'ESPERANDO_TERMO' 

        for tipo, valor in tokens:
            if tipo == 'TOKEN_VIRGULA':
                if dentro_de_se and estado == 'ESPERANDO_OPERADOR':
                    formula_tokens.append(')')
                    formula_tokens.append('→')
                    dentro_de_se = False
                    estado = 'ESPERANDO_TERMO'
                    continue 

                elif not dentro_de_se and estado == 'ESPERANDO_OPERADOR':
                    formula_tokens.append('∧')
                    estado = 'ESPERANDO_TERMO'
                    continue

            if estado == 'ESPERANDO_TERMO':
                if tipo == 'TOKEN_ENTAO':
                    if len(formula_tokens) > 0 and formula_tokens[-1] == '∧':
                        formula_tokens[-1] = self.simbolos['TOKEN_ENTAO']
                    continue

                if tipo == 'TOKEN_SE':
                    dentro_de_se = True
                    formula_tokens.append('(')
                    
                elif tipo == 'TOKEN_NAO':
                    formula_tokens.append(self.simbolos[tipo])
                    
                elif tipo == 'TOKEN_VARIAVEL':
                    letra = self.alocar_variavel(valor)
                    formula_tokens.append(letra)
                    ultima_variavel_texto = valor
                    estado = 'ESPERANDO_OPERADOR'
                    
                else:
                    raise SyntaxError(f"Erro gramatical: Esperava uma proposição, mas encontrei '{valor}'.")

            elif estado == 'ESPERANDO_OPERADOR':
                if tipo in ['TOKEN_E', 'TOKEN_OU']:
                    formula_tokens.append(self.simbolos[tipo])
                    estado = 'ESPERANDO_TERMO' 
                    
                elif tipo == 'TOKEN_ENTAO':
                    if dentro_de_se:
                        formula_tokens.append(')')
                        dentro_de_se = False
                    formula_tokens.append(self.simbolos[tipo])
                    estado = 'ESPERANDO_TERMO'
                    
                elif tipo == 'TOKEN_VARIAVEL':
                    
                    # 1. Pega qual letra (P, Q...) estava associada à palavra anterior
                    letra_associada = self.variaveis_map[ultima_variavel_texto]
                    
                    # 2. Deleta a entrada antiga ("eu": "P")
                    del self.variaveis_map[ultima_variavel_texto]
                    
                    # 3. Cria a nova frase com espaço ("eu" + " " + "quero" -> "eu quero")
                    novo_texto_junto = ultima_variavel_texto + " " + valor
                    
                    # 4. Salva no dicionário a frase completa com a mesma letra ("eu quero": "P")
                    self.variaveis_map[novo_texto_junto] = letra_associada
                    
                    # 5. Atualiza a memória para a próxima iteração
                    ultima_variavel_texto = novo_texto_junto
                    
                elif tipo == 'TOKEN_SE':
                    raise SyntaxError("Erro gramatical: Uso incorreto da palavra 'Se' no meio da frase.")

        if dentro_de_se:
            raise SyntaxError("Erro gramatical: Você abriu uma condição com 'Se', mas faltou o 'então'.")

        if estado == 'ESPERANDO_TERMO' and len(formula_tokens) > 0:
            raise SyntaxError("Erro gramatical: A frase não pode terminar com um conectivo inacabado.")

        formula_final = " ".join(formula_tokens)
        formula_final = formula_final.replace("( ", "(").replace(" )", ")").replace("¬ ", "¬")
        
        return formula_final, self.variaveis_map
