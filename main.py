from library.system_atm import Gerente

def workspace():
    gerente = Gerente("Nome", "151520", "10001", "0787")
       
    if(gerente.removerConta("Ana")):
        print("Remoção feita com sucesso")
    else:
        print("Falha ao remover")
    
    print("\n")
    
    gerente.visualizarConta("Ana")

if __name__ == "__main__":
    workspace()

