## Prompts enviados

### DeepSeek:PROMPT DE INICIO PARA DESARROLLO DE PRUEBA TÉCNICA - SISTEMA DE GESTIÓN DE VALOR GANADO

```
CONTEXTO
Eres un ingeniero de software senior con experiencia en arquitectura de sistemas (documento adjunto), desarrollo fullstack y metodologías ágiles. He recibido una prueba técnica sobre la cuál extraje los parámetros clave descritos a continuación. Tengo 10 horas para completarla. Necesito que actúes como mi asistente técnico para planificar y ejecutar este proyecto de manera estructurada y eficiente.
OBJETIVO DEL PROYECTO
Desarrollar un sistema fullstack para la gestión del valor ganado (EVM) que permita a los líderes de proyecto monitorear el desempeño de sus proyectos mediante indicadores como CPI y SPI, comparando el avance real contra el planificado.
REQUISITOS TÉCNICOS DETALLADOS

1. Configuración de linter en el repositorio
2. Fullstack: FastAPI (backend), Angular (frontend), PostgreSQL (base de datos)
3. Backend: Gestión CRUD de proyectos y actividades
4. Backend: Cálculo inmediato de indicadores EVM por actividad y consolidado por proyecto
5. Backend: Interpretación de CPI y SPI
6. Frontend: Dashboard con
   • Selector de proyecto activo, botón para agregar proyecto
   • Indicadores de proyecto SPI y CPI consolidados.
   • Indicadores adicionales consolidados
   • Graficos de barras con PV, EV y AC por actividad.
   • Tabla de detalle actividades e indicadores por actividad y botón de editar actividad.
   • Botón de agregar actividad.
   ESTÁNDARES DE CALIDAD:
7. Pruebas unitarias para toda lógica de cálculo (incluyendo casos borde)
8. Pruebas de integración para cada endpoint
9. Código limpio: sin bloques comentados, sin variables sin uso, sin números mágicos, nombres claros, arquitectura limpia, funciones con única responsabilidad, abstracción en repeticiones mayores a dos veces
10. Git Flow: main, develop, feature/\*, al menos un release, commits descriptivos en imperativo
11. OpenAPI: documentación accesible en /api-docs, cada endpoint con descripción, esquemas request/response, códigos de error
12. README para ejecución local
13. Script de inicialización de base de datos
14. Documentación del proceso con IA
15. Video explicativo
    MODELO DE DATOS:
    • Proyecto: nombre, presupuesto total, porcentaje de avance planificado a fecha de corte, porcentaje de avance real completado, costo real incurrido
    • Actividad: (relacionada a proyecto) con los mismos atributos
    DECISIONES DE NEGOCIO PREVIAS:
    • El sistema mostrará el estado actual del proyecto (instantánea), no histórico, pero debe ser escalable para incluirlo en el futuro
    DECISIONES TÉCNICAS PREVIAS:
    • La estructura de archivos reflejará una arquitectura por capas (Router-Service-Repo). Se consideró utilizar arquitectura limpia pero por la característica de desarrollo rápido y poco tiempo la de capas es la indicada.
    • Para el front la arquitectura será la clásica a utilizar en proyectos Angular (Componentes y servicios).
    • Debe ser escalable para manejo de usuarios (múltiples lideres de proyectos, cada uno con sus proyectos asignados). No se implementará para la actual entrega.
    MODO PLANIFICACIÓN
    Como asistente, debes generar un plan detallado de trabajo estructurado que incluya:
16. Lista de tareas ordenadas: Desglosa el proyecto en tareas específicas y ordenadas.
17. Estimación de pesos por tarea: Asigna un peso porcentual a cada tarea (sumando 100%) que refleje su esfuerzo relativo, complejidad e impacto en el éxito del proyecto. Estos pesos los usaré para hacer seguimiento en Excel.
18. Estimación de tiempo por tarea: Asigna tiempo estimado en minutos/horas para cada tarea, considerando que tengo 10 horas totales (600 minutos).
19. Estructura de Git Flow: Si una tarea está relacionada a desarrollo, define el nombre de la rama y commit sugerido.
20. Estrategia de pruebas: Especifica qué probarás primero y con qué prioridad.
```

#### Respuesta

La IA considera que en la redacción del Prompt hay problemas críticos que deben ser resueltos para la correcta planificación del proyecto. A saber:

- El prompt le pide a la IA que haga todo el plan y ejecute contigo. Pero el prompt no define para qué necesitas la IA en cada paso.
- Tu prompt pide pesos que sumen 100%, pero no defines qué es más importante para el evaluador.
- La IA no sabe: Tu velocidad de codificación, Tu familiaridad con FastAPI vs Angular, Tu experiencia con pruebas. Tu capacidad de edición de video.

A partir de lo propuesto y lo sugerido por la IA revisado se opta por el promt con el siguiente contenido.

```
PROMPT DE INICIO - PRUEBA TÉCNICA SISTEMA EVM
CONTEXTO
Tengo 10 horas para completar una prueba técnica de desarrollo fullstack. Los evaluadores dan mayor peso al video (10 min) y al documento AI_PROCESS.md que al código en sí mismo. Necesito maximizar mi tiempo para entregar:
1. Un sistema funcional (backend + frontend) que cumpla los requisitos mínimos
2. Un AI_PROCESS.md completo, honesto y bien estructurado
3. Un video de 10 minutos bien preparado
Necesito que actúes como mi asistente técnico en las siguientes capacidades:
- Fase 1 (planificación): Generar el plan de trabajo priorizado
- Fase 2 (backend): Generar código funcional que siga arquitectura por capas
- Fase 3 (frontend): Generar componentes Angular conectados a la API
- Fase 4 (documentación): Generar estructura del AI_PROCESS.md y guión del video
REQUISITOS PRIORIZADOS PARA EL SISTEMA
BACKEND (FastAPI + PostgreSQL):
- CRUD de proyectos: crear, listar, obtener, actualizar, eliminar
- CRUD de actividades: crear, listar por proyecto, obtener, actualizar, eliminar
- Cálculo automático de indicadores EVM al obtener proyectos/actividades:
  PV, EV, CV, SV, CPI, SPI, EAC, VAC
- Interpretación textual de CPI y SPI
- OpenAPI en /api-docs
- Pruebas unitarias de cálculos EVM (80% cobertura)
- Pruebas de integración de endpoints (uno por endpoint)
FRONTEND (Angular):
- Selector de proyecto activo
- Botón para agregar proyecto
- Indicadores consolidados del proyecto (CPI, SPI, PV, EV, AC, EAC, VAC)
- Indicadores visuales de estado (verde/rojo para CPI y SPI)
- Gráfica de barras comparativa PV, EV, AC por actividad
- Tabla de actividades con todos sus indicadores
- Botón para editar actividad (modal o inline)
- Botón para agregar actividad
MODELO DE DATOS (DEFINIDO):
Proyecto:
- id (PK)
- name (string, required)
- budget (float, BAC)
Actividad:
- id (PK)
- project_id (FK a proyecto)
- name (string, required)
- bac (float, Budget at Completion)
- planned_pct (float, % avance planificado a fecha de corte)
- real_pct (float, % avance real completado)
- actual_cost (float, AC)
RELACIÓN: Un proyecto tiene muchas actividades. Los indicadores consolidados del proyecto se calculan sumando/agregando los valores de sus actividades.
ARQUITECTURA DECIDIDA:
Backend: Router → Service → Repository (por capas)
- Router: recibe request, llama a service, devuelve response. Sin lógica.
- Service: aquí viven los cálculos EVM y reglas de negocio.
- Repository: acceso a BD con SQLAlchemy.
Frontend: Pages → Hooks → Services
- Pages: orquestan la vista, conectan hooks y componentes
- Hooks: contienen lógica de negocio del frontend (fetch, transformación)
- Services: llamadas HTTP a la API
ESTÁNDARES A CUMPLIR (NO NEGOCIABLES):
- Linter configurado en el repo
- Git Flow: main, develop, feature/*, release/*
- Commits descriptivos en imperativo
- Código sin code smells
- README con instrucciones de ejecución
- Script de inicialización de BD
- AI_PROCESS.md (estructura definida abajo)
- Video de 10 minutos (estructura definida abajo)
INSTRUCCIONES PARA CADA FASES
FASE 1: PLANIFICACIÓN (RESPONDER AHORA MISMO)
Genera un plan detallado con:
1. Lista de tareas ordenadas.Para cada tarea, asigna:
   - Peso (%) de esfuerzo (suma 100% en total)
   - Rango de tiempo estimado (promedio en minutos)
   - Indicador de CRÍTICO para el evaluador (SÍ/NO)
Si la tarea hace parte del desarrollo, su respectivo nombre de rama y commit propuesto.
Ten en cuenta que Orden de merges (feature → develop → release → main)
4. Estrategia de pruebas:
   - Orden de prioridad para escribir pruebas
   - Casos borde específicos a cubrir en EVM
FASE 2: BACKEND (CUANDO YO TE LO SOLICITE)
FASE 3: FRONTEND (CUANDO YO TE LO SOLICITE)
FASE 4: DOCUMENTACIÓN Y VIDEO (CUANDO YO TE LO SOLICITE)

INSTRUCCIONES ADICIONALES

- No uses emojis en la respuesta
- Sé conciso y directo
- Prioriza la utilidad práctica sobre la teoría
- Si algo no está claro, pregunta antes de asumir
- No generes código si no te lo pido.
RESPONDE CON LA PLANIFICACIÓN (FASE 1) EN TU PRÓXIMO MENSAJE.

```

## Claude PROMPT GENERADOR DE SCRIPT SQL (POSTGRESQL ESTRUCTURADO)

```
Tu tarea es generar un script SQL completo listo para ejecución que inicialice una base de datos relacional para un sistema de gestión de proyectos.

1. Reglas generales del script
Debe ser compatible con PostgreSQL.
Debe incluir eliminación de tablas existentes usando DROP TABLE IF EXISTS ... CASCADE.
Debe incluir creación de tablas con relaciones correctas.
Debe incluir claves primarias y foráneas correctamente definidas.
Debe usar tipos de datos apropiados.
Debe incluir datos de ejemplo (seed data).
Debe finalizar con consultas de verificación (SELECT).
2. Modelo de datos obligatorio

Debes crear exactamente estas dos tablas:

Tabla: projects

Descripción: representa proyectos del sistema.

Columnas obligatorias:

id: SERIAL PRIMARY KEY
name: VARCHAR(255) NOT NULL
description: TEXT NULL
created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Relaciones: Es tabla padre de activities.

Tabla: activities

Descripción: representa actividades dentro de un proyecto.

Columnas obligatorias:

id: SERIAL PRIMARY KEY
project_id: INTEGER NOT NULL (FK a projects.id)
name: VARCHAR(255) NOT NULL
bac: NUMERIC(12,2) NOT NULL (Budget at Completion)
planned_progress: NUMERIC(5,2) DEFAULT 0.00
actual_progress: NUMERIC(5,2) DEFAULT 0.00
actual_cost: NUMERIC(12,2) DEFAULT 0.00
created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Relaciones:

activities.project_id debe ser clave foránea que referencia projects.id
ON DELETE CASCADE debe estar habilitado

3. Datos de ejemplo obligatorios

Debes insertar:

projects
Exactamente 1 registro de proyecto.
activities
4 registros en total.
Todas las actividades deben estar asociadas al proyecto existente.

4. Reglas
No puede existir una actividad sin proyecto asociado.
Los valores de progreso deben estar entre 0 y 1(estándar, mantenlo consistente).

5. Selects

Al final del script debes incluir:

Conteo total de actividades.
Un SELECT simple que muestre la relación entre proyecto y actividad.
6. Restricciones de salida
Solo devuelve el script SQL.
No agregues explicaciones.
No uses markdown.
No incluyas texto adicional antes o después.
Debe ser un archivo .sql válido ejecutable directamente.
```

El sql generado se encuentra en el backend/scripts

## Claude: PROMPT DE CONSTRUCCIÓN DE SERVICIO VALOR GANADO

```
Con base en las especificaciones que hemos abordado en los casos pasados implementar un módulo de servicio en Python que calcule indicadores EVM bajo las siguientes especificaciones: 
1. Construir componente llamado EVMCalculator que permita
Calcular las métricas EVM por actividad
Calcular las métricas consolidadas por proyecto
2. Reglas
Usar dataclases para los modelos de salida
Sin librerías externas
Codigo limpio
No agregues emojis ni docstrings largos
3. ActivityEVM debe contener

Los datos base de la actividad
activity_id activity_name bac planned_progress actual_progress actual_cost

Y los indicadores

pv ev cv sv cpi spi eac vac

4. ProjectEVM debe contener

Los datos consolidados del proyecto
project_id project_name total_bac total_pv total_ev total_ac
Debe incluir la lista de ActivityEVM calculadas
El servicio debe tener dos metodos
calculate_activity_evm()

calculate_project_evm()
```

Luego de revisar la respuesta se solificó el código con ajuste de reglas de negocio, interpretaciones para CPI y SPI.

## Claude: PROMPT DE CONSTRUCCIÓN DE DTOS
Por agilidad en la generación de los schemas se le dió instrucción a Claude con los siguientes criterios
```
Pasemos a los schemas de pydantic. Separardos por responsabilidad en lugar de tener todo en un solo archivo.

Una carpeta schemas con:
- common para los indicadores EVM que son los mismos para actividad y proyecto
- activity y project son carpetas separadas pero ambas tienen create, update, response y simple

- Los create para cuando el cliente envía datos (POST)
- update para cuando actualiza con PATCH, todos opcionales
- response para devolver datos completos con EVM calculado
- project tiene también simple para efectos de un selector que solo necesita nombre

Para ActivityCreate necesito: project_id, name, bac, planned_progress, actual_progress, actual_cost (todos obligatorios)
ActivityResponse: todo + EVM

Para ProjectCreate: name y description
ProjectUpdate: ambos opcionales
ProjectResponse: con actividades + EVM consolidado
ProjectSimpleResponse: solo nombre
```