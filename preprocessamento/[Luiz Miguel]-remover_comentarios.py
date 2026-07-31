import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox


def remover_comentarios_c(codigo_c: str) -> str:
    """Remove comentários // e /* ... */ de um código C,

    preservando exatamente o número de linhas e colunas.
    """
    resultado = []
    i = 0
    n = len(codigo_c)

    # Estados da máquina
    IN_NORMAL = 0
    IN_STRING = 1
    IN_CHAR = 2
    IN_LINE_COMMENT = 3
    IN_BLOCK_COMMENT = 4

    estado = IN_NORMAL

    while i < n:
        char = codigo_c[i]
        proximo = codigo_c[i + 1] if i + 1 < n else ""

        # --- ESTADO 0: CÓDIGO NORMAL ---
        if estado == IN_NORMAL:
            if char == '"':
                estado = IN_STRING
                resultado.append(char)
                i += 1
            elif char == "'":
                estado = IN_CHAR
                resultado.append(char)
                i += 1
            elif char == "/" and proximo == "/":
                estado = IN_LINE_COMMENT
                resultado.append(" ")  # Substitui '/' por espaço
                resultado.append(" ")  # Substitui '/' por espaço
                i += 2
            elif char == "/" and proximo == "*":
                estado = IN_BLOCK_COMMENT
                resultado.append(" ")  # Substitui '/' por espaço
                resultado.append(" ")  # Substitui '*' por espaço
                i += 2
            else:
                resultado.append(char)
                i += 1

        # --- ESTADO 1: DENTRO DE UMA STRING "..." ---
        elif estado == IN_STRING:
            resultado.append(char)
            # Ignora aspas escapadas como \"
            if char == "\\" and i + 1 < n:
                resultado.append(codigo_c[i + 1])
                i += 2
            elif char == '"':
                estado = IN_NORMAL
                i += 1
            else:
                i += 1

        # --- ESTADO 2: DENTRO DE UM CARACTERE '...' ---
        elif estado == IN_CHAR:
            resultado.append(char)
            # Ignora aspas escapadas como \'
            if char == "\\" and i + 1 < n:
                resultado.append(codigo_c[i + 1])
                i += 2
            elif char == "'":
                estado = IN_NORMAL
                i += 1
            else:
                i += 1

        # --- ESTADO 3: COMENTÁRIO DE LINHA // ---
        elif estado == IN_LINE_COMMENT:
            if char == "\n":
                estado = IN_NORMAL
                resultado.append("\n")  # Mantém a quebra de linha
            else:
                resultado.append(" ")  # Troca cada caractere por espaço
            i += 1

        # --- ESTADO 4: COMENTÁRIO DE BLOCO /* ... */ ---
        elif estado == IN_BLOCK_COMMENT:
            if char == "*" and proximo == "/":
                estado = IN_NORMAL
                resultado.append(" ")  # Troca '*' por espaço
                resultado.append(" ")  # Troca '/' por espaço
                i += 2
            elif char == "\n":
                resultado.append(
                    "\n"
                )  # Mantém o \n para não alterar número da linha
                i += 1
            else:
                resultado.append(" ")  # Troca o texto por espaço
                i += 1

    return "".join(resultado)


def selecionar_e_processar_arquivo():
    """Abre a janela gráfica de seleção de arquivo e processa o .c escolhido."""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter

    caminho_entrada = filedialog.askopenfilename(
        title="Selecione um arquivo de código fonte em C (.c)",
        filetypes=[
            ("Arquivos C / C++", "*.c *.h *.cpp"),
            ("Todos os arquivos", "*.*"),
        ],
    )

    if not caminho_entrada:
        return

    nome_base, ext = os.path.splitext(caminho_entrada)
    caminho_saida = f"{nome_base}_sem_comentarios{ext}"

    try:
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except UnicodeDecodeError:
        with open(caminho_entrada, "r", encoding="latin-1") as f:
            conteudo = f.read()

    codigo_limpo = remover_comentarios_c(conteudo)

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(codigo_limpo)

    mensagem = f"Sucesso!\nComentários removidos do arquivo C.\n\nSalvo em:\n{os.path.basename(caminho_saida)}"
    messagebox.showinfo("Concluído", mensagem)


if __name__ == "__main__":
    selecionar_e_processar_arquivo()