import tkinter as tk
import re

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
        
    mostrarFA(automato)
    
def confereTXT(automato):
    secObrigatorias = ["#states","#initial","#accepting","#alphabet","#transitions"]
    secoes = {}
    
    modeloGeral = re.compile(r"\w")
    transicaoModelo = re.compile(r"\w+:\w+>\w+(,\w+)*$")
    
    # Ler os conteúdos do arquivo e organizar as seções
    with open(automato,"r") as file:
        secAtual = None
        for linha in file:
            linha = linha.strip()
            if linha in secObrigatorias: # Se a linha lida estiver na lista secObg.
                secAtual = linha
                secoes[secAtual] = [] # Inserir seção atual nas seções contidas
            elif secAtual:
                secoes[secAtual].append(linha)
    
    naoLocalizadas = [sec for sec in secObrigatorias if sec not in secoes]
    if naoLocalizadas:
        print(f"ERRO: Seções obrigatórias faltando.")
        return False
    
    for estado in secoes["#states"]:
        if not modeloGeral.match(estado):
            print("ERRO: Formato errado de estado.")
    for estado in secoes["#initial"]:
        if not modeloGeral.match(estado):
            print("ERRO: Formato errado de estado inicial.")
    for estado in secoes["#accepting"]:
        if not modeloGeral.match(estado):
            print("ERRO: Formato errado de estado final.")
    for estado in secoes["#alphabet"]:
        if not modeloGeral.match(estado):
            print("ERRO: Formato errado de alfabeto.")
    for transicao in secoes["#transitions"]:
        if not transicaoModelo.match(transicao):
            print("ERRO: Formato errado de transição.")