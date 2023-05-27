from library.data_base import Banco_de_Dados
from random import choice
import string

class Entidade:
    
    def __init__(self, nome, senha, cad_Pessoa):
        self.nome = nome
        self.senha = senha
        self.cad_Pessoa = cad_Pessoa


class Cliente(Entidade):
    
    def __init__(self, nome, senha, cad_Pessoa, endereco, telefone, idConta):
        super().__init__(nome, senha, cad_Pessoa)
        self.endereco = endereco
        self.telefone = telefone
        self.idConta = idConta
        


class Gerente(Entidade):
    
    bancoDados = Banco_de_Dados()
    
    def __init__(self, nome, senha, identificacao, cad_Pessoa):
        super().__init__(nome, senha, cad_Pessoa)
        self.__identificacao = identificacao
        
    
    def gerarID(self):
        idLista = []
        numbers = string.digits
        randomNumber = "".join(choice(numbers) for _ in range(4))
        
        if randomNumber in idLista:
            return self.gerarID()
        else:
            return randomNumber 
        

    def criarConta(self, nome, senha, cad_Pessoa, endereco, telefone, saldo):
        idConta = self.gerarID()
        novaConta = Conta(nome, senha, cad_Pessoa, endereco, telefone, idConta, saldo)
        return self.bancoDados.criarContaDB(novaConta)
        
    
    def removerConta(self, nome):
        return self.bancoDados.excluirContaDB(nome)
    
    
    def atualizarContaNome(self, nomeAntigo, nomeNovo):
        return self.bancoDados.atualizarContaNomeDB(nomeAntigo, nomeNovo)
    
    
    def atualizarContaEndereco(self, nome, enderecoNovo):
        return self.bancoDados.atualizarContaEnderecoDB(nome, enderecoNovo)
    
    
    def atulizarContaTelefone(self, nome, telefoneNovo):
        return self.bancoDados.atualizarContaTelefoneDB(nome, telefoneNovo)
    
    
    def vizualizarCliente(self):
        return self.bancoDados.visualizarClientesDB()
    
    
    def visualizarConta(self, nome):
        return self.bancoDados.visualizarContaDB(nome)
    
    
        

class Conta(Cliente):
    
    def __init__(self, nome, senha, cad_Pessoa, endereco, telefone, idConta, saldo):
        super().__init__(nome, senha, cad_Pessoa, endereco, telefone, idConta)
        self._saldo = saldo

    
    def saque(self):
        pass
    
    
    def deposito(self):
        pass
    
    
    def pagamentoAgendado(self):
        pass
    
    
    def extrato(self):
        pass
    
    
    def solicitarCredito(self):
        pass



class Sistema:
    
    def __init__(self):
        pass


