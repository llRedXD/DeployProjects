import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from deploy import Deploy


class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.deploy = Deploy()

        # Configurações da janela
        self.root.title("Menu")
        self.root.geometry("600x400")

        self.environment_var = tk.StringVar()
        self.environment_var.set("Selecione o Ambiente")  # Set default value to "Dev"
        self.environment_options = ["Dev", "Prod"]

        self.os_var = tk.StringVar()
        self.os_var.set("Selecione o OS")  # Set default value to "Windows"
        self.os_options = ["Windows", "Linux"]

        self.language_var = tk.StringVar()
        self.language_var.set("Selecione a Linguagem")  # Set default value to "Python"
        self.language_options = ["Python", "React", "C#"]

        self.caminho_projeto = tk.StringVar()
        self.caminho_projeto.set("")

        self.caminho_deploy = tk.StringVar()
        self.caminho_deploy.set("")

        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=200, mode="indeterminate"
        )

        self.create_menu()

    # Funções para interagir com a interface
    def select_project_directory(self):
        self.deploy.os = self.os_var.get()
        if self.deploy.os == "Windows":
            desktop_path = os.path.join(
                os.path.join(os.environ["USERPROFILE"]), "Desktop"
            )
            self.deploy.project_path = filedialog.askdirectory(
                initialdir=desktop_path, title="Selecione uma pasta"
            )
        else:
            path_linux = "\\\\wsl.localhost/Ubuntu-22.04/home/"
            # Check if there is only one folder inside the 'home' directory
            folders = os.listdir(path_linux)
            if len(folders) == 1:
                path_linux = os.path.join(path_linux, folders[0])
            self.deploy.project_path = filedialog.askdirectory(
                initialdir=path_linux, title="Selecione uma pasta"
            )

        self.caminho_projeto.set(self.deploy.project_path)

    def select_deploy_folder(self):
        # Alimentar o objeto Deploy com as informações selecionadas
        self.deploy.set_base_path(self.environment_var.get())
        self.deploy.language = self.language_var.get()

        # Consultar pasta do projeto.
        folder_path = filedialog.askdirectory(
            initialdir=self.deploy.base_path,
            title="Selecione uma pasta",
        )
        self.deploy.deploy_path = folder_path
        # Faça algo com o caminho da pasta selecionada
        self.caminho_deploy.set(folder_path)
        if self.deploy.project_path:
            self.button_deploy.config(state=tk.NORMAL)

    def deploy_in_background(self):
        self.deploy.set_base_path(self.environment_var.get())
        self.deploy.os = self.os_var.get()
        self.deploy.language = self.language_var.get()
        self.deploy.deploy()
        self.on_deploy_finished()

    def deploy_action(self):
        deploy_thread = threading.Thread(target=self.deploy_in_background)
        deploy_thread.start()
        self.button_deploy.config(state=tk.DISABLED)
        self.progress_bar.pack()
        self.progress_bar.start()

    def on_deploy_finished(self):
        self.button_deploy.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        # Label de sucesso
        success_label = tk.Label(self.root, text="Deploy realizado com sucesso!")
        success_label.pack()
        time.sleep(7)
        success_label.pack_forget()

    # Funções para criar os elementos da interface
    def create_select(self, container, label, values, options):
        # Label
        label = ttk.Label(container, text=label)
        label.pack(side=tk.LEFT)

        # Campo de seleção
        select = tk.OptionMenu(container, values, *options)
        select["width"] = 20
        select.pack(side=tk.LEFT)

    def create_folder_selection(
        self, label_text, variable, button_text, button_command
    ):
        # Botão para selecionar a pasta
        button = tk.Button(self.root, text=button_text, command=button_command)
        button.pack()

        # Mostra o caminho da pasta selecionada
        container_folder = self.create_frame()
        # Rótulo
        label = tk.Label(container_folder, text=label_text)
        label.pack(side=tk.LEFT)

        # Caminho projeto
        path_label = tk.Label(container_folder, textvariable=variable)
        path_label.pack(side=tk.LEFT)

    def create_button(self, text, command, disabled=False):
        self.button_deploy = tk.Button(self.root, text=text, command=command)
        self.button_deploy.pack()
        self.button_deploy.config(state=tk.DISABLED if disabled else tk.NORMAL)

    def create_frame(self, height=200, width=200, padx=20, pady=10):
        frame = tk.Frame(self.root, height=height, width=width)
        frame.pack(padx=padx, pady=pady)
        return frame

    def create_menu(self):
        # Campos de seleção
        ambiente_container = self.create_frame()

        self.create_select(
            ambiente_container,
            "Ambiente",
            self.environment_var,
            self.environment_options,
        )

        os_container = self.create_frame()

        self.create_select(os_container, "OS", self.os_var, self.os_options)

        language_container = self.create_frame()

        self.create_select(
            language_container,
            "Linguagem",
            self.language_var,
            self.language_options,
        )

        # Call the function to create the folder selection
        self.create_folder_selection(
            "Pasta do Projeto:",
            self.caminho_projeto,
            "Selecionar pasta do projeto local",
            self.select_project_directory,
        )

        self.create_folder_selection(
            "Pasta para Deploy:",
            self.caminho_deploy,
            "Selecinar pasta para deploy no servidor",
            self.select_deploy_folder,
        )

        self.create_button("Deploy", self.deploy_action, True)

        self.root.mainloop()


if __name__ == "__main__":
    menu = Menu()
