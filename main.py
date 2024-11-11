import tkinter as tk
from tkinter import filedialog
from model import inserirFA, modelosFA, mostrarFA

global impWindow

def novaJanela(controller):
    janela = tk.Tk()
    janela.title("Simulador de Autômatos Finitos")
    
    tk.Label(janela, text="SimulAutômato", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(janela, text="Selecione uma das opções:", font=('Arial',12)).grid(row=1,column=0)
    
    tk.Button(janela, text="Importar Autômato", command=importar).grid(row=2,column=0,padx=20,pady=10)
    tk.Button(janela, text="Modelos Prontos", command=modelos).grid(row=3,column=0,padx=20,pady=10)
    tk.Button(janela, text="Escrever Autômato", command=inserir).grid(row=4,column=0,padx=20,pady=10)
    
    janela.mainloop()

def importar():
    global impWindow
    impWindow = tk.Tk()
    impWindow.title("SimulAutômato")
    
    tk.Label(impWindow, text="IMPORTAR .TXT", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(impWindow, text="Importe um autômato:").grid(row=1,column=0,padx=10,pady=5)
    
    tk.Button(impWindow, text="Selecionar arquivo", command=importarTxt).grid(row=2,column=0,padx=20,pady=5)
    
    impWindow.mainloop()

def importarTxt():
    global impWindow
    print("TXT")
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        tk.Label(impWindow,text="Arquivo localizado!").grid(row=3,column=0)
        tk.Button(impWindow,text="Simular", command=mostrarFA).grid(row=4,column=0,pady=10)

def modelos():
    print("Modelos")
    modelosFA()

def inserir():
    print("Escrever")
    inserirFA()


def main():
    janela = novaJanela(controller=globals())

if __name__ == "__main__":
    main()