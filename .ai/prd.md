# SmartFlow - Specyfikacja Aplikacji

## Cel aplikacji

**Problem:** Małe i średnie firmy (do 50 osób) słyszą o sztucznej inteligencji i automatyzacji, ale nie wiedzą gdzie zacząć ani które codzienne zadania warto usprawnić.

**Rozwiązanie:** SmartFlow to aplikacja internetowa wykorzystująca sztuczną inteligencję do analizy procesów biznesowych i tworzenia konkretnych porad automatyzacji dopasowanych do wielkości firmy, budżetu i umiejętności technicznych.

**Dla kogo:** Małe i średnie firmy (5-50 pracowników), każda branża, bez wymagań technicznych.

---

## Dla kogo tworzymy aplikację

### Główni użytkownicy:
- Właściciele małych firm (5-25 osób)
- Kierownicy w średnich firmach (25-50 osób)  
- Osoby odpowiedzialne za usprawnianie pracy w firmie

### Przykładowi użytkownicy:

**Anna (35) - Właścicielka agencji reklamowej (12 osób)**
- Problem: Za dużo czasu na administrację, mało na strategię
- Cel: Zautomatyzować tworzenie raportów i wystawianie faktur
- Umiejętności: Podstawowe (Excel, Canva, media społecznościowe)

**Michał (42) - Kierownik w firmie księgowej (28 osób)**
- Problem: Ręczne przetwarzanie faktur i deklaracji
- Cel: Zmniejszyć błędy i przyspieszyć procesy
- Umiejętności: Średnie (programy księgowe, podstawy automatyzacji)

---

## Główne funkcje aplikacji

### Wersja podstawowa (na 7 dni):

#### 1. Logowanie użytkowników
- Rejestracja i logowanie emailem
- Resetowanie hasła
- Bezpieczne przechowywanie danych

#### 2. Formularz analizy procesu
Prosty formularz zbierający informacje:

**O firmie:**
- Wielkość firmy: [5-10] [11-25] [26-50] osób
- Branża: [lista 10 najpopularniejszych]
- Budżet na usprawnienia: [do 500] [500-2000] [powyżej 2000] zł/miesiąc

**O procesie:**
- Nazwa procesu (np. "Wystawianie faktur")
- Jak często: [codziennie] [raz w tygodniu] [raz w miesiącu]
- Ile osób bierze udział: [1] [2-3] [4 lub więcej]
- Ile czasu zajmuje: [minuty/godziny]
- Opis procesu: [pole tekstowe]

**Cel usprawnienia:**
- Co chcesz poprawić: [szybkość] [mniej błędów] [mniej nudnej pracy] [oszczędność pieniędzy]

#### 3. Analiza sztuczną inteligencją
**Wejście:** Dane z formularza  
**Przetwarzanie:** ChatGPT analizuje i tworzy:
- Ocenę potencjału (skala 1-10)
- Identyfikację problemów
- Konkretne narzędzia do usprawnienia
- Szacunek oszczędności czasu i pieniędzy
- Plan wdrożenia krok po kroku

#### 4. Zarządzanie analizami
- Dodawanie nowych procesów do analizy
- Lista wszystkich przeanalizowanych procesów
- Podgląd szczegółów każdej analizy
- Usuwanie niepotrzebnych analiz

#### 5. Strona z wynikami
- Lista wszystkich procesów z oceną potencjału
- Ranking procesów do usprawienia
- Podsumowanie: łączne możliwe oszczędności

---

## Jak będzie działać aplikacja

### Typowe użycie:
1. **Rejestracja** → podanie emaila i hasła
2. **Pierwsze logowanie** → 3 podstawowe pytania o firmę
3. **Dodanie procesu** → kliknięcie "Przeanalizuj nowy proces"
4. **Wypełnienie formularza** → 2-3 minuty
5. **Opis procesu** → krótki tekst, 50-200 słów
6. **Otrzymanie analizy** → sztuczna inteligencja generuje wyniki w 30 sekund
7. **Przegląd porad** → konkretne narzędzia i plan działania
8. **Zapisanie wyników** → dashboard ze wszystkimi procesami

---

## Technologia

### Narzędzia:
- **Język programowania:** Python
- **Aplikacja internetowa:** Streamlit (szybkie tworzenie interfejsu)
- **Baza danych:** Supabase (przechowywanie danych w chmurze)
- **Logowanie:** Supabase (gotowe rozwiązanie)
- **Sztuczna inteligencja:** ChatGPT-4o
- **Publikacja:** Railway (automatyczne umieszczenie w internecie)
- **Programowanie:** Cursor (edytor z pomocą AI)

### Struktura bazy danych:

```sql
-- Użytkownicy (obsługuje Supabase)
users (
  id - unikalny identyfikator,
  email - adres email,
  data_utworzenia
)

-- Profile użytkowników
profiles (
  id - identyfikator użytkownika,
  wielkosc_firmy - rozmiar firmy,
  branza - sektor działalności,
  budzet - zakres budżetu,
  data_utworzenia
)

-- Przeanalizowane procesy
processes (
  id - unikalny identyfikator,
  uzytkownik_id - który użytkownik,
  nazwa - nazwa procesu,
  opis - opis procesu,
  dane_formularza - wszystkie odpowiedzi z formularza,
  analiza_ai - wyniki analizy,
  ocena_potencjalu - liczba od 1 do 10,
  status - czy zrealizowane,
  data_utworzenia,
  data_aktualizacji
)
```

---

## Jak działa sztuczna inteligencja

### Integracja z ChatGPT:

**Instrukcje dla sztucznej inteligencji:**
```
Jesteś ekspertem od usprawniania pracy w małych firmach (5-50 osób). 
Analizujesz procesy biznesowe pod kątem możliwości automatyzacji, uwzględniając:
- Budżet firmy
- Umiejętności techniczne zespołu  
- Zgodność z prawem (RODO, etc.)
- Zwrot z inwestycji w perspektywie 6-12 miesięcy

Zawsze podawaj konkretne narzędzia (Zapier, n8n, Airtable) zamiast ogólnych rad.
Odpowiadaj po polsku w strukturalnym formacie.
```

**Co dostaje sztuczna inteligencja:**
```json
{
  "firma": {
    "wielkosc": "11-25",
    "branza": "marketing", 
    "budzet": "500-2000",
    "umiejetnosci": "podstawowe"
  },
  "proces": {
    "nazwa": "Wystawianie faktur klientom",
    "czestotliwosc": "raz w tygodniu", 
    "uczestnicy": 2,
    "czas_godziny": 4,
    "opis": "..."
  }
}
```

**Co zwraca sztuczna inteligencja:**
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
    "Tydzień 2: Połączenie z systemem klientów przez Zapier"
  ],
  "uwagi": [
    "Wymaga zgodę klientów na automatyczne faktury"
  ]
}
```

---

## Testowanie

### Testy jednostkowe:
```python
# Test funkcji analizy
def test_analiza_procesu():
    dane_testowe = {...}
    wynik = analizuj_proces(dane_testowe)
    assert wynik["ocena_potencjalu"] >= 1
    assert wynik["ocena_potencjalu"] <= 10
    assert "rekomendacje" in wynik

# Test operacji na procesach
def test_utworz_proces():
    dane_procesu = {...}
    utworzony = utworz_proces(id_uzytkownika, dane_procesu)
    assert utworzony.id is not None
    assert utworzony.nazwa == dane_procesu["nazwa"]
```

### Test pełnej aplikacji:
```python
def test_pelny_przeplyw_uzytkownika():
    # 1. Zarejestruj użytkownika
    # 2. Zaloguj się
    # 3. Dodaj proces z formularzem
    # 4. Sprawdź czy analiza AI się wygenerowała
    # 5. Sprawdź czy proces widać na liście
    # 6. Edytuj proces
    # 7. Usuń proces
```

---

## Publikacja i automatyzacja

### Automatyczne wdrażanie (GitHub Actions):
```yaml
name: SmartFlow - Automatyczne wdrażanie
on: [push, pull_request]

jobs:
  testy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Instalacja Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Instalacja zależności
        run: pip install -r requirements.txt
      - name: Uruchomienie testów
        run: pytest tests/
      - name: Sprawdzenie kodu
        run: black --check . && flake8

  wdrozenie:
    needs: testy
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Wdrożenie na Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway deploy
```

---

## Jak zmierzymy sukces

### Wymagania techniczne:
- Wszystkie testy przechodzą (100% wymagane)
- Sztuczna inteligencja odpowiada w mniej niż 30 sekund
- Aplikacja działa bez przerw (99%+ czasu)
- Strona ładuje się w mniej niż 3 sekundy

### Wymagania użytkowe:
- 90%+ użytkowników kończy pełną analizę procesu
- Rady sztucznej inteligencji oceniane jako użyteczne (4/5+)
- Użytkownicy wracają analizować 2+ procesy
- Zero krytycznych błędów w działającej aplikacji

---

## Plan realizacji - 7 dni

### Dzień 1-2: Podstawy
- Konfiguracja Cursor i struktury projektu
- Ustawienie Supabase (logowanie + baza danych)
- Podstawowa aplikacja Streamlit z logowaniem
- Podstawowy formularz analizy

### Dzień 3-4: Główne funkcje
- Implementacja formularza z wszystkimi polami
- Integracja z ChatGPT i testowanie promptów
- Operacje na procesach (dodawanie, przeglądanie, usuwanie)
- Podstawowa strona z wynikami

### Dzień 5-6: Finalizacja
- Testy jednostkowe i pełnej aplikacji
- GitHub Actions (automatyczne wdrażanie)
- Publikacja na Railway
- Poprawki błędów i optymalizacja

### Dzień 7: Rezerwa
- Dodatkowe testowanie
- Dokumentacja
- Ostatnie poprawki
- Przygotowanie do wysłania

---

## Bezpieczeństwo

### Ochrona danych:
- Wszystkie klucze API w zmiennych środowiskowych
- Supabase Row Level Security (każdy widzi tylko swoje dane)
- Tylko HTTPS w wersji produkcyjnej
- Walidacja wszystkich danych wejściowych

### Zgodność z RODO:
- Możliwość usunięcia danych użytkownika
- Jasna polityka prywatności
- Zgoda na przetwarzanie danych
- Europejska instancja Supabase

---

## Czego NIE robimy w tej wersji

### Funkcje NIE uwzględnione:
- Współpraca wielu użytkowników
- Wgrywanie plików/dokumentów do analizy
- Zaawansowane raporty i analityka
- Integracja z zewnętrznymi narzędziami
- Aplikacja mobilna
- Personalizacja dla konkretnych firm
- System płatności
- Obsługa wielu języków

### Pomysły na przyszłość:
- Analiza dokumentów PDF
- Integracja z popularnymi narzędziami biznesowymi
- Funkcje zespołowe
- Zaawansowane analizy i raporty
- Aplikacja mobilna

---

## Definicja gotowości

### Aplikacja jest gotowa gdy:

1. **Logowanie działa**: Rejestracja, logowanie, wylogowanie
2. **Formularz funkcjonuje**: Wszystkie pola działają, walidacja danych
3. **Analiza AI działa**: Integracja z ChatGPT zwraca strukturalne wyniki
4. **Zarządzanie procesami**: Dodawanie, przeglądanie, edycja, usuwanie
5. **Strona wyników**: Lista procesów z ocenami potencjału
6. **Testy przechodzą**: Testy jednostkowe + przynajmniej jeden test pełnej aplikacji
7. **Automatyzacja działa**: GitHub Actions wdraża automatycznie
8. **Wersja produkcyjna**: Opublikowana na Railway, dostępna przez internet
9. **Dokumentacja**: README z instrukcją instalacji
10. **Przykłady działania**: Przynajmniej 3 przykładowe analizy procesów

---

## Lista kontrolna przed wysłaniem

### Do kursu 10xDevs:
- Repozytorium GitHub z kompletnym kodem
- Działający adres internetowy aplikacji
- README z opisem projektu
- Film demonstracyjny (opcjonalnie ale zalecane)
- Wszystkie wymagania spełnione:
  - Logowanie
  - Logika biznesowa
  - Operacje na danych
  - Testy
  - Automatyzacja

**Termin wysłania: 15 czerwca 2025**  
**Formularz: https://airtable.com/appJmaxL3gbDV0Qcv/pagLn96rJGZklZ0A4/form**

---

*Ten dokument służy jako kompletny plan implementacji aplikacji SmartFlow w ciągu 7 dni dla kursu 10xDevs.*