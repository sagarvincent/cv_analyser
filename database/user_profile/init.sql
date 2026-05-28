-- PostgreSQL initialisation script for cv_analyser user profile schema
-- Run once against a fresh database: psql -U postgres -d <dbname> -f init.sql

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ──────────────────────────────────────────────
-- ENUMs
-- ──────────────────────────────────────────────

CREATE TYPE qualification_type AS ENUM ('degree', 'certification', 'training');

CREATE TYPE source_type AS ENUM ('qualification', 'experience', 'portfolio');

CREATE TYPE skill_level AS ENUM ('beginner', 'intermediate', 'advanced', 'expert');

CREATE TYPE cv_status AS ENUM ('pending', 'parsed', 'failed');

-- ──────────────────────────────────────────────
-- Table 1: users
-- ──────────────────────────────────────────────

CREATE TABLE users (
    id             SERIAL PRIMARY KEY,
    username       VARCHAR(50)  UNIQUE NOT NULL,
    email          VARCHAR(255) UNIQUE NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    full_name      VARCHAR(255) NOT NULL,
    date_of_birth  DATE         NOT NULL,
    location       VARCHAR(255),
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email    ON users (email);

-- ──────────────────────────────────────────────
-- Table 2: qualifications
-- ──────────────────────────────────────────────

CREATE TABLE qualifications (
    id               SERIAL PRIMARY KEY,
    user_id          INTEGER             NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    type             qualification_type  NOT NULL,
    institution_name VARCHAR(255)        NOT NULL,
    degree_name      VARCHAR(255),                   -- populated for type = 'degree'
    course_name      VARCHAR(255),                   -- populated for type = 'certification' / 'training'
    start_date       DATE                NOT NULL,
    end_date         DATE,                           -- NULL = ongoing
    marks            NUMERIC(5, 2),                  -- percentage, e.g. 85.50
    created_at       TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_qualifications_user_id ON qualifications (user_id);

-- ──────────────────────────────────────────────
-- Table 3: experience
-- ──────────────────────────────────────────────

CREATE TABLE experience (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    job_title     VARCHAR(255) NOT NULL,
    company       VARCHAR(255) NOT NULL,
    salary        NUMERIC(12, 2),
    joining_date  DATE         NOT NULL,
    leaving_date  DATE,                              -- NULL = current role
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_experience_user_id ON experience (user_id);

-- ──────────────────────────────────────────────
-- Table 4: aspirations
-- ──────────────────────────────────────────────

CREATE TABLE aspirations (
    id             SERIAL PRIMARY KEY,
    user_id        INTEGER      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    desired_role   VARCHAR(255) NOT NULL,
    desired_salary NUMERIC(12, 2),
    active         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_aspirations_user_id ON aspirations (user_id);

-- ──────────────────────────────────────────────
-- Table 5: projects
-- ──────────────────────────────────────────────

CREATE TABLE projects (
    id                    SERIAL       PRIMARY KEY,
    user_id               INTEGER      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    domain                VARCHAR(100) NOT NULL,
    name                  VARCHAR(255) NOT NULL,
    fun_description       TEXT,
    techstack_description TEXT,
    start_date            DATE,
    end_date              DATE,
    deployed              BOOLEAN      NOT NULL DEFAULT FALSE,
    source_type           source_type  NOT NULL,
    qualification_id      INTEGER      REFERENCES qualifications (id) ON DELETE SET NULL,
    experience_id         INTEGER      REFERENCES experience (id)     ON DELETE SET NULL,
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_projects_source_fk CHECK (
        (source_type = 'qualification' AND qualification_id IS NOT NULL AND experience_id IS NULL)
        OR (source_type = 'experience'    AND experience_id   IS NOT NULL AND qualification_id IS NULL)
        OR (source_type = 'portfolio'     AND qualification_id IS NULL    AND experience_id IS NULL)
    )
);

CREATE INDEX idx_projects_user_id          ON projects (user_id);
CREATE INDEX idx_projects_qualification_id ON projects (qualification_id);
CREATE INDEX idx_projects_experience_id    ON projects (experience_id);

-- ──────────────────────────────────────────────
-- Table 6: skills
-- ──────────────────────────────────────────────

CREATE TABLE skills (
    id                    SERIAL       PRIMARY KEY,
    user_id               INTEGER      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    domain                VARCHAR(100) NOT NULL,
    skill_name            VARCHAR(255) NOT NULL,
    time_duration_months  INTEGER,                   -- months of hands-on experience
    level                 skill_level  NOT NULL,
    source_type           source_type  NOT NULL,
    qualification_id      INTEGER      REFERENCES qualifications (id) ON DELETE SET NULL,
    experience_id         INTEGER      REFERENCES experience (id)     ON DELETE SET NULL,
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_skills_source_fk CHECK (
        (source_type = 'qualification' AND qualification_id IS NOT NULL AND experience_id IS NULL)
        OR (source_type = 'experience'    AND experience_id   IS NOT NULL AND qualification_id IS NULL)
        OR (source_type = 'portfolio'     AND qualification_id IS NULL    AND experience_id IS NULL)
    )
);

CREATE INDEX idx_skills_user_id          ON skills (user_id);
CREATE INDEX idx_skills_qualification_id ON skills (qualification_id);
CREATE INDEX idx_skills_experience_id    ON skills (experience_id);

-- ──────────────────────────────────────────────
-- Table 7: cv_uploads
-- ──────────────────────────────────────────────

CREATE TABLE cv_uploads (
    id                SERIAL       PRIMARY KEY,
    user_id           INTEGER      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    storage_path      TEXT         NOT NULL,           -- key/path in object storage (MinIO / S3)
    original_filename VARCHAR(255) NOT NULL,
    file_size_bytes   INTEGER      NOT NULL,
    mime_type         VARCHAR(50)  NOT NULL,           -- e.g. application/pdf
    status            cv_status    NOT NULL DEFAULT 'pending',
    uploaded_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cv_uploads_user_id ON cv_uploads (user_id);
CREATE INDEX idx_cv_uploads_status  ON cv_uploads (status);
