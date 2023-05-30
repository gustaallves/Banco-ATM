from library.system_atm import Gerente

def workspace():
    gerente = Gerente("Gustavo", "151520", "10001", "0787")
       
#    if(gerente.removerConta("Ana")):
 #       print("Remoção feita com sucesso")
  #  else:
   #     print("Falha ao remover")
    
   # print("\n")
    conta = gerente.criarConta('Ana', 12345, 57629002106, 'Quadra', 61981297731, 1000.00)
    print(conta.saque(500.00))
    print(conta.deposito(200.00))
    print(conta.extrato())
    print(conta.solicitarCredito(1000.00))
    
    
   # print(gerente.visualizarConta("Ana"))
    
            
    

if __name__ == "__main__":
    workspace()

