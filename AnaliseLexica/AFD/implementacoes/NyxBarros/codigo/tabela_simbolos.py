from codigo.afd import AFD

import csv, json

class TabelaSimbolos:
    def __init__(self, arquivo_config_afd: str, arquivo_para_analizar=None) -> None:
        self.afd = AFD(arquivo_config_afd)
        self.analise = []

        if arquivo_para_analizar:
            self.analisar_arquivo(arquivo_para_analizar)

    def analisar_arquivo(self, arquivo_para_analizar: str) -> list:
        """
        Lê o arquivo, tokeniza cada palavra e preenche self.analise.
        Retorna a lista de dicionários (self.analise) para facilitar o uso.
        Em caso de erro, retorna a lista como está (vazia ou parcial).
        """
        with open(arquivo_para_analizar, 'r', encoding='utf-8') as arquivo:
            cont_linha = 1
            id_token = 1
            for linha in arquivo:
                linha_strip = linha.strip()
                if linha_strip:
                    palavras = linha_strip.split()
                    for palavra in palavras:
                        tipo = self.afd.reconhecer_termo(palavra)
                        self.analise.append({'ID': id_token, 'token': palavra, 'tipo': tipo, 'linha': cont_linha})
                        id_token += 1
                cont_linha += 1
        return self.analise

    def gerar_arquivo_csv(self, arquivo_final : str|None = None):
        arquivo_final = arquivo_final or 'tabela_de_simbolos.csv'
        with open(arquivo_final, 'w') as arquivo_tabela:
            arquivo_tabela.write(','.join(self.analise[0].keys())+'\n')
            for linha_tabela in self.analise:
                arquivo_tabela.write(','.join(str(v) for v in linha_tabela.values())+'\n')

    def gerar_arquivo_json(self, arquivo_final : str|None = None):
        arquivo_final = arquivo_final or 'tabela_de_simbolos.json'
        with open(arquivo_final, 'w') as arquivo_json:
            json.dump(self.analise, arquivo_json, indent=4)

