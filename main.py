from library.system_atm import Gerente
from library.data_base import Banco_de_Dados
from library.system_atm import Sistema


def workspace():
    
    banco_dados = Banco_de_Dados()
    gerente = Gerente("Gustavo", "123456", "789456", "07629002106")

    sistema = Sistema(banco_dados, gerente)
    

if __name__ == "__main__":
    workspace()

