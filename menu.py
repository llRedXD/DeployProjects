import os
import tkinter as tk
from tkinter import filedialog

from deployC import Deploy


class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.deploy = Deploy()

        # Configurações da janela
        self.root.title("Menu")
        self.root.geometry("600x400")

        self.environment_var = tk.StringVar()
        self.environment_var.set("Dev")  # Set default value to "Dev"
        self.environment_options = ["Dev", "Prod"]

        self.os_var = tk.StringVar()
        self.os_var.set("Windows")  # Set default value to "Windows"
        self.os_options = ["Windows", "Linux"]

        self.language_var = tk.StringVar()
        self.language_var.set("Python")  # Set default value to "Python"
        self.language_options = ["Python", ".Net", "React"]

        self.caminho_projeto = tk.StringVar()
        self.caminho_projeto.set("")

        self.caminho_deploy = tk.StringVar()
        self.caminho_deploy.set("")

        self.create_menu()

    def select_environment(self):
        # Dropdown menu to choose environment
        environment_menu = tk.OptionMenu(
            self.root, self.environment_var, *self.environment_options
        )
        environment_menu.pack()

    def select_os(self):
        os_menu = tk.OptionMenu(self.root, self.os_var, *self.os_options)
        os_menu.pack()

    def select_language(self):
        language_menu = tk.OptionMenu(
            self.root, self.language_var, *self.language_options
        )
        language_menu.pack()

    def open_folder_project(self):
        self.deploy.os = self.os_var.get()
        if self.deploy.os == "Windows":
            desktop_path = os.path.join(
                os.path.join(os.environ["USERPROFILE"]), "Desktop"
            )
            self.deploy.caminho_projeto = filedialog.askopenfilename(
                initialdir=desktop_path, title="Selecione um arquivo"
            )
        else:
            path_linux = "\\\\wsl.localhost/Ubuntu-22.04/home/"
            # Check if there is only one folder inside the 'home' directory
            folders = os.listdir(path_linux)
            if len(folders) == 1:
                path_linux = os.path.join(path_linux, folders[0])
            self.deploy.caminho_projeto = filedialog.askdirectory(
                initialdir=path_linux, title="Selecione uma pasta"
            )

        self.caminho_projeto.set(self.deploy.caminho_projeto)

    def open_folder_deploy(self):
        # Alimentar o objeto Deploy com as informações selecionadas
        self.deploy.definir_caminho_base(self.environment_var.get())
        self.deploy.language = self.language_var.get()

        # Consultar pasta do projeto.
        folder_path = filedialog.askdirectory(
            initialdir=self.deploy.caminho_base,
            title="Selecione uma pasta",
        )
        # Faça algo com o caminho da pasta selecionada
        self.caminho_deploy.set(folder_path)
        if self.deploy.caminho_projeto:
            self.button_deploy.config(state=tk.NORMAL)

    def create_menu(self):
        self.select_environment()
        self.select_os()
        self.select_language()

        # Rótulo
        label = tk.Label(self.root, text="Selecione uma pasta:")
        label.pack()

        # Caminho projeto
        caminho_projeto_label = tk.Label(self.root, textvariable=self.caminho_projeto)
        caminho_projeto_label.pack()

        button_projeto = tk.Button(
            self.root, text="Abrir pasta", command=self.open_folder_project
        )
        button_projeto.pack()

        # Caminho deploy
        caminho_deploy_label = tk.Label(self.root, textvariable=self.caminho_deploy)
        caminho_deploy_label.pack()

        button_path_deploy = tk.Button(
            self.root, text="Abrir pasta", command=self.open_folder_deploy
        )
        button_path_deploy.pack()

        self.button_deploy = tk.Button(
            self.root, text="Deploy", command=self.deploy.deploy
        )
        self.button_deploy.pack()
        self.button_deploy.config(state=tk.DISABLED)

        self.root.mainloop()


if __name__ == "__main__":
    menu = Menu()
