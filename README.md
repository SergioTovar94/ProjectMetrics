# ProjectMetrics

## 1. Descripción

Este proyecto fullstack tiene como objetivo poner a disposición de los lideres de proyectos una herramienta interna para que  puedan registrar el avance de sus actividades y entender, en tiempo real, si su proyecto va bien o mal en términos de cronograma y presupuesto.

Lo anterior a partir de la metodología de análisis de Valor Ganado (Earned Value Management).


## 2. Arquitectura y tecnologías

El proyecto será desarrollado a través de una arquitectura cliente servidor (backend consumido por fronted).

### Backend

- FastAPI
- SQLAlchemy
- Pydantic

### Frontend

- Angular
- TypeScript

### Base de datos

- PostgreSQL

### Pruebas

- Pytest

### Calidad de código

- Ruff

### Documentación

- OpenAPI (Swagger)

#### Uso de Linter

Verificar el código:

```bash
ruff check .
```

Formatear el código:

```bash
ruff format .
```