import json
import datetime as dt
from pathlib import Path

class Banco_de_Dados:
    
    __usersJson = "C:\\Users\\mathe\\UnB_POO\\Projeto ATM\\data base\\users.json"
    __bankHistory = "C:\\Users\\mathe\\UnB_POO\\Projeto ATM\\data base\\extratos\\"
    
    def __init__(self):
       self.__usersList = []
    
   
    def abrirDiretorioUsuarios(self, diretorio):
        with open(diretorio) as fp:
            self.__usersList = json.load(fp)
    
    def atualizarJson(self, diretorio, alvo):
        try:
            with open(diretorio, "w") as fp:
                json.dump(alvo, fp, indent=4)
                
        except Exception:
            return False
        
        return True
    
    def criarContaDB(self, conta):
        nomeArq = conta._idConta + ".txt"
        
        try:
            arqExtrato = open(Path(self.__bankHistory,nomeArq), "w")
            arqExtrato.write("==="*15 + "\n")
            arqExtrato.write(f"{conta.getNome()} - {conta._idConta}\n")
            arqExtrato.write("==="*15 + "\n")
            
        except FileNotFoundError:
            return False
        
        converterUsers = vars(conta)
        
        self.__usersList.append(converterUsers)
        self.__usersList.sort(key=lambda x: x.get("_Entidade__nome"))
        
        return self.atualizarJson(self.__usersJson, self.__usersList)
    
    
    def excluirContaDB(self, nome):
        for i in range(len(self.__usersList)):
            if self.__usersList[i]["_Entidade__nome"] == nome: #Alterar para idConta
                try:
                    self.__usersList.pop(i)
                except IndexError:
                    return False
                
                return self.atualizarJson(self.__usersJson, self.__usersList)
            
    
    def visualizarClientesDB(self):
        if not self.__usersList:
            print("Não possui clientes disponíveis para visualizar.")
            return False
        
        print("==="*13)
        print("  "*5 + "Clientes Disponíveis" )
        for i in range(len(self.__usersList)):
            print("",self.__usersList[i]["_Entidade__nome"]) 
        print("==="*13)
        
            
    def atualizarContaNomeDB(self, nomeAntigo, nomeNovo):
        with open(self.__usersJson, "r") as usersFile:
            self.__usersList = json.load(usersFile)

        for user in self.__usersList:
            if user["_Entidade__nome"] == nomeAntigo:
                user["_Entidade__nome"] = nomeNovo
                break
        else:
            print("Usuário não encontrado.")
            return False
    
        with open(self.__usersJson, "w") as updateFile:
            json.dump(self.__usersList, updateFile, indent=4)
                  
                
    def atualizarContaEnderecoDB(self, nome, enderecoNovo):
        for i in range(len(self.__usersList)):
            if self.__usersList[i]["_Entidade__nome"] == nome:
                self.__usersList[i]["_Cliente__endereco"] = enderecoNovo
                return True
        print("Usuario não encontrado.")
        return False
                
                
    def atualizarContaTelefoneDB(self, nome, telefoneNovo):
        for i in range(len(self.__usersList)):
            if self.__usersList[i]["_Entidade__nome"] == nome:
                self.__usersList[i]["_Cliente__telefone"] = telefoneNovo
                return True
        print("Usuario não encontrado.")
        return False
    
    def atualizarContaSaldoDB(self, idConta, valor):
        for i in range(len(self.__usersList)):
            if self.__usersList[i]["_idConta"] == idConta:
                self.__usersList[i]["_saldo"] += valor
                return True
        return False
                       
    
    def visualizarContaDB(self, nome):
       for i in range(len(self.__usersList)):
           if self.__usersList[i]["_Entidade__nome"] == nome:
               print("==="*13)
               print("Nome:", self.__usersList[i]["_Entidade__nome"])
               print("CPF/CNPJ:", self.__usersList[i]["_Entidade__cad_Pessoa"])
               print("Endereço:", self.__usersList[i]["_Cliente__endereco"])
               print("Telefone:", self.__usersList[i]["_Cliente__telefone"])
               print("Conta:", self.__usersList[i]["_idConta"])
               print("Saldo:", self.__usersList[i]["_saldo"])
               print("==="*13)
               return True
           
       print("Conta não encontrada")
       return False
   
    
    def dataAtualDB(self):
        data = dt.date.today()
        return data.strftime("%d/%m/%Y")
    
    
    def horaAtualDB(self):
        hora = dt.datetime.now()
        return hora.strftime("%H:%M:%S")
   
    def saqueDB(self, valorSaque, conta):
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (conta + ".txt")), "a")
            self.atualizarContaSaldoDB(conta, valorSaque)
            
        except FileNotFoundError:
            return False
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"- {valorSaque}\n")
        arqExtrato.write("==="*15 + "\n")
        
        arqExtrato.close()
        return True
    
    
    def depositoDB(self, valorDeposito, conta):
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (conta + ".txt")), "a")
            self.atualizarContaSaldoDB(conta, valorDeposito)
            
        except FileNotFoundError:
            return False
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"+ {valorDeposito}\n")
        arqExtrato.write("==="*15 + "\n")
        
        arqExtrato.close()
        return True
    
    
    def pagamentoAgendadoDB(self):
        pass
    
    
    def extratoDB(self, conta):
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (conta + ".txt")), "r")
            extrato = arqExtrato.read()
            print(extrato)
            
        except FileNotFoundError:
            return False

    
    def solicitarCreditoDB(self):
        pass

