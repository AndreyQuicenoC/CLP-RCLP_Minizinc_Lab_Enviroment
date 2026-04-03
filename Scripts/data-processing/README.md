# Data Processing Scripts

Scripts para procesar, validar y convertir archivos de datos entre diferentes formatos.

## Contenido

### `convert_json_to_integer_dzn.py`
Convierte archivos JSON con datos de instancias a formato MiniZinc (.dzn) con valores enteros escalados.

**Uso**:
```bash
python convert_json_to_integer_dzn.py <input.json> <output.dzn>
```

**Características**:
- Convierte valores decimales a enteros (escalados ×10)
- Valida rangos de valores
- Genera comentarios descriptivos en el archivo .dzn
- Compatible con el modelo CLP

### `validate_integer_dzn.py`
Valida que los archivos .dzn generados cumplan con los requisitos del modelo CLP.

**Uso**:
```bash
python validate_integer_dzn.py <file.dzn>
```

**Validaciones**:
- Estructura correcta de arrays
- Tipos de datos correctos (enteros)
- Valores dentro de rangos permitidos
- Coherencia entre parámetros

## Dependencies
- Python 3.8+
- numpy (opcional para análisis)

## Related Scripts
- Generation: `../generation/create_cork_variants.py` (produce datos para este módulo)
- Testing: `../testing/run_battery_project_tests.py` (valida la salida)
