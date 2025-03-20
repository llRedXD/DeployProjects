from datetime import datetime
import os
import re
import subprocess
import shutil


class Deploy:
    def __init__(self):
        self.caminho_dev = r"\\smydev\d$\inetpub\wwwroot\\"
        self.caminho_dev_bkp = r"\\smydev\\d$\\bkp\\"
        self.caminho_prod = r"\\smyapp2\d$\inetpub\wwwroot\\"
        self.caminho_prod_bkp = r"\\smyapp2\\d$\\bkp\\"
        self.temp_dir = "./temp/"
        self.base_path = ""
        self.backup_path = ""
        self.os = ""
        self.language = ""
        self.project_path = ""
        self.project = ""
        self.exclude_dir = [
            ".venv",
            "venv",
            ".git",
            ".vscode",
            "django-cache",
            "logs",
            "node_modules",
        ]

        self.exclude_file = [
            "example.env",
            ".gitignore",
            "README.md",
        ]

    def set_base_path(self, ambiente):
        if ambiente == "Dev":
            self.base_path = self.caminho_dev
            self.backup_path = self.caminho_dev_bkp
        else:
            self.base_path = self.caminho_prod
            self.backup_path = self.caminho_prod_bkp

    # React
    def create_build_react(self):
        try:
            if self.os == "Linux":
                path = self.temp_dir

                subprocess.run(
                    ["powershell", "-Command", "npm install"],
                    check=True,
                    cwd=path,
                )

            if self.os == "Windows":
                path = self.project_path

            subprocess.run(
                ["powershell", "-Command", "npm run build"],
                cwd=path,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando: {e}")
            print(f"Saída do erro: {e.stderr}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    # Deploy
    def create_backup(self):
        try:
            print("Criando backup")

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
                    *self.exclude_dir,  # Excluir diretório
                    "/XF",
                    *self.exclude_file,  # Excluir arquivo
                ],
                check=True,
            )
        except Exception as e:
            print(f"Erro ao criar backup: {e}")

    def create_temp(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        else:
            shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir)

    def import_project_to_temp(self):
        try:
            self.create_temp()
            print("Importando projeto para temp")
            if self.os == "Windows":
                if self.language == "React":
                    self.create_build_react()

            subprocess.run(
                [
                    "robocopy",
                    self.project_path,
                    self.temp_dir,
                    "/E",  # Copiar subdiretórios, incluindo vazios
                    "/XD",
                    *self.exclude_dir,  # Excluir diretório
                    "/XF",
                    *self.exclude_file,  # Excluir arquivo
                ],
                check=True,
            )

        except Exception as e:
            print(e)

    def up_project_to_base(self):
        try:
            print("Subindo projeto para base")
            if self.language == "React":
                if self.os == "Linux":
                    self.create_build_react()
                self.project = "dist"

            path_project_deploy = os.path.join(self.temp_dir, self.project)

            subprocess.run(
                [
                    "robocopy",
                    path_project_deploy,
                    self.base_path,
                    "/E",  # Copiar subdiretórios, incluindo vazios
                    "/XD",
                    *self.exclude_dir,  # Excluir diretório
                    "/XF",
                    *self.exclude_file,  # Excluir arquivo
                ],
                check=True,
            )
        except Exception as e:
            print(f"Erro ao subir projeto para base: {e}")

    def deploy(self):
        print(self.language)
        self.import_project_to_temp()
        # self.create_backup()
        self.up_project_to_base()
        print("Deploy")


if __name__ == "__main__":
    deploy = Deploy()
    deploy.set_base_path("Dev")
    deploy.language = "Python"
    deploy.os = "Linux"
    # deploy.os = "Windows"
    # deploy.project_path = r"C:\Users\gabriel.oliveira\Desktop\Dev\IntranetFrontend"
    # deploy.project_path = (
    #     "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/smy_intranet"
    # )
    # deploy.project_path = (
    #     r"C:\Users\gabriel.oliveira\Desktop\PlayGround\Projetos\SmyFlv"
    # )
    deploy.project_path = (
        "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/back-end-django"
    )
    # deploy.base_path = "\\\\smydev\d$\inetpub\wwwroot\SmyBackDjango"
    deploy.base_path = "\\\\smydev\d$\inetpub\wwwroot\TEste123"
    # deploy.base_path = "\\\\smydev\d$\inetpub\wwwroot\IntranetBackend"
    deploy.deploy()
