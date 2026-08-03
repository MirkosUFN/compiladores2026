import sys
import os

def remover_comentarios(codigo_fonte):
    estado = 'NORMAL'
    resultado = []
    i = 0
    n = len(codigo_fonte)

    while i < n:
        char = codigo_fonte[i]

        if estado == 'NORMAL':
            if char == '/' and i + 1 < n and codigo_fonte[i+1] == '/':
                estado = 'COMENTARIO_LINHA'
                resultado.append(' ')
                resultado.append(' ')
                i += 2
                continue
            
            elif char == '/' and i + 1 < n and codigo_fonte[i+1] == '*':
                estado = 'COMENTARIO_BLOCO'
                resultado.append(' ')
                resultado.append(' ')
                i += 2
                continue
            
            elif char == '"':
                estado = 'STRING'
                resultado.append(char)
            elif char == "'":
                estado = 'CHAR'
                resultado.append(char)
            else:
                resultado.append(char)

        elif estado == 'STRING':
            resultado.append(char)
            if char == '\\':
                i += 1
                if i < n:
                    resultado.append(codigo_fonte[i])
            elif char == '"':
                estado = 'NORMAL'

        elif estado == 'CHAR':
            resultado.append(char)
            if char == '\\':
                i += 1
                if i < n:
                    resultado.append(codigo_fonte[i])
            elif char == "'":
                estado = 'NORMAL'

        elif estado == 'COMENTARIO_LINHA':
            if char == '\\' and i + 1 < n and codigo_fonte[i+1] == '\n':
                resultado.append(' ')
                resultado.append('\n')
                i += 2
                continue
            
            elif char == '\n':
                estado = 'NORMAL'
                resultado.append(char)
            elif char == '\r':
                resultado.append(char) 
            else:
                resultado.append(' ')

        elif estado == 'COMENTARIO_BLOCO':
            if char == '*' and i + 1 < n and codigo_fonte[i+1] == '/':
                estado = 'NORMAL'
                resultado.append(' ')
                resultado.append(' ')
                i += 2
                continue
            
            elif char == '\n' or char == '\r':
                resultado.append(char)
            else:
                resultado.append(' ')

        i += 1

    return "".join(resultado)

def main():
    if len(sys.argv) < 2:
        print("Uso: python remove_comentarios.py <arquivo_entrada.c> [arquivo_saida.c]")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    
    if len(sys.argv) >= 3:
        arquivo_saida = sys.argv[2]
    else:
        nome, ext = os.path.splitext(arquivo_entrada)
        arquivo_saida = f"{nome}_limpo{ext}"

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            codigo = f.read()

        codigo_limpo = remover_comentarios(codigo)

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(codigo_limpo)

        print(f"Sucesso! Código sem comentários salvo em: {arquivo_saida}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
