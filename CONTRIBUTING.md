# Guía de Contribución

¡Gracias por tu interés en contribuir a CLP-RCLP MiniZinc Lab Environment!

## Reportar Problemas

Si encuentras un bug o tienes una sugerencia, por favor:

1. Verificar que no exista un issue similar ya abierto
2. Crear un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir (si es un bug)
   - Versión de Python, MiniZinc, OS
   - Logs relevantes

## Proponer Cambios

1. **Fork** el repositorio
2. **Crear una rama** para tu feature: `git checkout -b feature/mi-feature`
3. **Hacer commits** claros con mensajes descriptivos
4. **Agregar tests** si es aplicable
5. **Push** a tu fork
6. **Crear Pull Request** con descripción clara

## Estándares de Código

### Python
- Seguir [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Docstrings en formato Google
- Type hints donde sea posible
- Máximo 88 caracteres por línea (black standard)

```python
def function_name(parameter: type) -> return_type:
    """
    Breve descripción.

    Descripción más detallada si es necesario.

    Args:
        parameter: Descripción del parámetro

    Returns:
        Descripción del retorno

    Raises:
        Exception: Cuándo se lanza
    """
    pass
```

### Bash Scripts
- Variables UPPER_CASE
- Funciones lower_case
- Comentarios explicativos
- Manejo de errores con `set -e` o checks explícitos

```bash
#!/bin/bash
# Descripción del script

set -e  # Exit on error

VARIABLE_NAME="value"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

main() {
    log "Empezando..."
    # Tu código aquí
}

main "$@"
```

### Documentación
- Markdown bien formateado
- Índices de navegación
- Links internos relativos
- Ejemplos de código prácticos

## Estructura de Recursos

```
Scripts/
├── data-processing/     # Conversión y validación de datos
├── generation/          # Generación de instancias
├── testing/            # Suite de tests
├── setup/              # Configuración e initialization
└── utilities/          # Utilidades y diagnóstico

Docs/
├── generated-system/   # Sistema de generación
├── model/             # Documentación del modelo
└── analysis/          # Análisis y diagnóstico
```

Para agregar nuevo contenido:
1. Poner en categoría apropiada
2. Actualizar README.md correspondiente
3. Seguir estándares de código

## Testing

Antes de hacer PR:

```bash
# Validar scripts
python Scripts/data-processing/validate_integer_dzn.py

# Ejecutar tests
bash Scripts/testing/test_generator.sh

# Verificar generación
python Scripts/generation/create_cork_variants.py
```

## Commit Messages

Usar formato claro:
```
[TIPO] Descripción breve

Descripción detallada si es necesario.

- Punto 1
- Punto 2

Relacionado a #123
```

Tipos de commit:
- `[FEATURE]` - Nueva funcionalidad
- `[FIX]` - Corrección de bug
- `[DOCS]` - Documentación
- `[REFACTOR]` - Reorganización sin cambio funcional
- `[TEST]` - Adición o mejora de tests
- `[PERF]` - Mejora de performance

## Documentación de Cambios

Si tu PR incluye cambios significativos:
1. Actualizar README relevante
2. Agregar entrada a CHANGELOG.md
3. Actualizar docstrings
4. Incluir ejemplos de uso

## Preguntas

Para preguntas:
1. Revisar [Docs/README.md](Docs/README.md) primero
2. Chequear issues existentes
3. Abrir un issue con tag `question`

## Código de Conducta

- Ser respetuoso
- Acepta crítica constructiva
- Enfócate en lo que es mejor para el proyecto
- Reporta comportamiento inapropiado a los maintainers

## Reconocimiento

Los contribuyentes significativos serán reconocidos en el archivo de contribuyentes.

---

**Gracias por contribuir!** 🎉

*Última actualización: 2026-03-25*
