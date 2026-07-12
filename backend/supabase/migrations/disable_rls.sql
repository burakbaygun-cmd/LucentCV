-- Disable RLS on tables for Guest Mode (Development Only)
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.analyses DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.interviews DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.interview_questions DISABLE ROW LEVEL SECURITY;
