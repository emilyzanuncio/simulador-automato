import tkinter as tk
from tkinter import messagebox

def novaJanela(controller):
    janela = tk.Tk()
    janela.title("Simulador de Autômatos Finitos")
    
    tk.Label(janela, text="SimulAutômato", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(janela, text="Selecione uma das opções:", font=('Arial',12)).grid(row=1,column=0)
    
    tk.Button(janela, text="Importar Autômato", command=importarFA).grid(row=2,column=0,padx=20,pady=10)
    tk.Button(janela, text="Modelos Prontos", command=importarFA).grid(row=3,column=0,padx=20,pady=10)
    tk.Button(janela, text="Escrever Autômato", command=importarFA).grid(row=4,column=0,padx=20,pady=10)
    
    janela.mainloop()

def importarFA():
    print("Importar FA")
    
def inserirFA():
    print("Inserir FA")
    
def modelosFA():
    print("Modelos Exemplo")

def mostrarFA():
    print("Mostrar FA")

def main():
    janela = novaJanela(controller=globals())

if __name__ == "__main__":
    main()