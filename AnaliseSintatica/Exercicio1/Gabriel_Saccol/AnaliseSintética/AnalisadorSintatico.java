import java.util.ArrayList;
import java.util.List;

/**
 * Analisador sintatico (parser descendente recursivo) para a gramatica de
 * declaracao de variaveis, com ou sem inicializacao, e lista multipla:
 *
 *   [TIPO]          -> PR_INT | PR_CHAR | PR_FLOAT | PR_DOUBLE | PR_VOID | PR_BOOLEAN
 *   Declara         -> [TIPO] [NOMEVARIAVEL] Inicializacao [PV]
 *                    | [TIPO] [NOMEVARIAVEL] Inicializacao DeclaraMultiplo [PV]
 *   Inicializacao   -> [ATRIBUICAO] [VALOR] | epsilon
 *   DeclaraMultiplo -> [VG] [NOMEVARIAVEL] Inicializacao
 *                    | [VG] [NOMEVARIAVEL] Inicializacao DeclaraMultiplo
 *   [VALOR]         -> [INTEIRO] | [FRACIONARIO] | [NOMEVARIAVEL]
 *
 * Consome a lista de entradas da tabela de simbolos (tokens ja classificados
 * pelo ReconhecedorAFD), valida a sequencia contra a gramatica e monta uma
 * ARVORE SINTATICA (AST) com um no por regra/simbolo reconhecido, que pode
 * ser impressa de forma indentada.
 */
public class AnalisadorSintatico {

    /** Excecao lancada quando a sequencia de tokens nao segue a gramatica. */
    public static class ErroSintatico extends Exception {
        public ErroSintatico(String mensagem) {
            super(mensagem);
        }
    }

    /**
     * No da arvore sintatica. Um no "nao-terminal" (ex: Declara,
     * Inicializacao, DeclaraMultiplo) tem filhos; um no "terminal" representa
     * um token consumido da tabela de simbolos (ex: [TIPO]=int) e nao tem
     * filhos.
     */
    public static class NoArvore {
        private final String rotulo;
        private final ReconhecedorAFD.EntradaTabelaSimbolos token; // null se nao-terminal
        private final List<NoArvore> filhos = new ArrayList<>();

        /** Cria um no nao-terminal (regra da gramatica). */
        public NoArvore(String rotulo) {
            this.rotulo = rotulo;
            this.token = null;
        }

        /** Cria um no terminal (token consumido da tabela de simbolos). */
        public NoArvore(String rotulo, ReconhecedorAFD.EntradaTabelaSimbolos token) {
            this.rotulo = rotulo;
            this.token = token;
        }

        public void addFilho(NoArvore filho) {
            filhos.add(filho);
        }

        public List<NoArvore> getFilhos() {
            return filhos;
        }

        public String getRotulo() {
            return rotulo;
        }

        /** Representacao de uma linha do no (rotulo + info do token, se houver). */
        private String descricaoLinha() {
            if (token != null) {
                return rotulo + " -> \"" + token.getToken() + "\" (linha " + token.getLinha()
                        + ", coluna " + token.getColuna() + ")";
            }
            return rotulo;
        }

        /** Imprime a arvore de forma indentada, no estilo "galho" (└──/├──). */
        public void imprimir() {
            imprimir("", true);
        }

        private void imprimir(String prefixo, boolean ultimo) {
            System.out.println(prefixo + (ultimo ? "`-- " : "|-- ") + descricaoLinha());
            String novoPrefixo = prefixo + (ultimo ? "    " : "|   ");
            for (int i = 0; i < filhos.size(); i++) {
                filhos.get(i).imprimir(novoPrefixo, i == filhos.size() - 1);
            }
        }
    }

    private static final java.util.Set<String> TIPOS_VALIDOS = java.util.Set.of(
            "PR_INT", "PR_CHAR", "PR_FLOAT", "PR_DOUBLE", "PR_VOID", "PR_BOOLEAN");

    private static final java.util.Set<String> VALORES_VALIDOS = java.util.Set.of(
            "INTEIRO", "FRACIONARIO", "NOMEVARIAVEL");

    private final List<ReconhecedorAFD.EntradaTabelaSimbolos> tokens;
    private int posicao;

    public AnalisadorSintatico(List<ReconhecedorAFD.EntradaTabelaSimbolos> tokens) {
        this.tokens = tokens;
        this.posicao = 0;
    }

    /** Retorna o token atual sem consumir, ou null se acabaram os tokens. */
    private ReconhecedorAFD.EntradaTabelaSimbolos atual() {
        return posicao < tokens.size() ? tokens.get(posicao) : null;
    }

    /** Consome o token atual e avanca, se o tipo bater com o esperado; devolve o no terminal criado. */
    private NoArvore consumir(String tipoEsperado, String rotuloNo) throws ErroSintatico {
        ReconhecedorAFD.EntradaTabelaSimbolos t = atual();
        if (t == null) {
            throw new ErroSintatico("Fim inesperado da entrada; esperado token do tipo " + tipoEsperado + ".");
        }
        if (!t.getTipo().equals(tipoEsperado)) {
            throw new ErroSintatico(descreverErro(t, "esperado " + tipoEsperado));
        }
        posicao++;
        return new NoArvore(rotuloNo, t);
    }

    private boolean tipoAtualEh(String tipo) {
        ReconhecedorAFD.EntradaTabelaSimbolos t = atual();
        return t != null && t.getTipo().equals(tipo);
    }

    private String descreverErro(ReconhecedorAFD.EntradaTabelaSimbolos t, String detalhe) {
        return "Erro sintatico: token \"" + t.getToken() + "\" (tipo " + t.getTipo()
                + ") na linha " + t.getLinha() + ", coluna " + t.getColuna() + " - " + detalhe + ".";
    }

    /**
     * Ponto de entrada: tenta reconhecer UMA declaracao completa
     * (Declara -> ... [PV]) a partir da posicao atual, retornando a
     * subarvore correspondente ao no "Declara".
     * Lanca ErroSintatico se a sequencia nao for valida.
     */
    public NoArvore parseDeclaracao() throws ErroSintatico {
        NoArvore noDeclara = new NoArvore("Declara");

        // [TIPO]
        ReconhecedorAFD.EntradaTabelaSimbolos tipoTok = atual();
        if (tipoTok == null || !TIPOS_VALIDOS.contains(tipoTok.getTipo())) {
            if (tipoTok == null) {
                throw new ErroSintatico("Fim inesperado da entrada; esperado uma palavra reservada de tipo (int, char, float, double, void, boolean).");
            }
            throw new ErroSintatico(descreverErro(tipoTok, "esperado palavra reservada de tipo (int, char, float, double, void, boolean)"));
        }
        posicao++; // consome [TIPO]
        noDeclara.addFilho(new NoArvore("[TIPO]", tipoTok));

        // [NOMEVARIAVEL]
        noDeclara.addFilho(consumir("NOMEVARIAVEL", "[NOMEVARIAVEL]"));

        // Inicializacao -> [ATRIBUICAO][VALOR] | epsilon
        noDeclara.addFilho(parseInicializacao());

        // DeclaraMultiplo* -> ([VG][NOMEVARIAVEL] Inicializacao)*
        while (tipoAtualEh("VIRGULA")) {
            NoArvore noMultiplo = new NoArvore("DeclaraMultiplo");
            posicao++; // consome [VG] (nao guardamos o token da virgula na arvore por simplicidade visual)
            noMultiplo.addFilho(consumir("NOMEVARIAVEL", "[NOMEVARIAVEL]"));
            noMultiplo.addFilho(parseInicializacao());
            noDeclara.addFilho(noMultiplo);
        }

        // [PV]
        noDeclara.addFilho(consumir("PONTO_VIRGULA", "[PV]"));

        return noDeclara;
    }

    /**
     * Inicializacao -> [ATRIBUICAO][VALOR] | epsilon
     * Sempre retorna um no "Inicializacao" (com filhos se houve atribuicao,
     * ou vazio representando epsilon).
     */
    private NoArvore parseInicializacao() throws ErroSintatico {
        NoArvore noInit = new NoArvore("Inicializacao");
        if (tipoAtualEh("ATRIBUICAO")) {
            ReconhecedorAFD.EntradaTabelaSimbolos atrib = atual();
            posicao++; // consome [ATRIBUICAO]
            noInit.addFilho(new NoArvore("[ATRIBUICAO]", atrib));

            ReconhecedorAFD.EntradaTabelaSimbolos valor = atual();
            if (valor == null) {
                throw new ErroSintatico("Fim inesperado da entrada; esperado um valor (INTEIRO, FRACIONARIO ou NOMEVARIAVEL) apos '='.");
            }
            if (!VALORES_VALIDOS.contains(valor.getTipo())) {
                throw new ErroSintatico(descreverErro(valor, "esperado um valor (INTEIRO, FRACIONARIO ou NOMEVARIAVEL) apos '='"));
            }
            posicao++; // consome [VALOR]
            noInit.addFilho(new NoArvore("[VALOR]", valor));
        } else {
            noInit.addFilho(new NoArvore("epsilon"));
        }
        return noInit;
    }

    /**
     * Analisa a tabela de simbolos completa como uma sequencia de
     * declaracoes (uma apos a outra). Retorna a lista de subarvores
     * "Declara", uma por declaracao reconhecida; lanca ErroSintatico na
     * primeira declaracao invalida.
     */
    public List<NoArvore> parseTodasDeclaracoes() throws ErroSintatico {
        List<NoArvore> declaracoes = new ArrayList<>();
        while (atual() != null) {
            declaracoes.add(parseDeclaracao());
        }
        return declaracoes;
    }

    /**
     * Metodo de conveniencia: roda o parser sobre a tabela de simbolos
     * inteira, imprime o resultado (OK/FALHOU) e, em caso de sucesso,
     * imprime a arvore sintatica de cada declaracao reconhecida.
     */
    public static void validar(List<ReconhecedorAFD.EntradaTabelaSimbolos> tabela) {
        AnalisadorSintatico parser = new AnalisadorSintatico(tabela);
        try {
            List<NoArvore> declaracoes = parser.parseTodasDeclaracoes();
            System.out.println("Analise sintatica: OK (" + declaracoes.size() + " declaracao(oes) reconhecida(s)).");
            for (int i = 0; i < declaracoes.size(); i++) {
                System.out.println("\nArvore sintatica - declaracao " + (i + 1) + ":");
                declaracoes.get(i).imprimir();
            }
        } catch (ErroSintatico e) {
            System.out.println("Analise sintatica: FALHOU");
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) {
        ReconhecedorAFD afd = new ReconhecedorAFD();
        String caminhoConfig = "AFD_config.txt";
        String caminhoEntrada = "input.c";

        try {
            afd.carregarConfiguracao(caminhoConfig);
            afd.processarArquivo(caminhoEntrada);
            System.out.println();
            validar(afd.getTabelaSimbolos());
        } catch (java.io.IOException e) {
            System.out.println("Erro ao ler arquivo: " + e.getMessage());
        }
    }
}
