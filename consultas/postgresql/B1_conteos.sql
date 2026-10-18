-- ==========================================
-- PRUEBA CORTA 1 - CASO 9: GIMNASIO
-- B1 - CONTEO DE REGISTROS
-- ==========================================

-- Cantidad total de afiliados
SELECT COUNT(*) AS total_afiliados
FROM afiliados;

-- Cantidad total de pagos
SELECT COUNT(*) AS total_pagos
FROM pagos;

-- Verificacion conjunta de los registros
SELECT
    (SELECT COUNT(*) FROM afiliados) AS total_afiliados,
    (SELECT COUNT(*) FROM pagos) AS total_pagos;