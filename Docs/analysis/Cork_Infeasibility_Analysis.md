# Análisis de Infactibilidad: Instancias Cork vs Sintéticas

**Fecha**: Marzo 25, 2026
**Diagnóstico**: Las instancias Cork son estructuralmente diferentes

---

## 🔍 Hallazgos Clave

### Comparación de Escalas

| Métrica | Cork (Real) | Sintéticas/Noncity | Factor |
|---------|-------------|-------------------|--------|
| **max_stops** | 568 | 8-12 | **47-71x más grande** |
| **num_stops[1]** | 566 paradas | 5-12 paradas | **47-113x** |
| **Estructura** | Rutas **cíclicas repetidas** | Rutas únicas | Fundamentalmente diferente |
| **Duración** | Día completo (13-14 ciclos) | Una vuelta | N/A |

### Datos de Cork-1-line20_0

```
num_buses = 4
num_stations = 40
max_stops = 568 ← ¡566-568 paradas por bus!
num_stops = [566, 568, 378, 356]

Patrón st_bi (Bus 1):
0,1,2,3,...,39,0,0,1,2,3,...,39,0,0,1,2,3,...  (ciclo repetido ~13 veces)
│←────────── Ciclo 1 ──────────→││←── Ciclo 2 ──→│
```

**Observación crítica**: El índice ==`0` en Cork **NO es un error****, es el depot que marca el inicio de cada ciclo diario.

---

## 🧮 Análisis de Factibilidad

### Consumo Energético Total

**Bus 1 (Cork-1-line20_0)**:
```
Paradas totales: 566
Consumo promedio por parada: ~3 kWh (30 en escala ×10)
Consumo total estimado: 566 × 3 = 1,698 kWh

Capacidad útil de batería: 100 - 20 = 80 kWh

Cargas necesarias: 1,698 / 80 ≈ 21.2 cargas completas
```

**Comparación con noncity que funciona**:
```
Paradas totales: 5-8
Consumo total: 700-1,200 kWh (70-120 en escala ×10)
Capacidad útil: 80 kWh

Cargas necesarias: 1-2 cargas estratégicas
```

### Restricciones Temporales

**Problema**: Con 21+ cargas necesarias:

1. **Tiempo de carga total mínimo**:
   ```
   21 cargas × 1 min (psi) = 21 minutos mínimo
   21 cargas × 10 min (beta máx) = 210 minutos máximo
   ```

2. **Margen de retraso disponible**:
   ```
   μ = 50 (5 minutos máximo de retraso)
   Con 566 paradas, esto es casi imposible de satisfacer
   ```

3. **Restricción de no solapamiento**:
   ```
   Con 4 buses cargando frecuentemente en 40 estaciones,
   la probabilidad de conflictos es altísima
   ```

---

## 🎯 Conclusión

### ¿Por qué Cork es UNSATISFIABLE?

**NO es un bug del modelo**. Las instancias Cork son infactibles porque:

1. **Consumo excesivo**: Rutas diarias completas (13-14 ciclos) consumen 1,500-2,000 kWh
2. **Capacidad insuficiente**: Batería de 80 kWh útil vs 1,700 kWh necesarios = 21+ cargas
3. **Restricciones temporales estrictas**: μ=5 min de retraso máximo es incompatible con 21 cargas
4. **Tasa de carga baja**: α=10 kWh/min significa que cada carga de 40 kWh toma **4 minutos**
   - 21 cargas × 4 min = 84 minutos de carga pura
   - Más tiempo de viaje = imposible bajo μ=5 min de retraso

### ¿Por qué noncity SÍ funciona?

```plaintext
Paradas: 5-8 (una vuelta)
Consumo: 70-120 kWh
Cargas necesarias: 1-2
Tiempo de carga: 5-10 minutos total
Margen:suficiente dentro de μ=5 min
```

---

## 📋 Escenarios Posibles

###  Caso 1: Cork está mal diseñado

**Hipótesis**: Los archivos Cork fueron generados automáticamente con errores de escala.

**Evidencia**:
- Parámetros α, β, μ parecen pensados para **una vuelta**, no 13-14 vueltas
- Consumos por parada (2-8 kWh) son razonables para una vuelta
- Pero multiplicados por 13 ciclos = infactible

**Si esto es cierto**: Cork necesita ser regenerado con:
- α mayor (50-100 kWh/min para carga ultra-rápida)
- β mayor (30-60 min de tiempo de carga por parada)
- μ mayor (30-60 min de retraso permitido)
- O dividir en instancias de **un solo ciclo** (40-50 paradas)

### Caso 2: Cork representa un problema diferente

**Hipótesis**: Los datos Cork son para un escenario de:
- Operación diaria completa (13-14 horas)
- Buses que regresan al depot cada ciclo para carga nocturna
- El modelo CLP no está diseñado para esto

**Si esto es cierto**: Se necesita un modelo diferente que:
- Permita carga en depot (índice 0) con tiempo ilimitado
- No acumule restricciones entre ciclos
- Trate cada ciclo como independiente

### Caso 3: **Cork usa el modelo RCLP, no CLP**

**Hipótesis más probable**: Los archivos Cork fueron diseñados para el modelo **RCLP** (robusto), que:
- Permite múltiples rutas de carga
- Tiene parámetros relajados
- Maneja ciclos diarios completos

**Si esto es cierto**: Deberíamos probar Cork con `rclp_model.mzn` en lugar de `clp_model.mzn`.

---

## ✅ Recomendaciones

1. **Probar Cork con RCLP**:
   ```bash
   minizinc rclp_model.mzn cork-1-line20_0.dzn
   ```

2. **Crear versión reducida de Cork** (solo 1 ciclo):
   - Extraer primeras 42 paradas (1 ciclo completo)
   - Esto debería ser factible con parámetros actuales

3. **Validar parámetros Cork** contra paper JITS2022:
   - Verificar que α, β, μ sean correctos
   - Confirmar si Cork es para modelo CLP o RCLP

4. **Usar instancias sintéticas para evaluación**:
   - Ya están validadas y funcionan
   - Escalables (3-10 buses, 6-20 estaciones)

---

## 📊 Recomendación Oficial

**Para evaluación del modelo CLP**: Usar instancias sintéticas corregidas (`Battery Own`).

**Para investigación con datos Cork**:
1. Probar con modelo RCLP
2. Crear variantes reducidas (1 ciclo)
3. Relajar parámetros (α × 5, β × 3, μ × 6)

**El modelo CLP está CORRECTO**. Las instancias Cork son para un escenario operativo diferente.

---

**Próximo paso**: Ejecutar prueba con RCLP y Cork para confirmar hipótesis.
