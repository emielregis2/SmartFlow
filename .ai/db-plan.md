# SmartFlow - Plan bazy danych

## Przegląd

Ten dokument opisuje schemat bazy danych PostgreSQL dla aplikacji SmartFlow - systemu analizy procesów biznesowych z wykorzystaniem AI. Projekt został zoptymalizowany pod kątem MVP przy zachowaniu możliwości przyszłej rozbudowy.

## Architektura

### Platforma
- **Baza danych:** PostgreSQL 15+ (Supabase)
- **Autentykacja:** Supabase Auth (tabela auth.users)
- **Bezpieczeństwo:** Row Level Security (RLS)
- **Framework:** Python/Streamlit

### Główne założenia
- Prostota MVP przy zachowaniu elastyczności
- Bezpieczeństwo na poziomie wiersza (RLS)
- JSONB dla elastycznego przechowywania danych AI
- UUID klucze główne dla bezpieczeństwa
- Soft delete dla zachowania historii

## Schemat bazy danych

### 1. Tabela `profiles`
Przechowuje informacje o firmie użytkownika w relacji 1:1 z auth.users.

```sql
CREATE TABLE profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE NOT NULL,
    company_size company_size_enum NOT NULL,
    industry industry_enum NOT NULL,
    budget_range budget_range_enum NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
```

**Pola:**
- `id` - UUID, klucz główny
- `user_id` - UUID, referencja do auth.users, UNIQUE (relacja 1:1)
- `company_size` - enum, wielkość firmy
- `industry` - enum, branża
- `budget_range` - enum, zakres budżetu
- `created_at` - timestamp utworzenia
- `updated_at` - timestamp ostatniej modyfikacji

### 2. Tabela `processes`
Przechowuje procesy biznesowe użytkowników wraz z danymi analizy.

```sql
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
```

**Pola:**
- `id` - UUID, klucz główny
- `user_id` - UUID, właściciel procesu
- `title` - VARCHAR(255), nazwa procesu (NOT NULL)
- `description` - TEXT, opis procesu (nullable)
- `form_data` - JSONB, dane z formularza analizy
- `ai_analysis` - JSONB, wyniki analizy AI (nullable do czasu analizy)
- `potential_score` - INTEGER (1-10), ocena potencjału z AI
- `status` - enum, status procesu
- `deleted_at` - TIMESTAMPTZ, soft delete (nullable)
- `created_at` - timestamp utworzenia
- `updated_at` - timestamp ostatniej modyfikacji

## Enumeracje

### company_size_enum
```sql
CREATE TYPE company_size_enum AS ENUM (
    '5-10 osób',
    '11-25 osób', 
    '26-50 osób'
);
```

### industry_enum
```sql
CREATE TYPE industry_enum AS ENUM (
    'Marketing',
    'Księgowość',
    'Handel',
    'Produkcja',
    'Usługi'
);
```

### budget_range_enum
```sql
CREATE TYPE budget_range_enum AS ENUM (
    'do 500 zł/miesiąc',
    '500-2000 zł/miesiąc',
    'powyżej 2000 zł/miesiąc'
);
```

### process_status_enum
```sql
CREATE TYPE process_status_enum AS ENUM (
    'draft',
    'analyzed', 
    'implemented'
);
```

## Struktura JSONB

### form_data (processes.form_data)
```json
{
    "company": {
        "size": "11-25 osób",
        "industry": "Marketing",
        "budget": "500-2000 zł/miesiąc"
    },
    "process": {
        "name": "Wystawianie faktur",
        "frequency": "raz w tygodniu",
        "participants": "2-3 osoby", 
        "duration": 4.0,
        "description": "Proces tworzenia i wysyłania faktur do klientów..."
    },
    "improvement_goal": ["szybkość", "mniej błędów"]
}
```

### ai_analysis (processes.ai_analysis)
```json
{
    "ocena_potencjalu": 8,
    "mozliwe_oszczednosci": {
        "czas_godziny_miesiecznie": 16,
        "oszczednosci_pieniadze_miesiecznie": 2400
    },
    "rekomendacje": [
        {
            "narzedzie": "Zapier + InvoiceNinja",
            "czas_wdrozenia": "1 tydzień",
            "koszt_miesiecznie": 400,
            "opis": "Automatyczne tworzenie faktur z danych klientów"
        }
    ],
    "plan_wdrozenia": [
        "Tydzień 1: Konfiguracja InvoiceNinja",
        "Tydzień 2: Połączenie przez Zapier"
    ],
    "uwagi": [
        "Wymaga zgodę klientów na automatyczne faktury"
    ],
    "generated_at": "2025-06-08T10:30:00Z",
    "model_used": "gpt-4"
}
```

## Indeksy

### Indeksy podstawowe
```sql
-- Indeks na user_id dla szybkich zapytań użytkownika
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_processes_user_id ON processes(user_id);

-- Indeks na created_at dla sortowania chronologicznego
CREATE INDEX idx_processes_created_at ON processes(created_at DESC);

-- Indeks na status dla filtrowania
CREATE INDEX idx_processes_status ON processes(status) WHERE deleted_at IS NULL;

-- Indeks na soft delete
CREATE INDEX idx_processes_active ON processes(user_id, created_at) WHERE deleted_at IS NULL;
```

### Indeksy JSONB
```sql
-- GIN indeks dla zapytań po form_data
CREATE INDEX idx_processes_form_data ON processes USING GIN(form_data);

-- GIN indeks dla zapytań po ai_analysis  
CREATE INDEX idx_processes_ai_analysis ON processes USING GIN(ai_analysis);

-- Indeks na ocenę potencjału
CREATE INDEX idx_processes_potential_score ON processes(potential_score) WHERE potential_score IS NOT NULL;
```

## Row Level Security (RLS)

### Włączenie RLS
```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE processes ENABLE ROW LEVEL SECURITY;
```

### Policies dla tabeli `profiles`

```sql
-- Użytkownicy mogą widzieć tylko swój profil
CREATE POLICY "profiles_select_own" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

-- Użytkownicy mogą tworzyć tylko swój profil  
CREATE POLICY "profiles_insert_own" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Użytkownicy mogą edytować tylko swój profil
CREATE POLICY "profiles_update_own" ON profiles
    FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Użytkownicy mogą usuwać tylko swój profil
CREATE POLICY "profiles_delete_own" ON profiles
    FOR DELETE USING (auth.uid() = user_id);
```

### Policies dla tabeli `processes`

```sql
-- Użytkownicy mogą widzieć tylko swoje procesy (bez usuniętych)
CREATE POLICY "processes_select_own" ON processes
    FOR SELECT USING (auth.uid() = user_id AND deleted_at IS NULL);

-- Użytkownicy mogą tworzyć tylko swoje procesy
CREATE POLICY "processes_insert_own" ON processes  
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Użytkownicy mogą edytować tylko swoje procesy
CREATE POLICY "processes_update_own" ON processes
    FOR UPDATE USING (auth.uid() = user_id AND deleted_at IS NULL) 
    WITH CHECK (auth.uid() = user_id);

-- Użytkownicy mogą "usuwać" (soft delete) tylko swoje procesy
CREATE POLICY "processes_delete_own" ON processes
    FOR UPDATE USING (auth.uid() = user_id AND deleted_at IS NULL)
    WITH CHECK (auth.uid() = user_id);
```

## Funkcje pomocnicze

### Trigger automatycznej aktualizacji updated_at
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger dla profiles
CREATE TRIGGER profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Trigger dla processes
CREATE TRIGGER processes_updated_at
    BEFORE UPDATE ON processes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Funkcja soft delete
```sql
CREATE OR REPLACE FUNCTION soft_delete_process(process_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE processes 
    SET deleted_at = NOW(), updated_at = NOW()
    WHERE id = process_id AND user_id = auth.uid() AND deleted_at IS NULL;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Optymalizacje wydajności

### Strategia indeksowania
1. **Podstawowe zapytania** - indeksy na user_id i created_at
2. **JSONB queries** - GIN indeksy dla elastycznych zapytań
3. **Filtrowanie** - indeksy na często używane pola (status, potential_score)
4. **Soft delete** - indeksy częściowe wykluczające usunięte rekordy

### Przykładowe zapytania zoptymalizowane
```sql
-- Lista procesów użytkownika (używa idx_processes_active)
SELECT * FROM processes 
WHERE user_id = auth.uid() AND deleted_at IS NULL 
ORDER BY created_at DESC;

-- Procesy z wysoką oceną (używa idx_processes_potential_score)
SELECT * FROM processes 
WHERE user_id = auth.uid() AND potential_score >= 8 AND deleted_at IS NULL;

-- Wyszukiwanie w analizach AI (używa idx_processes_ai_analysis)
SELECT * FROM processes 
WHERE user_id = auth.uid() 
  AND ai_analysis ? 'rekomendacje' 
  AND deleted_at IS NULL;
```

## Skalowalność

### Partycjonowanie (przyszłość)
Gdy liczba procesów przekroczy 100K rekordów, można rozważyć partycjonowanie po:
- **Czasie** - partycje miesięczne po created_at
- **Użytkownikach** - hash partitioning po user_id

### Archiwizacja
Procesy starsze niż 2 lata można przenieść do tabeli archiwizacyjnej:
```sql
CREATE TABLE processes_archive (LIKE processes INCLUDING ALL);
```

## Bezpieczeństwo

### Ochrona danych
- **RLS policies** - izolacja danych między użytkownikami
- **UUID klucze** - trudne do zgadnięcia identyfikatory
- **Soft delete** - możliwość odzyskania omyłkowo usuniętych danych
- **Foreign key constraints** - integralność referencyjna

### Audit trail
Wszystkie tabele zawierają:
- `created_at` - kiedy rekord został utworzony
- `updated_at` - kiedy ostatnio modyfikowany
- `user_id` - kto jest właścicielem

### Backup i recovery
- Supabase automatyczne backupy
- JSONB pozwala na łatwe eksporty danych
- Point-in-time recovery przez Supabase

## Migracje

Struktura plików migracji (chronologicznie):
1. `001_create_enums.sql` - typy wyliczeniowe
2. `002_create_profiles.sql` - tabela profili
3. `003_create_processes.sql` - tabela procesów  
4. `004_create_indexes.sql` - indeksy wydajnościowe
5. `005_enable_rls.sql` - Row Level Security i policies
6. `006_create_functions.sql` - funkcje pomocnicze i triggery

## Walidacja schematu

### Ograniczenia integralności
- Foreign keys zapewniają spójność relacji
- Check constraints walidują zakresy wartości
- NOT NULL dla krytycznych pól
- UNIQUE constraints zapobiegają duplikatom

### Przykłady walidacji
```sql
-- Sprawdzenie struktury JSONB
SELECT id, title 
FROM processes 
WHERE NOT (form_data ? 'company' AND form_data ? 'process');

-- Statystyki analiz AI
SELECT 
    COUNT(*) as total_processes,
    COUNT(ai_analysis) as analyzed_processes,
    AVG(potential_score) as avg_score
FROM processes 
WHERE deleted_at IS NULL;
```

---

**Autor:** Sesja planistyczna z AI (10xDevs)  
**Data:** 8 czerwca 2025  
**Status:** Gotowy do implementacji