from library.data_base import Banco_de_Dados
from random import choice
import string

class Entidade:
    
    def __init__(self, nome, senha, cad_Pessoa):
        self.nome = nome
        self.senha = senha
        self.cad_Pessoa = cad_Pessoa


class Cliente(Entidade):
    
    def __init__(self, endereco, telefone, idConta):
        self.endereco = endereco
        self.telefone = telefone
        self.idConta = idConta
        


class Gerente(Entidade):
    
    def __init__(self, nome, senha, identificacao):
        super().__init__(nome, senha)
        self.__identificacao = identificacao
        
    def generateId():
        numbers = string.digits
        randomNumber = "".join(choice(numbers) for _ in range(4))
        return randomNumber

    def criarConta(self, nome, senha, endereco, telefone, saldo):
        idConta = self.generateId()
        
        newConta = Conta(nome, senha, endereco, telefone, idConta, saldo)
        Banco_de_Dados().criarContaDB(newConta)
        
        
        

class Conta(Cliente(Entidade)):
    
    def __init__(self, nome, senha, endereco, telefone, idConta, saldo):
        super().__init__(nome, senha, endereco, telefone, idConta)
        self._saldo = saldo



class Sistema:
    
    def __init__(self):
        pass


