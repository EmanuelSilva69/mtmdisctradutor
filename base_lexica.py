
class AnalisadorLexicoAFD:
    def __init__(self):
        self.tokens = []

    def normalizar(self, frase): 

        frase = frase.lower().strip()
        para_remover = ['.', '!', '?']
        for p in para_remover:
            frase = frase.replace(p, '')
            
        return frase + ' '

    def tokenizar(self, frase):
        frase_limpa = self.normalizar(frase)
        self.tokens = []
        
        estado = 'q0'
        buffer = '' 
     
        for char in frase_limpa:
            #Aqui começa o estado inicial, onde o autômato procura por caracteres que possam iniciar um token. 
            # Ele ignora espaços e reconhece vírgulas imediatamente. Para letras específicas, 
            # ele transita para estados de investigação para determinar se formam conectivos ou variáveis.
            if estado == 'q0':
                if char.isspace():
                    continue 
                elif char == ',':
                    self.tokens.append(('TOKEN_VIRGULA', ','))
                elif char == 'e':
                    buffer += char
                    estado = 'q_e' 
                elif char == 'o':
                    buffer += char
                    estado = 'q_o'  
                elif char == 's':
                    buffer += char
                    estado = 'q_s'  
                elif char == 'n':
                    buffer += char
                    estado = 'q_n'  
                elif char == 'l':
                    buffer += char
                    estado = 'q_l'  
                else:
                    buffer += char
                    estado = 'q_var' 
                    
            # Caminho do "se"
            elif estado == 'q_s':
                if char == 'e':
                    buffer += char
                    estado = 'q_se' # Formou "se"
                else:
                    buffer += char
                    estado = 'q_var' # Falso alarme (ex: "sapo")
                    
            # Caminho do "e" ou "então"
            elif estado == 'q_e':
                if char == 'n':
                    buffer += char
                    estado = 'q_en' # Formando "então"
                elif char.isspace() or char == ',':
                    self.tokens.append(('TOKEN_E', buffer)) # Era apenas "e"
                    buffer = ''
                    estado = 'q0'
                    if char == ',': self.tokens.append(('TOKEN_VIRGULA', ','))
                else:
                    buffer += char
                    estado = 'q_var'

            elif estado == 'q_en':
                if char == 't':
                    buffer += char
                    estado = 'q_ent'
                else: buffer += char; estado = 'q_var'
                
            elif estado == 'q_ent':
                if char == 'ã' or char == 'a':
                    buffer += char
                    estado = 'q_enta'
                else: buffer += char; estado = 'q_var'
                
            elif estado == 'q_enta':
                if char == 'o':
                    buffer += char
                    estado = 'q_entao' # Formou "então"
                else: buffer += char; estado = 'q_var'

            # Caminho do "ou"
            elif estado == 'q_o':
                if char == 'u':
                    buffer += char
                    estado = 'q_ou'
                else: buffer += char; estado = 'q_var'

            # Caminho do "não"
            elif estado == 'q_n':
                if char == 'ã' or char == 'a':
                    buffer += char
                    estado = 'q_na'
                else: buffer += char; estado = 'q_var'
                
            elif estado == 'q_na':
                if char == 'o':
                    buffer += char
                    estado = 'q_nao'
                else: buffer += char; estado = 'q_var'

            # Caminho do "logo"
            elif estado == 'q_l':
                if char == 'o': buffer += char; estado = 'q_lo'
                else: buffer += char; estado = 'q_var'
            elif estado == 'q_lo':
                if char == 'g': buffer += char; estado = 'q_log'
                else: buffer += char; estado = 'q_var'
            elif estado == 'q_log':
                if char == 'o': buffer += char; estado = 'q_logo'
                else: buffer += char; estado = 'q_var'

            # ESTADOS DE ACEITAÇÃO (Fechamento do Token)
            # O autômato só confirma o token se a palavra terminar (espaço ou vírgula)
            elif estado in ['q_se', 'q_entao', 'q_ou', 'q_nao', 'q_logo', 'q_var']:
                if char.isspace() or char == ',':
                    # Descobre qual token emitir baseado no estado de aceitação
                    if estado == 'q_se':
                        self.tokens.append(('TOKEN_SE', buffer))
                    elif estado in ['q_entao', 'q_logo']:
                        self.tokens.append(('TOKEN_ENTAO', buffer))
                    elif estado == 'q_ou':
                        self.tokens.append(('TOKEN_OU', buffer))
                    elif estado == 'q_nao':
                        self.tokens.append(('TOKEN_NAO', buffer))
                    elif estado == 'q_var':
                        self.tokens.append(('TOKEN_VARIAVEL', buffer))
                    
                    # Limpa o buffer e reinicia
                    buffer = ''
                    estado = 'q0'
                    
                    # Se o terminador foi uma vírgula, emitimos o token dela também
                    if char == ',':
                        self.tokens.append(('TOKEN_VIRGULA', ','))
                else:
                    buffer += char
                    estado = 'q_var' 

        return self.tokens