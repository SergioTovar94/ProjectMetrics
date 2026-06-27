# ProjectMetrics

## 1. Descripción

Este proyecto fullstack tiene como objetivo poner a disposición de los lideres de proyectos una herramienta interna para que  puedan registrar el avance de sus actividades y entender, en tiempo real, si su proyecto va bien o mal en términos de cronograma y presupuesto.

Lo anterior a partir de la metodología de análisis de Valor Ganado (Earned Value Management).

## 2. Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10+** - [Descargar](https://www.python.org/downloads/)
- **PostgreSQL 15+** - [Descargar](https://www.postgresql.org/download/)
- **Node.js 18+** - [Descargar](https://nodejs.org/)
- **Angular CLI 17+** - `npm install -g @angular/cli@17`
- **Git** - [Descargar](https://git-scm.com/downloads)

## 3. Arquitectura y tecnologías

El proyecto será desarrollado a través de una arquitectura cliente servidor (backend consumido por fronted).

### Backend

- FastAPI: Framework web
- SQLAlchemy: ORM para base de datos
- Pydantic: Validación de datos

### Frontend

- Angular: Framework frontend
- TypeScript: Tipado estático
- Angular Material: Componentes UI
- Chart.js: Gráficas

### Base de datos

- PostgreSQL 15+: Base de datos relacional

### Pruebas

- Pytest: Framework de pruebas
- Pytest-cov: Cobertura de código

### Calidad de código

- Ruff: Linter y formateador

### Documentación

- OpenAPI (Swagger): Documentación automática de API

#### Uso de Linter

Verificar el código:

```bash
ruff check .
```

Formatear el código:

```bash
ruff format .
```

## 4. Configuración Rápida

### 4.1. Clonar el repositorio

```bash
git clone https://github.com/SergioTovar94/ProjectMetrics.git
cd ProjectMetrics
```

### 4.2. Crear la base de datos

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear la base de datos
CREATE DATABASE trycore_evm;

-- Salir
\q
```
**Nota:** Si tu usuario de PostgreSQL es diferente a postgres, ajústalo en los siguientes comandos.

### 4.3. Inicializar la base de datos
Ejecuta el script de inicialización que crea las tablas y carga datos de ejemplo:

```
# Desde la raíz del proyecto
cd backend
psql -U tu_usuario -d trycore_evm -f scripts/init_db.sql
```
**Qué hace el script:**

- Crea las tablas projects y activities
- Inserta un proyecto de ejemplo con 4 actividades
- Los datos de ejemplo incluyen valores para cálculos EVM

## 4.4. Configurar el backend

### Crear y activar entorno virtual
Estando dentro de backend

```
python -m venv venv
source venv/bin/activate      # Linux/Mac
# o
venv\Scripts\activate         # Windows
```
### Instalar dependencias
```
pip install -r requirements.txt
```
### Configurar variables de entorno (crear archivo .env)

```
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/trycore_evm" > .env
```

Ajusta la URL según tu configuración:

```
# Sin contraseña
DATABASE_URL=postgresql://postgres@localhost:5432/trycore_evm

# Con contraseña
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/trycore_evm

# Con puerto diferente
DATABASE_URL=postgresql://postgres@localhost:5433/trycore_evm
```

### Iniciar el backend

```
uvicorn app.main:app --reload
```
El servidor estará disponible en: http://localhost:8000

API Docs (Swagger): http://localhost:8000/docs

## 4.5. Configurar el frontend

### Instalar dependencias

```
cd frontend
npm install
```

### Iniciar el frontend

```
ng serve --open
```

El servidor estará disponible en: http://localhost:4200

## 6. Estructura del Proyecto

```
ProjectMetrics/
├── backend/
│   ├── app/
│   │   ├── core/              # Configuración central
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Lógica de negocio (EVM Calculator)
│   │   ├── routers/           # Endpoints API
│   │   └── main.py            # FastAPI app
│   ├── scripts/
│   │   └── init_db.sql        # Script de inicialización
│   ├── tests/                 # Pruebas unitarias e integración
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/          # Models y services
│   │   │   └── components/    # Componentes Angular
│   │   ├── environments/
│   │   └── styles.css
│   ├── angular.json
│   └── package.json
├── AI_PROCESS.md
├── PROMPTS.md
└── README.md
```

# Evaluador
Este proyecto fue desarrollado como prueba técnica para Trycore Colombia.

Fecha de entrega: Sábado 27 de junio 2026# 