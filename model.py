import re
import tkinter as tk
from tkinter import messagebox

def validaAutomato(automato):
    # Envia o autômato para tratamento de erro
    valido,mensagem = confereTXT(automato)
    # Caso seja válido, iniciar simulação. Se não, enviar mensagem de erro.
    if valido:
        simuladorJanela()
    else:
        messagebox.showerror("ERRO", mensagem)

def salvarSimular(caixaTexto):
    entrada = caixaTexto.get("1.0", tk.END)
    # Copia autômato inserido para um arquivo txt
    automato = "./novoAutomato.txt"
    with open(automato,"w") as file:
        file.write(entrada)
    # Envia o autômato para o tratamento de erro para depois simular
    validaAutomato(automato)
    
def confereTXT(automato):
    secObrigatorias = ["#states","#initial","#accepting","#alphabet","#transitions"]
    global secoes 
    secoes = {}
    # Define o modelo das transições estadoA:simbolo>estadoB
    transicaoModelo = re.compile(r"\w+:(\w+|\#|\,|\$)>\w+(,\w+)*$")
    
    # Ler os conteúdos do arquivo e organizar as seções
    with open(automato,"r") as file:
        secAtual = None
        for linha in file:
            linha = linha.strip()
            if linha in secObrigatorias: # Se a linha lida estiver na lista de secObg
                secAtual = linha
                secoes[secAtual] = [] # Inserir seção atual nas seções contidas
            elif secAtual: # Se estivermos dentro de uma das seções contidas
                secoes[secAtual].append(linha) # Adiciona essa linha à sua seção correspondente em um dicionário
    
    # Checa se tem seções faltando
    naoLocalizadas = []
    for sec in secObrigatorias:
        if sec not in secoes: # Se a seção obrigatória lida não estiver na lista de seções contidas, reportar ERRO
            erro = f"ERRO: Seções faltando:\n {'\n '.join(naoLocalizadas)}"
            return False, erro
    
    # Checa se há seções vazias    
    for sec,conteudo in secoes.items():
        if not conteudo:
            erro = f"ERRO: Seção {sec} está vazia."
            return False, erro
    # Checa se há mais de um estado inicial
    if len(secoes["#initial"]) != 1:
        erro = f"A seção #initial deve conter somente um estado."
        return False, erro
    
    # Checa o formato e possíveis inconsistências dentro das seções
    for estado in secoes["#states"]:
        if not estado.isalnum():
            erro = "Formato de estado inválido."
            return False, erro
    
    estadosDefinidos = set(secoes["#states"]) # Copia os estados definidos numa variável
    alfabetoDefinido = set(secoes["#alphabet"]) # Copia o alfabeto definido numa variável
    
    # Verifica se o estado inicial listado faz parte dos estados definidos
    for estado in secoes["#initial"]:
        if estado not in estadosDefinidos:
            erro = f"O estado {estado} não é parte do autômato definido."
            return False, erro
    # Verifica se o estado final listado faz parte dos estados definidos
    for estado in secoes["#accepting"]:
        if estado not in estadosDefinidos:
            erro = f"O estado {estado} não é parte do autômato definido."
            return False, erro
    # Verifica inconsistências nas transições
    for transicao in secoes["#transitions"]:
        # Verifica se as transições listadas seguem o modelo estadoA:simbolo>estadoB
        if not transicaoModelo.match(transicao):
            erro = f"Formato errado de transição."
            return False, erro
        # Verifica se as transições listadas usam os estados e alfabeto definidos
        estadoOrigem,resto = transicao.split(":") # Copia estadoA para estadoOrigem e o resto da regEx para resto
        simbolo,estadoDestino = resto.split(">") # Copia estadoB para estadoDestino
        # Verifica se o estado origem da transição está nos estados definidos
        if estadoOrigem not in estadosDefinidos:
            erro = f"O estado {estadoOrigem} não é parte do autômato definido."
            return False, erro
        # Verifica se o estado destino da transição está nos estados definidos
        estadoDestino = estadoDestino.split(",")
        for destino in estadoDestino:
            if destino not in estadosDefinidos:
                erro = f"O estado {destino} não é parte do autômato definido."
                return False, erro
        
        # Verifica se o símbolo da transição está no alfabeto definido (permite transição vazia)
        if simbolo not in alfabetoDefinido and simbolo != '#':
            erro = f"O símbolo '{simbolo}' não é parte do alfabeto definido."
            return False, erro
    sucesso = "Autômato aceito."
    return True, sucesso

def simuladorJanela():
    janelaSimulador = tk.Tk()
    janelaSimulador.title("SimulAutômato - Simulador")
    # Título da janela do simulador
    tk.Label(janelaSimulador,text="SimulAutômato", font=('Arial',14)).pack(padx=20,pady=10)
    
    tk.Label(janelaSimulador,text="Insira a palavra a ser buscada:",font=('Arial',12)).pack(padx=25,pady=5)
    palavra = tk.Entry(janelaSimulador,width=20)
    palavra.pack(pady=(0,20))
    tk.Button(janelaSimulador,text="Buscar",command=lambda: buscaGUI(palavra)).pack(pady=10)
    
    janelaSimulador.mainloop()

def mostrarFA(automato):
    print("Mostrando visualmente")
    
def buscaGUI(palavra):
    palavra = palavra.get()
    # Inicia a simulação e envia os resultados para as variáveis encontrada e caminhoFinal
    encontrada, caminhoFinal = simularAutomato(palavra)
    
    print("Caminho percorrido:",caminhoFinal)
    # Abre uma caixa de mensagens para mostrar o resultado
    if encontrada:
        messagebox.showinfo("Resultado","A cadeia pertence ao autômato.\nCheque o terminal para o caminho percorrido.")
    else:
        messagebox.showerror("Resultado","A cadeia não pertence ao autômato.\nCheque o terminal para o caminho percorrido.")    

def simularAutomato(palavra):
    #estados = set(secoes["#states"]) # Copia estados p/ variável estados
    inicial = secoes["#initial"][0] # Copia estado inicial p/ variável inicial
    finais = set(secoes["#accepting"]) # Copia estados finais p/ variável finais
    transicoes = secoes["#transitions"] # Copia transições p/ variável transicoes
    #alfabeto = set(secoes["#alphabet"]) # Copia alfabeto p/ variável alfabeto
    #palavra = palavra.get()
    caminhoFinal = []
    encontrada = False
    #fimSimulacao = False
    
    def buscar(estadoAtual, posicao, caminhoAtual):
        nonlocal caminhoFinal, encontrada
        # Atualiza o caminho
        caminhoAtual = caminhoAtual + [estadoAtual]
        # Atualiza caminho final
        caminhoFinal = caminhoAtual
        # Caso a palavra tenha sido lida por completo
        if posicao == len(palavra):
            if estadoAtual in finais:
                encontrada = True
                return encontrada,caminhoFinal
            else:
                return encontrada,caminhoFinal
        
        # Não continuar caso a cadeia tenha sido encontrada
        if encontrada:
            return True
        
        # Processar transições normais (símbolo ∈ alfabeto)
        simbolo = palavra[posicao] # simbolo recebe o símbolo na posição atual
        
        for transicao in transicoes:
            origem, resto = transicao.split(":") # Separa o estado origem do resto
            simboloTransicao, destinos = resto.split(">") # Separa o símbolo dos estados destino
            destinos = destinos.split(",") # Separa os estados destino
            # Caso o estadoAtual corresponda ao inicial e o simbolo atual ao da transição, percorrer avançar
            if origem == estadoAtual and simboloTransicao == simbolo:
                for destino in destinos:
                    transicaoExecutada = f"{simboloTransicao}>{destino}"
                    buscar(destino, posicao + 1, caminhoAtual + [transicaoExecutada])
            # Caso o estado atual possua transições em vazio
            elif origem == estadoAtual and simboloTransicao == "#":
                for destino in destinos:
                    transicaoExecutada = f"{simboloTransicao}>{destino}"
                    buscar(destino, posicao, caminhoAtual + [transicaoExecutada])
        
    # Iniciar busca
    buscar(inicial, 0, [])
    # Enviar resultados
    caminhoFinal = caminhoFinal
    return encontrada, caminhoFinal