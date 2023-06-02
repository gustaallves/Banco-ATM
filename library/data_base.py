import os
import json
import datetime as dt
from pathlib import Path

class Banco_de_Dados:
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    caminho_featuresJson = os.path.join(diretorio_atual, "Projeto ATM", "data base", "features.json")
    caminho_extratos = os.path.join(diretorio_atual, "Projeto ATM", "data base", "extratos")
    caminho_Json = os.path.join(diretorio_atual, "Projeto ATM", "data base", "users.json")
    
    __usersJson = caminho_Json
    __bankHistory = caminho_extratos
    __bankFeatures = caminho_featuresJson
    
    def __init__(self):
        try:
            with open(self.__usersJson) as fp:
                self.__usersList = json.load(fp)
                
        except Exception:
            return None
        
        try:
            with open(self.__bankFeatures) as bd:
                self.__featuresLists = json.load(bd)
        
        except Exception:
            return None
   
    def abrirDiretorioUsuarios(self, diretorio):
        with open(diretorio) as fp:
            self.__usersList = json.load(fp)
    
    def atualizarJson(self, diretorio, arquivo):
        try:
            with open(diretorio, "w") as fp:
                json.dump(arquivo, fp, indent=4)
                return True
            
        except Exception:
            return False 
        
    def atualizarAtributoJson(self, idConta, campoJson, atributoNovo):
        with open(self.__usersJson, "r") as usersFile:
            self.__usersList = json.load(usersFile)

        for user in self.__usersList:
            if user["_idConta"] == idConta:
                user[campoJson] = atributoNovo
                break
        else:
            print("Usuário não encontrado.")
            return False
        
        self.atualizarJson(self.__usersJson, self.__usersList)
        
    
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
    
    
    def excluirContaDB(self, idConta):
        for i in range(len(self.__usersList)):
            if self.__usersList[i]["_idConta"] == idConta:
                try:
                    self.__usersList.pop(i)
                except IndexError:
                    return False
                
                return self.atualizarJson(self.__usersJson, self.__usersList)
            
    
    def visualizarClientesDB(self):
        if (not self.__usersList):
            print("Não possui clientes disponíveis para visualizar.")
            return False
        
        else:
            print("==="*13)
            print("  "*5 + "Clientes Disponíveis" )
            for i in range(len(self.__usersList)):
                print("-",self.__usersList[i]["_Entidade__nome"]) 
            print("==="*13)
        
            
    def atualizarContaNomeDB(self, idConta, nomeNovo):
        return self.atualizarAtributoJson(idConta, "_Entidade__nome", nomeNovo)
                  
                
    def atualizarContaEnderecoDB(self, idConta, enderecoNovo):
        return self.atualizarAtributoJson(idConta, "_Cliente__endereco", enderecoNovo)
                
                
    def atualizarContaTelefoneDB(self, idConta, telefoneNovo):
        return self.atualizarAtributoJson(idConta, "_Cliente__telefone", telefoneNovo)
    
    def atualizarContaSaldoDB(self, idConta, valor):
        with open(self.__usersJson, "r") as usersFile:
            self.__usersList = json.load(usersFile)

        for user in self.__usersList:
            if user["_idConta"] == idConta:
                user["_saldo"] = user["_saldo"] + valor
                break
        else:
            print("Usuário não encontrado.")
            return False
    
        return self.atualizarJson(self.__usersJson, self.__usersList)
                       
    
    def visualizarContaDB(self, idConta):
       for i in range(len(self.__usersList)):
           if self.__usersList[i]["_idConta"] == idConta:
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
   
    def saqueDB(self, valorSaque, idConta):
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        saldoAtual = 0.0
        
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                if (user["_saldo"] >= valorSaque):
                    try:
                        arqExtrato = open(Path(self.__bankHistory, (idConta + ".txt")), "a")
                        self.atualizarContaSaldoDB(idConta, -float((abs(valorSaque))))
                        saldoAtual = user["_saldo"]
                        
                    except FileNotFoundError:
                        return False
                else:
                    print("impossivel sacar.\n")
                    return False
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"- {valorSaque}\n")
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Saldo Atual: R$ {saldoAtual:.2}\n")
        
        arqExtrato.close()
        return True
    
    
    def depositoDB(self, valorDeposito, idConta):
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (idConta + ".txt")), "a")
            self.atualizarContaSaldoDB(idConta, abs(valorDeposito))
            
        except FileNotFoundError:
            return False
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"+ {valorDeposito}\n")
        arqExtrato.write("==="*15 + "\n")
        
        arqExtrato.close()
        return True
    
    # A DATA DEVE SER DIGITADA ASSIM: (dd/mm/aaaa)
    def pagamentoAgendadoDB(self, valor, data, idConta):
        data_obj = dt.datetime.strptime(data, "%d/%m/%Y").date()

        data_formatada = data_obj.strftime("%d/%m/%Y")
        
        pagamento = {"_idConta": idConta,"valorPagamento": valor ,"dataPagamento": data_formatada}
        self.__featuresLists.append(pagamento)
        self.__featuresLists.sort(key=lambda x: x.get("_idConta"))
        
        try:
            with open(self.__bankFeatures, "w") as fp:
                json.dump(self.__featuresLists, fp, indent=4)
                return True
            
        except Exception:
            return False 
        
    
    def verificarPagamentoAgendadoDB(self, idConta):
        dataAtualF = self.dataAtualDB()
        
        for user in self.__featuresLists:
            if user["_idConta"] == idConta:
                if user["dataPagamento"] == dataAtualF:
                    valor = user["valorPagamento"]
                    self.saqueDB(valor, idConta)
                    return True
                
        return False
    
    
    def extratoDB(self, idConta):
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (idConta + ".txt")), "r")
            extrato = arqExtrato.read()
            print(extrato)
            
        except FileNotFoundError:
            return False


    def depositoAgendadoDB(self, valor, data, idConta):
        data_obj = dt.datetime.strptime(data, "%d/%m/%Y").date()

        data_formatada = data_obj.strftime("%d/%m/%Y")
        
        deposito = {"_idConta": idConta,"valorPagamento": valor ,"dataPagamento": data_formatada}
        self.__featuresLists.append(deposito)
        self.__featuresLists.sort(key=lambda x: x.get("_idConta"))
        
        try:
            with open(self.__bankFeatures, "w") as fp:
                json.dump(self.__featuresLists, fp, indent=4)
                return True
            
        except Exception:
            return False 
        
        
    def verificarDepositoAgendadoDB(self, idConta):
        dataAtualF = self.dataAtualDB()
        
        for user in self.__featuresLists:
            if user["_idConta"] == idConta:
                if user["dataPagamento"] == dataAtualF:
                    valor = user["valorPagamento"]
                    self.depositoDB(valor, idConta)
                    return True
                
        return False 
    
    
    def solicitarCreditoDB(self, valor, data, idConta):
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                if len(user["_Entidade__cad_Pessoa"] == 11): #CPF
                    if valor <= (user["_saldo"]*0.25):
                        self.depositoAgendadoDB(valor, data, idConta)
                
                else:                                        #CNPJ
                    if valor <= (user["_saldo"]*0.5):
                        self.depositoAgendadoDB(valor, data, idConta)
