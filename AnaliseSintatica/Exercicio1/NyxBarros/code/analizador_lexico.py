import json
from code.afd import AFD
from code.no import No
from typing import Any

class AnalizadorLexico:
    def __init__(self, arquivo_config: str, arquivo_palavras_reservadas: str = '') -> None:
        self.automato = AFD(arquivo_config, arquivo_palavras_reservadas)
        self.__tabela_simbolos: list[dict[str, str|int]] = []

    @property
    def tabela_simbolos(self):
        return self.__tabela_simbolos

    @tabela_simbolos.setter
    def tabela_simbolos(self, arquivo:str) -> None:
        """função que cria a tabela de simbolos a partir de um código

        Args:
            arquivo (str): arquivo que será analizado
        """        
        self.__tabela_simbolos = self.automato.analisar_arquivo(arquivo)

    def gerar_arquivo_csv(self, arquivo_final : str = 'teste/tabela_de_simbolos.csv'):
        if len(self.tabela_simbolos) == 0:
            print('não existe tabela de simbolos')
            return
        with open(arquivo_final, 'w') as arquivo_tabela:
            arquivo_tabela.writelines(','.join(self.tabela_simbolos[0].keys())+'\n')
            for linha_tabela in self.tabela_simbolos:
                arquivo_tabela.writelines(','.join(str(v) for v in linha_tabela.values())+'\n')

    def gerar_arquivo_json(self, arquivo_final : str = 'teste/tabela_de_simbolos.json'):
        if len(self.tabela_simbolos) == 0:
            print('não existe tabela de simbolos')
            return
        with open(arquivo_final, 'w') as arquivo_json:
            json.dump(self.tabela_simbolos, arquivo_json, indent=4)
 
    def gerar_arquivo_md(self, arquivo_final : str = 'teste/tabela_de_simbolos.md'):
        if len(self.tabela_simbolos) == 0:
            print('não existe tabela de simbolos')
            return
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

