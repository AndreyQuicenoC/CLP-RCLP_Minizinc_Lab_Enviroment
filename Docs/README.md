# Documentación del Proyecto CLP-RCLP MiniZinc

Directorio central de documentación técnica, análisis y guías del proyecto CLP-RCLP.

## 📁 Estructura

```
Docs/
├── generated-system/       # Sistema de generación de instancias
│   ├── README.md          # Guía completa del generador
│   └── INDEX.md           # Índice y navegación
│
├── model/                 # Documentación del modelo matemático
│   ├── MathModel.tex      # Formulación LaTeX
│   ├── PROJECT_SUMMARY.md
│   ├── QUICKSTART.md
│   └── README.md          # Índice del modelo
│
├── analysis/              # Análisis y diagnóstico
│   ├── Cork_Infeasibility_Analysis.md
│   ├── DataCorrections.md
│   ├── ModelModificationJustification.md
│   ├── CHECKLIST_FINAL.md
│   └── README.md          # Índice de análisis
│
└── README.md              # Este archivo
```

## 🎯 Inicio Rápido por Tipo de Usuario

### 👨‍💼 Ejecutivo / Project Manager
1. Leer: `generated-system/README.md` (Overview seccion)
2. Ver: `model/PROJECT_SUMMARY.md`
3. Consultar: `analysis/CHECKLIST_FINAL.md`

### 👨‍💻 Desarrollador / Investigador
1. Empezar: `generated-system/README.md` (Quick Start)
2. Entender: `model/MathModel.tex`
3. Analizar: `analysis/Cork_Infeasibility_Analysis.md`
4. Implementar: Scripts en `../Scripts/`

### 🔬 Scientífico / Data Analyst
1. Revisar: `model/MathModel.tex`
2. Estudiar: `analysis/DataCorrections.md`
3. Investigar: `analysis/ModelModificationJustification.md`
4. Ejecutar: Scripts en `../Scripts/testing/`

## 📚 Documentos por Funcionalidad

### Sistema de Generación
**Archivo Principal**: `generated-system/README.md`

Contiene:
- Descripción del sistema
- Cómo generar instancias
- Algoritmo experto
- Troubleshooting
- Performance metrics

### Modelo Matemático
**Archivo Principal**: `model/MathModel.tex`

Contiene:
- Formulación completa
- Variables y restricciones
- Parámetros
- Ejemplos

Resumen ejecutivo: `model/PROJECT_SUMMARY.md`
Guía rápida: `model/QUICKSTART.md`

### Análisis Técnico
**Archivo Principal**: `analysis/README.md`

Contiene:
- Problemas de Cork
- Correcciones de datos
- Modificaciones del modelo
- Hallazgos clave

## 🔍 Búsqueda Rápida por Tema

### Cork Instances
- **Problema**: `analysis/Cork_Infeasibility_Analysis.md`
- **Solución**: `generated-system/README.md` (Cork Variants)

### Data Issues
- **Correcciones**: `analysis/DataCorrections.md`
- **Validación**: `generated-system/README.md` (Validation)

### Model Questions
- **Formulación**: `model/MathModel.tex`
- **Cambios**: `analysis/ModelModificationJustification.md`

### Generation System
- **Guía completa**: `generated-system/README.md`
- **Algoritmo**: `generated-system/README.md` (Algorithm Design)

### First Time Setup
- **Pasos**: `model/QUICKSTART.md`
- **Checklist**: `analysis/CHECKLIST_FINAL.md`

## 📋 Documentos por Formato

### Markdown (.md)
- `**/README.md` - Guías principales
- `**/INDEX.md` - Índices de navegación
- `analysis/*.md` - Análisis detallados

### LaTeX (.tex)
- `model/MathModel.tex` - Formulación matemática

### Text (.txt)
- `analysis/INSTALLATION_SUCCESS.txt` - Log de instalación

## 🔗 Enlaces Relacionados

- [Scripts del Proyecto](../Scripts/README.md)
- [Generator GUI](../Generator/README_BUILD.md)
- [Modelo MiniZinc](../Models/)
- [Datos](../Data/)

## 🤝 Contribuir

Para agregar documentación:
1. Determinar categoría (generated-system, model, analysis)
2. Crear archivo Markdown con nombre descriptivo
3. Agregar índice en el README.md correspondiente
4. Actualizar este archivo si es necesario

## 📊 Estado de Documentación

| Sección | Completa | Actualizada |
|---------|----------|-------------|
| generated-system/ | ✓ | Sí (2026-03-25) |
| model/ | ✓ | Sí (2026-03-25) |
| analysis/ | ✓ | Sí (2026-03-25) |
| Índices | ✓ | Sí (2026-03-25) |

## 📝 Historial de Cambios

- **2026-03-25**: Reorganización profesional de documentación
  - Estructurados en 3 categorías principales
  - Agregados índices de navegación
  - Actualizadas rutas de referencias

**Última Actualización**: 2026-03-25
