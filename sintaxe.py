#se eu aprendi corretamente, isso aqui é uma Máquina de Estados Finitos com Alternância
# O estado da máquina é controlado pela variável 'estado', que alterna entre 'ESPERANDO_TERMO' e 'ESPERANDO_OPERADOR' conforme processamos os tokens.
# no papo to fazendo isso aqui só pra me lembrar do conteúdo, n é éficiente não.
class AnalisadorSintatico:
    def __init__(self):

        #não coloquei o valor inicial da letra pois em teste o negócio ia pra Z rapidinho, aí eu deixo pra inicializar na função de parse mesmo, que é onde a gente começa a processar os tokens. Assim, toda vez que chamarmos parse, a contagem de letras começa do zero (P) e o mapeamento de variáveis é limpo, o que é ideal para analisar frases distintas sem interferência.
        # Mapeamento dos nossos tokens para os símbolos lógicos matemáticos #aqui eu adicionarei os outros símbolos de preposição depois, mas por enquanto só tem os conectivos mesmo (isso se eu botar preposição)
        self.simbolos = {
            'TOKEN_E': '∧',
            'TOKEN_OU': '∨',
            'TOKEN_NAO': '¬',
            'TOKEN_ENTAO': '→'
        }

    def alocar_variavel(self, texto):
        
        #Garante que a mesma palavra sempre receba a mesma letra.
       # Ex: se 'chove' apareceu duas vezes, ambas serão 'P'.
        
        if texto not in self.variaveis_map:
            self.variaveis_map[texto] = chr(self.letra_atual)
            self.letra_atual += 1
        return self.variaveis_map[texto]

    def parse(self, tokens):
                # Dicionário para guardar o mapeamento (ex: {'chove': 'P', 'venta': 'Q'}) -> só serve pra deixar a fórmula mais legível, não é obrigatório para o processo lógico em si
        self.variaveis_map = {}
        # Usamos a tabela ASCII para gerar as letras sequencialmente. 80 = 'P' (sinceramente prof, eu sei que pode desviar um pouco do formal, mas pegar a letra pela tabela em ASCII me lembra muito de C, não tem outra forma mais fácil em python? deve ter)
        self.letra_atual = 80 
        #Lê a lista de tokens do Léxico e monta a equação.
        
        formula_tokens = []
        dentro_de_se = False
        ultima_variavel_texto = ""
        # Nossa máquina de estados sintática. Uma frase válida sempre alterna
        # entre pedir um TERMO (P, Q) e pedir um OPERADOR (e, ou, então).
        estado = 'ESPERANDO_TERMO' 

        for tipo, valor in tokens:
            
            #isso aqui é o caso especial da vírgula, que pode ser tanto um respiro quanto um "então" implícito (n sei oq vão digitar)
            if tipo == 'TOKEN_VIRGULA':
                # Se estamos num bloco "Se" e já lemos uma variável, a vírgula age como "então"
                if dentro_de_se and estado == 'ESPERANDO_OPERADOR':
                    formula_tokens.append(')')
                    formula_tokens.append('→')
                    dentro_de_se = False
                    estado = 'ESPERANDO_TERMO'
                # Olha, limitação aqui ok? eu não sei como fazer isso daqui diferenciar de "Pausa na escrita " e "adição implicita " Então eu coloquei apenas a ultima da adição implícia. Ia ficar muito complicado se não fizessemos isso. 
                    continue 
                elif not dentro_de_se and estado == 'ESPERANDO_OPERADOR':
                    # Vírgula fora do "Se" vira o conectivo "E"
                    formula_tokens.append('∧')
                    estado = 'ESPERANDO_TERMO'
                    continue
            #esse estado aqui espera uma váriável ou um "Se" ou um "Não". Ele é o estado inicial e também o estado para onde voltamos depois de ler um operador.
            if estado == 'ESPERANDO_TERMO':
                if tipo == 'TOKEN_ENTAO':
                    # A vírgula anterior já fez o papel do "então".
                    # Ignoramos a palavra e continuamos esperando a variável.
                    continue

                if tipo == 'TOKEN_SE':
                    dentro_de_se = True
                    formula_tokens.append('(')
                    
                elif tipo == 'TOKEN_NAO':
                    # A negação gruda na próxima variável, então continuamos esperando o termo
                    formula_tokens.append(self.simbolos[tipo])
                    
                elif tipo == 'TOKEN_VARIAVEL':
                    letra = self.alocar_variavel(valor)
                    formula_tokens.append(letra)
                    ultima_variavel_texto = valor
                    # Achamos a variável, agora a regra exige um operador
                    estado = 'ESPERANDO_OPERADOR'
                    
                else:
                    raise SyntaxError(f"Erro gramatical: Esperava uma proposição, mas encontrei '{valor}'.")

            # --- ESTADO 2: OBRIGATÓRIO VIR UM CONECTIVO ---
            elif estado == 'ESPERANDO_OPERADOR':
                if tipo in ['TOKEN_E', 'TOKEN_OU']:
                    formula_tokens.append(self.simbolos[tipo])
                    estado = 'ESPERANDO_TERMO' # Volta a pedir variável
                    
                elif tipo == 'TOKEN_ENTAO':
                    # Fechamos os parênteses da premissa antes de colocar a flecha
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
                    
                    # Fizemos isso aqui pois às vezes o usuário pode querer usar uma frase como variável, tipo "eu quero", e o Léxico vai separar "eu" e "quero" como variáveis distintas. Com esse processo, juntamos elas de volta para que a fórmula final fique mais legível (ex: "P ∧ Q" ao invés de "P ∧ R" onde P = "eu" e R = "quero").
                    # Note que isso é só para deixar a fórmula mais bonita, não é obrigatório para o negócio lógico em si. Se o usuário quiser usar "eu" e "quero" como variáveis distintas, ele pode colocar uma vírgula entre elas ("eu, quero") para que o Léxico trate como duas variáveis separadas.
                
                elif tipo == 'TOKEN_SE':
                    raise SyntaxError("Erro gramatical: Uso incorreto da palavra 'Se' no meio da frase.")

        #Validação final: Se terminamos dentro de um "Se", é porque faltou o "então"
        if dentro_de_se:
            raise SyntaxError("Erro gramatical: Você abriu uma condição com 'Se', mas faltou o 'então'.")

        if estado == 'ESPERANDO_TERMO' and len(formula_tokens) > 0:
            raise SyntaxError("Erro gramatical: A frase não pode terminar com um conectivo inacabado.")

        # Junta a lista de símbolos numa string de equação limpa
        formula_final = " ".join(formula_tokens)
        
        # Limpa espaços em volta dos parênteses e da negação para ficar bonito
        formula_final = formula_final.replace("( ", "(").replace(" )", ")").replace("¬ ", "¬")
        
        return formula_final, self.variaveis_map


# ÁREA DE TESTE INTEGRADO (Léxico + Sintático) - Uso próprio para teste

if __name__ == "__main__":
    # Importamos o Léxico que criamos no passo anterior
    from base_lexica import AnalisadorLexicoAFD
    
    lexico = AnalisadorLexicoAFD()
    sintatico = AnalisadorSintatico()
    
    frases_para_testar = [
        "chove e venta",
        "se estudo, então passo",
        "Se estudo e não durmo, logo passo ou surto",
        "Se chove, então não saio e durmo ou jogo",
        "Como ou bebo água", 
        "Ando por ai pulando e dançando durante o carnaval ou fico em casa assistindo Netflix",
        "Ela dança, eu danço, ela dança, eu danço"
    ]
    
    for frase in frases_para_testar:
        print(f"\n--- Analisando: '{frase}' ---")
        try:
            # Passo 1: O Léxico fatia as palavras
            tokens = lexico.tokenizar(frase)
            
            # Passo 2: O Sintático monta a equação
            formula, variaveis = sintatico.parse(tokens)
            
            print(f"Mapeamento: {variaveis}")
            print(f"Fórmula Matemática: {formula}")
        except Exception as e:
            print(e)
    #FINALMENTE ISSO AQUI TA FUNCIONAL MEU DEUS