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
        self.caminho_base = ""
        self.caminho_bkp = ""
        self.os = ""
        self.language = ""
        self.caminho_projeto = ""
        self.projeto = ""

    def definir_caminho_base(self, ambiente):
        if ambiente == "Dev":
            self.caminho_base = self.caminho_dev
            self.caminho_bkp = self.caminho_dev_bkp
        else:
            self.caminho_base = self.caminho_prod
            self.caminho_bkp = self.caminho_prod_bkp

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
                        self.projeto = settings_module.split(".")[0]

    def get_projeto_python(self):
        manage_path = os.path.join(self.caminho_projeto, "manage.py")
        self.get_name_project(manage_path)
        self.caminho_projeto = os.path.join(self.caminho_projeto, self.projeto)

    # React
    def get_projeto_react(self):
        build_path = os.path.join(self.caminho_projeto, "build")
        print(self.caminho_projeto)
        if not os.path.exists(build_path):
            subprocess.run(["powershell", "cd", self.caminho_projeto])
            subprocess.run(
                [("wsl" if self.os == "Linux" else ""), "npm", "run", "build"]
            )
        self.caminho_projeto = build_path

    def criar_backup(self):
        print("Criando backup")
        if self.language == "Python":
            self.get_projeto_python()
        if self.language == "React":
            self.get_projeto_react()
        subprocess.run(
            [
                "powershell",
                "cp",
                "-r",
                self.caminho_projeto,
                self.caminho_bkp
                + self.caminho_base.split("\\")[-1]
                + f"_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            ],
        )

    def deploy(self):
        print(self.language)
        self.criar_backup()


if __name__ == "__main__":
    deploy = Deploy()
    deploy.definir_caminho_base("Dev")
    deploy.language = "React"
    deploy.os = "Linux"
    deploy.caminho_projeto = (
        "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/smy_intranet"
    )
    # deploy.caminho_projeto = (
    #     "\\\\wsl.localhost/Ubuntu-22.04/home/red/workspace/back-end-django"
    # )
    # deploy.caminho_base = "\\\\smydev\d$\inetpub\wwwroot\SmyBackDjango"
    deploy.caminho_base = "\\\\smydev\d$\inetpub\wwwroot\IntranetFrontend"
    deploy.deploy()
