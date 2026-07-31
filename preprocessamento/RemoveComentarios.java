import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class RemoveComentarios {

    public static String remover(String codigo) {

        StringBuilder sb = new StringBuilder();

        int n = codigo.length();
        int i = 0;

        boolean dentroString = false;
        boolean dentroChar = false;

        while (i < n) {

            char atual = codigo.charAt(i);
            char proximo = (i + 1 < n) ? codigo.charAt(i + 1) : '\0';

            if (dentroString) {

                sb.append(atual);

                if (atual == '\\' && i + 1 < n) {
                    sb.append(proximo);
                    i += 2;
                    continue;
                }

                if (atual == '"') {
                    dentroString = false;
                }

                i++;
                continue;
            }

            if (dentroChar) {

                sb.append(atual);

                if (atual == '\\' && i + 1 < n) {
                    sb.append(proximo);
                    i += 2;
                    continue;
                }

                if (atual == '\'') {
                    dentroChar = false;
                }

                i++;
                continue;
            }

            if (atual == '"') {

                dentroString = true;
                sb.append(atual);
                i++;

                continue;
            }

            if (atual == '\'') {

                dentroChar = true;
                sb.append(atual);
                i++;

                continue;
            }

            if (atual == '/' && proximo == '/') {

                sb.append(' ');
                sb.append(' ');

                i += 2;

                while (i < n && codigo.charAt(i) != '\n') {

                    if (codigo.charAt(i) == '\r') {
                        sb.append('\r');
                    } else {
                        sb.append(' ');
                    }

                    i++;
                }

                if (i < n && codigo.charAt(i) == '\n') {
                    sb.append('\n');
                    i++;
                }

                continue;
            }

            if (atual == '/' && proximo == '*') {

                sb.append(' ');
                sb.append(' ');

                i += 2;

                while (i < n) {

                    char c = codigo.charAt(i);

                    if (c == '*' &&
                        i + 1 < n &&
                        codigo.charAt(i + 1) == '/') {

                        sb.append(' ');
                        sb.append(' ');

                        i += 2;

                        break;
                    }

                    if (c == '\n') {
                        sb.append('\n');
                    } else if (c == '\r') {
                        sb.append('\r');
                    } else {
                        sb.append(' ');
                    }

                    i++;
                }

                continue;
            }

            sb.append(atual);
            i++;
        }

        return sb.toString();
    }

    public static void main(String[] args) throws IOException {

        if (args.length < 1) {

            System.out.println(
                "Uso: java RemoveComentarios <arquivo-entrada> [arquivo-saida]"
            );

            return;
        }

        Path entrada = Path.of(args[0]);

        String codigo = Files.readString(entrada);

        String resultado = remover(codigo);

        if (args.length >= 2) {

            Path saida = Path.of(args[1]);

            Files.writeString(saida, resultado);

            System.out.println("Arquivo salvo em: " + saida);

        } else {

            System.out.println(resultado);
        }
    }
}
