import sys
import re

def extrair_comentarios(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    comentarios = []
    novas_linhas = []

    dentro_de_bloco = False

    for i, linha in enumerate(linhas, start=1):
        # Trata docstrings/comentários de bloco (''' ou """)
        if re.search(r"'''|\"\"\"", linha):
            if dentro_de_bloco:
                comentarios.append(f"Linha {i}: {linha.strip()}")
                novas_linhas.append("\n")
                dentro_de_bloco = False
            else:
                comentarios.append(f"Linha {i}: {linha.strip()}")
                novas_linhas.append("\n")
                dentro_de_bloco = True
            continue

        if dentro_de_bloco:
            comentarios.append(f"Linha {i}: {linha.strip()}")
            novas_linhas.append("\n")
            continue

        # Trata comentários de linha (#), ignorando # dentro de strings simples/duplas
        sem_strings = re.sub(r'"[^"]*"|\'[^\']*\'', lambda m: " " * len(m.group()), linha)
        pos = sem_strings.find("#")
        if pos != -1:
            comentarios.append(f"Linha {i}: {linha[pos+1:].strip()}")
            linha = linha[:pos].rstrip() + "\n"

        novas_linhas.append(linha)

    return "".join(novas_linhas), comentarios


def main():
    if len(sys.argv) != 2:
        print("Uso: python extrator_simples.py arquivo.py")
        return

    caminho = sys.argv[1]
    codigo_limpo, comentarios = extrair_comentarios(caminho)

    with open(caminho.replace(".py", "_sem_comentarios.py"), "w", encoding="utf-8") as f:
        f.write(codigo_limpo)

    with open(caminho.replace(".py", "_comentarios.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(comentarios))

    print(f"{len(comentarios)} comentários extraídos.")


if __name__ == "__main__":
    main()
