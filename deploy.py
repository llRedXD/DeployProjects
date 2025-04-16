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
        self.deploy_path = ""
        self.project = ""
        self.dist_build = False
        self.exclude_dir = [
            ".venv",
            "venv",
            ".git",
            ".vscode",
            "django-cache",
            "logs",
            "node_modules",
            "__pycache__",
        ]

        self.exclude_file = [
            ".env",
            "example.env",
            ".gitignore",
            "README.md",
            "*.pyc",
            "*.sqlite3",
            "*.djcache",
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
            if self.dist_build:
                return
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

    def verify_build_react(self):
        try:
            path = os.path.join(self.project_path, "dist")
            if os.path.exists(path):
                print("Build do React encontrado.")
                self.dist_build = True
                self.project_path = path
                return True
            else:
                print("Build do React não encontrado.")
                return False
        except Exception as e:
            print(f"Erro ao verificar o build do React: {e}")

    # C#
    def create_publish_csharp(self):
        try:
            path = self.project_path
            print("Criando publish")

            subprocess.run(
                ["powershell", "-Command", "dotnet publish", "-c", "Release"],
                cwd=path,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando: {e}")
            print(f"Saída do erro: {e.stderr}")
        except Exception as e:
            print(f"Ocorreu um erro ao criar o publish: {e}")

    def get_path_publish_csharp(self):
        try:
            folder_path = os.path.join(
                self.project_path,
                f"{self.project_path.split('/')[-1]}/bin/Release",
            )

            contents = os.listdir(folder_path)

            directories = [
                d for d in contents if os.path.isdir(os.path.join(folder_path, d))
            ]

            if len(directories) == 1:
                unique_folder_name = directories[0]
            else:
                print("Não há exatamente uma pasta dentro do diretório especificado.")

            path = os.path.join(folder_path, rf"{unique_folder_name}\publish")

            return path

        except Exception as e:
            print(f"Erro ao buscar o caminho do publish: {e}")

    # Deploy
    def create_backup(self):
        try:
            print("Criando backup")

            backup_directory = (
                self.backup_path
                + self.deploy_path.split("/")[-1]
                + f"_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
            )
            print(backup_directory)

            subprocess.run(
                [
                    "robocopy",
                    self.deploy_path,
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
            exclude_file = self.exclude_file
            if self.language == "React":
                self.verify_build_react()
            if self.os == "Windows":
                if self.language == "React":
                    self.create_build_react()
                if self.language == "C#":
                    self.create_publish_csharp()
                    self.project_path = self.get_path_publish_csharp()

            subprocess.run(
                [
                    "robocopy",
                    self.project_path,
                    self.temp_dir,
                    "/E",  # Copiar subdiretórios, incluindo vazios
                    "/XD",
                    *self.exclude_dir,  # Excluir diretório
                    "/XF",
                    *exclude_file,
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
            else:
                self.project = ""

            path_project_deploy = os.path.join(self.temp_dir, self.project)
            if self.dist_build:
                path_project_deploy = self.temp_dir

            subprocess.run(
                [
                    "robocopy",
                    path_project_deploy,
                    self.deploy_path,
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
        self.import_project_to_temp()
        self.create_backup()
        self.up_project_to_base()


if __name__ == "__main__":
    deploy = Deploy()
    deploy.set_base_path("Dev")
    deploy.language = "C#"
    deploy.os = "Windows"
    deploy.project_path = (
        r"C:\Users\gabriel.oliveira\Desktop\PlayGround\Projetos\Smy_EU"
    )
    deploy.deploy_path = "\\\\smydev\d$\inetpub\wwwroot\SmyEu"
    deploy.deploy()
