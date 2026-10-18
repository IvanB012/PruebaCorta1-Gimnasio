// A1 - Afiliados de Colombia (CO), mayores de 50 anios y activos
// Base pc1, coleccion afiliados (Caso 9 - Gimnasio)
db = db.getSiblingDB("pc1");

const totalA1 = db.afiliados.countDocuments({ pais: "CO", edad: { $gt: 50 }, activo: true });
print("Afiliados CO, edad > 50, activos:", totalA1);
