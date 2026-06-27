-- ============================================
-- 1. ELIMINAR TABLAS SI EXISTEN (para reinicio)
-- ============================================
DROP TABLE IF EXISTS activities CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
-- ============================================
-- 2. CREAR TABLA DE PROYECTOS
-- ============================================
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ============================================
-- 3. CREAR TABLA DE ACTIVIDADES
-- ============================================
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    bac NUMERIC(12, 2) NOT NULL,
    planned_progress NUMERIC(3, 2) DEFAULT 0.00,
    actual_progress NUMERIC(3, 2) DEFAULT 0.00,
    ac NUMERIC(12, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_activity_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
-- 4. DATOS DE EJEMPLO (para pruebas)
-- ============================================
INSERT INTO projects (name, description)
VALUES (
        'Proyecto EVM Demo',
        'Proyecto de ejemplo para demostrar indicadores EVM'
    );
INSERT INTO activities (
        project_id,
        name,
        bac,
        planned_progress,
        actual_progress,
        ac
    )
VALUES (
        1,
        'Diseño de UI/UX',
        5000.00,
        0.80,
        0.60,
        4500.00
    ),
    (
        1,
        'Desarrollo Frontend',
        12000.00,
        0.50,
        0.40,
        7000.00
    ),
    (
        1,
        'Desarrollo Backend',
        15000.00,
        0.60,
        0.70,
        9500.00
    ),
    (1, 'Pruebas QA', 8000.00, 0.30, 0.20, 3000.00);
-- ============================================
-- 6. VERIFICACIÓN
-- ============================================
SELECT '✅ Base de datos inicializada correctamente!' as status;
SELECT (
        SELECT COUNT(*)
        FROM projects
    ) as total_projects,
    (
        SELECT COUNT(*)
        FROM activities
    ) as total_activities;