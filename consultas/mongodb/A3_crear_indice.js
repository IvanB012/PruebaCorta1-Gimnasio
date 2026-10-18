// A3 - Indice compuesto: igualdad por pais primero, rango por edad despues
db = db.getSiblingDB("pc1");

print("Indice creado:", db.afiliados.createIndex({ pais: 1, edad: 1 }));
print("Indices existentes:", JSON.stringify(db.afiliados.getIndexes().map(i => i.name)));
