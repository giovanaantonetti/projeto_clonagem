import datetime

class Caixa:
    def __init__(self):
        self._total_dia = 0.0
        self._itens_vendidos = 0

    def registrar_venda(self, total_compra: float, itens_vendidos: int):
        '''Registra uma venda, somando os valores e itens ao total do dia'''
        self._total_dia += total_compra
        self._itens_vendidos += itens_vendidos

    def fechamento(self):
        '''Gera e exibe o relatório de fechamento do caixa, tanto no console 
        quanto em um arquivo de texto'''
        print("#### Fechamento do caixa ####")
        print(f"Total arrecadado no dia R$ {self._total_dia:.2f}")
        print(f"Total de itens vendidos: {self._itens_vendidos}")
        print("#"*30)

        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"relatorio_{agora}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("#### Fechamento do caixa ####\n")
            f.write(f"Total arrecadado no dia R$ {self._total_dia:.2f}\n") 
            f.write(f"Total de itens vendidos: {self._itens_vendidos}\n")
            f.write("#############################\n")
        print(f"Relatório salvo em: {filename}")           