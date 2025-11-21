class Pagamento:
    def __init__(self, total: float):
        self._total = float(total)
        self.valor_final = 0.0
        self.forma = ""

    def calcular_pagamento(self, opcao: int):
        if opcao == 1:
            self.valor_final = self._total * 0.90
            self.forma = "Dinheiro ou PIX - 10% desconto"
        elif opcao == 2:
            self.valor_final = self._total * 0.95
            self.forma = "Cartão de débito - 5% desconto"
        elif opcao == 3:
            self.valor_final = self._total
            self.forma = "Cartão de crédito 1x - mesmo valor"
        elif opcao == 4:
            self.valor_final = self._total * 1.05
            self.forma = "Cartão de crédito 2x - 5% acréscimo"
        elif opcao == 5:
            self.valor_final = self._total * 1.10
            self.forma = "Cartão de crédito 3x - 10% acréscimo"
        elif opcao == 6:
            self.valor_final = self._total * 1.15
            self.forma = "Cartão de crédito 4x - 15% acréscimo"
        else:
            raise ValueError("Opção inválida de pagamento.")

        