CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,

    assessment_phase VARCHAR(10)
        CHECK (assessment_phase IN ('pre', 'post')) NOT NULL,

    summary_mode VARCHAR(20)
        CHECK (summary_mode IN ('basic', 'conceptual', 'detailed')) NOT NULL,

    accuracy NUMERIC(5,2) NOT NULL,
    total_score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,

    difficulty_analysis JSONB NOT NULL,
    concept_analysis JSONB NOT NULL,

    attempt_metadata JSONB,
    integrity_score NUMERIC(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,

    best_accuracy NUMERIC(5,2) NOT NULL,
    certificate_version INTEGER DEFAULT 1,

    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,

    certificate_data JSONB NOT NULL,

    UNIQUE (student_id, topic)
);

