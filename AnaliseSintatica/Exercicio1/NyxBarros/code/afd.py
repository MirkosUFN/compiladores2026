import json
from code.no import No
from typing import Any

class AFD:
    def __init__(self, arquivo_config: str, arquivo_palavras_reservadas: str = '') -> None:
        self.estados = {}
        self.estado_inicial = None
        self.estados_finais = {}
        self.simbolos = {}
        self.palavras_reservadas: set[str] = set()

        self.reconhecer_palavras_reservadas(arquivo_palavras_reservadas)
        self.montar_automato(arquivo_config)

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

    def reconhecer_palavras_reservadas(self, arquivo_palavras_reservadas) -> None:
        with open(arquivo_palavras_reservadas, 'r') as f:
            self.palavras_reservadas = set(f.read().split('\n'))
        print(self.palavras_reservadas)

    def analisar_arquivo(self, arquivo_para_analizar: str) -> list[dict[str, Any]]:
        tabela_simbolos = []
        with open(arquivo_para_analizar, 'r', encoding='utf-8') as arquivo:
            id_token = 1
            for cont_linha, linha in enumerate(arquivo):
                linha = linha if linha[-1] != '\n' else linha[:-1]
                analise_linha = self.reconhecer_linha(linha)
                if analise_linha:
                    for i in analise_linha:
                        token = linha[i['coluna_inicio']:i['coluna_fim']]
                        tipo = f'PALAVRA_RESERVADA {token.upper()}'if token in self.palavras_reservadas else i['tipo']
                        coluna = i['coluna_inicio']
                        tabela_simbolos.append({'ID': id_token, 'token': token, 'tipo': tipo, 'linha': cont_linha+1, 'coluna': coluna})
                        id_token += 1
        return tabela_simbolos

    def reconhecer_linha(self, linha: str) -> list[dict[str, int]]|None:
        estado_atual = self.estado_inicial
        analise_linha = [{'coluna_inicio': 0}]
        coluna = 0

        while coluna < len(linha):
            caractere = linha[coluna]

            # Se o último token já foi fechado, inicia um novo
            if 'tipo' in analise_linha[-1]:
                analise_linha.append({'coluna_inicio': coluna})

            # Se for espaço, finaliza o token atual (se houver) e reseta
            if caractere == ' ':
                # Fecha o token atual usando o estado atual (deve ser final)
                analise_linha[-1]['tipo'] = estado_atual.resultado_parada
                analise_linha[-1]['coluna_fim'] = coluna
                estado_atual = self.estado_inicial
                coluna += 1
                continue

            # Se não há transição para este caractere a partir do estado atual
            if caractere not in estado_atual.regras_transicao:
                # Se já estamos no estado inicial, caractere inválido
                if estado_atual == self.estado_inicial:
                    return None

                # Finaliza o token atual com o estado atual (que deve ser final)
                analise_linha[-1]['tipo'] = estado_atual.resultado_parada
                analise_linha[-1]['coluna_fim'] = coluna

                # Reinicia o autômato, mas não incrementa coluna, para que o mesmo caractere seja processado no próximo ciclo
                estado_atual = self.estado_inicial
                # Não incrementa coluna aqui!
                continue

            # Se chegou aqui, há transição para o caractere

            # Realiza a transição
            estado_atual = estado_atual.regras_transicao[caractere]
            coluna += 1

        # Após o loop, finaliza o último token
        analise_linha[-1]['tipo'] = estado_atual.resultado_parada
        analise_linha[-1]['coluna_fim'] = len(linha)
        estado_atual = self.estado_inicial

        return list(filter(lambda obj: obj['tipo'], analise_linha))
