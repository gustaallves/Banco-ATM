class Entidade:
    
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha


class Cliente(Entidade):
    
    def __init__(self, endereco, telefone, idConta):
        self.endereco = endereco
        self.telefone = telefone
        self.idConta = idConta
        


class Gerente(Entidade):
    
    def __init__(self, identificacao):
        self.identificacao = identificacao



class Conta:
    
    def __init__(self, idConta, saldo):
        self.idConta = idConta
        self.saldo = saldo



class Sistema:
    
    def __init__(self):
        pass


