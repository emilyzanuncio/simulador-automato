import tkinter as tk
import visual_automata

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