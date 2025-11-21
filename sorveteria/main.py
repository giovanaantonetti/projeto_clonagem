from controllers.sistema import Sistema

def main():
    sistema = Sistema()
    while True:
        print("#### Sistema do Mercado ####")
        print("[1] - Gerenciar produtos (adicionar / listar)")
        print("[2] - Abrir caixa e iniciar atendimento")
        print("[3] - Fechar programa")
        opc = input("Escolha uma opção: ")
        if opc == "1":
            sistema.menu_gerenciar_produtos()
        elif opc == "2":
            sistema.abrir_caixa_e_atender()
        elif opc == "3":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main()            