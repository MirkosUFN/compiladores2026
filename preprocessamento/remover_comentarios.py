import os
import sys

def remover_comentarios_cpp(codigo_fonte: str) -> str:
    estado = "NORMAL"
    saida = []
    i = 0
    n = len(codigo_fonte)

    while i < n:
        char = codigo_fonte[i]
        prox_char = codigo_fonte[i + 1] if i + 1 < n else ""

        if estado == "NORMAL":
            # Início de comentário de linha (//)
            if char == "/" and prox_char == "/":
                estado = "COMENTARIO_LINHA"
                i += 2
                continue
            # Início de comentário de bloco (/*)
            elif char == "/" and prox_char == "*":
                estado = "COMENTARIO_BLOCO"
                i += 2
                continue
            # Início de string ("...")
            elif char == '"':
                estado = "STRING"
                saida.append(char)
                i += 1
                continue
            # Início de caractere ('...')
            elif char == "'":
                estado = "CHAR"
                saida.append(char)
                i += 1
                continue
            else:
                saida.append(char)
                i += 1

        elif estado == "STRING":
            # Trata caracteres escapados dentro da string (ex: \" ou \\)
            if char == "\\" and i + 1 < n:
                saida.append(char)
                saida.append(codigo_fonte[i + 1])
                i += 2
            elif char == '"':
                saida.append(char)
                estado = "NORMAL"
                i += 1
            else:
                saida.append(char)
                i += 1

        elif estado == "CHAR":
            # Trata caracteres escapados dentro do char literal (ex: \' ou \\)
            if char == "\\" and i + 1 < n:
                saida.append(char)
                saida.append(codigo_fonte[i + 1])
                i += 2
            elif char == "'":
                saida.append(char)
                estado = "NORMAL"
                i += 1
            else:
                saida.append(char)
                i += 1

        elif estado == "COMENTARIO_LINHA":
            # Ao encontrar quebra de linha, preserva o '\n' e volta ao normal
            if char == "\n":
                saida.append("\n")
                estado = "NORMAL"
            i += 1

        elif estado == "COMENTARIO_BLOCO":
            # Fim do comentário de bloco (*/)
            if char == "*" and prox_char == "/":
                estado = "NORMAL"
                i += 2
                continue
            # CRUCIAL: preserva quebras de linha dentro do bloco para manter a numeração
            elif char == "\n":
                saida.append("\n")
            i += 1

    return "".join(saida)


def processar_arquivo_cpp(caminho_origem: str, caminho_destino: str = None):
    """Lê um arquivo .cpp, remove os comentários preservando as linhas e salva em um novo arquivo."""
    if not os.path.exists(caminho_origem):
        print(f"[ERRO] O arquivo '{caminho_origem}' não foi encontrado.")
        return

    try:
        # Lê o arquivo original
        with open(caminho_origem, "r", encoding="utf-8") as f:
            codigo_origem = f.read()
    except UnicodeDecodeError:
        # Fallback caso o arquivo tenha sido salvo em encoding padrão do Windows (Latin-1/CP1252)
        with open(caminho_origem, "r", encoding="latin-1") as f:
            codigo_origem = f.read()

    # Processa o código
    codigo_processado = remover_comentarios_cpp(codigo_origem)

    # Se não for informado um arquivo de destino, cria um com sufixo "_preprocessado"
    if not caminho_destino:
        base, ext = os.path.splitext(caminho_origem)
        caminho_destino = f"{base}_preprocessado{ext}"

    # Salva o arquivo final
    with open(caminho_destino, "w", encoding="utf-8") as f:
        f.write(codigo_processado)

    # Exibe resumo
    total_linhas_origem = len(codigo_origem.splitlines())
    total_linhas_destino = len(codigo_processado.splitlines())

    print("--- PROCESSAMENTO CONCLUÍDO ---")
    print(f"Arquivo de entrada : {caminho_origem} ({total_linhas_origem} linhas)")
    print(
        f"Arquivo gerado     : {caminho_destino} ({total_linhas_destino} linhas)"
    )
    print("-------------------------------")


# ==========================================================
# Execução
# ==========================================================
if __name__ == "__main__":
    # Opção 1: Passar o caminho via argumento de linha de comando
    # Exemplo: python script.py main.cpp main_limpo.cpp
    if len(sys.argv) >= 2:
        arquivo_entrada = sys.argv[1]
        arquivo_saida = sys.argv[2] if len(sys.argv) >= 3 else None
        processar_arquivo_cpp(arquivo_entrada, arquivo_saida)

    # Opção 2: Perguntar diretamente no terminal ao rodar o script
    else:
        arquivo = input("Digite o caminho do arquivo .cpp a ser processado: ").strip()
        if arquivo:
            processar_arquivo_cpp(arquivo)
