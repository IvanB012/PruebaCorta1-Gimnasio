// A3 - Plan de ejecucion de la consulta A1 con executionStats
// Se ejecuta ANTES y DESPUES de crear el indice { pais: 1, edad: 1 }
db = db.getSiblingDB("pc1");

print("Indices existentes:", JSON.stringify(db.afiliados.getIndexes().map(i => i.name)));

const plan = db.afiliados
  .find({ pais: "CO", edad: { $gt: 50 }, activo: true })
  .explain("executionStats");

// Recorre el winningPlan para mostrar las etapas anidadas (FETCH -> IXSCAN, o COLLSCAN)
const etapas = [];
let etapa = plan.queryPlanner.winningPlan;
while (etapa) {
  etapas.push(etapa.stage + (etapa.indexName ? " (" + etapa.indexName + ")" : ""));
  etapa = etapa.inputStage;
}

const stats = plan.executionStats;
print("winningPlan.stage    :", etapas.join(" -> "));
print("nReturned            :", stats.nReturned);
print("totalKeysExamined    :", stats.totalKeysExamined);
print("totalDocsExamined    :", stats.totalDocsExamined);
print("executionTimeMillis  :", stats.executionTimeMillis);
