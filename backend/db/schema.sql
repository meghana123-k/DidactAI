CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,

    mode VARCHAR(20) CHECK (mode IN ('pre', 'post')) NOT NULL,

    accuracy NUMERIC(5,2) NOT NULL,
    total_score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,

    difficulty_analysis JSONB NOT NULL,
    concept_analysis JSONB NOT NULL,

    attempt_metadata JSONB,         -- timing, tab switch, etc (future)
    integrity_score NUMERIC(5,2),   -- optional

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    student_id VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,

    best_accuracy NUMERIC(5,2) NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    certificate_data JSONB NOT NULL,

    UNIQUE (student_id, topic)
);
