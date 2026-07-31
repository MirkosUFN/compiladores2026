def remover_comentarios(texto):
    # Converte a string em uma lista de caracteres mutável
    caracteres = list(texto)
    n = len(caracteres)

    poli_linha = False
    mono_linha = False

    i = 0
    while i < n:
        # Estado 1: Dentro de um comentário de linha (//)
        if mono_linha:
            if caracteres[i] == '\n':
                mono_linha = False
            else:
                caracteres[i] = ' '
            i += 1
            continue

        # Estado 2: Dentro de um comentário de bloco (/* ... */)
        if poli_linha:
            if i + 1 < n and caracteres[i] == '*' and caracteres[i + 1] == '/':
                caracteres[i] = ' '
                caracteres[i + 1] = ' '
                poli_linha = False
                i += 2
            else:
                if caracteres[i] != '\n':
                    caracteres[i] = ' '
                i += 1
            continue

        # Estado 3: Código normal (Procurando abertura de comentários)
        if i + 1 < n and caracteres[i] == '/' and caracteres[i + 1] == '*':
            caracteres[i] = ' '
            caracteres[i + 1] = ' '
            poli_linha = True
            i += 2
        elif i + 1 < n and caracteres[i] == '/' and caracteres[i + 1] == '/':
            caracteres[i] = ' '
            caracteres[i + 1] = ' '
            mono_linha = True
            i += 2
        else:
            i += 1

    return "".join(caracteres)

def processar_arquivo(arquivo_entrada, arquivo_saida):
    try:
        # Abre o arquivo .c original para leitura
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()

        # Processa o texto usando a função de remoção
        conteudo_limpo = remover_comentarios(conteudo_original)

        # Salva o resultado no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo_limpo)

        print(f"Sucesso! Comentários removidos. Salvo em: {arquivo_saida}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    arq_in = input('arquivo a ser lido: ')
    arq_out = input('arquivo final: ')
    processar_arquivo(arq_in, arq_out)
