# Documentación del Modelo Matemático

Documentación técnica y formación matemática del modelo CLP-RCLP.

## 📁 Contenido

### Archivos Principales

- **MathModel.tex** - Formulación matemática completa en LaTeX
  - Definición de variables
  - Función objetivo
  - Restricciones
  - Parámetros

- **PROJECT_SUMMARY.md** - Resumen ejecutivo del proyecto
  - Objetivos
  - Alcance
  - Resultados

- **QUICKSTART.md** - Guía rápida para empezar
  - Instalación
  - Primer test
  - Ejemplos básicos

## 🔬 Estructura del Modelo

### Parámetros Principales

| Parámetro | Valor | Significado |
|-----------|-------|-----------|
| Cmax | 1000 | Capacidad máxima (100 kWh) |
| Cmin | 200 | Reserva mínima (20 kWh) |
| alpha | 100 | Tasa de carga (10 kWh/min) |
| mu | 50 | Máximo retraso (5 min) |

### Variables de Decisión

- `x_bi` - Binaria: ¿Se carga en parada (b,i)?
- `e_bi` - Continua: Energía al final de parada (b,i)
- `ct_bi` - Continua: Tiempo de carga en parada (b,i)

## 📊 Resultados Típicos

Para instancia noncity_5buses-8stations:
- **Total estaciones**: 3/8 instaladas
- **Desviación total**: ~1564
- **Tiempo de resolución**: < 1 segundo

## 🔗 Links Relacionados

- [Sistema de Generación](../generated-system/)
- [Análisis Detallado](../analysis/)
- [Modelo MiniZinc](../../Models/)

## 📚 Para Más Información

Ver la formulación completa en MathModel.tex (compilar con LaTeX).

**Última Actualización**: 2026-03-25
