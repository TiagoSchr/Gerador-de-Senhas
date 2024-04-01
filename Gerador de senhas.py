import tkinter as tk
from tkinter import messagebox
import random
import string
import os
import subprocess
import platform
from datetime import datetime

def gerar_senha_segura(comprimento, palavra_especifica='', incluir_palavra=False):
    comprimento_minimo = len(palavra_especifica) + 4 if incluir_palavra and palavra_especifica else 8
    comprimento = max(comprimento, comprimento_minimo)

    caracteres = string.ascii_letters + string.digits + string.punctuation
    while True:
        senha = ''.join(random.choice(caracteres) for i in range(comprimento - (len(palavra_especifica) if incluir_palavra and palavra_especifica else 0)))

        if (any(c.islower() for c in senha) and any(c.isupper() for c in senha) and
            any(c.isdigit() for c in senha) and any(c in string.punctuation for c in senha)):

            if incluir_palavra and palavra_especifica:
                posicao = random.randint(0, len(senha))
                senha = senha[:posicao] + palavra_especifica + senha[posicao:]

            return senha

def gerar_senha():
    comprimento = int(comprimento_entrada.get())
    palavra = palavra_entrada.get()
    incluir_palavra = incluir_var.get()
    descricao = descricao_entrada.get()

    senha = gerar_senha_segura(comprimento, palavra, incluir_palavra)
    resultado_var.set(f"Sua senha gerada é: {senha}")
    
    try:
        # Obter a data e hora atuais
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        arquivo_senhas = os.path.join(app.caminho_desktop, 'senhas_geradas.txt')
        with open(arquivo_senhas, "a") as arquivo:
            # Escrever no arquivo com a descrição, senha e a data e hora atuais
            arquivo.write(f"{descricao} - {senha} - Criada em: {agora}\n")
        resultado_var.set(f"Senha salva em: {arquivo_senhas}")
        app.arquivo_senhas = arquivo_senhas  # Armazenar o caminho no objeto app para uso posterior
    except Exception as e:
        resultado_var.set(f"Erro ao salvar senha: {str(e)}")

def abrir_caminho_arquivo():
    try:
        caminho_desktop = os.path.join(os.path.expanduser('~'), 'senhas')
        arquivo_senhas = os.path.join(caminho_desktop, 'senhas_geradas.txt')
        
        if platform.system() == 'Windows':
            os.startfile(caminho_desktop)
        else:
            opener = 'open' if platform.system() == 'Darwin' else 'xdg-open'
            subprocess.call([opener, caminho_desktop])
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o diretório: {str(e)}")

app = tk.Tk()
app.title("Gerador de Senhas Seguras")
app.geometry("400x300")

app.caminho_desktop = os.path.join(os.path.expanduser('~'), 'senhas')
app.arquivo_senhas = ''

# Configuração da descrição da senha
tk.Label(app, text="Descrição da senha (ex: Instagram, banco):").pack()
descricao_entrada = tk.Entry(app)
descricao_entrada.pack(pady=5)

# Configuração da palavra específica
tk.Label(app, text="Palavra Específica (opcional):").pack()
palavra_entrada = tk.Entry(app)
palavra_entrada.pack(pady=5)

# Configuração para incluir a palavra específica
incluir_var = tk.BooleanVar()
tk.Checkbutton(app, text="Incluir palavra na senha", variable=incluir_var).pack()

# Configuração do comprimento da senha
tk.Label(app, text="Comprimento da senha:").pack()
comprimento_entrada = tk.Spinbox(app, from_=8, to=128, width=5)
comprimento_entrada.pack(pady=5)

# Botão para gerar a senha
tk.Button(app, text="Gerar Senha", command=gerar_senha).pack(pady=5)

# Exibição do resultado
resultado_var = tk.StringVar()
tk.Label(app, textvariable=resultado_var).pack()

abrir_button = tk.Button(app, text="Abrir Local do Arquivo", command=abrir_caminho_arquivo)
abrir_button.pack(pady=5)

app.mainloop()
