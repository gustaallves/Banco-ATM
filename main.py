from library.data_base import Banco_de_Dados
from library.system_atm import Sistema, Gerente

def workspace():
    
    banco_dados = Banco_de_Dados()
    gerente = Gerente("Mestre", "123456", "0001", "111.222.333-44")
    
    sistema = Sistema(banco_dados, gerente)
    sistema.interface_Principal()


if __name__ == "__main__":
    workspace()

