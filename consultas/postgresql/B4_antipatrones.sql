-- ==========================================
-- PRUEBA CORTA 1 - CASO 9: GIMNASIO
-- B4 - ANTIPATRONES Y OPTIMIZACION SQL
-- ==========================================

-- ANTIPATRON 1: EXTRACT(YEAR FROM fecha)
-- Aplica una funcion sobre la columna fecha.

EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM pagos
WHERE estado = 'ACREDITADO'
  AND EXTRACT(YEAR FROM fecha) = 2024;


-- VERSION OPTIMIZADA: RANGO DE FECHAS
-- Permite aprovechar el indice compuesto.

EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM pagos
WHERE estado = 'ACREDITADO'
  AND fecha >= DATE '2024-01-01'
  AND fecha < DATE '2025-01-01';


-- VERIFICACION DE EQUIVALENCIA
-- Ambas consultas deben devolver 63407.

SELECT
    (
        SELECT COUNT(*)
        FROM pagos
        WHERE estado = 'ACREDITADO'
          AND EXTRACT(YEAR FROM fecha) = 2024
    ) AS conteo_extract,
    (
        SELECT COUNT(*)
        FROM pagos
        WHERE estado = 'ACREDITADO'
          AND fecha >= DATE '2024-01-01'
          AND fecha < DATE '2025-01-01'
    ) AS conteo_rango;


-- ANTIPATRON 2: SELECT *
-- Recupera todas las columnas, aunque no
-- sean necesarias para el resultado.

EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM pagos
WHERE estado = 'ACREDITADO'
  AND fecha >= DATE '2024-01-01'
  AND fecha < DATE '2025-01-01';


-- VERSION OPTIMIZADA: COLUMNAS ESPECIFICAS
-- El indice contiene las columnas solicitadas.

EXPLAIN (ANALYZE, BUFFERS)
SELECT afiliado_id, fecha, estado
FROM pagos
WHERE estado = 'ACREDITADO'
  AND fecha >= DATE '2024-01-01'
  AND fecha < DATE '2025-01-01';


-- ==========================================
-- RESULTADOS REGISTRADOS
-- ==========================================

-- COMPARACION 1: EXTRACT VS RANGO
-- EXTRACT:
-- Execution Time: 35.511 ms
-- Operador: Parallel Seq Scan
--
-- RANGO:
-- Execution Time: 12.423 ms
-- Operador: Index Only Scan
-- Heap Fetches: 0
--
-- Conteos: 63407 en ambas consultas.
-- Reduccion del tiempo: aproximadamente 65.02 %


-- COMPARACION 2: SELECT * VS COLUMNAS
-- SELECT *:
-- Execution Time: 26.279 ms
-- Operador: Bitmap Heap Scan
--
-- COLUMNAS ESPECIFICAS:
-- Execution Time: 16.464 ms
-- Operador: Index Only Scan
-- Heap Fetches: 0
--
-- Filas seleccionadas: 63407 en ambos casos.
-- La segunda consulta devuelve menos columnas.
-- Reduccion del tiempo: aproximadamente 37.35 %

-- NOTA:
-- Los tiempos corresponden a ejecuciones reales
-- de la practica y pueden variar al repetirlas.