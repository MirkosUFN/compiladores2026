from typing import override

class No:
    def __init__(self, nome = ''):
        self.nome = nome
        self.regras_transicao = dict()
        self.resultado_parada = None

    @override
    def __repr__(self):
        return self.nome

    def regras_transicao_string(self):
        return [f'{self.nome} - {i[0]} → {i[1]}' for i in self.regras_transicao.items()]