import tkinter as tk
from tkinter import filedialog, scrolledtext
from model import validaAutomato, salvarSimular

global mainWindow, impWindow, mdWindow, addWindow

def novaJanela(controller):
    global mainWindow
    mainWindow = tk.Tk()
    mainWindow.title("Simulador de Autômatos Finitos")
    
    tk.Label(mainWindow, text="SimulAutômato", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(mainWindow, text="Selecione uma das opções:", font=('Arial',12)).grid(row=1,column=0)
    
    tk.Button(mainWindow, text="Importar Autômato", command=importar).grid(row=2,column=0,padx=20,pady=10)
    tk.Button(mainWindow, text="Modelos Prontos", command=modelos).grid(row=3,column=0,padx=20,pady=10)
    tk.Button(mainWindow, text="Escrever Autômato", command=inserir).grid(row=4,column=0,padx=20,pady=10)
    
    mainWindow.mainloop()

def importar():
    global impWindow
    impWindow = tk.Toplevel(mainWindow)
    impWindow.title("SimulAutômato - Importar Autômato")
    
    tk.Label(impWindow, text="IMPORTAR .TXT", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(impWindow, text="Importe um autômato:").grid(row=1,column=0,padx=10,pady=5)
    
    tk.Button(impWindow, text="Selecionar arquivo", command=importarTxt).grid(row=2,column=0,padx=20,pady=5)
    
    impWindow.mainloop()

def importarTxt():
    global impWindow
    automato = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")])
    
    if automato:
        tk.Label(impWindow,text="Arquivo localizado!").grid(row=3,column=0)
        tk.Button(impWindow,text="Simular", command=validaAutomato(automato)).grid(row=4,column=0,pady=10)

def modelos():
    global mdWindow
    mdWindow = tk.Toplevel()
    mdWindow.title("SimulAutômato - Modelos Disponíveis")
    
    tk.Label(mdWindow, text="MODELOS", font=('Arial',18)).grid(row=0,column=0,padx=20,pady=20)
    tk.Label(mdWindow, text="Autômatos disponíveis", font=('Arial',14)).grid(row=1,column=0,padx=10,pady=5)
    
    realFA = "./modelosFA/reconheceReal.txt"
    thompsonAFD = "./modelosFA/thompsonAFD.txt"
    thompsonAFNe = "./modelosFA/thompsonAFNe.txt"
    erro = "./modelosFA/erro.txt"
    
    tk.Button(mdWindow, text="Real", command=lambda: validaAutomato(realFA)).grid(row=2,column=0,padx=20,pady=5)
    tk.Button(mdWindow, text="(a+b)*a - AFD", command=lambda: validaAutomato(thompsonAFD)).grid(row=3,column=0,padx=20,pady=5)
    tk.Button(mdWindow, text="(a+b)*a - AFN-e", command=lambda: validaAutomato(thompsonAFNe)).grid(row=4,column=0,padx=20,pady=5)
    tk.Button(mdWindow, text="exemplo de erro", command=lambda: validaAutomato(erro)).grid(row=5,column=0,padx=20,pady=5)
    
    mdWindow.mainloop()

def inserir():
    global addWindow
    addWindow = tk.Tk()
    addWindow.title("SimulAutômato - Inserir Autômato")
    # Título da Janela de Inserção
    tk.Label(addWindow, text="Escreva seu autômato", font=('Arial',14)).grid(row=0,column=0,padx=20,pady=20)
    
    tk.Label(addWindow,text="Utilize o formato:\n#states\ns0\ns1\n#initial\ns0\n#accepting\ns1\n#alphabet\na\nb\n#transitions\ns0:a>s0\ns0:b>s0,s1",
             font=('Arial',12)).grid(row=1,column=0,pady=5)
    tk.Label(addWindow, text="Delete linhas vazias.\nUse $ para transições vazias.", font=('Arial',12)).grid(row=2,column=0,padx=20,pady=20)
    
    caixaTexto = scrolledtext.ScrolledText(addWindow, wrap=tk.WORD, width=40, height=8)
    caixaTexto.grid(row=3,column=0,padx=10,pady=10)
    tk.Button(addWindow,text="Simular", command=lambda: salvarSimular(caixaTexto)).grid(row=4,column=0,pady=10)
    addWindow.mainloop()


def main():
    novaJanela(controller=globals())

if __name__ == "__main__":
    main()