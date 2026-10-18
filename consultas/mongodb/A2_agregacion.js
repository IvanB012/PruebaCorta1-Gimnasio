// A2 - Total de afiliados por pais, de mayor a menor (empate: pais ascendente)
db = db.getSiblingDB("pc1");

db.afiliados.aggregate([
  { $group: { _id: "$pais", total: { $sum: 1 } } },
  { $sort: { total: -1, _id: 1 } }
]).forEach(d => print(JSON.stringify(d)));
