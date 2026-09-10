const { readFileSync, writeFileSync } = require("fs");
const { join } = require("path");

const ARQUIVO_AFD = join(__dirname, "AFD_config.txt");
const ARQUIVO_ENTRADA = join(__dirname, "input.c");
const ARQUIVO_SAIDA = join(__dirname, "tabSimbolos.json");

const estados = [];
const estadosFinais = [];
const simbolos = [];
const regras_transicao = [];

const config = readFileSync(ARQUIVO_AFD)
  .toString()
  .split("\n")
  .filter((l) => l.trim() !== "");

const linhaEstados = config[0].trim().split(" ");
estados.push(...linhaEstados);
const estadoInicial = linhaEstados[0];

const linhaSimbolos = config[1].trim().split(" ");
simbolos.push(...linhaSimbolos);

const linhaEstadosFinais = config[2].trim().split(" ");
estadosFinais.push(...linhaEstadosFinais.map((e) => e.split(":")[0]));

const tipoPorEstadoFinal = {};
for (const par of linhaEstadosFinais) {
  const [estado, tipo] = par.split(":");
  tipoPorEstadoFinal[estado] = tipo;
}

const linhasRegras = config.slice(3);
for (const linha of linhasRegras) {
  regras_transicao.push(...linha.trim().split(" "));
}

const transicoes = {};
for (const regra of regras_transicao) {
  const [origem, simbolo, destino] = regra.split(":");
  if (!transicoes[origem]) transicoes[origem] = {};
  transicoes[origem][simbolo] = destino;
}

const tipoDoTermo = (termo) => {
  let estadoAtual = estadoInicial;

  for (const simbolo of termo) {
    const proximoEstado = transicoes[estadoAtual]?.[simbolo];
    if (!proximoEstado) return null;
    estadoAtual = proximoEstado;
  }

  return estadosFinais.includes(estadoAtual)
    ? tipoPorEstadoFinal[estadoAtual]
    : null;
};

const fonte = readFileSync(ARQUIVO_ENTRADA);
const codigoFonte = fonte.toString().split("\n");

console.log(
  `${fonte.length} bytes\nProcessando ${codigoFonte.length} linhas do arquivo ${ARQUIVO_ENTRADA}...`
);

const tabSimbolos = [];
let proximoId = 1;

codigoFonte.forEach((linha, indice) => {
  const numeroDaLinha = indice + 1;
  let i = 0;

  while (i < linha.length) {
    if (/\s/.test(linha[i])) {
      i++;
      continue;
    }

    const coluna = i + 1;
    let j = i;
    while (j < linha.length && !/\s/.test(linha[j])) {
      j++;
    }

    const termo = linha.slice(i, j);
    const tipo = tipoDoTermo(termo);

    if (tipo) {
      tabSimbolos.push({
        id: proximoId++,
        token: termo,
        tipo,
        linha: numeroDaLinha,
        coluna,
      });
    }

    i = j;
  }
});

writeFileSync(ARQUIVO_SAIDA, JSON.stringify(tabSimbolos, null, 2));
console.log(
  `Tabela de simbolos gerada em ${ARQUIVO_SAIDA} (${tabSimbolos.length} tokens reconhecidos).`
);
