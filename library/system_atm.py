from library.data_base import Banco_de_Dados
from random import choice
import string, sys
import platform

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
        
    def verificarIdentificacao(self, identificacao, senha):
        if self.__identificacao == identificacao and self._Entidade__senha == senha:
            return True
        
        else:
            return False
    
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
    
    
    def atualizarContaTelefone(self, idConta, telefoneNovo):
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
        self.__bancoDados.verificarDepositoAgendadoDB(idConta)
        

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
        
        
    def limparTela(self):
        if platform.system() == 'Windows':
            print('\033[H\033[J')
        else:
            print('\033c', end='') 
        

    def pauseTela(self):
        print("\nPressione Enter para continuar...\n")
        input()
        
        
    def interface_Principal(self):
        while True:
            self.limparTela()
            
            print("====================Banco ATM====================\n")
            print("Bem-Vindo ao Banco ATM!\n")
            print("[1] Login\n")
            print("[2] Sair\n")
            opcao = input("Digite uma opção: ")
            print("=================================================\n")
            
            if opcao == "1":
                self.limparTela()
                print("====================Banco ATM====================\n")
                print("Login\n")
                idConta = input("Digite o ID do usuário: ")
                senha = input("Digite a Senha: ")
                print("=================================================\n")
                
                identificacao = idConta
                
                if self.banco_dados.verificarSenhaClienteDB(idConta, senha):
                    # Login do cliente bem-sucedido
                    self.interface_Cliente(idConta, senha)
                    break
                    
                elif self.verificarIdentificacaoGerente(identificacao, senha):
                    # Verificação da identificação do gerente
                    self.interface_Gerente()
                    break
                    
                else:   # Login falhou
                    self.limparTela()
                    print("Falha no login. Verifique o ID e a senha.\n")
                    self.pauseTela()
            
            
            elif opcao == "2":
                self.limparTela()
                print("Saindo do sistema...")
                print("Obrigado por utilizar o nosso Sistema ATM!\n")
                sys.exit()
                
                
            else:
                self.limparTela()
                print("Digite uma opção válida!")
                self.pauseTela()

                

    def verificarIdentificacaoGerente(self, identificacao, senha):
        return self.gerente.verificarIdentificacao(identificacao, senha)

    def interface_Gerente(self):

        while True:
                self.limparTela()
                print("====================Banco ATM====================\n")
                print("Selecione uma opção:\n")
                print("[1] Criar Conta\n")
                print("[2] Remover Conta\n")
                print("[3] Atualizar Conta\n")
                print("[4] Visualizar Conta\n")
                print("[5] Sair\n")
                print("=================================================\n")
    
                opcao = input("Digite o número da opção desejada: ")
    
                if opcao == "1":
                    self.limparTela()
                    self.criar_conta()
                    
    
                elif opcao == "2":
                    self.limparTela()
                    idConta = input("Digite o ID da conta a ser removida: ")
                    
                    if self.gerente.removerConta(idConta):
                        print("Conta removida com sucesso!")
                        self.pauseTela()
                        
                    else:
                        print("Não foi possível remover a conta.")
                        self.pauseTela()
                        
                    self.limparTela()
    
                elif opcao == "3":
                    self.limparTela()
                    idConta = input("Digite o ID da conta a ser atualizada: ")
                    
                    if self.banco_dados.verificarIdConta(idConta):
                        print("Selecione uma opção:\n")
                        print("[1] Atualizar nome\n")
                        print("[2] Atualizar endereço\n")
                        print("[3] Atualizar telefone\n")
    
                        sub_opcao = input("Digite o número da opção desejada: ")
    
                        if sub_opcao == "1":
                            self.limparTela()
                            novo_nome = input("Digite o novo nome: ")
                            
                            if self.gerente.atualizarContaNome(idConta, novo_nome):
                                print("Nome atualizado com Sucesso.")
                                self.pauseTela()
                                
                            else:
                                print("Não foi possivel atualizar o nome da conta.")
                                self.pauseTela()
                            
                            self.limparTela()
    
                        elif sub_opcao == "2":
                            self.limparTela()
                            novo_endereco = input("Digite o novo endereço: ")
                            
                            if self.gerente.atualizarContaEndereco(idConta, novo_endereco):
                                print("Endereço da conta atualizado com sucesso!")
                                self.pauseTela()
                                
                            else:
                                print("Não foi possível atualizar o endereço da conta.")
                                self.pauseTela()
                            
                            self.limparTela()
    
                        elif sub_opcao == "3":
                            self.limparTela()
                            novo_telefone = input("Digite o novo telefone: ")
                            
                            if self.gerente.atualizarContaTelefone(idConta, novo_telefone):
                                print("Telefone da conta atualizado com sucesso!")
                                self.pauseTela()
                                
                            else:
                                print("Não foi possível atualizar o telefone da conta.")
                                self.pauseTela()
                            
                            self.limparTela()
    
                        else:
                            self.limparTela()
                            print("Opção inválida.")
                            self.pauseTela()
    
                    else:
                        self.limparTela()
                        print("Conta Inválida.")
                        self.pauseTela()
                        
                    self.limparTela()
    
                elif opcao == "4":
                    self.limparTela()
                    idConta = input("Digite o ID da conta a ser visualizada: ")
                    
                    self.gerente.visualizarConta(idConta)
                    self.pauseTela()
    
                elif opcao == "5":
                    self.limparTela()
                    print("Voltando a Tela Inicial")
                    self.interface_Principal()  # Sai do loop e encerra o programa
    
                else:
                    self.limparTela()
                    print("Digite um valor válido.\n")
                    self.pauseTela()
                   
    
            
    
    def criar_conta(self):
        self.limparTela()
    
        print("====================Banco ATM====================\n")
        print("Digite os dados do cliente:\n")
    
        nome = input("Nome: ")
        cad_Pessoa = input("CPF/CNPJ: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        saldo = float(input("Saldo Inicial: "))
        senha = input("Senha com 6 dígitos: ")
        
        while len(senha) != 6:
            print("A senha precisa ter exatamente 6 dígitos.\n")
            senha = input("Senha com 6 dígitos: ")
    
        conta = self.gerente.criarConta(nome, senha, cad_Pessoa, endereco, telefone, saldo)
        if conta and saldo >= 0:
            print("Conta criada com sucesso!")
            print("ID da conta:", conta._idConta)
            self.pauseTela()
    
        else:
            print("Não foi possível criar a conta.")
            self.pauseTela()
    
        self.limparTela()


    
    def interface_Cliente(self, idConta, senha):
    
        if self.banco_dados.verificarSenhaClienteDB(idConta, senha):
            info = self.banco_dados.getConta(idConta)
            conta = Conta(info[0], info[1], info[2], info[3], info[4], info[5], info[6])
            
            while True:
                self.limparTela()
    
                print("====================Banco ATM====================\n")
                print("Selecione uma opção:\n")
                print("[1] Saque\n")
                print("[2] Depósito\n")
                print("[3] Pagamento Agendado\n")
                print("[4] Solicitar Crédito\n")
                print("[5] Extrato\n")
                print("[6] Sair\n")
                print("=================================================\n")
    
                opcao = input("Digite o número da opção desejada: ")
    
                if opcao == "1":
                    self.limparTela()
                    saldo = 0.0
                    saldo = self.banco_dados.getSaldoDB(idConta)
                    
                    print(f"Seu saldo atual é: R$ {saldo}")
                    valor = float(input("Digite o valor do saque: "))
                    
                    if conta.saque(valor, idConta):
                        print("Saque realizado com sucesso!")
                        self.pauseTela()
                        
                    else:
                        print("Não foi possível realizar o saque.")
                        self.pauseTela()
                    
                    self.limparTela()
    
                elif opcao == "2":
                    self.limparTela()
                    saldo = 0.0
                    saldo = self.banco_dados.getSaldoDB(idConta)
                    
                    print(f"Seu saldo atual é: R$ {saldo}")
                    valor = float(input("Digite o valor do depósito: "))
                    
                    if conta.deposito(valor, idConta):
                        print("Depósito realizado com sucesso!")
                        self.pauseTela()
                        
                    else:
                        print("Não foi possível realizar o depósito.")
                        self.pauseTela()
                    
                    self.limparTela()
    
                elif opcao == "3":
                    self.limparTela()
                    saldo = 0.0
                    saldo = self.banco_dados.getSaldoDB(idConta)
                    
                    print(f"Seu saldo atual é: R$ {saldo}")
                    valor = float(input("Digite o valor do pagamento: "))
                    data = input("Digite a data do pagamento (dd/mm/aaaa): ")
                    
                    if conta.pagamentoAgendado(valor, data, idConta):
                        print("Pagamento agendado com sucesso!")
                        self.pauseTela()
                        
                    else:
                        print("Não foi possível agendar o pagamento.")
                        self.pauseTela()
                        
                    self.limparTela()
    
                elif opcao == "4":
                    self.limparTela()
                    print("ATENÇÃO")
                    print("Total disponivel para solicitar crédito: ")
                    print("Pessoa Física: 25% do seu saldo atual.")
                    print("Pessoa Juridica: 50% do seu saldo atual.\n")
                    
                    saldo = 0.0
                    saldo = self.banco_dados.getSaldoDB(idConta)
                    
                    print(f"Seu saldo atual é: R$ {saldo}")
                    valor_credito = float(input("Digite o valor do crédito: "))
                    data_credito = input("Digite a data do crédito (dd/mm/aaaa): ")
                    
                    if conta.solicitarCredito(valor_credito, data_credito, idConta):
                        print("Crédito solicitado com sucesso!")
                        self.pauseTela()
                        
                    else:
                        print("Não foi possível solicitar o crédito.")
                        self.pauseTela()
                    
                    self.limparTela()
    
                elif opcao == "5":
                    self.limparTela()
                    conta.extrato(idConta)
                    self.pauseTela()
    
                elif opcao == "6":
                    self.limparTela()
                    print("Saindo do sistema...")
                    self.interface_Principal()
                    break  # Sai do loop e encerra o programa
    
                else:
                    self.limparTela()
                    print("Digite um valor válido.\n")
                    self.pauseTela()
                
                self.limparTela()
    
        else:
            self.limparTela()
            print("Credenciais inválidas.")
            self.pauseTela()   
 