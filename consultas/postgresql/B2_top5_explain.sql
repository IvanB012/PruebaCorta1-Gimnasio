-- ==========================================
-- PRUEBA CORTA 1 - CASO 9: GIMNASIO
-- B2 - TOP 5 AFILIADOS Y EXPLAIN INICIAL
-- ==========================================

-- Parametros:
-- Pais: CO
-- Anio: 2024
-- Estado: ACREDITADO

-- 1. Consulta principal: Top 5 de afiliados
-- con mayor monto acreditado durante 2024.

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


-- 2. Plan de ejecucion inicial.
-- IMPORTANTE:
-- Este EXPLAIN se registro ANTES de crear
-- los indices adicionales de B3.
-- Ejecutarlo ahora no reproducira el plan
-- original porque los indices ya existen.

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