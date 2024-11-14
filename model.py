import re
import tkinter as tk
from tkinter import messagebox

def simularFA(automato):
    f = open(automato,"r")
    print(f.read())

def mostrarFA(automato):
    print("Mostrandoooo")

def salvarSimular(caixaTexto):
    entrada = caixaTexto.get("1.0", tk.END)
    
    automato = "./novoAutomato.txt"
    with open(automato,"w") as file:
        file.write(entrada)
        
    validar,mensagem = confereTXT(automato)
    #print(validar)
    if validar:
        # =========================
        #TROCAR PRA SIMULAR
        # =========================
        messagebox.showinfo("SUCESSO", mensagem)
    else:
        messagebox.showerror("ERRO", mensagem)
    
def confereTXT(automato):
    secObrigatorias = ["#states","#initial","#accepting","#alphabet","#transitions"]
    secoes = {}
    # Define o modelo das transições estadoA:simbolo>estadoB
    transicaoModelo = re.compile(r"\w+:(\w+|\$)>\w+(,\w+)*$")
    
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
            erro = "Formato errado de transição."
            return False, erro
        # Verifica se as transições listadas usam os estados e alfabeto definidos
        estadoOrigem,resto = transicao.split(":") # Copia estadoA para estadoOrigem e o resto da regEx para resto
        simbolo,estadoDestino = resto.split(">") # Copia estadoB para estadoDestino
        # Verifica se o estado origem da transição está nos estados definidos
        if estadoOrigem not in estadosDefinidos:
            erro = f"ERRO: O estado {estadoOrigem} não é parte do autômato definido."
            return False, erro
        # Verifica se o estado destino da transição está nos estados definidos
        if estadoDestino not in estadosDefinidos:
            erro = f"O estado {estadoDestino} não é parte do autômato definido."
            return False, erro
        # Verifica se o símbolo da transição está no alfabeto definido (permite transição vazia)
        if simbolo not in alfabetoDefinido and simbolo != '$':
            erro = f"O símbolo '{simbolo}' não é parte do alfabeto definido."
            return False, erro
    sucesso = "Autômato aceito."
    return True, sucesso