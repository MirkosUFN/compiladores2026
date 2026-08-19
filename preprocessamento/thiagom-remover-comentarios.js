const fs = require("fs");
const path = require("path");

/**
 * Remove comentários // e /* ... *\/ de um código C,
 * preservando exatamente o número de linhas e colunas.
 */
function removerComentariosC(codigoC) {
  const resultado = [];
  let i = 0;
  const n = codigoC.length;

  // Estados da máquina
  const IN_NORMAL = 0;
  const IN_STRING = 1;
  const IN_CHAR = 2;
  const IN_LINE_COMMENT = 3;
  const IN_BLOCK_COMMENT = 4;

  let estado = IN_NORMAL;

  while (i < n) {
    const char = codigoC[i];
    const proximo = i + 1 < n ? codigoC[i + 1] : "";

    // --- ESTADO 0: CÓDIGO NORMAL ---
    if (estado === IN_NORMAL) {
      if (char === '"') {
        estado = IN_STRING;
        resultado.push(char);
        i += 1;
      } else if (char === "'") {
        estado = IN_CHAR;
        resultado.push(char);
        i += 1;
      } else if (char === "/" && proximo === "/") {
        estado = IN_LINE_COMMENT;
        resultado.push(" "); // Substitui '/' por espaço
        resultado.push(" "); // Substitui '/' por espaço
        i += 2;
      } else if (char === "/" && proximo === "*") {
        estado = IN_BLOCK_COMMENT;
        resultado.push(" "); // Substitui '/' por espaço
        resultado.push(" "); // Substitui '*' por espaço
        i += 2;
      } else {
        resultado.push(char);
        i += 1;
      }

      // --- ESTADO 1: DENTRO DE UMA STRING "..." ---
    } else if (estado === IN_STRING) {
      resultado.push(char);
      // Ignora aspas escapadas como \"
      if (char === "\\" && i + 1 < n) {
        resultado.push(codigoC[i + 1]);
        i += 2;
      } else if (char === '"') {
        estado = IN_NORMAL;
        i += 1;
      } else {
        i += 1;
      }

      // --- ESTADO 2: DENTRO DE UM CARACTERE '...' ---
    } else if (estado === IN_CHAR) {
      resultado.push(char);
      // Ignora aspas escapadas como \'
      if (char === "\\" && i + 1 < n) {
        resultado.push(codigoC[i + 1]);
        i += 2;
      } else if (char === "'") {
        estado = IN_NORMAL;
        i += 1;
      } else {
        i += 1;
      }

      // --- ESTADO 3: COMENTÁRIO DE LINHA // ---
    } else if (estado === IN_LINE_COMMENT) {
      if (char === "\n") {
        estado = IN_NORMAL;
        resultado.push("\n"); // Mantém a quebra de linha
      } else {
        resultado.push(" "); // Troca cada caractere por espaço
      }
      i += 1;

      // --- ESTADO 4: COMENTÁRIO DE BLOCO /* ... *\/ ---
    } else if (estado === IN_BLOCK_COMMENT) {
      if (char === "*" && proximo === "/") {
        estado = IN_NORMAL;
        resultado.push(" "); // Troca '*' por espaço
        resultado.push(" "); // Troca '/' por espaço
        i += 2;
      } else if (char === "\n") {
        resultado.push("\n"); // Mantém o \n para não alterar número da linha
        i += 1;
      } else {
        resultado.push(" "); // Troca o texto por espaço
        i += 1;
      }
    }
  }

  return resultado.join("");
}

/** Lê o arquivo .c informado, remove os comentários e grava o resultado. */
function processarArquivo(caminhoEntrada) {
  if (!caminhoEntrada) {
    console.error("Uso: node remover-comentarios.js <arquivo.c>");
    process.exit(1);
  }

  if (!fs.existsSync(caminhoEntrada)) {
    console.error(`Arquivo não encontrado: ${caminhoEntrada}`);
    process.exit(1);
  }

  const extensao = path.extname(caminhoEntrada);
  const nomeBase = caminhoEntrada.slice(0, caminhoEntrada.length - extensao.length);
  const caminhoSaida = `${nomeBase}_sem_comentarios${extensao}`;

  let conteudo;
  try {
    conteudo = fs.readFileSync(caminhoEntrada, "utf-8");
  } catch {
    conteudo = fs.readFileSync(caminhoEntrada, "latin1");
  }

  const codigoLimpo = removerComentariosC(conteudo);

  fs.writeFileSync(caminhoSaida, codigoLimpo, "utf-8");

  console.log("Sucesso!");
  console.log("Comentários removidos do arquivo C.");
  console.log(`Salvo em: ${path.basename(caminhoSaida)}`);
}

if (require.main === module) {
  const caminhoEntrada = process.argv[2];
  processarArquivo(caminhoEntrada);
}

module.exports = { removerComentariosC };
