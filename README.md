# CLP-RCLP MiniZinc Lab Environment

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![MiniZinc](https://img.shields.io/badge/minizinc-2.5+-blue)

## 📋 Descripción

Entorno de laboratorio profesional para investigación y optimización del **problema de ubicación de carga (CLP)** y su extensión robusta **(RCLP)** para flotas de autobuses eléctricos.

Este proyecto incluye:
- ✅ Modelos matemáticos en MiniZinc (CLP y RCLP)
- ✅ Sistema profesional de generación de instancias de prueba
- ✅ Suite completa de testing automatizado
- ✅ Documentación técnica exhaustiva
- ✅ Conjuntos de datos variados (Cork, sintéticos, validados)

## 🎯 Características Principales

### 1. Modelos Matemáticos
- **CLP**: Ubicación óptima de estaciones de carga bajo condiciones normales
- **RCLP**: Versión robusta con resiliencia ante fallos

### 2. Sistema de Generación Automática
- Generador GUI con algoritmo experto
- Validación automática con MiniZinc
- Auto-corrección para instancias infactibles
- Almacenamiento de resultados esperados para testing

### 3. Conjuntos de Datos
- **Cork City** (Real): Instancias del caso irlandés
- **Noncity** (Validadas): Casos de prueba validados manualmente
- **Sintéticos** (Escalables): Instancias generadas proceduralmente
- **Variantas Cork** (Single-cycle): Reducción de instancias Cork

### 4. Suite de Testing
- 7 tests del sistema completo
- Tests preliminares y de validación
- Reportes detallados con estadísticas
- 100% pass rate en release

## 🚀 Inicio Rápido

### 1️⃣ Prerequisitos

```bash
# Python 3.8+
python --version

# MiniZinc 2.5+
minizinc --version

# Si no lo tienes, descargar de https://www.minizinc.org/
```

### 2️⃣ Setup Inicial

```bash
# Validar configuración
python Scripts/setup/setup_and_validate.py

# Generar variantes Cork (si es necesario)
python Scripts/generation/create_cork_variants.py

# Ejecutar tests
bash Scripts/testing/test_generator.sh
```

### 3️⃣ Usar el Generador

```bash
# GUI interactivo
python Generator/generator.py

# O desde línea de comandos
python Scripts/testing/test_initial_small_case.py
```

### 4️⃣ Ejecutar Modelo

```bash
# Test rápido con instancia validada
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Own/noncity_5buses-8stations.dzn

# Con instancia generada
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Generated/generated_1_5buses_8stations.dzn
```

## 📁 Estructura del Proyecto

```
CLP-RCLP Minizinc/
│
├── 📂 Models/                      # Modelos matemáticos
│   ├── clp_model.mzn              # Modelo CLP (principal)
│   ├── rclp_model.mzn             # Modelo RCLP (robusto)
│   └── clp_model_backup.mzn       # Backup
│
├── 📂 Data/                        # Conjuntos de datos
│   ├── Battery Project Integer/   # Cork (instancias reales)
│   ├── Battery Project Variant/   # Cork single-cycle
│   ├── Battery Generated/         # Instancias generadas
│   └── Battery Own/               # Noncity + sintéticas
│
├── 📂 Scripts/                     # Scripts organizados
│   ├── data-processing/           # Conversión y validación
│   ├── generation/                # Generación de variantes
│   ├── testing/                   # Suite de tests
│   ├── setup/                     # Setup e inicialización
│   ├── utilities/                 # Herramientas y diagnóstico
│   └── README.md                  # Guía de scripts
│
├── 📂 Generator/                   # Sistema de generación
│   ├── generator.py               # GUI interactivo
│   └── README_BUILD.md            # Instrucciones build
│
├── 📂 Docs/                        # Documentación
│   ├── generated-system/          # Sistema de generación
│   ├── model/                     # Documentación del modelo
│   ├── analysis/                  # Análisis y diagnóstico
│   └── README.md                  # Índice de documentación
│
├── 📂 Tests/                       # Resultados de tests
│
├── 📄 README.md                    # Este archivo
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Guía de contribución
├── 📄 CHANGELOG.md                 # Historial de cambios
└── 📄 .gitignore                   # Configuración Git
```

## 📚 Documentación

### Inicio Rápido
- **[Scripts/README.md](Scripts/README.md)** - Guía de scripts por funcionalidad
- **[Docs/README.md](Docs/README.md)** - Índice central de documentación
- **[Docs/generated-system/README.md](Docs/generated-system/README.md)** - Sistema de generación

### Documentación Técnica
- **[Docs/model/MathModel.tex](Docs/model/MathModel.tex)** - Formulación matemática
- **[Docs/model/PROJECT_SUMMARY.md](Docs/model/PROJECT_SUMMARY.md)** - Resumen del proyecto
- **[Docs/analysis/](Docs/analysis/)** - Análisis detallado

### Guías Específicas
- **[Generator/README_BUILD.md](Generator/README_BUILD.md)** - Compilar ejecutable
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de versiones

## 🔄 Flujos de Trabajo Típicos

### Generar Nuevas Instancias
```bash
python Generator/generator.py          # GUI interactivo
# o
python Scripts/generation/create_cork_variants.py  # Cork
```

### Validar Instancias Existentes
```bash
python Scripts/data-processing/validate_integer_dzn.py Data/Battery\ Generated/*.dzn
```

### Ejecutar Tests Completos
```bash
bash Scripts/testing/test_generator.sh    # Suite principal (recomendado)
python Scripts/testing/run_battery_project_tests.py  # Tests Battery
```

### Diagnosticar Problemas
```bash
python Scripts/setup/setup_and_validate.py  # Validar entorno
bash Scripts/utilities/diagnose_cork.sh    # Diagnosticar Cork
```

## 📊 Conjuntos de Datos

| Dataset | Origen | Instancias | Estado | Recomendación |
|---------|--------|-----------|--------|---------------|
| **Cork** | Real (Irlanda) | 182+ | Infactible* | RCLP o Ciclos únicos |
| **Cork Variants** | Reducido | 5 | Factible | Testing, Research |
| **Noncity** | Validadas | 10+ | Factible✅ | **Recomendado** |
| **Sintéticas** | Generadas | Variables | Factible✅ | **Recomendado** |
| **Generated** | Sistema Gen. | 3+ | Factible✅ | **Recomendado** |

*Cork es infactible para CLP básico. Ver [análisis](Docs/analysis/Cork_Infeasibility_Analysis.md)*

## 🧪 Estado de Testing

```
Total Tests:     7
Passed:          7 ✅
Failed:          0
Success Rate:    100%

Instancias Validadas:
  - Cork Variants:    5 (warning expected)
  - Generated:        3 (SATISFIABLE)
  - Noncity:         10+ (SATISFIABLE)
```

## 🛠️ Herramientas Empleadas

| Herramienta | Versión | Propósito |
|------------|---------|----------|
| MiniZinc | 2.5+ | Modelado de restricciones |
| Python | 3.8+ | Scripts de utilidad |
| Bash | Linux/macOS | Automation scripts |
| Git | Cualquiera | Versionamiento |

### Solvers Soportados
- ✅ Chuffed (recomendado)
- ✅ Gecode
- ✅ COIN-BC

## 📖 Conceptos Clave

### CLP (Charging Location Problem)
Problema base de programación por restricciones que determina la ubicación óptima de estaciones de carga minimizando número de estaciones mientras garantiza factibilidad operativa.

### RCLP (Robust CLP)
Extensión robusta que agrega resiliencia ante fallos potenciales en el sistema de carga.

### Escalado (×10)
Todos los valores se escalan por 10 para usar aritmética entera en MiniZinc, mejorando precisión numérica.

### Factibilidad
Una instancia es "factible" si existe una solución válida donde todos los buses completan sus rutas respetando restricciones.

## ❓ Preguntas Frecuentes

### ¿Dónde empiezo?
1. Ejecutar `bash Scripts/testing/test_generator.sh` primero
2. Revisar [Docs/README.md](Docs/README.md) para documentación
3. Usar `python Generator/generator.py` para crear instancias

### ¿Por qué Cork es infactible?
Cork contiene 13-14 ciclos diarios (~400-500 paradas) con consumo ~1700 kWh vs 80 kWh de capacidad útil. Requiere 3+ modelos RCLP o reducción a ciclos únicos.

### ¿Cómo genero instancias personalizadas?
Usar `python Generator/generator.py` (GUI) o modificar `Scripts/generation/` para automatización.

### ¿Dónde puedo ver los resultados esperados?
Ver `Data/Battery Generated/Expected Results/*.json`

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Leer [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork el repositorio
3. Crear rama: `git checkout -b feature/tu-feature`
4. Hacer commits descriptivos
5. Pull Request con descripción clara

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **AVISPA Research Team** - Investigación principal
- **Andrey Quiceño** - Development y mantenimiento

## 📞 Soporte

- 🐛 **Reportar Bugs**: [GitHub Issues](../../issues)
- 💬 **Preguntas**: Ver [Docs/README.md](Docs/README.md)
- 📚 **Documentación**: [Docs/](Docs/)

## 🎯 Roadmap Futuro

- [ ] Batch generation mode
- [ ] Custom parameter profiles
- [ ] CLI mode mejorado
- [ ] Real-time visualization
- [ ] Integración con benchmark suite
- [ ] API REST

## 📊 Estadísticas del Proyecto

- **Líneas de Código**: 2000+
- **Documentación**: 3000+ líneas
- **Tests Automatizados**: 7 test suites
- **Conjuntos de Datos**: 200+ instancias
- **Instancias Validadas**: 18+

---

**Versión**: 1.0.0
**Última Actualización**: 2026-03-25
**Estado**: ✅ Production Ready

## 📝 Nota Técnica

Todos los parámetros numéricos están escalados ×10 para usar aritmética entera:

- **Tiempo**: `4200` = 420.0 minutos = 7:00 AM
- **Energía**: `250` = 25.0 kWh
- **Capacidad**: `1000` = 100.0 kWh

## 📚 Referencias

Este proyecto se basa en la investigación publicada en:

- **JITS 2022**: Journal of Intelligent Transportation Systems
- **Modelo original**: Véase carpeta `JITS2022/`

[⬆ Volver arriba](#clp-rclp-minizinc-lab-environment)
