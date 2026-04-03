# Testing Scripts

Scripts para validar, prueba y verificación del sistema completo CLP-RCLP.

## Contenido

### `test_generator.sh` ⭐ PRINCIPAL
Script de testing comprehensivo del sistema de generación de instancias.

**Uso**:
```bash
bash test_generator.sh
```

**Tests Incluidos**:
1. Verificar existencia de variantes Cork
2. Verificar disponibilidad del script generador
3. Verificar instalación de MiniZinc
4. Validar variante Cork con modelo CLP
5. Verificar estructura de directorios generados
6. Validar instancia generada existente
7. Verificar documentación completa

**Salida**: Reporte detallado con color y estadísticas

### `test_clp_preliminary.sh`
Tests preliminares para validar funcionamiento básico del modelo CLP.

**Uso**:
```bash
bash test_clp_preliminary.sh
```

### `run_battery_project_tests.py`
Suite de tests para las instancias del proyecto Battery.

**Uso**:
```bash
python run_battery_project_tests.py [opciones]
```

### `test_initial_small_case.py`
Tests de caso pequeño inicial para verificar funcionalidad básica.

**Uso**:
```bash
python test_initial_small_case.py
```

## Test Workflow

```
test_generator.sh (MAIN)
├── Validar Cork variants
├── Validar installation (MiniZinc)
├── Resolver instancias
└── Reporte final

Después:
├── run_battery_project_tests.py (validación completa)
└── test_clp_preliminary.sh (diagnóstico)
```

## Dependencies
- bash (para scripts .sh)
- Python 3.8+ (para scripts .py)
- MiniZinc 2.5+ (para validación)
- minizinc Python module (para algunos scripts)

## Expected Results
- **SUCCESS**: 100% test pass rate, todas las instancias SATISFIABLE
- **INFO**: Warnings esperados para Cork (instancias complejas)
- **TIMEOUT**: Aceptable para instancias muy grandes (>20 buses)

## Related Documentation
- Main test guide: `../../Docs/generated-system/README.md`
- Model info: `../../Docs/model/`
