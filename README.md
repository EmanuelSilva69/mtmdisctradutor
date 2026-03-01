#   (Lógica Proposicional e Predicados).
Este projeto é uma ferramenta interativa para análise e avaliação de expressões da Lógica Proposicional e de Predicados, desenvolvida como parte dos estudos em Lógica e Matemática Discreta. O sistema permite interpretar fórmulas lógicas, avaliar proposições com base em diferentes contextos e gerar automaticamente tabelas-verdade, possibilitando a verificação formal de equivalências, tautologias, contradições e validade lógica de expressões inseridas pelo usuário.

## Descrição do Problema
O desafio consiste em desenvolver um software para manipular e avaliar expressões da Lógica Proposicional, com as seguintes restrições:

* **Entrada de Dados:** O usuário deve fornecer uma **fórmula lógica** bem formada, composta por **proposições simples** (ex: P, Q, R) e conectivos lógicos como **negação** (¬), **conjunção** (∧), **disjunção** (∨), **implicação** (→) e **bicondicional** (↔).
* **Validação Sintática em:** O sistema deve verificar se a expressão inserida é válida, garantindo o **uso correto** de **parênteses**, **operadores** e **estrutura lógica adequada**.
* **Processamento e Saída:** O programa deve identificar e exibir automaticamente as subexpressões intermediárias, permitindo ao usuário acompanhar detalhadamente o processo de avaliação lógica:
    * Identificar automaticamente as **proposições simples** presentes na fórmula.
    * Gerar todas as combinações possíveis de valores lógicos **(Verdadeiro e Falso)**.
    * Avaliar cada subexpressão da fórmula com base em um determinado contexto de valores.
    * Exibir a **tabela-verdade** completa da expressão.
    * Permitir a análise da fórmula quanto à sua classificação lógica, determinando se é uma **tautologia**, **contradição** ou **contingência**.

##  Objetivo do Programa

O objetivo central deste software é servir como uma ferramenta didática e funcional para a análise formal de expressões da Lógica Proposicional, permitindo a visualização estruturada do processo de avaliação lógica por meio da geração de tabelas-verdade.

* **Demonstrar a Lógica Algorítmica:** Evidenciar o funcionamento interno da avaliação de fórmulas lógicas através da implementação manual dos algoritmos responsáveis por interpretar expressões, gerar combinações de valores lógicos e calcular os resultados de cada conectivo, evitando dependência de funções prontas que abstraiam o raciocínio lógico.
* **Validar Propriedades Matemáticas:** Aplicar na prática conceitos como tautologia, contradição e contingência, garantindo que o sistema respeite rigorosamente as regras formais da Lógica Matemática durante a avaliação das expressões.
* **Facilitar a Visualização:** Proporcionar uma forma clara e organizada de exibir a tabela-verdade completa, incluindo subexpressões intermediárias, permitindo que o usuário acompanhe detalhadamente cada etapa do processo de avaliação lógica.

## Funcionalidades Principais

* **Geração de Tabela-Verdade**: Criação automática da tabela-verdade completa a partir de uma fórmula lógica inserida pelo usuário.
* **Avaliação de Expressões**: Interpretação e cálculo do valor lógico da expressão com base em diferentes atribuições de Verdadeiro (V) e Falso (F).
* **Extração de Subexpressões**: Identificação automática das subexpressões intermediárias para detalhar o processo de avaliação lógica.
* **Classificação da Fórmula**: Determinação se a expressão é uma tautologia, contradição ou contingência.
* **Validação Sintática**: Verificação da estrutura da fórmula, garantindo o uso correto de conectivos e parênteses antes da avaliação.
##  Fundamentos Teóricos
Este projeto implementa os conceitos fundamentais da Lógica Proposicional, aplicados à construção e análise de tabelas-verdade:
* **Proposição**: Sentença declarativa que pode assumir apenas dois valores lógicos: Verdadeiro (V) ou Falso (F).
* **Negação (¬P)**:Inverte o valor lógico de uma proposição.
* **Conjunção (P ∧ Q)**: É verdadeira somente quando ambas as proposições são verdadeiras.
* **Disjunção (P ∨ Q)**: É verdadeira quando pelo menos uma das proposições é verdadeira.
* **Implicação (P → Q)**: É falsa apenas quando P é verdadeira e Q é falsa.
* **Bicondicional (P ↔ Q)**: É verdadeira quando ambas as proposições possuem o mesmo valor lógico.
* **Tabela-Verdade**: Estrutura que apresenta todas as possíveis combinações de valores lógicos das proposições simples e o resultado final da expressão composta.

### Propriedades Verificadas
* **Tautologia**: Expressão que é verdadeira para todas as combinações possíveis de valores lógicos.
* **Contradição**: Expressão que é falsa para todas as combinações possíveis.
* **Contingência**: Expressão que pode assumir tanto valores verdadeiros quanto falsos, dependendo do contexto lógico.
* **Equivalência Lógica**: Duas expressões são equivalentes quando apresentam os mesmos valores lógicos em todas as linhas da tabela-verdade.
  
##  Interface e Experiência do Usuário  FALTA FAZER
O projeto utiliza a biblioteca CustomTkinter para oferecer uma interface moderna com suporte a temas e elementos visuais dinâmicos.
<h3> Funcionalidades da Interface</h3>

* **Validação em Tempo Real**: O sistema verifica se o conjunto inserido possui entre **4 e 8 elementos**, disparando um feedback visual temporário em caso de erro.
* **Geração Aleatória Dinâmica**: O usuário pode alternar entre modos (**números, letras ou misto**) para gerar o **Conjunto B** automaticamente, utilizando um seletor segmentado.
* **Visualização Formatada**: Os resultados são exibidos em blocos estilizados por cores através de uma classe de texto customizada:
    * **Azul/Roxo**: Listagem detalhada dos conjuntos (A, B e Universo).
    * **Icy Blue**: Resultados das operações matemáticas.
    * **Neon Ice**: Cálculos de cardinalidade.
    * **Roxo Escuro**: Análise de subconjuntos e disjunção.
* **Fallback para Conjunto Vazio**: Se a interseção for vazia, o app exibe o símbolo matemático $\emptyset$ para clareza acadêmica.

<h3> Identidade Visual (UI/UX)</h3>

O projeto adota uma estética **Modern Slate**, focada em legibilidade e conforto visual através de um modo escuro profundo.

### Paleta de Cores (Slate Style)
| Elemento | Cor | Hexadecimal |
| :--- | :--- | :--- |
| **Fundo** | Slate 900 | `#0F172A` |
| **Cards** | Slate 800 | `#1E293B` |
| **Destaque** | Sky Blue | `#38BDF8` |
| **Botão** | Indigo | `#6366F1` |
| **Sucesso** | Emerald | `#10B981` |
| **Erro** | Red/Rose | `#EF4444` |

<h3> Tecnologias Utilizadas</h3>

* **Python 3.x**: Linguagem base.
* **CustomTkinter**: Interface gráfica moderna com suporte a temas.

* **Estrutura de Módulos**:
    * `base_lexica.py`: Implementação das funções de armazenar e tokenizar.
    * `modulo_matematico.py`: Implementação das funções matemáticas.
    * `sintaxe.py`: Lógica de fazer parse e alocar variável.
    * `design.py`: Gerenciamento de cores, fontes e temas globais.
    * `main.py`: Orquestrador da interface e fluxo do app.

##  Arquitetura do Código

### [`base_lexica.py`](base_lexica.py) - Analisador Léxico (AFD)
Implementa manualmente um Autômato Finito Determinístico para reconhecimento de conectivos lógicos e variáveis proposicionais, utilizando leitura caractere por caractere, controle explícito de estados e uso de buffer:

* `normalizar(frase)`<br>
→ Converte a frase para minúsculas.<br>
→ Remove pontuações irrelevantes (., !, ?).<br>
→ Mantém vírgula como símbolo lógico.<br>
→ Adiciona espaço ao final da string para garantir o fechamento correto do último token.<br>

* `tokenizar(frase)`<br>
→ Percorre a string caractere por caractere.<br>
→ Controla transições entre estados (q0, q_e, q_se, q_entao, q_nao, q_ou, q_logo, q_var, etc.).<br>
→ Utiliza um buffer para acumular caracteres até formar um token válido.<br>

* **TOKENS RECONHECIDOS**: <br>
**TOKEN_SE** → palavra “se”<br>
**TOKEN_ENTAO** → palavras “então” ou “logo”<br>
**TOKEN_E** → conectivo “e”<br>
**TOKEN_OU** → conectivo “ou”<br>
**TOKEN_NAO** → negação “não”<br>
**TOKEN_VIRGULA** → símbolo “,"<br>
**TOKEN_VARIAVEL** → qualquer outra palavra tratada como proposição<br>

 `FUNCIONAMENTO INTERNO`
→ O estado inicial (q0) ignora espaços e identifica possíveis inícios de conectivos.<BR>
→ Estados intermediários verificam se a sequência de caracteres realmente forma um conectivo válido.<BR>
→ Caso a sequência deixe de corresponder a um conectivo, o estado é rebaixado para q_var.<BR>
→ Um token só é confirmado quando encontra delimitador (espaço ou vírgula).<BR>
→ Após confirmar o token, o buffer é limpo e o autômato retorna ao estado inicial. <BR>

### [`modulo_matematico.py`](modulo_matematico.py) - Motor Matemático (Avaliação Lógica)
Principais métodos:

* **gerar_tabela_verdade(formula)**
* **avaliar(exp, contexto)**
* **imprimir_tabela(...)**
* **extrair_subexpressoes_automaticas(...)**
Responsável por avaliação lógica e geração de tabela-verdade.

### [`sintaxe.py`](sintaxe.py) - Analisador Sintático
*     Classe: AnalisadorSintatico

Principais métodos:
responsável por transformar a sequência de tokens gerada pelo analisador léxico em uma fórmula lógica formal da Lógica Proposicional. <BR>
O controle da análise é feito pela variável estado, que alterna entre:

* ESPERANDO_TERMO

* ESPERANDO_OPERADOR <BR>

Essa alternância garante que a estrutura da frase respeite a gramática lógica básica.

### [`main_app.py`](main_app.py) - Interface Principal FALTA
A:
* A

<h1> Como Instalar e Executar</h1>

Siga estes passos para configurar o projeto na sua máquina:
1. **Clone o repositório** (ou baixe os arquivos):
  ```bash
git clone https://github.com/EmanuelSilva69/mtmdisctradutor.git
```
2. **Entrar na pasta do projeto**:
```bash
cd mtmdisctradutor
```
3. **Instale as bibliotecas necessárias:**:
```PowerShell
py -m pip install 
```
 3. **Inicie a aplicação**:   
```PowerShell
py main.py
```
