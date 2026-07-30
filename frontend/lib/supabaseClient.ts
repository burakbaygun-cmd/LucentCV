import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "https://runvrifzcsjptzluyvqq.supabase.co";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1bnZyaWZ6Y3NqcHR6bHV5dnFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM4NDg2NzUsImV4cCI6MjA5OTQyNDY3NX0.49VvSYNOvrcHanaakM_SrcdwzUDu27JC32qTDl7-g-g";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
