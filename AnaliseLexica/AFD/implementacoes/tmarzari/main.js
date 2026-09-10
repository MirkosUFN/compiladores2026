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

const fonte = readFileSync(ARQUIVO_ENTRADA);
const codigoFonte = fonte.toString().split("\n");

console.log(
  `${fonte.length} bytes\nProcessando ${codigoFonte.length} linhas do arquivo ${ARQUIVO_ENTRADA}...`
);

const tabSimbolos = [];
let proximoId = 1;

codigoFonte.forEach((linha, indice) => {
  const numeroDaLinha = indice + 1;
  let estadoAtual = estadoInicial;
  let pilha = [];
  let colunaInicio = 1;
  let valido = true;

  const emitirToken = () => {
    if (pilha.length === 0) return;

    if (valido && estadosFinais.includes(estadoAtual)) {
      tabSimbolos.push({
        id: proximoId++,
        token: pilha.join(""),
        tipo: tipoPorEstadoFinal[estadoAtual],
        linha: numeroDaLinha,
        coluna: colunaInicio,
      });
    }

    pilha = [];
    estadoAtual = estadoInicial;
    valido = true;
  };

  for (let i = 0; i < linha.length; i++) {
    const char = linha[i];

    if (/\s/.test(char)) {
      emitirToken();
      continue;
    }

    if (pilha.length === 0) {
      colunaInicio = i + 1;
    }

    const proximoEstado = transicoes[estadoAtual]?.[char];
    if (!proximoEstado) {
      valido = false;
      pilha.push(char);
      continue;
    }

    pilha.push(char);
    estadoAtual = proximoEstado;
  }

  emitirToken();
});

// 32 
const palavrasReservadas = new Set([
  "auto",
  "break",
  "case",
  "char",
  "const",
  "continue",
  "default",
  "do",
  "double",
  "else",
  "enum",
  "extern",
  "float",
  "for",
  "goto",
  "if",
  "int",
  "long",
  "register",
  "return",
  "short",
  "signed",
  "sizeof",
  "static",
  "struct",
  "switch",
  "typedef",
  "union",
  "unsigned",
  "void",
  "volatile",
  "while",
]);

for (const simbolo of tabSimbolos) {
  if (
    simbolo.tipo === "NOMEVARIAVEL" &&
    palavrasReservadas.has(simbolo.token)
  ) {
    simbolo.tipo = "PALAVRARESERVA";
  }
}

writeFileSync(ARQUIVO_SAIDA, JSON.stringify(tabSimbolos, null, 2));
console.log(
  `Tabela de simbolos gerada em ${ARQUIVO_SAIDA} (${tabSimbolos.length} tokens reconhecidos).`
);
