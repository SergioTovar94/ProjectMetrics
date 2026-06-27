# AI Process

## Herramientas IA utilizadas y por qué

Durante el desarrollo se utilizaron distintas herramientas de IA con objetivos específicos. Se buscó aprovechar las fortalezas de cada una para planificación, comprensión del dominio y apoyo en el desarrollo.

Claude Sonnet: IA Central para tareas de planificación del proyecto.
DeepSeek: Optimizar los prompts para suministrarlos a Claude.

| Herramienta | Objetivo | Resultado |
|-------------|----------|-----------|
| Claude Sonnet | IA Central para planificación, código y solución de problemas | Generó el plan de trabajo, el código base y ayudó a depurar errores |
| DeepSeek | Optimización de prompts y validación de conceptos | Refinó la estructura de prompts y ayudó a validar fórmulas EVM |
| ChatGPT | Comprensión de EVM y validación de ejemplos | Ayudó a verificar la correcta implementación de las fórmulas y casos borde |

**Nota:** Para facilidad de lectura, los promps completos se encuentran en el archivo PROMPTS.md

El prompt ejecutado en Claude generó una tabla de seguimiento que sirve como apoyo para el control del tiempo de desarrollo.
https://docs.google.com/spreadsheets/d/184F8tHBly0nTT289iX1E2ab7KTB1-UE2f9pNYQ5W4eQ/edit?usp=sharing

## Mecanismo de aprendizaje de EVM

Fase 1: Revisión de explicación por parte de expertos.
Fase 2: Apuntes de clase y mapa mental en cuaderno.
Fase 3: Apuntes de clase a DeepSeek para su revisión.

```
Tengo esta tabla de fórmulas EVM.

Indicador, Variable, Fórmula, Inglés
Costo real, AC, -, Actual Cost
Presupuesto total, BAC, -, Budget at completion
Valor Planeado, PV, %planificado*BAC, Planned Value
Valor Ganado, EV, %completado*BAC, Earned Value
Variación de costo, CV, EV-AC, Cost Variance
Variación de cronograma, SV, EV-PV, Schedule variance
Índice de costo, CPI, EV/AC, Cost Performance Index
Índice de cronograma, SPI, EV/PV, Schedule Performance Index
Estimado al completar, EAC, BAC/CPI, Estimate at Completion
Variación al completar, VAC, BAC-EAC, Variance at Completion

ACCIONES:
1. Corrige errores en mi tabla si los hay
2. Explica cada fórmula en 2 párrafos máximo:
   - Qué mide
   - Ejemplo concreto
```

Con lo anterior se pudo ajustar el excel y así poder simular una actividad y sus indicadores.

https://docs.google.com/spreadsheets/d/184F8tHBly0nTT289iX1E2ab7KTB1-UE2f9pNYQ5W4eQ/edit?usp=sharing

## Decisiones donde no seguí lo que dijo la IA

### 1. PUT vs PATCH en los endpoints de actualización

**Propuesta IA:** La IA genera el código de los CRUD de forma adecuada exceptuando en el caso de actualización, donde sugirió usar put en vez de patch. 
**Camino tomado:** Se reemplaza por código orientado permitir actualización parcial del proyecto o actividad. Esta decisión se tomó porque:
- PATCH es el adecuado para actualizaciones parciales
- Reduce el payload de la red y el riesgo de sobrescribir datos accidentalmente

### 2. Estructura de los Schemas de Pydantic

**Propuesta IA:** La IA sugirió tener todos los schemas de Pydantic en un solo archivo (`schemas.py`) para simplificar y reducir el número de archivos. Argumentaba que tener muchos archivos pequeños complicaba la navegación.

**Camino tomado:** Se optó por una estructura separada por responsabilidad:

```
schemas/
├── common.py # Schemas compartidos (EVMIndicators)
├── activity/
│ ├── create.py # ActivityCreate
│ ├── update.py # ActivityUpdate
│ ├── response.py # ActivityResponse
└── project/
├── create.py # ProjectCreate
├── update.py # ProjectUpdate
├── response.py # ProjectResponse
└── simple.py # ProjectSimpleResponse
```
Esta decisión se tomó porque:
- Es más fácil de mantener y escalar
- Cada archivo tiene una responsabilidad única
- Los nuevos desarrolladores pueden entender rápidamente qué hace cada archivo

## Verificación del cálculo, no solo que el código funciona.

Para validar que los cálculos EVM son correctos, se utilizó una hoja de cálculo con los mismos datos que se usaron en el código: https://docs.google.com/spreadsheets/d/184F8tHBly0nTT289iX1E2ab7KTB1-UE2f9pNYQ5W4eQ/edit?usp=sharing.

### Proceso de verificación:
1. Se ingresaron los mismos datos (BAC, planned_progress, actual_progress, actual_cost) en la hoja de cálculo
2. Se calcularon manualmente los 8 indicadores EVM usando las fórmulas estándar
3. Se ejecutó el código con los mismos datos de entrada
4. Se compararon los resultados de la hoja de cálculo con los del código
5. Se verificaron casos borde: AC=0, PV=0, BAC=0, progreso 0%

### Resultado:
Los resultados del código coinciden con los de la hoja de cálculo, validando que:
- Las fórmulas están correctamente implementadas
- El manejo de divisiones por cero (CPI y SPI) funciona correctamente
- Los redondeos a 2 decimales son consistentes
- Las interpretaciones de CPI y SPI son correctas según los valores calculados

## Decisión de arquitectura que tomé de forma independiente.

Como se pudo observar en el prompt inicial. La decisión de arquitectura fue para el backend por capas (Router Service Repository) y frontend estructura de componentes Anglar (Components Services). Por escalabilidad y robustez, la arquitectura limpia o hexagonal suele ser ideal. Sin embargo, debido a los tiempos establecidos para el desarrollo se determinó que la arquitectura por capas es la que mejor se adapta a la agilidad requerida.

Por otro lado, en algunas solicitudes la IA generó código que, si bien cumplía con el Principio de Responsabilidad Simple, concentraba demasiada lógica dentro de una misma clase o archivo. En estos casos, se optó por dividir el código en módulos más pequeños y especializados, mejorando la organización, la mantenibilidad y la escalabilidad de la aplicación.

## Reflexión honesta de qué cambiaría si repitiera el ejercicio
1. Durante el desarrollo del proyecto se generaron inconsistencias entre los models, schemas y la base de datos. Considero necesario que si repitiera el ejercicio estaría más pendiente de que haya consistencia.
2. Hubo un error en la configuración inicial del .gitignore que permitió versionar archivos __pycache__. Aunque posteriormente se corrigió el .gitignore, los archivos que ya estaban siendo rastreados por Git no fueron retirados en ese momento.
3. Algunos commits incluyeron cambios que no estaban directamente relacionados con la funcionalidad de la feature, como ajustes de configuración del proyecto. En una nueva iteración procuraría realizar commits más atómicos y enfocados en una única responsabilidad, facilitando la revisión y el mantenimiento del historial del repositorio.
4. Los Pull Requests podrían incluir una descripción más detallada. En la mayoría de los casos se crearon únicamente con el mensaje del commit, sin proporcionar contexto adicional sobre los cambios realizados, las decisiones tomadas o los aspectos que debían revisarse.
5. Pruebas unitarias desde el inicio: Aunque se implementaron pruebas unitarias para el EVM Calculator, se hicieron después de implementar el servicio. En una nueva iteración, escribiría las pruebas antes o durante la implementación, lo que habría ayudado a:
- Validar las fórmulas antes de integrarlas con la base de datos
- Reducir el tiempo de depuración
