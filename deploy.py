from datetime import datetime
import subprocess
import os as os_lib
import json

caminho_dev = r"\\smydev\d$\inetpub\wwwroot\\"
caminho_dev_bkp = r"\\smydev\\d$\\bkp\\"
caminho_prod = r"\\smyapp2\d$\inetpub\wwwroot\\"
caminho_prod_bkp = r"\\smyapp2\\d$\\bkp\\"
caminho_temp = "./temp/"


def obter_branch_git(caminho_pasta, os):
    """
    Obtém o nome da branch atual de um repositório Git.

    Args:
        caminho_pasta (str): Caminho para a pasta do repositório Git.
        os (str): Sistema operacional ("Linux" ou "Windows").

    Returns:
        str: Nome da branch atual ou None em caso de erro.
    """
    try:
        if os == "Linux":
            comando = [
                "wsl",
                "cd",
                caminho_pasta,
                "&&",
                "git",
                "rev-parse",
                "--abbrev-ref",
                "HEAD",
            ]
        elif os == "Windows":
            comando = [
                "cmd",
                "/c",
                f"cd {caminho_pasta} && git rev-parse --abbrev-ref HEAD",
            ]
        else:
            return None

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        branch = resultado.stdout.strip()
        return branch
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None


def selecionar_projeto(projetos):
    """
    Permite ao usuário selecionar um projeto de uma lista de projetos.

    Args:
        projetos (dict): Dicionário contendo informações dos projetos.

    Returns:
        dict: Dicionário com informações do projeto selecionado.
    """
    while True:
        try:
            for num, (key, value) in enumerate(projetos.items(), 1):
                print(f"Projeto {num}: {key}")
            projeto_escolhido = int(input("Digite o número do projeto: "))
            if 1 <= projeto_escolhido <= len(projetos):
                return list(projetos.values())[projeto_escolhido - 1]
            else:
                print("Número do projeto inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


def selecionar_ambiente():
    """
    Permite ao usuário selecionar um ambiente de deploy.

    Returns:
        str: Nome do ambiente selecionado.
    """
    ambientes = ["dev", "prod"]
    while True:
        try:
            print("Escolha o ambiente de deploy:")
            for num, ambiente in enumerate(ambientes, 1):
                print(f"{num} - {ambiente.capitalize()}")
            ambiente_escolhido = int(input("Digite o número do ambiente: "))
            if 1 <= ambiente_escolhido <= len(ambientes):
                return ambientes[ambiente_escolhido - 1]
            else:
                print("Número do ambiente inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


def fazer_deploy(projetos):
    """
    Realiza o deploy de um projeto selecionado.

    Args:
        projetos (list): Lista de dicionários contendo informações dos projetos.

    Raises:
        KeyError: Se uma chave esperada não for encontrada no dicionário do projeto.
        Exception: Para qualquer outro erro inesperado.
    """
    try:
        # Seleciona o projeto a ser deployado
        projeto = selecionar_projeto(projetos)
        # Seleciona o ambiente para o deploy
        ambiente_escolhido = selecionar_ambiente()

        # Extrai informações do projeto
        caminho = projeto["path"]
        nome_projeto = projeto["projeto"]
        caminho_app = projeto["app"]
        caminho_os = projeto["os"]
        linguagem = projeto["linguagem"]

        # Se a linguagem for C#, cria o publish
        if linguagem == "C#":
            criar_publish(caminho, ambiente_escolhido)

        # Cria um backup do projeto
        criar_backup(nome_projeto, caminho_app, ambiente_escolhido, linguagem)

        # Realiza o upload do projeto
        upar_projeto(
            caminho,
            nome_projeto,
            caminho_app,
            ambiente_escolhido,
            caminho_os,
            linguagem,
        )
    except KeyError as e:
        print(
            f"Erro: Chave {e} não encontrada no projeto. Verifique se todas as chaves necessárias estão presentes."
        )
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def criar_publish(caminho, ambiente):
    """
    Cria o publish de um projeto .NET.

    Args:
        caminho (str): Caminho para a pasta do projeto.
        ambiente (str): Ambiente de deploy (dev ou prod).

    Returns:
        None
    """
    try:
        # Executa o comando de publish usando PowerShell
        subprocess.run(
            ["powershell", "cd", caminho, ";", "dotnet", "publish", "-c", "Release"],
            check=True,
        )
        print(f"Publish criado com sucesso para o ambiente {ambiente}!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar publish: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def criar_backup(nome_projeto, app, ambiente, linguagem):
    """
    Cria um backup do projeto especificado.

    Args:
        nome_projeto (str): Nome do projeto.
        app (str): Caminho do aplicativo dentro do projeto.
        ambiente (str): Ambiente de deploy (dev ou prod).
        linguagem (str): Linguagem de programação do projeto.

    Returns:
        None
    """
    print("Criando backup do projeto...")

    # Ajusta o caminho do app se a linguagem for C#
    if linguagem == "C#":
        app = ""

    try:
        # Define o caminho de destino do backup com base no ambiente
        if ambiente == "dev":
            caminho_deploy = caminho_dev
            caminho_bkp = caminho_dev_bkp
        elif ambiente == "prod":
            caminho_deploy = caminho_prod
            caminho_bkp = caminho_prod_bkp
        else:
            print(f"Ambiente '{ambiente}' não suportado para backup.")

        pasta_destino = (
            caminho_bkp
            + nome_projeto
            + "_"
            + datetime.now().strftime("%Y_%m_%d_%H%M%S")
        )

        # Executa o comando de backup usando PowerShell
        subprocess.run(
            [
                "powershell",
                "cp",
                "-r",
                f"{caminho_deploy}{nome_projeto}/{app}",
                pasta_destino,
            ],
            check=True,
        )
        print("Backup criado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar backup: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def upar_projeto(caminho, nome_projeto, app, ambiente, os, linguagem):
    """
    Realiza o deploy do projeto especificado.

    Args:
        caminho (str): Caminho do projeto.
        nome_projeto (str): Nome do projeto.
        app (str): Caminho do aplicativo dentro do projeto.
        ambiente (str): Ambiente de deploy (dev ou prod).
        os (str): Sistema operacional (Linux ou Windows).
        linguagem (str): Linguagem de programação do projeto.

    Returns:
        None
    """
    print("Iniciando deploy do projeto...")

    try:
        # Obtém a branch atual do repositório Git
        branch = obter_branch_git(caminho, os)

        # Remove o diretório temporário, se existir
        if os_lib.path.exists(caminho_temp):
            subprocess.run(["powershell", "rm", "-r", f"{caminho_temp}"], check=True)

        # Copia os arquivos do projeto para o diretório temporário
        if os == "Linux":
            subprocess.run(
                [
                    "powershell",
                    "wsl",
                    "cp",
                    "-r",
                    f"{caminho}{app}",
                    caminho_temp,
                ],
                check=True,
            )
        elif os == "Windows":
            subprocess.run(
                [
                    "powershell",
                    "cp",
                    "-r",
                    f"{caminho}{app}",
                    caminho_temp,
                ],
                check=True,
            )

        # Ajusta o caminho do app se a linguagem for C#
        if linguagem == "C#":
            app = ""

        if ambiente == "dev":
            caminho_deploy = caminho_dev
        elif ambiente == "prod":
            if branch != "prod":
                raise (Exception("Branch diferente de 'prod'. Deploy não permitido."))
            caminho_deploy = caminho_prod

        # Remove o diretório de destino, se existir
        subprocess.run(
            ["powershell", "rm", "-r", f"{caminho_deploy}{nome_projeto}/{app}"],
            check=True,
        )

        # Copia os arquivos do diretório temporário para o diretório de destino
        subprocess.run(
            [
                "powershell",
                "cp",
                "-r",
                f"{caminho_temp}",
                f"{caminho_deploy}{nome_projeto}/{app}",
            ],
            check=True,
        )
        print("Deploy realizado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


with open("projetos.json", "r") as file:
    projetos = json.load(file)

if __name__ == "__main__":
    continuar = "s"
    while continuar.lower() == "s":
        fazer_deploy(projetos)
        continuar = input("Deseja realizar outro deploy? (s/n) ")
