import os
import json
import string
import platform
import datetime as dt
from pathlib import Path
from random import choice


class Banco_de_Dados:
    
    diretorio_atual = os.getcwd()
    so = platform.system()
    
    if so == "Windows":
        caminho_featuresJson = str(diretorio_atual + "\\data base\\features.json")
        caminho_extratos = str(diretorio_atual + "\\data base\\extratos")
        caminho_Json = str(diretorio_atual + "\\data base\\users.json")
        caminho_idContas = str(diretorio_atual + "\\data base\\idContas.json")
    
    else:
        caminho_featuresJson = str(diretorio_atual + "//data base//features.json")
        caminho_extratos = str(diretorio_atual + "//data base//extratos")
        caminho_Json = str(diretorio_atual + "//data base//users.json")
        caminho_idContas = str(diretorio_atual + "//data base//idContas.json")
    
    __usersJson = caminho_Json
    __bankHistory = caminho_extratos
    __bankFeatures = caminho_featuresJson
    __idContasJson = caminho_idContas
    
    
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
        
        try:
            with open(self.__idContasJson) as ids:
                self.__idContasList = json.load(ids)
                
        except Exception:
            return None
        
   
    def abrirDiretorioUsuarios(self, diretorio):
        with open(diretorio) as fp:
            self.__usersList = json.load(fp)
    
    
    def atualizarJson(self, diretorio, arquivo):
        with open(diretorio, "w") as fp:
            json.dump(arquivo, fp, indent=4)
            return True
            
        
    def atualizarAtributoJson(self, idConta, campoJson, atributoNovo):
        self.atualizarDB()

        encontrado = False  # Variável de controle
    
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                user[campoJson] = atributoNovo
                encontrado = True
                break
    
        if not encontrado:
            print("Usuário não encontrado.")
            return False
    
        self.atualizarJson(self.__usersJson, self.__usersList)
        return True
        
        
    
    def criarContaDB(self, conta):
        self.atualizarDB()
        nomeArq = conta._idConta + ".txt"
        
        try:
            arqExtrato = open(Path(self.__bankHistory,nomeArq), "w")
            arqExtrato.write("==="*15 + "\n")
            arqExtrato.write(f"{conta.getNome()} - {conta._idConta}\n")
            arqExtrato.write("==="*15 + "\n")
            arqExtrato.write(f"Saldo: R$ {conta._saldo:.2f}\n")
            arqExtrato.write("==="*15 + "\n")
            
        except FileNotFoundError:
            return False
        
        converterUsers = vars(conta)
        
        self.__usersList.append(converterUsers)
        self.__usersList.sort(key=lambda x: x.get("_Entidade__nome"))
        
        self.atualizarJson(self.__usersJson, self.__usersList)
        return True
    
    
    def excluirContaDB(self, idConta):
        self.atualizarDB()
        encontrado = False
        
        for i in reversed(range(len(self.__usersList))):
            if (not self.__usersList):
                print("Não possui clientes disponíveis.")
            
            elif self.__usersList[i]["_idConta"] == idConta and self.__usersList[i]["_saldo"] == 0:
                    nomeArq = idConta + ".txt"
                    arqExtrato = Path(self.__bankHistory, nomeArq)
                    os.remove(arqExtrato)

                    self.excluirFeatures(idConta, "valorDeposito")
                    self.excluirFeatures(idConta, "valorPagamento")
                    
                    self.__usersList.pop(i)
                    self.removerID(idConta)
                    encontrado = True
                    
            else:
                print("Usuario não possui saldo zerado, impossivel remover.")
                return False
            
        if not encontrado:
            print("Usuário não encontrado.")
            return False
        
        self.atualizarJson(self.__usersJson, self.__usersList)
        return encontrado
            
    
    def visualizarClientesDB(self):
        self.atualizarDB()
        
        if (not self.__usersList):
            print("Não possui clientes disponíveis para visualizar.")
            return False
        
        else:
            print("==="*13)
            print("  "*5 + "Clientes Disponíveis" )
            for i in range(len(self.__usersList)):
                print("-",self.__usersList[i]["_Entidade__nome"]) 
            print("==="*13)
            return True
        
            
    def atualizarContaNomeDB(self, idConta, nomeNovo):
        return self.atualizarAtributoJson(idConta, "_Entidade__nome", nomeNovo)
                  
                
    def atualizarContaEnderecoDB(self, idConta, enderecoNovo):
        return self.atualizarAtributoJson(idConta, "_Cliente__endereco", enderecoNovo)
                
                
    def atualizarContaTelefoneDB(self, idConta, telefoneNovo):
        return self.atualizarAtributoJson(idConta, "_Cliente__telefone", telefoneNovo)
    
    
    def atualizarContaSaldoDB(self, idConta, valor):
        self.atualizarDB()

        for user in self.__usersList:
            if user["_idConta"] == idConta:
                user["_saldo"] = user["_saldo"] + valor
                break
        else:
            print("Usuário não encontrado.")
            return False
    
        self.atualizarJson(self.__usersJson, self.__usersList)
        return True
                       
    
    def visualizarContaDB(self, idConta):
        self.atualizarDB()
        
        for i in range(len(self.__usersList)):
           if self.__usersList[i]["_idConta"] == idConta:
               print("==="*13)
               print("Nome:", self.__usersList[i]["_Entidade__nome"])
               print("CPF/CNPJ:", self.__usersList[i]["_Entidade__cad_Pessoa"])
               print("Endereço:", self.__usersList[i]["_Cliente__endereco"])
               print("Telefone:", self.__usersList[i]["_Cliente__telefone"])
               print("Conta:", self.__usersList[i]["_idConta"])
               print("Saldo: R$", round(self.__usersList[i]["_saldo"], 2))
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
        self.atualizarDB()
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        saldoAtual = 0.0
        
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                if (user["_saldo"] >= valorSaque):
                    try:
                        arqExtrato = open(Path(self.__bankHistory, (idConta + ".txt")), "a")
                        self.atualizarContaSaldoDB(idConta, -float((abs(valorSaque))))
                        
                    except FileNotFoundError:
                        return False
                    
                else:
                    print("Saldo insuficiente.\n")
                    return False
                
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                saldoAtual = round(user["_saldo"], 2) 
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"- {valorSaque}\n")
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Saldo: R$ {saldoAtual:.2f}\n")
        
        arqExtrato.close()
        return True
    
    
    def depositoDB(self, valorDeposito, idConta):
        self.atualizarDB()
        dataAtualF = self.dataAtualDB()
        horaAtual = self.horaAtualDB()
        saldoAtual = 0.0
        
        try:
            arqExtrato = open(Path(self.__bankHistory, (idConta + ".txt")), "a")
            self.atualizarContaSaldoDB(idConta, +float(abs(valorDeposito)))
            
        except FileNotFoundError:
            return False
        
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                saldoAtual = round(user["_saldo"], 2) 
        
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Data: {dataAtualF}   -   {horaAtual}\n")
        arqExtrato.write(f"+ {valorDeposito}\n")
        arqExtrato.write("==="*15 + "\n")
        arqExtrato.write(f"Saldo: R$ {saldoAtual:.2f}\n")
        
        arqExtrato.close()
        return True
    
    
    def excluirFeatures(self, idConta, tipoFeature):
        self.atualizarDB()
        
        with open(self.__bankFeatures, "r") as fp:
            self.__featuresLists = json.load(fp)
        
        encontrado = False
        for i in reversed(range(len(self.__featuresLists))):
            if (not self.__featuresLists):
                print("Não possui clientes disponíveis.")
            
            elif self.__featuresLists[i]["_idConta"] == idConta and tipoFeature == "valorDeposito":
                if "valorDeposito" in self.__featuresLists[i]:
                    self.__featuresLists.pop(i)
                    encontrado = True
                    break
            
            elif self.__featuresLists[i]["_idConta"] == idConta and tipoFeature == "valorPagamento":
                if "valorPagamento" in self.__featuresLists[i]:
                    self.__featuresLists.pop(i)
                    encontrado = True
                    break
            
        if not encontrado:
            return False
        
        self.atualizarJson(self.__bankFeatures, self.__featuresLists)
        return encontrado
    
    
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
        encontrado = False
    
        if not self.__featuresLists:
            return False
    
        else:
            for user in reversed(self.__featuresLists):
                if user["_idConta"] == idConta:
                    if "dataPagamento" in user and user["dataPagamento"] == dataAtualF:
                        valor = user["valorPagamento"]
                        self.saqueDB(valor, idConta)
                        self.excluirFeatures(idConta, "valorPagamento")
                        encontrado = True
    
        return encontrado
    
    
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
        
        deposito = {"_idConta": idConta,"valorDeposito": valor ,"dataDeposito": data_formatada}
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
        encontrado = False

    
        if not self.__featuresLists:
            return False
    
        else:
            for user in reversed(self.__featuresLists):
                if user["_idConta"] == idConta:
                    if "dataDeposito" in user and user["dataDeposito"] == dataAtualF:
                        valor = user["valorDeposito"]
                        self.depositoDB(valor, idConta)
                        self.excluirFeatures(idConta, "valorDeposito")
                        encontrado = True
    
        return encontrado
    
    def solicitarCreditoDB(self, valor, data, idConta):
        self.atualizarDB()
        
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                if len(user["_Entidade__cad_Pessoa"]) == 11:  # CPF
                    if valor <= (user["_saldo"] * 0.25):
                        self.depositoAgendadoDB(valor, data, idConta)
                        return True
                    
                    else:
                        return False
                    
                else:  # CNPJ
                    if valor <= (user["_saldo"] * 0.5):
                        self.depositoAgendadoDB(valor, data, idConta)
                        return True
                        
                    else:
                        return False

                 
    def verificarSenhaClienteDB(self, idConta, senha):
        self.atualizarDB()
            
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                if user["_Entidade__senha"] == senha:
                    return True
        
        self.atualizarJson(self.__usersJson, self.__usersList)        
        
        return False

    
    def getSaldoDB(self, idConta):
        saldo = 0.0
        
        self.atualizarDB()

        for user in self.__usersList:
            if user["_idConta"] == idConta:
                saldo = user["_saldo"]
                break
    
        self.atualizarJson(self.__usersJson, self.__usersList)
                
        return saldo
        
                
                
    def getConta(self, idConta):
        self.atualizarDB()
        
        informacoes = []
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                informacoes.append(user["_Entidade__nome"])
                informacoes.append(user["_Entidade__senha"])
                informacoes.append(user["_Entidade__cad_Pessoa"])
                informacoes.append(user["_Cliente__endereco"])
                informacoes.append(user["_Cliente__telefone"])
                informacoes.append(user["_idConta"])
                informacoes.append(user["_saldo"])
                
        return informacoes
    
    
    def verificarIdConta(self, idConta):
        self.atualizarDB()
            
        for user in self.__usersList:
            if user["_idConta"] == idConta:
                return True
                break
            
        else:
            return False
        
        
    def atualizarDB(self):
        with open(self.__usersJson, "r") as usersFile:
            self.__usersList = json.load(usersFile)
    
    
    def gerarID(self):
        with open(self.__idContasJson, "r") as cl:
            self.__idContasList = json.load(cl)
            
        numbers = string.digits
        randomNumber = "".join(choice(numbers) for _ in range(4))
        
        for user in self.__idContasList:
            if user["idConta"] == randomNumber:
                return self.gerarID()
        
        else:
            idGerado = {"idConta": randomNumber}
            self.__idContasList.append(idGerado)
            self.__idContasList.sort(key=lambda x: x.get("idConta"))
            
            try:
                with open(self.__idContasJson, "w") as fp:
                    json.dump(self.__idContasList, fp, indent=4)
                    return randomNumber
                
            except Exception:
                return False
            
            
    def removerID(self, idConta):
        encontrado = False
        with open(self.__idContasJson, "r") as cl:
            self.__idContasList = json.load(cl)
        
        for i in reversed(range(len(self.__idContasList))):
            if (not self.__idContasList):
                print("Não possui clientes disponíveis.")
            
            elif self.__idContasList[i]["idConta"] == idConta:
                self.__idContasList.pop(i)
                encontrado = True
                break
            
        if not encontrado:
            return False
        
        self.atualizarJson(self.__idContasJson, self.__idContasList)
        return encontrado
