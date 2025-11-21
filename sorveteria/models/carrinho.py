from models.produto import Produto

class Carrinho:
    def __init__(self):
        self.__itens: dict[Produto, int] = {}

    def adicionar(self, produto: Produto, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        produto.reduzir_estoque(quantidade)

        if produto in self.__itens:
            self.__itens[produto] += quantidade
        else:
            self.__itens[produto] = quantidade

    def remover(self, produto: Produto, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade inválida.")
        if produto in self.__itens:
            qtd_no_carrinho = self.__itens[produto]
            if quantidade >= qtd_no_carrinho:
                produto.aumentar_estoque(qtd_no_carrinho)
                del self.__itens[produto]
            else: 
                self.__itens[produto] -= quantidade
                produto.aumentar_estoque(quantidade)

    def listar_itens(self):
        '''Método público para acessar os itens  do carrinho de forma segura'''
        return self.__itens.items()
    def calcular_total(self) -> float:
        return sum(produto.preco * qtd for produto, qtd in self.__itens.items())
    def total_itens(self) -> int:
        return sum(qtd for qtd in self.__itens.values())
    def vazio(self) -> bool:
        return len(self.__itens) == 0                    