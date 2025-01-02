from datetime import datetime
import os
import subprocess

caminho_dev = r"\\smydev\d$\inetpub\wwwroot\\"
caminho_dev_bkp = r"\\smydev\\d$\\bkp\\"
caminho_temp = "./temp/"

projeto = {
    "Backend Django2": {
        "projeto": "SmyDjangoV2",
        "path": "/home/red/workspace/SmyBackDjango",
        "app": "/project",
        "requirements": "requirements.txt",
        ".env": ".env",
        "os": "Linux",
        "linguagem": "Python",
    },
    "Controle Uni": {
        "projeto": "SmyControleUni",
        "path": "C:/Users/gabriel.oliveira/Desktop/Dev/SmyControleUni/SmyControleUni",
        "app": "/bin/Release/net6.0/publish",
        "requirements": "",
        ".env": "",
        "os": "Windows",
        "linguagem": "C#",
    },
}


def obter_branch_git(caminho_pasta):
    try:
        resultado = subprocess.check_output(
            ["powershell", "wsl", "git", "rev-parse", "--abbrev-ref", "HEAD"],
        )
        branch = resultado.decode().strip()
        return branch
    except subprocess.CalledProcessError:
        return None


def fazer_deploy(projeto):
    for num, (key, value) in enumerate(projeto.items(), 1):
        print(f"Projeto {num}: {key}")

    # projeto_escolido = int(input("Digite o número do projeto: "))
    # print("Escolha o ambiente de deploy:")
    # print("1 - Dev")
    # print("2 - Prod")

    ambientes = ["dev", "prod"]

    # ambiente = int(input("Digite o número do ambiente: "))
    # ambiente_escolido = ambientes[ambiente - 1]
    ambiente_escolido = "dev"

    projeto_escolido = 2

    projeto = list(projeto.values())[projeto_escolido - 1]
    caminho = projeto["path"]
    nome_projeto = projeto["projeto"]
    caminho_app = projeto["app"]
    # caminho_requirements = projeto["requirements"]
    # caminho_env = projeto[".env"]
    caminho_os = projeto["os"]
    linguagem = projeto["linguagem"]

    if linguagem == "C#":
        criar_publish(caminho, ambiente_escolido)

    criar_backup(nome_projeto, caminho_app, ambiente_escolido, linguagem)

    upar_projeto(
        caminho, nome_projeto, caminho_app, ambiente_escolido, caminho_os, linguagem
    )


def criar_publish(caminho, ambiente):
    subprocess.run(
        ["powershell", "cd", caminho, ";", "dotnet", "publish -c Release"],
    )


def criar_backup(nome_projeto, app, ambiente, linguagem):
    print("Criando backup do projeto...")
    if linguagem == "C#":
        app = ""
    if ambiente == "dev":
        pasta_destino = (
            caminho_dev_bkp
            + nome_projeto
            + "_"
            + datetime.now().strftime("%Y_%m_%d_%M")
        )

        subprocess.run(
            [
                "powershell",
                "cp",
                "-r",
                f"{caminho_dev}{nome_projeto}Teste/{app}",
                pasta_destino,
            ]
        )
    print("Backup criado com sucesso!")


def upar_projeto(caminho, nome_projeto, app, ambiente, os, linguagem):
    print("Iniciando deploy do projeto...")
    branch = obter_branch_git(caminho)
    subprocess.run(["powershell", "rm", "-r", f"{caminho_temp}"])

    if branch == "dev" and ambiente == "dev":
        if os == "Linux":
            subprocess.run(
                [
                    "powershell",
                    "wsl",
                    "cp",
                    "-r",
                    f"{caminho}{app}",
                    caminho_temp,
                ]
            )
        elif os == "Windows":
            subprocess.run(
                [
                    "powershell",
                    "cp",
                    "-r",
                    f"{caminho}{app}",
                    caminho_temp,
                ]
            )

        if linguagem == "C#":
            app = ""

        subprocess.run(
            ["powershell", "rm", "-r", f"{caminho_dev}{nome_projeto}Teste/{app}"]
        )

        subprocess.run(
            [
                "powershell",
                "cp",
                "-r",
                f"{caminho_temp}",
                f"{caminho_dev}{nome_projeto}Teste/{app}",
            ]
        )
        print("Deploy realizado com sucesso!")


fazer_deploy(projeto)
