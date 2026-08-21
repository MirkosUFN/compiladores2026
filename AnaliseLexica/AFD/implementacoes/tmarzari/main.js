//Estados

const { readFileSync, writeFileSync } = require("fs");

//Estado inicial e final
const estados = [];
const estadosFinais = [];
const simbolos = [];
const regras_transicao = [];

//Abrindo o arquivo de config do AFD
const config = readFileSync("config.md");
const linhas = config
  .toString()
  .split("\n") //separa as linhas do arquivo
  .filter((l) => l.trim() !== ""); //remove as linhas vazias

//Linha 0: todos os estados (o primeiro é o estado inicial, por convenção)
const linhaEstados = linhas[0].trim().split(" ");
estados.push(...linhaEstados);
const estadoInicial = linhaEstados[0];

//Linha 1: todos os simbolos do alfabeto
const linhaSimbolos = linhas[1].trim().split(" ");
simbolos.push(...linhaSimbolos);

//Linha 2: todos os estados finais (formato Qx:NOME)
const linhaEstadosFinais = linhas[2].trim().split(" ");
estadosFinais.push(...linhaEstadosFinais.map((e) => e.split(":")[0]));

//Mapa estado final -> tipo (ex: Q1 -> INTEIRO)
const tipoPorEstadoFinal = {};
for (const par of linhaEstadosFinais) {
  const [estado, tipo] = par.split(":");
  tipoPorEstadoFinal[estado] = tipo;
}

//Linhas 3 em diante: regras de transicao (formato Qorigem:simbolo:Qdestino)
const linhasRegras = linhas.slice(3);
for (const linha of linhasRegras) {
  const regras = linha.trim().split(" ");
  regras_transicao.push(...regras);
}

//Mapa de transicoes: { "Qorigem": { "simbolo": "Qdestino" } }
const transicoes = {};
for (const regra of regras_transicao) {
  const [origem, simbolo, destino] = regra.split(":");
  if (!transicoes[origem]) transicoes[origem] = {};
  transicoes[origem][simbolo] = destino;
}

//Percorre o AFD com o termo inteiro e retorna o tipo do estado final
//alcancado (ex: "INTEIRO", "FRACIONÁRIO", "NOMEVARIAVEL") ou null se o
//termo nao for reconhecido.
const tipoDoTermo = (termo) => {
  let estadoAtual = estadoInicial;

  for (const simbolo of termo) {
    const proximoEstado = transicoes[estadoAtual]?.[simbolo];
    if (!proximoEstado) return null;
    estadoAtual = proximoEstado;
  }

  return estadosFinais.includes(estadoAtual)
    ? tipoPorEstadoFinal[estadoAtual]
    : null; // AFD terminou em um estado não final, termo não reconhecido
}

//Le o arquivo de entrada (um termo por linha) e monta a tabela de simbolos
const codigoFonte = readFileSync("numeros.txt")
  .toString()
  .split("\n");



const fonte = readFileSync("numeros.txt")

console.log(`${fonte.length} bytes \nProcessando ${codigoFonte.length} linhas do arquivo numeros.txt...`);

const tabSimbolos = [];
let proximoId = 1;

codigoFonte.forEach((linha, indice) => {
  const numeroDaLinha = indice + 1;

  for (const termo of linha.trim().split(" ")) {
    if (termo === "") continue;

    const tipo = tipoDoTermo(termo);
    if (!tipo) continue;

    tabSimbolos.push({
      id: proximoId++,
      token: termo,
      tipo,
      linha: numeroDaLinha,
    });
  }
});

writeFileSync("tabSimbolos.json", JSON.stringify(tabSimbolos, null, 2));
console.log(`Tabela de simbolos gerada em tabSimbolos.json (${tabSimbolos.length} tokens reconhecidos).`);

