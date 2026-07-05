CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    cv_text TEXT,
    job_text TEXT,
    match_score INTEGER,
    summary TEXT,
    strengths JSONB,
    weaknesses JSONB,
    missing_skills JSONB,
    recommendations JSONB,
    raw_response JSONB,
    status TEXT
);

CREATE TABLE IF NOT EXISTS interview_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    question TEXT,
    expected_answer TEXT,
    difficulty TEXT,
    category TEXT,
    order_index INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS interview_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID REFERENCES interview_questions(id) ON DELETE CASCADE,
    answer TEXT,
    score INTEGER,
    feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_interview_questions_analysis_id ON interview_questions(analysis_id);
CREATE INDEX IF NOT EXISTS idx_interview_questions_created_at ON interview_questions(created_at);
CREATE INDEX IF NOT EXISTS idx_interview_answers_question_id ON interview_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_interview_answers_created_at ON interview_answers(created_at);
