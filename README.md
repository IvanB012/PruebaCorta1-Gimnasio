# Prueba Corta 1 — Gimnasio

**Curso:** ISW-623 — Base de Datos Avanzadas  
**Institución:** Universidad Técnica Nacional (UTN)  
**Integrantes:** Iván Barboza Blanco y Wilberth  
**Caso asignado:** 9 — Gimnasio

## Descripción

Proyecto académico para analizar consultas, índices y planes de ejecución en PostgreSQL y MongoDB, además de operaciones con sesiones y contadores en Redis.

## Parámetros personalizados

| Parámetro | Valor |
|---|---|
| Carnés | 208820443 y 208830343 |
| Caso | 9 — Gimnasio |
| País | CO |
| Edad | 50 |
| Año | 2024 |
| Monto | 150 |
| Usuario Redis | u241 |
| Código de integridad | 316164E0 |

## Distribución del trabajo

**Iván — PostgreSQL (Parte B)**

- B1: Conteo de afiliados y pagos.
- B2: Consulta JOIN y plan de ejecución inicial.
- B3: Creación de índices y comparación de rendimiento.
- B4: Identificación y corrección de antipatrones SQL.

**Wilberth — MongoDB y Redis (Parte A)**

- A1: Consulta de filtrado.
- A2: Agregación por país.
- A3: Análisis de índices mediante `explain`.
- A4: Sesiones, contadores y expiración en Redis.

**Trabajo conjunto**

- C1: Comparación entre los tres motores.
- C2: Reflexión técnica.
- C3: Organización del informe.
- Grabación del video demostrativo.

## Requisitos

- Docker Desktop.
- Contenedores PostgreSQL, MongoDB y Redis configurados para la práctica.
- Python 3 para regenerar los datos.
- Git y Visual Studio Code.

## Preparación de los datos

Los archivos personalizados se encuentran en `datos/`.

Para regenerarlos:

```powershell
python generar_dataset.py 208830343 208820443 9
```

Antes de ejecutar los comandos de `datos/cargar.txt`, verificar que los contenedores estén funcionando y que no contengan información que deba conservarse.

Los comandos de carga del profesor están escritos para una terminal compatible con redirección `<`. En PowerShell deben adaptarse cuando sea necesario.

## Organización

- `datos/`: archivos generados para la pareja.
- `consultas/postgresql/`: consultas de Iván.
- `consultas/mongodb/`: consultas de Wilberth.
- `consultas/redis/`: comandos de Wilberth.
- `evidencias/`: capturas de pantalla de ambos.
- `informe/`: documentación final.
- `video/`: guion y preparación de la demostración.

## Flujo de trabajo

Cada integrante trabaja en su propia rama de Git y sube sus avances al repositorio.

Las ramas se integrarán a `main` después de revisar los resultados y evidencias.

**Importante:** No crear índices antes de registrar los planes de ejecución iniciales. Las comparaciones de rendimiento deben realizarse con resultados reales.