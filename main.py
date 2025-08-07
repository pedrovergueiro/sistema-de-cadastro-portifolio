from database import criar_tabela
from produtos import cadastrar_produtos, listar_produtos, excluir_produto

def menu():
    criar_tabela()
    while True:
        print("\n1 - Cadastrar")
        print("2 - Listar")
        print("3 - Excluir")
        print("4 - Sair")
        op = input("Escolha: ")
        if op == '1':
            cadastrar_produtos()
        elif op == '2':
            listar_produtos()
        elif op == '3':
            excluir_produto()
        elif op == '4':
            break
        else:
            print("Opção inválida")

menu()
