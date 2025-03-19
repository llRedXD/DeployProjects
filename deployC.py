from datetime import datetime
import os
import re
import subprocess
from unittest import result


class Deploy:
    def __init__(self):
        self.caminho_dev = r"\\smydev\d$\inetpub\wwwroot\\"
        self.caminho_dev_bkp = r"\\smydev\\d$\\bkp\\"
        self.caminho_prod = r"\\smyapp2\d$\inetpub\wwwroot\\"
        self.caminho_prod_bkp = r"\\smyapp2\\d$\\bkp\\"
        self.caminho_temp = "./temp/"
        self.base_path = ""
        self.backup_path = ""
        self.os = ""
        self.language = ""
        self.project_path = ""
        self.project = ""

    def set_base_path(self, ambiente):
        if ambiente == "Dev":
            self.base_path = self.caminho_dev
            self.backup_path = self.caminho_dev_bkp
        else:
            self.base_path = self.caminho_prod
            self.backup_path = self.caminho_prod_bkp

    def if_linux(self, command):
        if self.os == "Linux":
            return ["wsl", command]
        return command

    # Python
    def get_name_project(self, path):
        with open(path, "r") as file:
            for line in file:
                if 'os.environ.setdefault("DJANGO_SETTINGS_MODULE"' in line:
                    match = re.search(
                        r'os\.environ\.setdefault\("DJANGO_SETTINGS_MODULE",\s*"(.*?)"\)',
                        line,
                    )
                    if match:
                        settings_module = match.group(1)
                        self.project = settings_module.split(".")[0]

    def get_projeto_python(self):
        manage_path = os.path.join(self.project_path, "manage.py")
        self.get_name_project(manage_path)

    # React
    def get_projeto_react(self):
        build_path = os.path.join(self.project_path, "build")
        print(self.project_path.replace("\\\\wsl.localhost/Ubuntu-22.04", ""))
        if not os.path.exists(build_path):
            if self.os == "Linux":
                initial_command = [
                    "wsl",
                    "cd",
                    self.project_path.replace("\\\\wsl.localhost/Ubuntu-22.04", ""),
                ]
                subprocess.run(initial_command)
            else:
                subprocess.run(["powershell", "cd", self.project_path])
                subprocess.run(
                    [("wsl" if self.os == "Linux" else ""), "npm", "run", "build"]
                )
        self.project_path = build_path

    def create_backup(self):
        print("Criando backup")

        exclude_dir = [
            ".venv",
            "venv",
            ".git",
            ".vscode",
            "django-cache",
            "logs",
        ]

        exclude_archive = [
            "example.env",
            ".gitignore",
            "README.md",
        ]

        backup_directory = (
            self.backup_path
            + self.base_path.split("\\")[-1]
            + f"_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )

        subprocess.run(
            [
                "robocopy",
                self.base_path,
                backup_directory,
                "/E",  # Copiar subdiretórios, incluindo vazios
                "/XD",
                *exclude_dir,  # Excluir diretório
                "/XF",
                *exclude_archive,  # Excluir arquivo
            ],
            check=True,
        )

    def deploy(self):
        print(self.language)
        self.create_backup()


if __name__ == "__main__":
    deploy = Deploy()
    deploy.set_base_path("Dev")
    deploy.language = "Python"
    deploy.os = "Linux"
    deploy.project_path = (
        "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/smy_intranet"
    )
    # deploy.caminho_projeto = (
    #     "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/back-end-django"
    # )
    # deploy.caminho_base = "\\\\smydev\d$\inetpub\wwwroot\SmyBackDjango"
    # deploy.caminho_base = "\\\\smydev\d$\inetpub\wwwroot\IntranetFrontend"
    deploy.base_path = "\\\\smydev\d$\inetpub\wwwroot\IntranetBackend"
    deploy.deploy()
