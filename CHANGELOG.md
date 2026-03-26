# Changelog

Todos los cambios significativos en este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [1.0.0] - 2026-03-25

### ✨ Características Principales

#### Agregado
- **Sistema Profesional de Generación de Instancias CLP**
  - Generador GUI interactivo con Tkinter
  - Algoritmo experto basado en análisis de instancias validadas
  - Validación automática con MiniZinc
  - Auto-corrección para instancias UNSAT
  - Gestión de expected results en JSON

- **Organización Profesional del Proyecto**
  - Scripts agrupados en 5 categorías funcionales
  - Documentación estructurada en 3 seções temáticas
  - README en cada directorio de scripts
  - Índices de navegación en documentación

- **Scripts de Generación y Validación**
  - `create_cork_variants.py` - Reducción de instancias Cork (full-day → single-cycle)
  - `convert_json_to_integer_dzn.py` - Conversión JSON → .dzn
  - `validate_integer_dzn.py` - Validación de integridad

- **Suite Completa de Testing**
  - `test_generator.sh` - 7 tests del sistema
  - `test_clp_preliminary.sh` - Tests preliminares
  - `run_battery_project_tests.py` - Suite Battery Project
  - Todos con reportes detallados

### 🔧 Modificaciones Técnicas

- Modelo CLP con restricciones mejoradas para manejo de depot
- Escalado ×10 de todos los valores para aritmética entera
- Manejo UTF-8 en todas las plataformas (Windows, Linux, macOS)

### 📚 Documentación

- Documentación completa del generador (600+ líneas)
- Análisis de infactibilidad de Cork
- Justificación de cambios del modelo
- Guía rápida de inicio
- Ejemplos de uso

### 🧪 Pruebas y Validación

- 100% de tests pasados (7/7)
- 3 instancias generadas validadas
- 5 variantes Cork creadas exitosamente
- Expected results storage para regression testing

## [0.9.0] - 2026-03-20 (Pre-release)

### Agregado
- Estructuras iniciales de proyectos
- Esquemas de datos básicos
- Primeras versiones de scripts

---

## Notas de Cambios

### Versión 1.0.0
**Hito**: Sistema completo y funcional

- ✅ Sistema de generación profesional
- ✅ Organización de proyecto limpia
- ✅ Documentación completa
- ✅ Suite de tests completa
- ✅ Ready for production use

### Cambios Futuros Planificados

#### [1.1.0] - Próxima Liberación
- [ ] Batch generation mode (generar N instancias)
- [ ] Custom parameter profiles
- [ ] Advanced constraints support
- [ ] Real-time route visualization
- [ ] CLI mode para automatización

#### [1.2.0] - Mejoras de Rendimiento
- [ ] Optimizaciones de algoritmo
- [ ] Caching de instancias generadas
- [ ] Parallelización de generación
- [ ] Reduced memory footprint

#### [2.0.0] - Expansión
- [ ] Integración con benchmark suite
- [ ] Soporte para múltiples modelos
- [ ] API REST para generación remota
- [ ] Interfaz web

---

## Resumen de Cambios Estructurales

### Reorganización de Proyecto (2026-03-25)

**Antes**:
```
Scripts/
├── *.py (11 scripts sueltos)
├── *.sh (3 scripts sueltos)
└── Generated System/
    ├── *.py
    └── *.sh
```

**Después**:
```
Scripts/
├── data-processing/    [*.py de conversión]
├── generation/         [create_cork_variants.py]
├── testing/           [tests y validación *.py *.sh]
├── setup/             [configuración *.py *.sh]
└── utilities/         [herramientas y diagnóstico]
```

### Documentación (2026-03-25)

**Antes**:
```
Docs/
├── Generated System/
├── Corrected/
└── Public/
```

**Después**:
```
Docs/
├── generated-system/  [sistema de generación]
├── model/            [documentación del modelo]
└── analysis/         [análisis y diagnóstico]
```

---

## Estabilidad de Versión

### API/Interface
- ✅ Generador GUI - Stable
- ✅ Scripts CLI - Stable
- ✅ Formato .dzn - Stable

### Performance
- ✅ Generación < 1s (sin MiniZinc)
- ✅ Validación < 30s (instancias normales)
- ✅ Suite tests ~ 2 minutos

### Compatibilidad
- ✅ Python 3.8+
- ✅ MiniZinc 2.5+
- ✅ Windows / Linux / macOS

---

## Incidentes Resueltos

| Problema | Causa | Solución | Versión |
|----------|-------|----------|---------|
| Cork UNSAT | Demasiadas paradas | Single-cycle reduction | 1.0.0 |
| Encoding errors | Windows console | UTF-8 config | 1.0.0 |
| Path issues | Espacios en nombres | Quoting | 1.0.0 |
| Algorithm UNSAT | Insuficientes stops | Buffer +2 stops | 1.0.0 |

---

**Nota**: Este archivo se actualiza con cada liberación significativa.

Para cambios no liberados, consultar commits recientes en Git.

*Última actualización: 2026-03-25*
