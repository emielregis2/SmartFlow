-- SmartFlow - Konfiguracja bazy danych Supabase
-- Skopiuj i wklej ten kod do Supabase SQL Editor

-- =====================================================
-- 1. ENUMY (Typy wyliczeniowe)
-- =====================================================

CREATE TYPE company_size_enum AS ENUM (
    '5-10 osób',
    '11-25 osób', 
    '26-50 osób'
);

CREATE TYPE industry_enum AS ENUM (
    'Marketing',
    'Księgowość',
    'Handel',
    'Produkcja',
    'Usługi'
);

CREATE TYPE budget_range_enum AS ENUM (
    'do 500 zł/miesiąc',
    '500-2000 zł/miesiąc',
    'powyżej 2000 zł/miesiąc'
);

CREATE TYPE process_status_enum AS ENUM (
    'draft',
    'analyzed', 
    'implemented'
);

-- =====================================================
-- 2. TABELE
-- =====================================================

-- Tabela profiles (profil firmy użytkownika)
CREATE TABLE profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE NOT NULL,
    company_size company_size_enum NOT NULL,
    industry industry_enum NOT NULL,
    budget_range budget_range_enum NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Tabela processes (procesy biznesowe)
CREATE TABLE processes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    form_data JSONB NOT NULL,
    ai_analysis JSONB,
    potential_score INTEGER CHECK (potential_score >= 1 AND potential_score <= 10),
    status process_status_enum DEFAULT 'draft' NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- =====================================================
-- 3. INDEKSY
-- =====================================================

-- Indeksy podstawowe
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_processes_user_id ON processes(user_id);
CREATE INDEX idx_processes_created_at ON processes(created_at DESC);
CREATE INDEX idx_processes_status ON processes(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_processes_active ON processes(user_id, created_at) WHERE deleted_at IS NULL;

-- Indeksy JSONB
CREATE INDEX idx_processes_form_data ON processes USING GIN(form_data);
CREATE INDEX idx_processes_ai_analysis ON processes USING GIN(ai_analysis);
CREATE INDEX idx_processes_potential_score ON processes(potential_score) WHERE potential_score IS NOT NULL;

-- =====================================================
-- 4. ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Włączenie RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE processes ENABLE ROW LEVEL SECURITY;

-- Policies dla tabeli profiles
CREATE POLICY "profiles_select_own" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "profiles_insert_own" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "profiles_update_own" ON profiles
    FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

CREATE POLICY "profiles_delete_own" ON profiles
    FOR DELETE USING (auth.uid() = user_id);

-- Policies dla tabeli processes
CREATE POLICY "processes_select_own" ON processes
    FOR SELECT USING (auth.uid() = user_id AND deleted_at IS NULL);

CREATE POLICY "processes_insert_own" ON processes  
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "processes_update_own" ON processes
    FOR UPDATE USING (auth.uid() = user_id AND deleted_at IS NULL) 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "processes_delete_own" ON processes
    FOR UPDATE USING (auth.uid() = user_id AND deleted_at IS NULL)
    WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- 5. FUNKCJE POMOCNICZE
-- =====================================================

-- Funkcja automatycznej aktualizacji updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggery dla automatycznej aktualizacji updated_at
CREATE TRIGGER profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER processes_updated_at
    BEFORE UPDATE ON processes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Funkcja soft delete
CREATE OR REPLACE FUNCTION soft_delete_process(process_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE processes 
    SET deleted_at = NOW(), updated_at = NOW()
    WHERE id = process_id AND user_id = auth.uid() AND deleted_at IS NULL;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 6. TESTOWE DANE (OPCJONALNE)
-- =====================================================

-- Dodaj przykładowe dane tylko jeśli chcesz przetestować strukturę
-- INSERT INTO profiles (user_id, company_size, industry, budget_range) 
-- VALUES (auth.uid(), '11-25 osób', 'Marketing', '500-2000 zł/miesiąc');

-- =====================================================
-- GOTOWE! 
-- =====================================================
-- Baza danych SmartFlow została skonfigurowana.
-- Możesz teraz uruchomić aplikację z pełną integracją. 