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
        
    
    def removerConta(self, idConta):
        return self.__bancoDados.excluirContaDB(idConta)
    
    
    def atualizarContaNome(self, idConta, nomeNovo):
        return self.__bancoDados.atualizarContaNomeDB(idConta, nomeNovo)
    
    
    def atualizarContaEndereco(self, idConta, enderecoNovo):
        return self.__bancoDados.atualizarContaEnderecoDB(idConta, enderecoNovo)
    
    
    def atulizarContaTelefone(self, idConta, telefoneNovo):
        return self.__bancoDados.atualizarContaTelefoneDB(idConta, telefoneNovo)
    
    
    def vizualizarCliente(self):
        return self.__bancoDados.visualizarClientesDB()
    
    
    def visualizarConta(self, idConta):
        return self.__bancoDados.visualizarContaDB(idConta)
    
    
        

class Conta(Cliente):
    
    __bancoDados = Banco_de_Dados()

    def __init__(self, nome, senha, cad_Pessoa, endereco, telefone, idConta, saldo):
        super().__init__(nome, senha, cad_Pessoa, endereco, telefone, idConta)
        self._saldo = saldo
        self.__bancoDados.verificarPagamentoAgendadoDB(idConta)
        

    def saque(self, valor, idConta):
        return self.__bancoDados.saqueDB(valor, idConta)


    def deposito(self, valor, idConta):
        return self.__bancoDados.depositoDB(valor, idConta)


        # A DATA DEVE SER DIGITADA ASSIM: (dd/mm/aaaa)
    def pagamentoAgendado(self, valor, data, idConta):
        return self.__bancoDados.pagamentoAgendadoDB(valor, data, idConta)


    def extrato(self, idConta):
        return self.__bancoDados.extratoDB(idConta)


    def solicitarCredito(self, valor, data, idConta):
        return self.__bancoDados.solicitarCreditoDB(valor, data, idConta)



class Sistema:
    
    def __init__(self):
        pass


