import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Reconhecedor de tokens baseado em Automato Finito Deterministico (AFD).
 *
 * Le a configuracao do AFD (estados, simbolos, estados finais e regras de
 * transicao) a partir de um arquivo de texto, e reconhece termos como:
 *   - Numeros inteiros              (ex: 5, 567)
 *   - Numeros fracionarios/reais    (ex: 3.14)
 *   - Numeros negativos/positivos   (ex: -8, -12.5, +7)
 *   - Variaveis / identificadores   (ex: nome, var1, X)
 *   - Atribuicao                    (ex: =)
 *   - Sinais de comparacao          (ex: ==, <, >, <=, >=)
 *   - Virgula                       (ex: ,)
 *   - Ponto e virgula               (ex: ;)
 *
 * Agora o analisador reconhece MULTIPLOS TOKENS POR LINHA: cada linha do
 * arquivo de entrada e quebrada em tokens separados por espacos em branco,
 * e cada token e reconhecido individualmente pelo AFD.
 *
 * Alem do reconhecimento, gera uma TABELA DE SIMBOLOS com ID, TOKEN, TIPO,
 * LINHA e COLUNA de cada termo processado, exportando o resultado em HTML.
 *
 * Formato do arquivo de configuracao (AFD_config.txt):
 *   Linha 1: lista de estados, separados por espaco (o primeiro e o inicial)
 *   Linha 2: lista de simbolos do alfabeto, separados por espaco
 *   Linha 3: lista de estados finais no formato estado:TIPO, separados por espaco
 *   Linhas seguintes: regras de transicao no formato estadoAtual:simbolo:estadoDestino
 */
public class ReconhecedorAFD {

    /** Representa uma entrada da tabela de simbolos. */
    public static class EntradaTabelaSimbolos {
        private final int id;
        private final String token;
        private final String tipo;
        private final int linha;
        private final int coluna;

        public EntradaTabelaSimbolos(int id, String token, String tipo, int linha, int coluna) {
            this.id = id;
            this.token = token;
            this.tipo = tipo;
            this.linha = linha;
            this.coluna = coluna;
        }

        public int getId() { return id; }
        public String getToken() { return token; }
        public String getTipo() { return tipo; }
        public int getLinha() { return linha; }
        public int getColuna() { return coluna; }
    }

    private final Set<String> estados = new HashSet<>();
    private final Set<String> simbolos = new HashSet<>();
    // estado -> tipo (para estados finais)
    private final Map<String, String> estadosFinais = new HashMap<>();
    // "estadoAtual:simbolo" -> estadoDestino  (acesso O(1), evita busca linear a cada caractere)
    private final Map<String, String> transicoes = new HashMap<>();
    private String estadoInicial;

    // tabela de simbolos acumulada durante o processamento do arquivo de entrada
    private final List<EntradaTabelaSimbolos> tabelaSimbolos = new ArrayList<>();

    /**
     * Carrega a configuracao do AFD a partir do arquivo indicado.
     */
    public void carregarConfiguracao(String caminho) throws IOException {
        try (BufferedReader config = new BufferedReader(
                new InputStreamReader(Files.newInputStream(Paths.get(caminho)), StandardCharsets.UTF_8))) {

            // Linha 1: estados
            String linhaEstados = config.readLine();
            if (linhaEstados == null || linhaEstados.trim().isEmpty()) {
                throw new IOException("Arquivo de configuracao invalido: linha de estados ausente.");
            }
            String[] listaEstados = linhaEstados.trim().split("\\s+");
            for (String e : listaEstados) {
                estados.add(e);
            }
            estadoInicial = listaEstados[0];

            // Linha 2: simbolos
            String linhaSimbolos = config.readLine();
            if (linhaSimbolos == null) {
                throw new IOException("Arquivo de configuracao invalido: linha de simbolos ausente.");
            }
            for (String s : linhaSimbolos.trim().split("\\s+")) {
                simbolos.add(s);
            }

            // Linha 3: estados finais (estado:TIPO)
            String linhaFinais = config.readLine();
            if (linhaFinais == null) {
                throw new IOException("Arquivo de configuracao invalido: linha de estados finais ausente.");
            }
            for (String f : linhaFinais.trim().split("\\s+")) {
                String[] par = f.split(":");
                if (par.length == 2) {
                    estadosFinais.put(par[0], par[1]);
                }
            }

            // Linhas seguintes: regras de transicao (estadoAtual:simbolo:estadoDestino)
            String linha;
            while ((linha = config.readLine()) != null) {
                if (linha.trim().isEmpty()) {
                    continue;
                }
                for (String r : linha.trim().split("\\s+")) {
                    String[] partes = r.split(":");
                    if (partes.length != 3) {
                        throw new IOException("Regra de transicao invalida: \"" + r + "\"");
                    }
                    // chave = origem:simbolo -> destino
                    transicoes.put(partes[0] + ":" + partes[1], partes[2]);
                }
            }
        }
    }

    /**
     * Tenta reconhecer o termo informado, percorrendo o AFD simbolo a simbolo.
     * Retorna o TIPO do token se aceito por um estado final, ou null caso o
     * termo nao seja reconhecido (erro lexico).
     */
    public String reconheceTermo(String termo) {
        String estadoAtual = estadoInicial; // reinicia o AFD a cada novo termo

        for (int i = 0; i < termo.length(); i++) {
            String caractereAtual = String.valueOf(termo.charAt(i));

            if (!simbolos.contains(caractereAtual)) {
                return null;
            }

            String chave = estadoAtual + ":" + caractereAtual;
            String proximoEstado = transicoes.get(chave);

            if (proximoEstado == null) {
                return null;
            }
            estadoAtual = proximoEstado;
        }

        return estadosFinais.get(estadoAtual);
    }

    /**
     * Processa um arquivo de entrada linha a linha, reconhecendo MULTIPLOS
     * TOKENS POR LINHA (tokens separados por espacos em branco) e alimentando
     * a tabela de simbolos (id, token, tipo, linha, coluna).
     *
     * A coluna registrada corresponde a posicao (em caracteres, 1-based) em
     * que o token comeca dentro da linha original.
     */
    public void processarArquivo(String caminhoEntrada) throws IOException {
        int idAtual = 1;
        try (BufferedReader arquivo = new BufferedReader(
                new InputStreamReader(Files.newInputStream(Paths.get(caminhoEntrada)), StandardCharsets.UTF_8))) {
            String linhaTexto;
            int numeroLinha = 0;
            while ((linhaTexto = arquivo.readLine()) != null) {
                numeroLinha++;
                if (linhaTexto.trim().isEmpty()) {
                    continue;
                }

                // Quebra a linha em tokens, preservando a posicao (coluna) de cada um.
                int posicao = 0;
                while (posicao < linhaTexto.length()) {
                    // pula espacos em branco
                    while (posicao < linhaTexto.length() && Character.isWhitespace(linhaTexto.charAt(posicao))) {
                        posicao++;
                    }
                    if (posicao >= linhaTexto.length()) {
                        break;
                    }

                    int inicioToken = posicao;
                    while (posicao < linhaTexto.length() && !Character.isWhitespace(linhaTexto.charAt(posicao))) {
                        posicao++;
                    }

                    String token = linhaTexto.substring(inicioToken, posicao);
                    int coluna = inicioToken + 1; // coluna 1-based

                    String tipo = reconheceTermo(token);
                    if (tipo != null) {
                        System.out.println(token + ":" + tipo + " (linha " + numeroLinha + ", coluna " + coluna + ")");
                        tabelaSimbolos.add(new EntradaTabelaSimbolos(idAtual++, token, tipo, numeroLinha, coluna));
                    } else {
                        System.out.println("Token nao reconhecido: \"" + token + "\" (linha " + numeroLinha
                                + ", coluna " + coluna + ")");
                        tabelaSimbolos.add(new EntradaTabelaSimbolos(idAtual++, token, "ERRO", numeroLinha, coluna));
                    }
                }
            }
        }
    }

    public List<EntradaTabelaSimbolos> getTabelaSimbolos() {
        return tabelaSimbolos;
    }

    // Exportação em HTML
    public void exportarTabelaSimbolosHtml(String caminhoSaida) throws IOException {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>\n");
        html.append("<html lang=\"pt-BR\">\n<head>\n");
        html.append("<meta charset=\"UTF-8\">\n");
        html.append("<title>Tabela de Simbolos - Reconhecedor AFD</title>\n");
        html.append("<style>\n");
        html.append("  body { font-family: 'Segoe UI', Arial, sans-serif; background:#f4f6f8; margin:0; padding:32px; color:#1f2937; }\n");
        html.append("  h1 { font-size: 22px; margin-bottom: 4px; }\n");
        html.append("  p.subtitulo { color:#6b7280; margin-top:0; margin-bottom:24px; }\n");
        html.append("  table { border-collapse: collapse; width:100%; max-width:900px; background:#fff; box-shadow:0 1px 3px rgba(0,0,0,0.1); }\n");
        html.append("  th, td { padding:10px 16px; text-align:left; border-bottom:1px solid #e5e7eb; }\n");
        html.append("  th { background:#111827; color:#fff; font-size:13px; text-transform:uppercase; letter-spacing:0.04em; }\n");
        html.append("  tr:nth-child(even) { background:#f9fafb; }\n");
        html.append("  tr:hover { background:#eef2ff; }\n");
        html.append("  td.token { font-family: Consolas, monospace; font-weight:600; }\n");
        html.append("  .tipo { display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:600; }\n");
        html.append("  .INTEIRO { background:#dbeafe; color:#1d4ed8; }\n");
        html.append("  .FRACIONARIO { background:#dcfce7; color:#15803d; }\n");
        html.append("  .NOMEVARIAVEL { background:#fef3c7; color:#a16207; }\n");
        html.append("  .ATRIBUICAO { background:#ede9fe; color:#6d28d9; }\n");
        html.append("  .SINAL_COMPARACAO { background:#ffe4e6; color:#be123c; }\n");
        html.append("  .VIRGULA { background:#e0f2fe; color:#0369a1; }\n");
        html.append("  .PONTO_VIRGULA { background:#f3e8ff; color:#7e22ce; }\n");
        html.append("  .ERRO { background:#fee2e2; color:#b91c1c; }\n");
        html.append("</style>\n</head>\n<body>\n");
        html.append("<h1>Tabela de Simbolos</h1>\n");
        html.append("<p class=\"subtitulo\">Gerada automaticamente pelo Reconhecedor AFD</p>\n");
        html.append("<table>\n<thead>\n<tr><th>ID</th><th>Token</th><th>Tipo</th><th>Linha</th><th>Coluna</th></tr>\n</thead>\n<tbody>\n");

        for (EntradaTabelaSimbolos e : tabelaSimbolos) {
            html.append("<tr>")
                .append("<td>").append(e.getId()).append("</td>")
                .append("<td class=\"token\">").append(escapeHtml(e.getToken())).append("</td>")
                .append("<td><span class=\"tipo ").append(e.getTipo()).append("\">").append(e.getTipo()).append("</span></td>")
                .append("<td>").append(e.getLinha()).append("</td>")
                .append("<td>").append(e.getColuna()).append("</td>")
                .append("</tr>\n");
        }

        html.append("</tbody>\n</table>\n</body>\n</html>\n");

        try (PrintWriter writer = new PrintWriter(
                Files.newBufferedWriter(Paths.get(caminhoSaida), StandardCharsets.UTF_8))) {
            writer.write(html.toString());
        }
    }

    private static String escapeHtml(String texto) {
        return texto.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;");
    }

    public static void main(String[] args) {
        ReconhecedorAFD afd = new ReconhecedorAFD();

        String caminhoConfig = "AFD_config.txt";
        String caminhoEntrada = "input.c";
        String caminhoSaidaHtml = "tabelaSimbolos.html";

        try {
            afd.carregarConfiguracao(caminhoConfig);
            afd.processarArquivo(caminhoEntrada);
            afd.exportarTabelaSimbolosHtml(caminhoSaidaHtml);
            System.out.println("\nTabela de simbolos exportada para: " + caminhoSaidaHtml);
        } catch (IOException e) {
            System.out.println("Erro ao ler arquivo: " + e.getMessage());
        }
    }
}
