from codigo.no import No

import json

class AFD:
    def __init__(self, arquivo_config: str) -> None:
        self.estados = {}
        self.estado_inicial = None
        self.estados_finais = {}
        self.simbolos = {}
        self.montar_automato(arquivo_config)
        self.tabela_simbolos : list(dict) = []
        self.buffer = {}

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

    def analisar_arquivo(self, arquivo_para_analizar: str) -> list:
        with open(arquivo_para_analizar, 'r', encoding='utf-8') as arquivo:
            id_token = 1
            for cont_linha, linha in enumerate(arquivo):
                linha = linha if linha[-1] != '\n' else linha[:-1]
                analise_linha = self.reconhecer_linha(linha)
                if analise_linha:
                    for i in analise_linha:
                        token = linha[i['coluna_inicio']:i['coluna_fim']]
                        tipo = i['tipo']
                        coluna = i['coluna_inicio']
                        self.tabela_simbolos.append({'ID': id_token, 'token': token, 'tipo': tipo, 'linha': cont_linha+1, 'coluna': coluna})
                        self.buffer[token] = tipo
                        id_token += 1
        return self.tabela_simbolos

    def reconhecer_linha(self, linha: str) -> list:
        estado_atual = self.estado_inicial
        analise_linha = [{'coluna_inicio': 0}]
        coluna = 0

        while coluna < len(linha):
            caractere = linha[coluna]

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
            # Se o último token já foi fechado, inicia um novo
            if 'tipo' in analise_linha[-1]:
                analise_linha.append({'coluna_inicio': coluna})

            # Realiza a transição
            estado_atual = estado_atual.regras_transicao[caractere]
            coluna += 1

        # Após o loop, finaliza o último token
        analise_linha[-1]['tipo'] = estado_atual.resultado_parada
        analise_linha[-1]['coluna_fim'] = len(linha)
        estado_atual = self.estado_inicial

        return analise_linha
    def gerar_arquivo_csv(self, arquivo_final : str|None = None):
        arquivo_final = arquivo_final or 'teste/tabela_de_simbolos.csv'
        with open(arquivo_final, 'w') as arquivo_tabela:
            arquivo_tabela.writelines(','.join(self.tabela_simbolos[0].keys())+'\n')
            for linha_tabela in self.tabela_simbolos:
                arquivo_tabela.writelines(','.join(str(v) for v in linha_tabela.values())+'\n')

    def gerar_arquivo_json(self, arquivo_final : str|None = None):
        arquivo_final = arquivo_final or 'teste/tabela_de_simbolos.json'
        with open(arquivo_final, 'w') as arquivo_json:
            json.dump(self.tabela_simbolos, arquivo_json, indent=4)
 
    def gerar_arquivo_mk(self, arquivo_final : str|None = None):
        arquivo_final = arquivo_final or 'teste/tabela_de_simbolos.md'

        # planejar tabela
        ## selecionar campos
        campos = self.tabela_simbolos[0].keys()

        ## selecionar tamanhos minimos
        tamanhos_campos = {}
        for campo in campos:
            tamanhos_campos[campo] = len(campo)

        ## varredura pela tabela
        for linha in self.tabela_simbolos:
            for campo in campos:
                tamanhos_campos[campo] = max(tamanhos_campos[campo], len(str(linha[campo])))

        # gerar tabela
        md = []
        
        md.append('|') # cabeçalho
        for i in campos:
            md[-1] += f' {i:{tamanhos_campos[i]}} |'

        md.append('|') # divisão do cabeçalho e corpo
        for i in tamanhos_campos.values():
            md[-1] += '-'*(i+2)+'|'
        
        for linha in self.tabela_simbolos: # corpo
            md.append('|')
            for campo in campos:
                md[-1] += f' {linha[campo]:{tamanhos_campos[campo]}} |'
                
        print('\n'.join(md))

        with open(arquivo_final, 'w') as arquivo_tabela:
            arquivo_tabela.writelines('\n'.join(md))
