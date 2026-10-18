-- ==========================================
-- PRUEBA CORTA 1 - CASO 9: GIMNASIO
-- B3 - CREACION DE INDICES Y OPTIMIZACION
-- ==========================================

-- IMPORTANTE:
-- Los indices de este archivo ya fueron creados
-- durante la practica.
-- No volver a ejecutar CREATE INDEX sobre
-- la misma base de datos sin comprobar
-- previamente si existen.

-- 1. Indice compuesto para la tabla pagos.
-- Facilita el filtrado por estado y fecha,
-- incluyendo afiliado_id para la relacion JOIN.

CREATE INDEX idx_pagos_estado_fecha_afiliado
ON pagos (estado, fecha, afiliado_id);

-- 2. Indice para buscar afiliados por pais.

CREATE INDEX idx_afiliados_pais
ON afiliados (pais);

-- 3. Actualizar las estadisticas del optimizador.

ANALYZE afiliados;
ANALYZE pagos;

-- 4. Consulta optimizada: Top 5 de afiliados
-- con mayor monto acreditado durante 2024.

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    a.id AS afiliado_id,
    a.nombre,
    SUM(p.monto) AS total_acreditado
FROM afiliados AS a
INNER JOIN pagos AS p
    ON a.id = p.afiliado_id
WHERE a.pais = 'CO'
  AND p.estado = 'ACREDITADO'
  AND p.fecha >= DATE '2024-01-01'
  AND p.fecha < DATE '2025-01-01'
GROUP BY a.id, a.nombre
ORDER BY total_acreditado DESC, a.id ASC
LIMIT 5;

-- ==========================================
-- RESULTADOS REGISTRADOS
-- ==========================================

-- ANTES DE LOS INDICES:
-- Execution Time: 53.983 ms
-- Planning Time: 1.170 ms
-- Costo estimado final: 7014.95
-- Acceso a pagos: Parallel Seq Scan
-- Acceso a afiliados: Seq Scan

-- DESPUES DE LOS INDICES:
-- Execution Time: 28.920 ms
-- Planning Time: 0.755 ms
-- Costo estimado final: 5798.06
-- Acceso a pagos: Bitmap Index Scan + Bitmap Heap Scan
-- Acceso a afiliados: Bitmap Index Scan + Bitmap Heap Scan

-- REDUCCION DEL TIEMPO:
-- ((53.983 - 28.920) / 53.983) * 100
-- Resultado aproximado: 46.43 %