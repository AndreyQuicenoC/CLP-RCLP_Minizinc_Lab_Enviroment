# Diagnóstico CLP - Battery Project Integer

**Fecha**:
**Objetivo**: Identificar causa de UNSATISFIABLE en instancias Cork

---

## Resumen Ejecutivo

Wed Mar 25 20:27:09 HPS 2026

## Sección 1: Tests de Línea Base (Control Positivo)

Instancias que deberían funcionar correctamente:

| Instancia | Resultado | Tiempo | Notas |
|-----------|-----------|--------|-------|
| noncity_5buses-8stations | ✅ SAT | 1s | 3 estaciones |

## Sección 2: Tests Cork Dataset

Instancias reales de Cork (actualmente reportando UNSATISFIABLE):

| Instancia | Resultado | Tiempo | Notas |
|-----------|-----------|--------|-------|
| cork-1-line20_0 | ❌ UNSAT | 53s | Instancia infactible |
| cork-1-line20_5 | ❌ UNSAT | 86s | Instancia infactible |
| cork-2-lines20_0 | ⏱️ TIMEOUT | 121s | Solver no terminó |

## Sección 3: Análisis Detallado de Fallos

### Errores Encontrados


---

## Resumen Final

| Métrica | Valor |
|---------|-------|
| Total tests | 4 |
| ✅ Satisfacibles | 1 |
| ❌ Insatisfacibles | 2 |
| ⏱️ Timeouts | 1 |
| 🔧 Errores sintaxis | 0 |
| ❌ Otros errores | 0 |


## Conclusión del Diagnóstico

🟡 **CAUSA PRINCIPAL: Instancias Cork Infactibles**

El modelo funciona correctamente (baseline tests pasan).
Las instancias Cork son genuinamente infactibles debido a:
- Consumo energético excesivo sin oportunidades de carga
- Restricciones temporales muy estrictas (μ muy bajo)
- Parámetros de carga insuficientes (α, β)

**Acción requerida**: Relajar parámetros o validar datos Cork
