#!/usr/bin/env python3
"""
ISW-623 Base de Datos Avanzadas - UTN Sede San Carlos
Prueba Corta 1 (practica, en casa): generador de dataset PERSONAL.

Uso (trabajo EN PAREJAS: ambos carnes; el orden no importa):
    python3 generar_dataset.py <carne1> <carne2> <caso 1-40>

Genera la carpeta datos_<carne1>_<carne2>/ con:
    postgres.sql   -> esquema + datos para PostgreSQL (con el vocabulario de su caso)
    <entidad>.json -> documentos para MongoDB (mongoimport --jsonArray)
    cargar.txt     -> comandos de carga listos para copiar
    redis.txt      -> comandos para Redis (redis-cli)
    ficha.txt      -> sus parametros personales y su codigo de integridad

El dataset depende SOLO de los carnes de la pareja: parejas distintas reciben datos,
parametros y respuestas distintos. Use los carnes reales de su pareja.
"""
import hashlib
import json
import os
import random
import sys
from datetime import date, timedelta

PAISES = ["CR", "PA", "MX", "CO", "GT", "HN", "SV", "NI", "DO", "EC"]
NOMBRES = ["Ana", "Luis", "Marta", "Pedro", "Iris", "Carlos", "Sofia", "Diego", "Laura", "Mateo",
           "Valeria", "Andres", "Camila", "Jose", "Daniela", "Miguel", "Paula", "Jorge", "Elena", "Raul"]
APELLIDOS = ["Rojas", "Gomez", "Solis", "Vargas", "Chaves", "Mora", "Jimenez", "Quesada", "Araya", "Soto",
             "Campos", "Salas", "Brenes", "Calderon", "Segura", "Alvarado", "Rivera", "Cordero", "Mendez", "Picado"]
ESTADOS = ["PAGADO", "PENDIENTE", "CANCELADO"]
INICIO = date(2023, 1, 1)
DIAS = (date(2026, 6, 30) - INICIO).days



# Un CASO de negocio por pareja (1-40). Solo cambia el VOCABULARIO (nombres de tablas, colecciones, columnas y estados);
# los datos y las respuestas de la pareja dependen unicamente de los carnes.
# (caso, entidad1 plural, entidad1 singular, entidad2 plural, columna de monto, estado OK, estado pendiente, estado negativo, descripcion)
CASOS = {
    1: ("Cooperativa de ahorro y credito", "asociados", "asociado", "movimientos", "monto", "APLICADO", "PENDIENTE", "RECHAZADO"),
    2: ("Cadena de farmacias", "clientes", "cliente", "ventas", "total", "PAGADA", "PENDIENTE", "ANULADA"),
    3: ("Clinica privada", "pacientes", "paciente", "citas", "costo", "ATENDIDA", "PROGRAMADA", "CANCELADA"),
    4: ("Transporte publico (autobuses)", "usuarios", "usuario", "viajes", "tarifa", "COMPLETADO", "EN_CURSO", "CANCELADO"),
    5: ("Aerolinea regional", "pasajeros", "pasajero", "reservas", "valor", "CONFIRMADA", "PENDIENTE", "CANCELADA"),
    6: ("Hotel", "huespedes", "huesped", "estancias", "total", "FACTURADA", "ABIERTA", "ANULADA"),
    7: ("Red de supermercados", "socios", "socio", "compras", "total", "PAGADA", "PENDIENTE", "DEVUELTA"),
    8: ("Universidad", "estudiantes", "estudiante", "matriculas", "costo", "PAGADA", "PENDIENTE", "ANULADA"),
    9: ("Gimnasio", "afiliados", "afiliado", "pagos", "monto", "ACREDITADO", "PENDIENTE", "RECHAZADO"),
    10: ("Empresa de telecomunicaciones", "suscriptores", "suscriptor", "recargas", "monto", "ACREDITADA", "PENDIENTE", "FALLIDA"),
    11: ("Marketplace de comercio electronico", "compradores", "comprador", "ordenes", "total", "ENTREGADA", "EN_TRANSITO", "CANCELADA"),
    12: ("Municipalidad", "contribuyentes", "contribuyente", "cobros", "monto", "PAGADO", "PENDIENTE", "ANULADO"),
    13: ("Distribuidora de electricidad", "abonados", "abonado", "facturas", "monto", "PAGADA", "PENDIENTE", "ANULADA"),
    14: ("Cadena de cines", "espectadores", "espectador", "entradas", "precio", "VENDIDA", "RESERVADA", "ANULADA"),
    15: ("Agroindustria (cooperativa de cafe)", "productores", "productor", "entregas", "valor", "LIQUIDADA", "PENDIENTE", "RECHAZADA"),
    16: ("Aseguradora", "asegurados", "asegurado", "reclamos", "monto", "PAGADO", "EN_REVISION", "RECHAZADO"),
    17: ("Emisor de tarjetas de credito", "tarjetahabientes", "tarjetahabiente", "consumos", "monto", "LIQUIDADO", "PENDIENTE", "CONTRACARGO"),
    18: ("Comida a domicilio", "clientes", "cliente", "entregas", "total", "ENTREGADO", "EN_RUTA", "CANCELADO"),
    19: ("Taller mecanico", "propietarios", "propietario", "servicios", "costo", "FACTURADO", "EN_PROCESO", "CANCELADO"),
    20: ("Plataforma de cursos en linea", "alumnos", "alumno", "inscripciones", "precio", "PAGADA", "PENDIENTE", "REEMBOLSADA"),
    21: ("Biblioteca universitaria", "lectores", "lector", "prestamos", "multa", "DEVUELTO", "PRESTADO", "EXTRAVIADO"),
    22: ("Parqueos publicos", "conductores", "conductor", "estacionamientos", "tarifa", "PAGADO", "ACTIVO", "ANULADO"),
    23: ("Empresa de mensajeria", "remitentes", "remitente", "envios", "valor", "ENTREGADO", "EN_TRANSITO", "DEVUELTO"),
    24: ("Concesion vial (peajes)", "titulares", "titular", "pasos", "tarifa", "COBRADO", "PENDIENTE", "EXONERADO"),
    25: ("Agencia de viajes", "viajeros", "viajero", "paquetes", "precio", "CONFIRMADO", "COTIZADO", "CANCELADO"),
    26: ("Acueducto rural (ASADA)", "consumidores", "consumidor", "lecturas", "cobro", "FACTURADA", "PENDIENTE", "ANULADA"),
    27: ("Estacion de servicio (flotas)", "titulares_flota", "titular_flota", "tanqueos", "monto", "FACTURADO", "PENDIENTE", "ANULADO"),
    28: ("Ferreteria con credito", "clientes_credito", "cliente_credito", "ventas_credito", "total", "SALDADA", "PENDIENTE", "ANULADA"),
    29: ("Veterinaria", "tutores", "tutor", "consultas", "costo", "COBRADA", "PENDIENTE", "ANULADA"),
    30: ("Academia de idiomas", "aprendices", "aprendiz", "mensualidades", "monto", "PAGADA", "PENDIENTE", "EXONERADA"),
    31: ("Empresa de reciclaje", "generadores", "generador", "recolecciones", "valor", "LIQUIDADA", "PROGRAMADA", "CANCELADA"),
    32: ("Feria del agricultor", "feriantes", "feriante", "ventas_feria", "total", "PAGADA", "PENDIENTE", "ANULADA"),
    33: ("Plataforma de video por suscripcion", "televidentes", "televidente", "suscripciones", "precio", "ACTIVA", "PENDIENTE", "CANCELADA"),
    34: ("Videojuegos en linea", "jugadores", "jugador", "compras_juego", "monto", "ACREDITADA", "PENDIENTE", "REEMBOLSADA"),
    35: ("Espacios de coworking", "miembros", "miembro", "reservas_sala", "tarifa", "FACTURADA", "PENDIENTE", "CANCELADA"),
    36: ("Organizacion de donaciones (ONG)", "donantes", "donante", "donaciones", "monto", "RECIBIDA", "PROMETIDA", "RECHAZADA"),
    37: ("Clinica odontologica", "consultantes", "consultante", "tratamientos", "costo", "FINALIZADO", "EN_CURSO", "CANCELADO"),
    38: ("Inmobiliaria (alquileres)", "inquilinos", "inquilino", "alquileres", "renta", "COBRADO", "PENDIENTE", "INCOBRABLE"),
    39: ("Servicio de taxis por aplicacion", "pasajeros_taxi", "pasajero_taxi", "carreras", "tarifa", "COMPLETADA", "EN_CURSO", "CANCELADA"),
    40: ("Alquiler de vehiculos", "arrendatarios", "arrendatario", "alquileres_auto", "total", "DEVUELTO", "EN_USO", "CANCELADO"),
}


def vocabulario(caso):
    """Nombres que usara la pareja. Sin caso -> nombres logicos del enunciado (clientes/pedidos/PAGADO)."""
    if caso is None:
        return {"caso": "(sin caso: nombres logicos)", "e1": "clientes", "e1s": "cliente", "e2": "pedidos", "monto": "monto",
                "ok": "PAGADO", "pend": "PENDIENTE", "neg": "CANCELADO"}
    c = CASOS[caso]
    return {"caso": c[0], "e1": c[1], "e1s": c[2], "e2": c[3], "monto": c[4], "ok": c[5], "pend": c[6], "neg": c[7]}


def clave_pareja(carnes):
    """Identificador estable de la pareja (independiente del orden)."""
    return "_".join(sorted(str(c).strip() for c in carnes))


def generar(carne):
    carne = str(carne).strip()   # para parejas: clave_pareja([c1, c2])
    seed = int(hashlib.sha256(("ISW623-PC1-" + carne).encode()).hexdigest(), 16) % (2 ** 63)
    rng = random.Random(seed)

    params = {
        "pais": rng.choice(PAISES),
        "edad": rng.randint(25, 50),
        "anio": rng.choice([2024, 2025]),
        "monto": rng.randint(100, 300),          # colones no; unidades monetarias
        "usuario": None,
    }
    n_clientes = rng.randint(5000, 8000)
    n_pedidos = rng.randint(250000, 400000)
    params["usuario"] = rng.randint(1, 300)

    clientes = []
    for cid in range(1, n_clientes + 1):
        clientes.append({
            "id": cid,
            "nombre": f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}",
            "pais": rng.choice(PAISES),
            "edad": rng.randint(18, 75),
            "activo": rng.random() < 0.85,
        })

    pedidos = []
    for pid in range(1, n_pedidos + 1):
        pedidos.append({
            "id": pid,
            "cliente_id": rng.randint(1, n_clientes),
            "fecha": (INICIO + timedelta(days=rng.randint(0, DIAS))).isoformat(),
            "monto_cent": rng.randint(500, 50000),   # centavos enteros: evita errores de redondeo
            "estado": rng.choices(ESTADOS, weights=[70, 20, 10])[0],
        })

    contador = rng.randint(1000, 9000)
    sesiones = {}
    for u in range(1, 301):
        sesiones[u] = {"usuario": f"u{u}", "pais": rng.choice(PAISES), "carrito": rng.randint(0, 9)}

    integridad = hashlib.sha256(
        f"{n_clientes}|{n_pedidos}|{sum(p['monto_cent'] for p in pedidos)}|{contador}".encode()
    ).hexdigest()[:8].upper()

    return {"params": params, "clientes": clientes, "pedidos": pedidos,
            "contador": contador, "sesiones": sesiones, "integridad": integridad,
            "n_clientes": n_clientes, "n_pedidos": n_pedidos}


def escribir(carne, d, caso=None):
    v = vocabulario(caso)
    e1, e1s, e2, mc = v["e1"], v["e1s"], v["e2"], v["monto"]
    emap = {"PAGADO": v["ok"], "PENDIENTE": v["pend"], "CANCELADO": v["neg"]}
    carpeta = f"datos_{carne}"
    os.makedirs(carpeta, exist_ok=True)

    with open(os.path.join(carpeta, "postgres.sql"), "w", encoding="utf-8") as f:
        f.write(f"DROP TABLE IF EXISTS {e2};\nDROP TABLE IF EXISTS {e1};\n")
        f.write(f"CREATE TABLE {e1} (id INT PRIMARY KEY, nombre TEXT NOT NULL, pais CHAR(2) NOT NULL, "
                "edad INT NOT NULL, activo BOOLEAN NOT NULL);\n")
        f.write(f"CREATE TABLE {e2} (id INT PRIMARY KEY, {e1s}_id INT NOT NULL REFERENCES {e1}(id), "
                f"fecha DATE NOT NULL, {mc} NUMERIC(10,2) NOT NULL, estado TEXT NOT NULL);\n")
        f.write(f"COPY {e1} (id, nombre, pais, edad, activo) FROM stdin;\n")
        for c in d["clientes"]:
            f.write(f"{c['id']}\t{c['nombre']}\t{c['pais']}\t{c['edad']}\t{'t' if c['activo'] else 'f'}\n")
        f.write("\\.\n")
        f.write(f"COPY {e2} (id, {e1s}_id, fecha, {mc}, estado) FROM stdin;\n")
        for p in d["pedidos"]:
            m = p["monto_cent"]
            f.write(f"{p['id']}\t{p['cliente_id']}\t{p['fecha']}\t{m // 100}.{m % 100:02d}\t{emap[p['estado']]}\n")
        f.write(f"\\.\nANALYZE {e1};\nANALYZE {e2};\n")

    with open(os.path.join(carpeta, f"{e1}.json"), "w", encoding="utf-8") as f:
        json.dump([{"_id": c["id"], "nombre": c["nombre"], "pais": c["pais"], "edad": c["edad"],
                    "activo": c["activo"]} for c in d["clientes"]], f, ensure_ascii=False)

    with open(os.path.join(carpeta, "redis.txt"), "w", encoding="utf-8") as f:
        f.write("FLUSHALL\n")
        for u, s_ in d["sesiones"].items():
            f.write(f"SET sesion:u{u} '{json.dumps(s_, separators=(',', ':'))}'\n")
        f.write(f"SET contador_visitas {d['contador']}\n")

    with open(os.path.join(carpeta, "cargar.txt"), "w", encoding="utf-8") as f:
        f.write(f"# Comandos de carga para su caso ({v['caso']}). Ejecutelos dentro de esta carpeta.\n")
        f.write("docker exec -i isw623_db psql -U estudiante -d laboratorio1 < postgres.sql\n")
        f.write(f"docker cp {e1}.json isw623_mongo:/tmp/{e1}.json\n")
        f.write(f"docker exec isw623_mongo mongoimport -u estudiante -p isw623 --authenticationDatabase admin "
                f"--db pc1 --collection {e1} --drop --jsonArray --file /tmp/{e1}.json\n")
        f.write("docker exec -i isw623_redis redis-cli < redis.txt\n")

    p = d["params"]
    with open(os.path.join(carpeta, "ficha.txt"), "w", encoding="utf-8") as f:
        f.write(f"FICHA DE LA PAREJA - Prueba Corta 1 - Carnes {carne.replace('_', ' y ')}\n")
        f.write("=" * 52 + "\n")
        f.write(f"CASO     = {caso if caso else '-'} - {v['caso']}\n")
        f.write(f"PAIS     = {p['pais']}\n")
        f.write(f"EDAD     = {p['edad']}\n")
        f.write(f"ANIO     = {p['anio']}\n")
        f.write(f"MONTO    = {p['monto']}\n")
        f.write(f"USUARIO  = u{p['usuario']}   (clave Redis: sesion:u{p['usuario']})\n")
        f.write(f"CODIGO DE INTEGRIDAD = {d['integridad']}\n")
        f.write("\nVOCABULARIO DE SU CASO (sustituya los nombres logicos del enunciado por estos):\n")
        f.write(f"  clientes (tabla y coleccion)  ->  {e1}\n")
        f.write(f"  pedidos (tabla)               ->  {e2}\n")
        f.write(f"  cliente_id (llave foranea)    ->  {e1s}_id\n")
        f.write(f"  monto (columna)               ->  {mc}\n")
        f.write(f"  estado PAGADO / PENDIENTE / CANCELADO  ->  {v['ok']} / {v['pend']} / {v['neg']}\n")
        f.write("\nCopie estos valores y el codigo de integridad en la portada de su informe.\n")
    return carpeta


def main():
    args = sys.argv[1:]
    if len(args) not in (2, 3) or not all(x.strip() for x in args) or args[0].strip() == args[1].strip():
        print("Uso: python3 generar_dataset.py <carne1> <carne2> <caso 1-40>   (trabajo en parejas)")
        sys.exit(1)
    caso = None
    if len(args) == 3:
        if not args[2].isdigit() or int(args[2]) not in CASOS:
            print("El caso debe ser un numero entre 1 y 40 (vea su asignacion en el Excel de casos).")
            sys.exit(1)
        caso = int(args[2])
    carne = clave_pareja(args[:2])
    d = generar(carne)
    carpeta = escribir(carne, d, caso)
    print(f"Dataset generado en ./{carpeta}/")
    print(open(os.path.join(carpeta, "ficha.txt"), encoding="utf-8").read())


if __name__ == "__main__":
    main()
