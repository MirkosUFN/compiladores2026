import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
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
 *   - Delimitadores                 (ex: (, ), {, }, [, ])
 *
 * Alem do reconhecimento, gera uma TABELA DE SIMBOLOS com ID, TOKEN, TIPO,
 * LINHA, COLUNA e REF (referencia do token de abertura correspondente) de
 * cada termo processado, exportando o resultado em HTML.
 */
public class ReconhecedorAFD {

    /** Representa uma entrada da tabela de simbolos. */
    public static class EntradaTabelaSimbolos {
        private final int id;
        private final String token;
        private final String tipo;
        private final int linha;
        private final int coluna;
        private String ref; // Referencia ao ID do token de abertura correspondente

        public EntradaTabelaSimbolos(int id, String token, String tipo, int linha, int coluna) {
            this.id = id;
            this.token = token;
            this.tipo = tipo;
            this.linha = linha;
            this.coluna = coluna;
            this.ref = "-";
        }

        public int getId() { return id; }
        public String getToken() { return token; }
        public String getTipo() { return tipo; }
        public int getLinha() { return linha; }
        public int getColuna() { return coluna; }
        public String getRef() { return ref; }
        public void setRef(String ref) { this.ref = ref; }
    }

    private final Set<String> estados = new HashSet<>();
    private final Set<String> simbolos = new HashSet<>();
    private final Map<String, String> estadosFinais = new HashMap<>();
    private final Map<String, String> transicoes = new HashMap<>();
    private String estadoInicial;

    private static final Map<String, String> PALAVRAS_RESERVADAS = new HashMap<>();
    static {
        PALAVRAS_RESERVADAS.put("int", "PR_INT");
        PALAVRAS_RESERVADAS.put("char", "PR_CHAR");
        PALAVRAS_RESERVADAS.put("float", "PR_FLOAT");
        PALAVRAS_RESERVADAS.put("double", "PR_DOUBLE");
        PALAVRAS_RESERVADAS.put("void", "PR_VOID");
        PALAVRAS_RESERVADAS.put("boolean", "PR_BOOLEAN");
    }

    private final List<EntradaTabelaSimbolos> tabelaSimbolos = new ArrayList<>();

    public void carregarConfiguracao(String caminho) throws IOException {
        try (BufferedReader config = new BufferedReader(
                new InputStreamReader(Files.newInputStream(Paths.get(caminho)), StandardCharsets.UTF_8))) {

            String linhaEstados = config.readLine();
            if (linhaEstados == null || linhaEstados.trim().isEmpty()) {
                throw new IOException("Arquivo de configuracao invalido: linha de estados ausente.");
            }
            String[] listaEstados = linhaEstados.trim().split("\s+");
            for (String e : listaEstados) {
                estados.add(e);
            }
            estadoInicial = listaEstados[0];

            String linhaSimbolos = config.readLine();
            if (linhaSimbolos == null) {
                throw new IOException("Arquivo de configuracao invalido: linha de simbolos ausente.");
            }
            for (String s : linhaSimbolos.trim().split("\s+")) {
                simbolos.add(s);
            }

            String linhaFinais = config.readLine();
            if (linhaFinais == null) {
                throw new IOException("Arquivo de configuracao invalido: linha de estados finais ausente.");
            }
            for (String f : linhaFinais.trim().split("\s+")) {
                String[] par = f.split(":");
                if (par.length == 2) {
                    estadosFinais.put(par[0], par[1]);
                }
            }

            String linha;
            while ((linha = config.readLine()) != null) {
                if (linha.trim().isEmpty()) {
                    continue;
                }
                for (String r : linha.trim().split("\s+")) {
                    String[] partes = r.split(":");
                    if (partes.length != 3) {
                        throw new IOException("Regra de transicao invalida: "" + r + """);
                    }
                    transicoes.put(partes[0] + ":" + partes[1], partes[2]);
                }
            }
        }
    }

    public String reconheceTermo(String termo) {
        String estadoAtual = estadoInicial;

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

        String tipo = estadosFinais.get(estadoAtual);

        if ("NOMEVARIAVEL".equals(tipo) && PALAVRAS_RESERVADAS.containsKey(termo)) {
            return PALAVRAS_RESERVADAS.get(termo);
        }

        return tipo;
    }

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

                int posicao = 0;
                while (posicao < linhaTexto.length()) {
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
                    int coluna = inicioToken;

                    String tipo = reconheceTermo(token);
                    if (tipo != null) {
                        System.out.println(token + ":" + tipo + " (linha " + numeroLinha + ", coluna " + coluna + ")");
                        tabelaSimbolos.add(new EntradaTabelaSimbolos(idAtual++, token, tipo, numeroLinha, coluna));
                    } else {
                        System.out.println("Token nao reconhecido: "" + token + "" (linha " + numeroLinha
                                + ", coluna " + coluna + ")");
                        tabelaSimbolos.add(new EntradaTabelaSimbolos(idAtual++, token, "ERRO", numeroLinha, coluna));
                    }
                }
            }
        }

        // Processar balanceamento de delimitadores e preencher a coluna 'Ref'
        verificarEAssociarDelimitadores();
    }

    /**
     * Classe interna para manter os elementos de abertura na pilha.
     */
    private static class ElementoDelimitador {
        final String token;
        final int id;

        ElementoDelimitador(String token, int id) {
            this.token = token;
            this.id = id;
        }
    }

    /**
     * Valida o balanceamento de (), {}, [] e associa a referencia Ref ao token de abertura.
     */
    public boolean verificarEAssociarDelimitadores() {
        Deque<ElementoDelimitador> pilha = new ArrayDeque<>();

        int abrePar = 0, fechaPar = 0;
        int abreChave = 0, fechaChave = 0;
        int abreCol = 0, fechaCol = 0;

        boolean balanceado = true;

        for (EntradaTabelaSimbolos e : tabelaSimbolos) {
            String tok = e.getToken();

            if (tok.equals("(")) {
                abrePar++;
                pilha.push(new ElementoDelimitador(tok, e.getId()));
            } else if (tok.equals("{")) {
                abreChave++;
                pilha.push(new ElementoDelimitador(tok, e.getId()));
            } else if (tok.equals("[")) {
                abreCol++;
                pilha.push(new ElementoDelimitador(tok, e.getId()));
            } else if (tok.equals(")")) {
                fechaPar++;
                if (!pilha.isEmpty() && pilha.peek().token.equals("(")) {
                    ElementoDelimitador topo = pilha.pop();
                    e.setRef("ID " + topo.id);
                } else {
                    balanceado = false;
                    e.setRef("ERRO (Sem abertura correspondente)");
                }
            } else if (tok.equals("}")) {
                fechaChave++;
                if (!pilha.isEmpty() && pilha.peek().token.equals("{")) {
                    ElementoDelimitador topo = pilha.pop();
                    e.setRef("ID " + topo.id);
                } else {
                    balanceado = false;
                    e.setRef("ERRO (Sem abertura correspondente)");
                }
            } else if (tok.equals("]")) {
                fechaCol++;
                if (!pilha.isEmpty() && pilha.peek().token.equals("[")) {
                    ElementoDelimitador topo = pilha.pop();
                    e.setRef("ID " + topo.id);
                } else {
                    balanceado = false;
                    e.setRef("ERRO (Sem abertura correspondente)");
                }
            }
        }

        if (!pilha.isEmpty()) {
            balanceado = false;
        }

        boolean contagemIgual = (abrePar == fechaPar) && (abreChave == fechaChave) && (abreCol == fechaCol);

        System.out.println("
--- RELATORIO DE DELIMITADORES ---");
        System.out.println("Parêntesis:  ( = " + abrePar + " | ) = " + fechaPar);
        System.out.println("Chaves:      { = " + abreChave + " | } = " + fechaChave);
        System.out.println("Colchetes:   [ = " + abreCol + " | ] = " + fechaCol);
        System.out.println("Status de Balanceamento: " + (balanceado && contagemIgual ? "CORRETO" : "INCORRETO / DESBALANCEADO"));

        return balanceado && contagemIgual;
    }

    public List<EntradaTabelaSimbolos> getTabelaSimbolos() {
        return tabelaSimbolos;
    }

    public void exportarTabelaSimbolosHtml(String caminhoSaida) throws IOException {
        StringBuilder html = new StringBuilder();
        html.append("<!DOCTYPE html>
");
        html.append("<html lang="pt-BR">
<head>
");
        html.append("<meta charset="UTF-8">
");
        html.append("<title>Tabela de Simbolos - Reconhecedor AFD</title>
");
        html.append("<style>
");
        html.append("  body { font-family: 'Segoe UI', Arial, sans-serif; background:#f4f6f8; margin:0; padding:32px; color:#1f2937; }
");
        html.append("  h1 { font-size: 22px; margin-bottom: 4px; }
");
        html.append("  p.subtitulo { color:#6b7280; margin-top:0; margin-bottom:24px; }
");
        html.append("  table { border-collapse: collapse; width:100%; max-width:950px; background:#fff; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
");
        html.append("  th, td { padding:10px 16px; text-align:left; border-bottom:1px solid #e5e7eb; }
");
        html.append("  th { background:#111827; color:#fff; font-size:13px; text-transform:uppercase; letter-spacing:0.04em; }
");
        html.append("  tr:nth-child(even) { background:#f9fafb; }
");
        html.append("  tr:hover { background:#eef2ff; }
");
        html.append("  td.token { font-family: Consolas, monospace; font-weight:600; }
");
        html.append("  td.ref { font-family: Consolas, monospace; color:#4b5563; font-weight:600; }
");
        html.append("  .tipo { display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:600; }
");
        html.append("  .INTEIRO { background:#dbeafe; color:#1d4ed8; }
");
        html.append("  .FRACIONARIO { background:#dcfce7; color:#15803d; }
");
        html.append("  .NOMEVARIAVEL { background:#fef3c7; color:#a16207; }
");
        html.append("  .ATRIBUICAO { background:#ede9fe; color:#6d28d9; }
");
        html.append("  .SINAL_COMPARACAO { background:#ffe4e6; color:#be123c; }
");
        html.append("  .VIRGULA { background:#e0f2fe; color:#0369a1; }
");
        html.append("  .PONTO_VIRGULA { background:#f3e8ff; color:#7e22ce; }
");
        html.append("  .ABRE_PAR, .FECHA_PAR { background:#e0e7ff; color:#3730a3; }
");
        html.append("  .ABRE_CHAVE, .FECHA_CHAVE { background:#fce7f3; color:#9d174d; }
");
        html.append("  .ABRE_COLCHETE, .FECHA_COLCHETE { background:#ffedd5; color:#c2410c; }
");
        html.append("  .PR_INT, .PR_CHAR, .PR_FLOAT, .PR_DOUBLE, .PR_VOID, .PR_BOOLEAN { background:#d1fae5; color:#065f46; }
");
        html.append("  .ERRO { background:#fee2e2; color:#b91c1c; }
");
        html.append("</style>
</head>
<body>
");
        html.append("<h1>Tabela de Simbolos</h1>
");
        html.append("<p class="subtitulo">Gerada automaticamente pelo Reconhecedor AFD</p>
");
        html.append("<table>
<thead>
<tr><th>ID</th><th>Token</th><th>Tipo</th><th>Linha</th><th>Coluna</th><th>Ref.</th></tr>
</thead>
<tbody>
");

        for (EntradaTabelaSimbolos e : tabelaSimbolos) {
            html.append("<tr>")
                .append("<td>").append(e.getId()).append("</td>")
                .append("<td class="token">").append(escapeHtml(e.getToken())).append("</td>")
                .append("<td><span class="tipo ").append(e.getTipo()).append("">").append(e.getTipo()).append("</span></td>")
                .append("<td>").append(e.getLinha()).append("</td>")
                .append("<td>").append(e.getColuna()).append("</td>")
                .append("<td class="ref">").append(escapeHtml(e.getRef())).append("</td>")
                .append("</tr>
");
        }

        html.append("</tbody>
</table>
</body>
</html>
");

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
            System.out.println("
Tabela de simbolos exportada para: " + caminhoSaidaHtml);
        } catch (IOException e) {
            System.out.println("Erro ao ler arquivo: " + e.getMessage());
        }
    }
}
