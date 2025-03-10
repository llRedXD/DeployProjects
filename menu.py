import tkinter as tk
from tkinter import filedialog

from deployC import Deploy


class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.deploy = Deploy()

        # Configurações da janela
        self.root.title("Menu")
        self.root.geometry("400x200")

        self.environment_var = tk.StringVar()
        self.environment_var.set("Dev")  # Set default value to "Dev"
        self.environment_options = ["Dev", "Prod"]

        self.os_var = tk.StringVar()
        self.os_var.set("Windows")  # Set default value to "Windows"
        self.os_options = ["Windows", "Linux"]

        self.language_var = tk.StringVar()
        self.language_var.set("Python")  # Set default value to "Python"
        self.language_options = ["Python", ".Net", "React"]

        self.caminho_pasta = tk.StringVar()
        self.caminho_pasta.set("")

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

    def open_folder(self):
        # Alimentar o objeto Deploy com as informações selecionadas
        self.deploy.definir_caminho_base(self.environment_var.get())
        self.deploy.os = self.os_var.get()
        self.deploy.language = self.language_var.get()

        # Consultar pasta do projeto.
        folder_path = filedialog.askdirectory(
            initialdir=self.deploy.caminho_base,
            title="Selecione uma pasta",
        )
        # Faça algo com o caminho da pasta selecionada
        self.caminho_pasta.set(folder_path)

    def create_menu(self):
        self.select_environment()
        self.select_os()
        self.select_language()

        # Rótulo
        label = tk.Label(self.root, text="Selecione uma pasta:")
        label.pack()

        caminho_pasta_label = tk.Label(self.root, textvariable=self.caminho_pasta)
        caminho_pasta_label.pack()

        button = tk.Button(self.root, text="Abrir pasta", command=self.open_folder)
        button.pack()

        self.root.mainloop()


if __name__ == "__main__":
    menu = Menu()
