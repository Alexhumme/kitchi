# 08 · Concurrencia, multiprocesamiento y paralelismo — Kitchi Studio

Casos de uso académicos, evidencia y estrategia · Versión 1.0

> Esta sección debe diseñarse en función de los criterios de evaluación del profesor. Como la rúbrica aún no está disponible, la estrategia es demostrar cada concepto por separado y mantener **evidencias reproducibles** en [`reports/`](reports/). La rúbrica obtenida se transcribe aquí antes de cerrar el alcance (tarea P01).

## Definiciones (no confundir)

- **Concurrencia:** organizar varias tareas para que progresen durante intervalos solapados.
- **Paralelismo:** ejecutar operaciones realmente al mismo tiempo, por ejemplo en distintos núcleos de CPU.
- **Multiprocesamiento:** utilizar varios procesos independientes, lo que puede permitir paralelismo y aislamiento de fallos.

`asyncio` facilita concurrencia cooperativa, especialmente para operaciones de E/S. **No** hace que el procesamiento intensivo de imágenes se ejecute en paralelo automáticamente.

## Caso de uso A — Concurrencia con `asyncio`

Al generar un paquete, la aplicación puede necesitar consultar varios recursos o solicitar varias operaciones de red. Se demuestra ejecutando varias solicitudes de E/S asíncronas independientes, con límites y manejo de errores.

Ejemplo ilustrativo:

```python
import asyncio

async def consultar_recurso(nombre):
    await asyncio.sleep(1)
    return f"Recurso procesado: {nombre}"

async def main():
    resultados = await asyncio.gather(
        consultar_recurso("pose_1"),
        consultar_recurso("pose_2"),
        consultar_recurso("pose_3"),
    )
    print(resultados)

asyncio.run(main())
```

Este ejemplo demuestra tareas concurrentes simulando espera de E/S; **no es todavía una integración real**. En la implementación, la espera debe sustituirse por operaciones reales, por ejemplo peticiones HTTP asíncronas al servicio de IA.

**Evidencia requerida:** tiempo total de ejecución, comportamiento cuando una petición falla y prueba de que la interfaz no queda bloqueada esperando el resultado.

## Caso de uso B — Multiprocesamiento

La composición o transformación de imágenes puede ser una tarea intensiva en CPU. El equipo ejecuta trabajos independientes en un grupo de procesos.

Ejemplo de estructura:

```python
from concurrent.futures import ProcessPoolExecutor

def procesar_pose(datos):
    # La función real compondrá y exportará una pose.
    return datos["pose_id"]

def generar_paquete(trabajos):
    with ProcessPoolExecutor(max_workers=3) as pool:
        return list(pool.map(procesar_pose, trabajos))
```

Restricciones del código real:

- El código es ilustrativo; debe adaptarse al motor gráfico real.
- Las funciones ejecutadas en procesos deben ser **importables**, recibir **argumentos serializables** y no depender de objetos de interfaz, conexiones de base de datos abiertas o estado compartido no controlado.
- En Windows y macOS es especialmente importante utilizar el punto de entrada adecuado (`if __name__ == "__main__":`) para crear procesos y evitar que la importación del módulo vuelva a iniciar el programa.

**Evidencia requerida:** identificación de los procesos trabajadores y sus resultados (AC-10).

## Caso de uso C — Paralelismo medible

Para demostrar paralelismo de manera convincente, se procesa un **conjunto fijo de imágenes** en dos modalidades:

1. Ejecución secuencial.
2. Ejecución con un grupo de procesos.

Mismo conjunto de recursos y misma configuración. Se registran: tiempo de inicio, tiempo de finalización, cantidad de imágenes, errores y número de trabajadores.

La aceleración se calcula como:

```
S = T_secuencial / T_paralelo
```

Si la ejecución secuencial tarda 4 s y la paralela 2,5 s, la aceleración observada sería 1,6.

> No se debe asumir que la ejecución paralela siempre será más rápida: para trabajos pequeños, el coste de crear procesos y serializar datos puede superar el beneficio. Presentar el resultado real, sea favorable o no (AC-11, informe reproducible en [`reports/`](reports/)).

## Qué evitar

- Crear un proceso por cada tarea sin límite.
- Lanzar procesos desde una petición web y bloquear la respuesta hasta terminar.
- Usar `asyncio` para envolver una función intensiva de CPU sin delegar el trabajo.
- Abrir una conexión MySQL antes de crear procesos y reutilizarla en todos.
- Utilizar una sola prueba artificial como única evidencia de los requisitos académicos.
- Medir solamente el tiempo total sin registrar qué se está comparando.

## Estrategia de implementación en cinco semanas

1. Primero se implementa el **motor secuencial correcto**.
2. Después se añaden las pruebas de concurrencia y paralelismo como **módulos claramente separados**.
3. Solo cuando estén verificadas se integran con la interfaz.

Si el profesor exige tecnologías concretas (`threading`, `multiprocessing`, `asyncio`, `ProcessPoolExecutor`, `ThreadPoolExecutor`), esa decisión se ajusta a la rúbrica. No conviene añadir todos estos mecanismos sin necesidad antes de conocer los requisitos.

## Tareas relacionadas

- P20 — Demostrar concurrencia.
- P21 — Demostrar multiprocesamiento.
- P22 — Ejecutar benchmark de paralelismo (`scripts/benchmark_generation.py`).
- P27 — Documentar resultados de rendimiento ([09_TEST_PLAN.md](09_TEST_PLAN.md#pruebas-de-rendimiento)).
