# Análisis Detallado del Proyecto

Documentación de análisis, diagnóstico y problemas técnicos del proyecto CLP-RCLP.

## 📁 Contenido

### Archivos de Análisis

- **Cork_Infeasibility_Analysis.md** - Análisis de infactibilidad de Cork
  - Problema: Cork instances tienen 378-568 paradas
  - Impacto: Infactibles para modelo CLP estándar
  - Solución: Extracción single-cycle (42 paradas)

- **DataCorrections.md** - Registro de correcciones de datos
  - Problemas encontrados
  - Ajustes realizados
  - Validaciones aplicadas

- **ModelModificationJustification.md** - Justificación de cambios del modelo
  - Cambios al modelo MiniZinc
  - Razones técnicas
  - Impacto en resultados

- **CHECKLIST_FINAL.md** - Lista de verificación final
  - Requisitos completados
  - Tests pasados
  - Documentación lista

- **ProjectSummary.md** - Resumen del proyecto
- **INSTALLATION_SUCCESS.txt** - Registro de instalación exitosa

## 🔬 Problemas Técnicos Identificados

### Cork Infeasibility
- **Problema**: Instancias Cork originales tienen demasiadas paradas
- **Síntoma**: MiniZinc retorna UNSATISFIABLE
- **Causa**: Overconsumption > 2x capacity
- **Solución**: Reducir a single cycle (~42 paradas)

### Data Corrections
- **Formato**: Conversión JSON → .dzn con escalado ×10
- **Validación**: Rangos de parámetros correctos
- **Coherencia**: Arrays dimensionalmente consistentes

### Model Modifications
- **Cambios**: Agregadas restricciones para manejo de depot
- **Versión**: v2 con mejoras de factibilidad
- **Impacto**: +15% instancias SAT vs versión anterior

## 📊 Key Findings

| Aspecto | Hallazgo |
|---------|----------|
| Cork Feasibility | 0% → 100% después de single-cycle reduction |
| Generated Feasibility | 98%+ con algoritmo experto |
| Avg Resolution Time | < 5 segundos para instancias normales |
| Model Correctness | 100% de instancias noncity validadas |

## 🔗 Links Relacionados

- [Generación de Instancias](../generated-system/)
- [Documentación del Modelo](../model/)
- [Scripts de Diagnóstico](../../Scripts/setup/)

## 📚 Para Investigar Más

1. Revisar Cork_Infeasibility_Analysis.md para entender la problemática
2. Ver DataCorrections.md para cambios de datos
3. Consultar ModelModificationJustification.md para cambios técnicos

**Última Actualización**: 2026-03-25
