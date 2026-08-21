from codigo.no import No

class AFD:
    def __init__(self, arquivo: str) -> None:
        self.estados = {}
        self.estado_inicial = None
        self.estados_finais = {}
        self.simbolos = {}
        self.montar_automato(arquivo)

    def montar_automato(self, arquivo: str) -> None:
        with open(arquivo, 'r') as configAfd:
            # nós
            for no in configAfd.readline().strip().split(' '):
                no_obj = No(no)
                self.estados[no] = no_obj
                if not self.estado_inicial:
                    self.estado_inicial = no_obj
            ## nós finais
            for no_final in configAfd.readline().strip().split(' '):
                aux = no_final.split(':')
                self.estados_finais[aux[0]] = aux[1]
                self.estados[aux[0]].resultado_parada = aux[1]

            # simbolos
            self.simbolos = set(configAfd.readline().strip().split(' '))

            # regras de transição
            while True:
                linha = configAfd.readline()
                if not linha:
                    break
                linha = linha.replace('\n','').split(':')
                if len(linha) != 3:
                    continue

                self.estados[linha[0]].regras_transicao[linha[1]] = self.estados[linha[2]]

    def reconhecer_termo(self, termo : str) -> str:
        estado_atual = self.estado_inicial
        for c in termo:
            # validar caractere
            if c not in self.simbolos:
                return None
            if c not in estado_atual.regras_transicao:
                return None

            # transicao
            estado_atual = estado_atual.regras_transicao[c]

        return estado_atual.resultado_parada
            