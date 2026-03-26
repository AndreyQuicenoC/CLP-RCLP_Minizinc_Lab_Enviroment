# Generation Scripts

Scripts para generar variantes de instancias y crear nuevas instancias de prueba.

## Contenido

### `create_cork_variants.py`
Extrae ciclos individuales de instancias completas del proyecto Cork transformándolas en variantes factibles single-cycle.

**Descripción**:
El proyecto Cork contiene instancias de múltiples ciclos (378-568 paradas) que son infactibles para el modelo CLP estándar. Este script extrae el primer ciclo operativo (~42 paradas) creando instancias más manejables.

**Uso**:
```bash
python create_cork_variants.py
```

**Entrada**: `Data/Battery Project Integer/cork-*.dzn`
**Salida**: `Data/Battery Project Variant/cork-*_1cycle.dzn`

**Características**:
- Extrae exactamente 42 paradas del primer ciclo
- Mantiene estructura coherente de tiempos y consumos
- Crea archivos .dzn bien formateados con comentarios
- Manejo de encoding UTF-8 para compatibilidad Windows/Linux

---

### `generate_synthetic_data.py`
Genera datos sintéticos de instancias CLP para pruebas y desarrollo.

**Uso**:
```bash
python generate_synthetic_data.py [opciones]
```

**Características**:
- Generación de instancias aleatorias configurables
- Exportación a formato MiniZinc (.dzn)
- Estructura válida y testeable
- Escalado automático de valores

**Parámetros principales**:
- `--buses N`: Número de buses
- `--stations M`: Número de estaciones
- `--output FILE`: Directorio/archivo de salida

**Ejemplo**:
```bash
python generate_synthetic_data.py --buses 10 --stations 15
```

## Related Scripts
- Data Processing: `../data-processing/` (para validar los datos generados)
- Testing: `../testing/test_generator.sh` (para verificar las variantes)
- Utilities: `../utilities/diagnose_cork.sh` (para diagnosticar problemas)
- GUI: `../../Generator/generator.py` (generador interactivo de instancias)

## Dependencies
- Python 3.8+
- Standard library: re, sys, pathlib

## Architecture
```
Cork Original (378-568 stops)
    ↓
create_cork_variants.py
    ↓
Cork Variant (1 cycle, ~42 stops) ✓ FEASIBLE
```

## Troubleshooting
- **UTF-8 Encoding**: Script auto-configura encoding en Windows
- **Missing Files**: Verifica que exista `Data/Battery Project Integer/`
- **Invalid Format**: Asegúrate que los archivos Cork tengan comentarios % Bus X
