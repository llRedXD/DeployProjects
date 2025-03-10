class Deploy:
    def __init__(self):
        self.caminho_dev = r"\\smydev\d$\inetpub\wwwroot\\"
        self.caminho_dev_bkp = r"\\smydev\\d$\\bkp\\"
        self.caminho_prod = r"\\smyapp2\d$\inetpub\wwwroot\\"
        self.caminho_prod_bkp = r"\\smyapp2\\d$\\bkp\\"
        self.caminho_temp = "./temp/"
        self.caminho_base = ""
        self.os = ""
        self.language = ""

    def definir_caminho_base(self, ambiente):
        if ambiente == "Dev":
            self.caminho_base = self.caminho_dev
        else:
            self.caminho_base = self.caminho_prod
