-- Create profiles table (Guest Mode compatible)
CREATE TABLE public.profiles (
    id TEXT PRIMARY KEY,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Insert a default guest user
INSERT INTO public.profiles (id, full_name) VALUES ('guest', 'Guest User') ON CONFLICT DO NOTHING;

-- Create analyses table
CREATE TABLE public.analyses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT REFERENCES public.profiles(id) NOT NULL,
    cv_text TEXT NOT NULL,
    job_text TEXT NOT NULL,
    match_score INTEGER NOT NULL,
    strengths JSONB DEFAULT '[]'::jsonb,
    missing_skills JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    summary TEXT,
    report TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create interviews table
CREATE TABLE public.interviews (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    analysis_id UUID REFERENCES public.analyses(id) ON DELETE CASCADE NOT NULL,
    user_id TEXT REFERENCES public.profiles(id) NOT NULL,
    overall_score INTEGER,
    feedback_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create interview_questions table
CREATE TABLE public.interview_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    interview_id UUID REFERENCES public.interviews(id) ON DELETE CASCADE NOT NULL,
    question_text TEXT NOT NULL,
    focus_area TEXT,
    question_type TEXT,
    user_answer TEXT,
    score INTEGER,
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
