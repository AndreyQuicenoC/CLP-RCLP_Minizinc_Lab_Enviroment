# Setup & Diagnosis Scripts

Scripts para configuración inicial, diagnóstico y resolución de problemas del proyecto CLP-RCLP.

## Contenido

### `setup_and_validate.py`
Script de configuración inicial que verifica todos los requisitos y prepara el entorno.

**Uso**:
```bash
python setup_and_validate.py
```

**Validaciones**:
- Estructura de directorios correcta
- Instalación de Python 3.8+
- Disponibilidad de MiniZinc
- Archivos de modelo presentes
- Datos base disponibles

**Salida**: Reporte de configuración con pasos para resolver problemas

## Setup Workflow

1. **Primera vez**:
   ```bash
   python setup_and_validate.py    # Validará requisitos
   ```

2. **Si hay problemas con Cork**:
   ```bash
   bash ../utilities/diagnose_cork.sh           # Diagnosticará
   python ../generation/create_cork_variants.py  # Regenerará
   ```

3. **Verificar todo funciona**:
   ```bash
   bash ../testing/test_generator.sh  # Test completo
   ```

## Dependencies
- Python 3.8+
- bash (para scripts .sh)
- MiniZinc 2.5+ (https://www.minizinc.org)
- git (para clonar/actualizar)

## Troubleshooting

### MiniZinc not found
```bash
# Linux (Debian/Ubuntu)
sudo apt install minizinc

# macOS
brew install minizinc

# Windows
# Descargar desde https://www.minizinc.org/software.html
```

### Python version too old
```bash
python3 --version  # Must be 3.8+
pip install --upgrade pip
```

### Directory structure issues
```bash
# Regenerate directories
python setup_and_validate.py --fix
```

## Related Documentation
- Quick Start Guide: `../../README.md`
- Model Documentation: `../../Docs/model/README.md`
