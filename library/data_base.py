import json, os

class Banco_de_Dados:
    
    usersJson = "C:/Users/gugu8/Projeto_ATM/Projeto-ATM/data base/users.json"
    bankHistoryJson = "C:/Users/gugu8/Projeto_ATM/Projeto-ATM/data base/extrato.txt"
    
    def __init__(self):
       self.usersList = []
    
   
    def abrirDiretorioUsuarios(self, diretorio):
        with open(diretorio) as fp:
            self.usersList = json.load(fp)
    
    def atualizarJson(self, diretorio, alvo):
        try:
            with open(diretorio, "w") as fp:
                json.dump(alvo, fp, indent=4)
        except Exception:
            return False
        return True
    
    def criarContaDB(self, conta):
        converterUsers = vars(conta)
        
        self.usersList.append(converterUsers)
        self.usersList.sort(key=lambda x: x.get("nome"))
        
        return self.atualizarJson(self.usersJson, self.usersList)
    
    
    def excluirContaDB(self, nome):
        for i in range(len(self.usersList)):
            if self.usersList[i]["nome"] == nome: #Alterar para idConta
                try:
                    self.usersList.pop(i)
                except IndexError:
                    return False
                
                return self.atualizarJson(self.usersJson, self.usersList)
            
    
    def visualizarClientesDB(self):
        if not self.usersList:
            print("Não possui clientes disponíveis para visualizar.")
            return False
        print("==="*13)
        print("  "*5 + "Clientes Disponíveis" )
        for i in range(len(self.usersList)):
            print("",self.usersList[i]["nome"]) 
        print("==="*13)
        
            
    def atualizarContaNomeDB(self, nomeAntigo, nomeNovo):
        for i in range(len(self.usersList)):
            if self.usersList[i]["nome"] == nomeAntigo:
                self.usersList[i]["nome"] = nomeNovo
                return True
        print("Usuario não encontrado.")
        return False
                  
                
    def atualizarContaEnderecoDB(self, nome, enderecoNovo):
        for i in range(len(self.usersList)):
            if self.usersList[i]["nome"] == nome:
                self.usersList[i]["endereco"] = enderecoNovo
                return True
        print("Usuario não encontrado.")
        return False
                
                
    def atualizarContaTelefoneDB(self, nome, telefoneNovo):
        for i in range(len(self.usersList)):
            if self.usersList[i]["nome"] == nome:
                self.usersList[i]["telefone"] = telefoneNovo
                return True
        print("Usuario não encontrado.")
        return False
                       
    
    def visualizarContaDB(self, nome):
       for i in range(len(self.usersList)):
           if self.usersList[i]["nome"] == nome:
               print("==="*13)
               print("Nome:", self.usersList[i]["nome"])
               print("CPF/CNPJ:", self.usersList[i]["cad_Pessoa"])
               print("Endereço:", self.usersList[i]["endereco"])
               print("Telefone:", self.usersList[i]["telefone"])
               print("Conta:", self.usersList[i]["idConta"])
               print("Saldo:", self.usersList[i]["_saldo"])
               print("==="*13)
               return True
           
       print("Conta não encontrada")
       return False
   
    
   
    def saqueDB(self):
        pass
    
    
    def depositoDB(self):
        pass
    
    
    def pagamentoAgendadoDB(self):
        pass
    
    
    def extratoDB(self):
        pass
    
    
    def solicitarCreditoDB(self):
        pass

