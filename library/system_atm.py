from library.data_base import Banco_de_Dados
from random import choice
import string

class Entidade:
    
    def __init__(self, nome, senha, cad_Pessoa):
        self.__nome = nome
        self.__senha = senha
        self.__cad_Pessoa = cad_Pessoa
        
        
    def getNome(self):
        return self.__nome


class Cliente(Entidade):
    
    def __init__(self, nome, senha, cad_Pessoa, endereco, telefone, idConta):
        super().__init__(nome, senha, cad_Pessoa)
        self.__endereco = endereco
        self.__telefone = telefone
        self._idConta = idConta
         


class Gerente(Entidade):
    
    __bancoDados = Banco_de_Dados()
    
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
        if self.__bancoDados.criarContaDB(novaConta):
            return novaConta
        else:
            return None
        
    
    def removerConta(self, nome):
        return self.__bancoDados.excluirContaDB(nome)
    
    
    def atualizarContaNome(self, nomeAntigo, nomeNovo):
        return self.__bancoDados.atualizarContaNomeDB(nomeAntigo, nomeNovo)
    
    
    def atualizarContaEndereco(self, nome, enderecoNovo):
        return self.__bancoDados.atualizarContaEnderecoDB(nome, enderecoNovo)
    
    
    def atulizarContaTelefone(self, nome, telefoneNovo):
        return self.__bancoDados.atualizarContaTelefoneDB(nome, telefoneNovo)
    
    
    def vizualizarCliente(self):
        return self.__bancoDados.visualizarClientesDB()
    
    
    def visualizarConta(self, nome):
        return self.__bancoDados.visualizarContaDB(nome)
    
    
        

class Conta(Cliente):

    def __init__(self, nome, senha, cad_Pessoa, endereco, telefone, idConta, saldo):
        super().__init__(nome, senha, cad_Pessoa, endereco, telefone, idConta)
        self._saldo = saldo


    def saque(self, valor, conta):
        return self.__bancoDados.saqueDB(valor, conta)


    def deposito(self, valor, conta):
        return self.__bancoDados.depositoDB(valor, conta)


    def pagamentoAgendado(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            return f"Pagamento agendado de R${valor:.2f} realizado com sucesso. Saldo atual: R${self._saldo:.2f}"
        else:
            return "Saldo insuficiente para realizar o pagamento agendado."


    def extrato(self, conta):
        return self.__bancoDados.extratoDB(conta)


    def solicitarCredito(self, valor):
        if valor > 0:
            return f"Solicitação de crédito de R${valor:.2f} realizada com sucesso."
        else:
            return "Valor inválido para solicitar crédito."



class Sistema:
    
    def __init__(self):
        pass


