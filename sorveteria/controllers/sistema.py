import datetime
from models.produto import Produto
from models.carrinho import Carrinho
from models.pagamento import Pagamento
from models.caixa import Caixa

class Sistema:
    def __init__(self):
        self.produtos: list[Produto] = [
            Produto(1, "Sorvete de flocos 1,5L", 15.00, estoque=10),
            Produto(2, "Sorvete Napolitano 3L", 38.00, estoque=10),
            Produto(3, "Sorvete Caramelo com sal Marinho 2L", 30.00, estoque=10),
            Produto(4, "Sorvete de Uva 2,5L", 28.00, estoque=10),
            Produto(5, "Sorvete Chocolate com Amendoim 3,5L", 35.90, estoque=10)
        ]
        self.caixa = Caixa()
        self._proximo_codigo = len(self.produtos) + 1

    # Funções administrativas
    def menu_gerenciar_produtos(self):
        while True:
            print("#### Gerenciar produtos ####")
            print("[1] - Listar produtos")
            print("[2] - Adicionar produto")
            print("[3] - Ajustar estoque de um produto")
            print("[0] - Voltar")
            opc = input("Escolha uma opção: ")

            if opc == "1":
                self.listar_produtos()
            elif opc == "2":
                self.adicionar_produto_interativo()
            elif opc == "3":
                self.ajustar_estoque_interativo()
            elif opc == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def listar_produtos(self):
        print("#### Produtos ####")
        for p in self.produtos:
            print(p)   

    def adicionar_produto_interativo(self):
        '''Permite adicionar um novo produto via entrada do usuário'''
        try:
            nome = input("Nome do produto: ")
            preco = float(input("Preço unitário (ex: 14.50): "))
            estoque = int(input("Quantidade inicial em estoque: "))
            novo = Produto(self._proximo_codigo, nome, preco, estoque=estoque)
            self.produtos.append(novo)
            self._proximo_codigo += 1
            print(f"Produto '{nome}' adicionado com código {novo.codigo}.")
        except ValueError:
            print("Entrada inválida. Use valores numéricos para preço e estoque")

    def ajustar_estoque_interativo(self):
        '''Ajustar o estoque de um produto existente'''
        try:
            codigo = int(input("Informe o código do produto: ")) 
            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if produto is None:
                print("Produto não encontrado.")
                return
            novo_estoque = int(input(f"Novo estoque para '{produto.nome}': "))
            produto.atualizar_estoque(novo_estoque)
            print(f"Estoque de '{produto.nome}' atualizado para {produto.estoque}")
        except ValueError:
            print("Entrada inválida. Use números inteiros para código/estoque")

    def abrir_caixa_e_atender(self):
        '''Inicia o ciclo de atendimento ao cliente, que pode ser repetido 
        até que o usuário opte por fechar o caixa'''
        print("#### Caixa aberto: Iniciando atendimento ####")
        while True:
            print("[1] - Atender próximo cliente")
            print("[2] - Fechar caixa e gerar relatório diário")
            opc = input("Escolha uma opção: ")
            if opc == "1":
                self.processo_compra()
            elif opc == "2":
                print("Fechando caixa...") 
                self.fechamento_dia()
                break
            else:
                print("Opção inválida. Digite 1 ou 2.")

    def exibir_menu_produtos(self):
        '''Exibe o catálogo de produtos com indices para seleção'''
        print("#### Produtos disponíveis ####") 
        for idx, produto in enumerate(self.produtos, start=1):
            print(f"[{idx}] {produto}")
        print("[0] - Remover item do carrinho")    
        print("[9] - Finalizar compra")

    def escolher_produto(self, opcao: int):
        '''Retorna o produto correspondente ao índice do menu'''
        if 1 <= opcao <= len(self.produtos):
            return self.produtos[opcao - 1]
        return None

    # Continuamos amanhã......    
    def processo_compra(self):
        '''Gerencia o fluxo de compra para um único cliente, 
        do carrinho ao pagamento'''
        carrinho = Carrinho()
        while True:
            self.exibir_menu_produtos()
            try:
                opcao = int(input("Escolha uma opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue
            if opcao == 9:
                if carrinho.vazio():
                    print("O carrinho está vazio")
                    continue
                else:
                    break
            elif opcao == 0:
                self.remover_do_carrinho(carrinho)
                continue
            produto = self.escolher_produto(opcao)
            if produto:
                try:
                    qtd = int(input(f"Quantos '{produto.nome}' deseja adicionar: "))
                    carrinho.adicionar(produto, qtd)
                    print(f"{qtd}x '{produto.nome}' adicionado ao carrinho")
                except ValueError as e:
                    print(e)
            else:
                print("Opção inválida")
        self.finalizar_compra(carrinho)

    def remover_do_carrinho(self, carrinho: Carrinho):
        '''Permite ao cliente remover itens já adicionados ao carrinho'''
        if carrinho.vazio():
            print("O carrinho está vazio, não há itens para remover")
            return
        print("#### Itens no carrinho ####") 
        itens = list(carrinho.listar_itens())
        for idx, (produto, qtd) in enumerate(itens, start=1):
            print(f"[{idx}] {produto.nome} - {qtd} unidade(s)")

        try:
            opcao = int(input("Escolha um item que deseja remover: "))
            if 1 <= opcao <= len(itens):
                produto, _ = itens[opcao - 1]
                qtd_remover = int(input(f"Quantas unidades de '{produto.nome}' deseja remover: "))
                if qtd_remover > 0:
                    carrinho.remover(produto, qtd_remover)
                    print(f"{qtd_remover}x '{produto.nome}' removido do carrinho")
                else:
                    print("Quantidade inválida")
            else:
                print("Opção inválida")
        except ValueError:
            print("Digite um número válido")

    def finalizar_compra(self, carrinho: Carrinho):
        '''Processa pagamento, gera nota fiscal e registra a venda no caixa'''
        total = carrinho.calcular_total()
        print("#### Forma de pagamento ####") 
        print("[1] - Dinheiro ou PIX - 10% desconto")
        print("[2] - Cartão de débito - 5% desconto")
        print("[3] - Cartão de crédito 1x - mesmo valor")
        print("[4] - Cartão de crédito 2x - 5% acréscimo")
        print("[5] - Cartão de crédito 3x - 10% acréscimo")
        print("[6] - Cartão de crédito 4x - 15% acréscimo")

        while True:
            try:
                opcao = int(input("Escolha uma forma de pagamento: "))
                pagamento = Pagamento(total) 
                pagamento.calcular_pagamento(opcao)
                break
            except (ValueError, Exception) as e:
                print(e)
                print("Opção inválida! Tente novamente.")

        print("#### Resumo da compra ####")
        for produto, qtd in carrinho.listar_itens():
            print(f"{qtd}x {produto.nome} - R$ {produto.preco * qtd:.2f}")
        print(f"Forma de pagamento: {pagamento.forma}")
        print(f"Total a pagar R$ {pagamento.valor_final:.2f}")

        self.caixa.registrar_venda(pagamento.valor_final, carrinho.total_itens())

        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"nota_fiscal_{agora}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#### Nota fiscal ####\n")
            f.write(f"Data/Hora: {agora}\n\n")
            for produto, qtd in carrinho.listar_itens():
                f.write(f"{qtd}x {produto.nome} - R$ {produto.preco * qtd:.2f}\n")
            f.write(f"\nForma de pagamento: {pagamento.forma}\n")
            f.write(f"Total a pagar R$ {pagamento.valor_final:.2f}\n")
            f.write("######################\n")
        print(f"Nota fiscal salva em: {filename}")

    def fechamento_dia(self):
        '''Exibe e salva o relatório diário chamando o método da classe Caixa'''
        self.caixa.fechamento()                                              



