from library.system_atm import Gerente, Conta
from library.data_base import Banco_de_Dados

def workspace():
    gerente = Gerente("Matheus", "150226", "0001", "15165156")
    
    contaCarlos = gerente.criarConta("CArlos", "1234", "141562185", "Lugar", "9999999", 10000)
    contaJoao = gerente.criarConta("Joao", "senha", "cad_Pessoa", "endereco", "telefone", 1500)
    banco = Banco_de_Dados()
    
    banco.saqueDB(500, contaCarlos._idConta)
    banco.depositoDB(550.50, contaCarlos._idConta)
    banco.extratoDB(contaCarlos._idConta)
    
    banco.visualizarClientesDB()
    
    banco.atualizarContaNomeDB("CArlos", "Flavio")
    
    banco.visualizarClientesDB()

if __name__ == "__main__":
    workspace()

