import os

def remover_comentarios_mantendo_linhas(codigo_fonte):
    # Estados da Máquina de Estados
    NORMAL = 0
    STRING = 1
    CHAR = 2
    COMENTARIO_LINHA = 3
    COMENTARIO_BLOCO = 4
    
    estado = NORMAL
    resultado = []
    
    i = 0
    n = len(codigo_fonte)
    
    while i < n:
        c = codigo_fonte[i]
        prox_c = codigo_fonte[i + 1] if i + 1 < n else ''
        
        if estado == NORMAL:
            if c == '/' and prox_c == '/':
                estado = COMENTARIO_LINHA
                i += 1 # Pula a segunda barra
            elif c == '/' and prox_c == '*':
                estado = COMENTARIO_BLOCO
                i += 1 # Pula o asterisco
            elif c == '"':
                estado = STRING
                resultado.append(c)
            elif c == "'":
                estado = CHAR
                resultado.append(c)
            else:
                resultado.append(c)
                
        elif estado == STRING:
            resultado.append(c)
            if c == '\\': # Trata caracteres de escape (ex: \")
                resultado.append(prox_c)
                i += 1
            elif c == '"':
                estado = NORMAL
                
        elif estado == CHAR:
            resultado.append(c)
            if c == '\\':
                resultado.append(prox_c)
                i += 1
            elif c == "'":
                estado = NORMAL
                
        elif estado == COMENTARIO_LINHA:
            # Mantém a quebra de linha ao finalizar o comentário
            if c == '\n':
                resultado.append(c) 
                estado = NORMAL
                
        elif estado == COMENTARIO_BLOCO:
            # Mantém quebras de linha internas do comentário de bloco
            if c == '\n':
                resultado.append(c)
            elif c == '*' and prox_c == '/':
                estado = NORMAL
                # Adiciona um espaço para evitar junção indesejada de tokens
                resultado.append(' ')
                i += 1 # Pula a barra final
                
        i += 1
        
    return "".join(resultado)

if __name__ == "__main__":
    print("=== Pré-processador C: Removedor de Comentários ===")
    
    caminho_arquivo = input("Digite o caminho do arquivo .c: ").strip()

    if not os.path.exists(caminho_arquivo):
        print(f"\n[Erro] O arquivo '{caminho_arquivo}' não foi encontrado.")
    else:
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_c:
                codigo_original = arquivo_c.read()
            
            codigo_limpo = remover_comentarios_mantendo_linhas(codigo_original)
            
            print("\n=== ARQUIVO SEM COMENTÁRIOS ===")
            print(codigo_limpo)
            print("===============================")
            
        except Exception as erro:
            print(f"\n[Erro] Falha ao processar o arquivo: {erro}")