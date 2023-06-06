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
    
    def __init__(self, banco_dados, gerente):
        self.banco_dados = banco_dados
        self.gerente = gerente
        print("====================Banco ATM====================\n")
        print("Digite a opção que deseja acessar:\n")
        print("[1] Gerente\n")
        print("[2] Conta\n")
        print("=================================================\n")

        opcao = input("Digite o número da opção desejada: ")
        if opcao == "1":
            self.interface_Gerente()
        elif opcao == "2":
            self.interface_Cliente()
        else:
            print("Digite um valor válido.\n")

    def interface_Gerente(self):
        print("====================Banco ATM====================\n")
        print("Selecione uma opção:\n")
        print("[1] Criar Conta\n")
        print("[2] Remover Conta\n")
        print("[3] Atualizar Conta\n")
        print("[4] Visualizar Conta\n")
        print("=================================================\n")

        opcao = input("Digite o número da opção desejada: ")
        if opcao == "1":
            self.criar_conta()
        elif opcao == "2":
            idConta = input("Digite o ID da conta a ser removida: ")
            if self.removerConta(idConta):
                print("Conta removida com sucesso!")
            else:
                print("Não foi possível remover a conta.")
        elif opcao == "3":
            idConta = input("Digite o ID da conta a ser atualizada: ")
            print("Selecione uma opção:\n")
            print("[1] Atualizar nome\n")
            print("[2] Atualizar endereço\n")
            print("[3] Atualizar telefone\n")
            sub_opcao = input("Digite o número da opção desejada: ")

            if sub_opcao == "1":
                novo_nome = input("Digite o novo nome: ")
                if self.atualizarContaNome(idConta, novo_nome):
                    print("Nome da conta atualizado com sucesso!")
                else:
                    print("Não foi possível atualizar o nome da conta.")
            elif sub_opcao == "2":
                novo_endereco = input("Digite o novo endereço: ")
                if self.atualizarContaEndereco(idConta, novo_endereco):
                    print("Endereço da conta atualizado com sucesso!")
                else:
                    print("Não foi possível atualizar o endereço da conta.")
            elif sub_opcao == "3":
                novo_telefone = input("Digite o novo telefone: ")
                if self.atualizarContaTelefone(idConta, novo_telefone):
                    print("Telefone da conta atualizado com sucesso!")
                else:
                    print("Não foi possível atualizar o telefone da conta.")
            else:
                print("Opção inválida.")
        elif opcao == "4":
            idConta = input("Digite o ID da conta a ser visualizada: ")
            conta = self.visualizarConta(idConta)
            if conta:
                print("Detalhes da Conta:")
                print("Nome:", conta.getNome())
                # Exibir outros detalhes da conta, se necessário
            else:
                print("Conta não encontrada.")
        else:
            print("Digite um valor válido.\n")

    def criar_conta(self):
        print("====================Banco ATM====================\n")
        print("Digite os dados do cliente:\n")
        nome = input("Nome: ")
        cad_Pessoa = input("CPF/CNPJ: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        saldo = input("Saldo Inicial: ")
        senha = input("Senha: ")

        conta = self.criarConta(nome, senha, cad_Pessoa, endereco, telefone, saldo)
        if conta:
            print("Conta criada com sucesso!")
            print("ID da conta:", conta._idConta)
        else:
            print("Não foi possível criar a conta.")

    def interface_Cliente(self):
        idConta = input("Digite o ID da conta: ")
        senha = input("Digite a senha: ")
        conta = self.visualizarConta(idConta)
        if conta and conta._senha == senha:
            print("====================Banco ATM====================\n")
            print("Selecione uma opção:\n")
            print("[1] Saque\n")
            print("[2] Depósito\n")
            print("[3] Pagamento Agendado\n")
            print("[4] Extrato\n")
            print("=================================================\n")

            opcao = input("Digite o número da opção desejada: ")
            if opcao == "1":
                valor = input("Digite o valor do saque: ")
                if conta.saque(valor, idConta):
                    print("Saque realizado com sucesso!")
                else:
                    print("Não foi possível realizar o saque.")
            elif opcao == "2":
                valor = input("Digite o valor do depósito: ")
                if conta.deposito(valor, idConta):
                    print("Depósito realizado com sucesso!")
                else:
                    print("Não foi possível realizar o depósito.")
            elif opcao == "3":
                valor = input("Digite o valor do pagamento: ")
                data = input("Digite a data do pagamento (dd/mm/aaaa): ")
                if conta.pagamentoAgendado(valor, data, idConta):
                    print("Pagamento agendado com sucesso!")
                else:
                    print("Não foi possível agendar o pagamento.")
            elif opcao == "4":
                extrato = conta.extrato(idConta)
                print("Extrato:")
                for item in extrato:
                    print(item)
            else:
                print("Digite um valor válido.\n")
        else:
            print("Credenciais inválidas.")


