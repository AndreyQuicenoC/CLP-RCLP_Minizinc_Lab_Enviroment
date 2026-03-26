# Scripts Directory

Colección de scripts para generación, validación, testing y utilidades del proyecto CLP-RCLP MiniZinc.

## 📁 Estructura

```
Scripts/
├── data-processing/        # Conversión y validación de datos
│   ├── convert_json_to_integer_dzn.py
│   ├── validate_integer_dzn.py
│   └── README.md
│
├── generation/            # Generación de variantes e instancias
│   ├── create_cork_variants.py
│   ├── generate_synthetic_data.py
│   └── README.md
│
├── testing/              # Suite de tests y validación
│   ├── test_generator.sh              ⭐ PRINCIPAL
│   ├── test_clp_preliminary.sh
│   ├── run_battery_project_tests.py
│   ├── test_initial_small_case.py
│   └── README.md
│
├── setup/               # Configuración inicial
│   ├── setup_and_validate.py
│   └── README.md
│
├── utilities/           # Scripts de diagnóstico y utilidad
│   ├── diagnose_cork.sh
│   └── README.md
│
└── README.md            # Este archivo
```

## 🚀 Workflow Rápido

### Primera vez usando el proyecto
```bash
# 1. Setup inicial
python setup/setup_and_validate.py

# 2. Generar variantes Cork (si es necesario)
python generation/create_cork_variants.py

# 3. Ejecutar suite de tests
bash testing/test_generator.sh
```

### Uso del generador interactivo
```bash
cd .. && python Generator/generator.py
```

### Desarrollo y testing
```bash
# Tests individuales
bash testing/test_clp_preliminary.sh
python testing/run_battery_project_tests.py

# Diagnóstico Cork
bash utilities/diagnose_cork.sh

# Validar datos existentes
python data-processing/validate_integer_dzn.py ../Data/Battery\ Generated/*.dzn
```

## 📋 Módulos por Funcionalidad

### 🔄 Conversión & Validación (data-processing/)
Convierte entre formatos y valida integridad de datos.
- `convert_json_to_integer_dzn.py` - JSON → .dzn (scaled ×10)
- `validate_integer_dzn.py` - Verifica correctness de .dzn

**Entrada**: JSON, `.dzn` sin validar
**Salida**: Datos validados, `.dzn` correctos

### 🎲 Generación (generation/)
Crea variantes de instancias existentes e instancias sintéticas.
- `create_cork_variants.py` - Crea Cork single-cycle desde full-day
- `generate_synthetic_data.py` - Genera instancias sintéticas aleatorias

**Entrada**: Instancias full-day, parámetros personalizados
**Salida**: Variantes factible (cycle único), instancias sintéticas

### ✅ Testing (testing/)
Valida el sistema completo.
- `test_generator.sh` ⭐ - Suite principal (7 tests)
- `test_clp_preliminary.sh` - Tests iniciales básicos
- `run_battery_project_tests.py` - Tests Battery project
- `test_initial_small_case.py` - Tests de caso pequeño

**Entrada**: Instancias .dzn
**Salida**: Reporte de tests

### ⚙️ Setup (setup/)
Configura el entorno.
- `setup_and_validate.py` - Valida requisitos y estructura

**Entrada**: Entorno del sistema
**Salida**: Reporte de configuración y sugerencias

### 🛠️ Utilidades (utilities/)
Funciones de diagnóstico.
- `diagnose_cork.sh` - Analiza problemas con instancias Cork

## 🔧 Dependencias Globales

```bash
# Python 3.8+
python --version

# MiniZinc 2.5+
minizinc --version

# Git (para versionamiento)
git --version
```

## 📚 Runbook: Casos de Uso

### Caso 1: Generar nuevas instancias Cork
```bash
# Si no existen variantes:
python generation/create_cork_variants.py

# Verificar que se crearon:
ls ../Data/Battery\ Project\ Variant/cork-*_1cycle.dzn
```

### Caso 2: Validar datos existentes
```bash
# Validar un archivo .dzn
python data-processing/validate_integer_dzn.py ../Data/sample.dzn

# Validar todos en un directorio
for f in ../Data/Battery\ Generated/*.dzn; do
  python data-processing/validate_integer_dzn.py "$f"
done
```

### Caso 3: Testing completo
```bash
# Suite principal (recomendado)
bash testing/test_generator.sh

# Si falla, diagnosticar
bash setup/diagnose_cork.sh
```

### Caso 4: Desarrollo de nuevas instancias
```bash
# 1. Generar datos sintéticos
python generation/generate_synthetic_data.py --buses 8 --stations 10 --output test.dzn

# 2. Validar
python data-processing/validate_integer_dzn.py test.dzn

# 3. Probar con MiniZinc
minizinc --solver chuffed ../Models/clp_model.mzn test.dzn
```

## 📖 Documentación

Para información detallada de cada módulo, ver:
- [data-processing/README.md](data-processing/README.md)
- [generation/README.md](generation/README.md)
- [testing/README.md](testing/README.md)
- [setup/README.md](setup/README.md)
- [utilities/README.md](utilities/README.md)

## 🔄 Mantenimiento

- **Rutas**: Todos los scripts usan rutas relativas desde Scripts/
- **Encoding**: Scripts Python usan UTF-8 por defecto
- **Compatibilidad**: Windows (bash vía Git Bash), Linux, macOS

## 🤝 Contributing

Para agregar nuevos scripts:
1. Determinar categoría (data-processing, generation, testing, setup, utilities)
2. Crear archivo en subdirectorio correspondiente
3. Agregar documentación en README.md del subdirectorio
4. Actualizar rutas relativas si es necesario
5. Seguir convenciones de naming existentes

**Última Actualización**: 2026-03-25
