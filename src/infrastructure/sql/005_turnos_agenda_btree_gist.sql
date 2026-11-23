-- Migración DDL de referencia para prevención de solapamientos en PostgreSQL 15+
-- Change: crear-turno-sin-solapamientos (C-06)
-- Reglas cubiertas: RN-AU-01, RN-AG-01, RN-AG-02, RN-AG-03, RN-AG-04, RN-AU-05

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE IF NOT EXISTS turnos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultorio_id UUID NOT NULL REFERENCES consultorios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    profesional_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    sillon_id UUID NOT NULL REFERENCES sillones(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    prestacion_id UUID NOT NULL REFERENCES prestaciones(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    inicio TIMESTAMPTZ NOT NULL,
    fin TIMESTAMPTZ NOT NULL,
    duracion_minutos INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'reservado',
    origen TEXT NOT NULL DEFAULT 'interno',
    token_publico_hash TEXT NOT NULL UNIQUE,
    observaciones_agenda TEXT,
    creado_por_usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL ON UPDATE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_turnos_rango_valido CHECK (fin > inicio),
    CONSTRAINT chk_turnos_duracion_positiva CHECK (duracion_minutos > 0),
    CONSTRAINT chk_turnos_estado_valido CHECK (
        estado IN ('reservado', 'confirmado', 'en_atencion', 'atendido', 'ausente', 'cancelado')
    ),
    CONSTRAINT chk_turnos_origen_valido CHECK (origen IN ('interno', 'publico')),

    -- RN-AG-03: Ningún profesional puede tener dos turnos activos superpuestos en intervalo semiabierto [inicio, fin)
    CONSTRAINT excl_turnos_no_solapamiento_profesional EXCLUDE USING gist (
        consultorio_id WITH =,
        profesional_id WITH =,
        tstzrange(inicio, fin, '[)') WITH &&
    ) WHERE (estado <> 'cancelado'),

    -- RN-AG-04: Ningún sillón/box puede tener dos turnos activos superpuestos en intervalo semiabierto [inicio, fin)
    CONSTRAINT excl_turnos_no_solapamiento_sillon EXCLUDE USING gist (
        consultorio_id WITH =,
        sillon_id WITH =,
        tstzrange(inicio, fin, '[)') WITH &&
    ) WHERE (estado <> 'cancelado')
);

CREATE INDEX IF NOT EXISTS idx_turnos_consultorio_inicio_estado
    ON turnos (consultorio_id, inicio, estado);

CREATE INDEX IF NOT EXISTS idx_turnos_profesional_id
    ON turnos (profesional_id);

CREATE INDEX IF NOT EXISTS idx_turnos_sillon_id
    ON turnos (sillon_id);

CREATE INDEX IF NOT EXISTS idx_turnos_paciente_id
    ON turnos (paciente_id);
