# SmartFlow - System Analizy Procesów Biznesowych

System wykorzystujący sztuczną inteligencję do analizy i optymalizacji procesów biznesowych w małych i średnich firmach.

## 📚 O Projekcie

Aplikacja powstała w ramach kursu **10xDevs** - kursu o wykorzystaniu AI w programowaniu.

## 🎯 Cel Projektu

SmartFlow pomaga małym i średnim firmom (5-50 osób) zidentyfikować możliwości automatyzacji i optymalizacji codziennych procesów biznesowych. System wykorzystuje sztuczną inteligencję do analizy procesów i generowania konkretnych rekomendacji, uwzględniając:
- Wielkość firmy
- Budżet na usprawnienia
- Umiejętności techniczne zespołu
- Zgodność z prawem (RODO, etc.)
- Zwrot z inwestycji

## 🚀 Funkcjonalności

### Wersja Podstawowa
1. **Logowanie użytkowników**
   - Rejestracja i logowanie przez email
   - Bezpieczne przechowywanie danych
   - Resetowanie hasła

2. **Analiza procesów**
   - Formularz zbierający informacje o firmie i procesie
   - Analiza AI z wykorzystaniem OpenAI
   - Generowanie rekomendacji i planu wdrożenia

3. **Zarządzanie analizami**
   - Lista wszystkich przeanalizowanych procesów
   - Podgląd szczegółów każdej analizy
   - Możliwość edycji i usuwania analiz

## 🛠️ Technologie

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Baza danych**: Supabase
- **AI**: OpenAI GPT-4
- **Autentykacja**: Supabase Auth

## 📋 Wymagania

- Python 3.8 lub nowszy
- pip (menedżer pakietów Pythona)
- Konto Supabase (darmowe)
- Klucz API OpenAI

## 🚀 Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/dariuszgasior/smartflow.git
cd smartflow
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skopiuj plik .env.example do .env i wypełnij zmienne środowiskowe:
```bash
cp .env.example .env
```

## ⚙️ Konfiguracja

1. Utwórz konto na [Supabase](https://supabase.com)
2. Utwórz nowy projekt i skopiuj klucze API
3. Utwórz konto na [OpenAI](https://openai.com) i wygeneruj klucz API
4. Wypełnij plik .env swoimi kluczami API:
```env
SUPABASE_URL=twoj_url
SUPABASE_KEY=twoj_klucz
OPENAI_API_KEY=twoj_klucz
```

## 🏃‍♂️ Uruchomienie

```bash
streamlit run app.py
```

Aplikacja będzie dostępna pod adresem: http://localhost:8501

## 📁 Struktura Projektu

```
smartflow/
├── streamlit_app.py    # główny plik aplikacji
├── pages/             # strony Streamlit
├── components/        # komponenty (auth, forms, utils)
├── database/          # Supabase client i modele
├── ai/                # OpenAI integration
├── requirements.txt   # Zależności projektu
├── .env.example      # Przykładowa konfiguracja
├── README.md         # Dokumentacja
└── data/             # Dane testowe
```

## 🧪 Testy

```bash
pytest
```

## 📝 Przykład Użycia

1. **Rejestracja i logowanie**
   - Utwórz konto używając adresu email
   - Zaloguj się do systemu

2. **Dodanie procesu do analizy**
   - Kliknij "Przeanalizuj nowy proces"
   - Wypełnij formularz (2-3 minuty)
   - Opisz proces (50-200 słów)

3. **Otrzymanie analizy**
   - System generuje wyniki w 30 sekund
   - Przeglądaj rekomendacje i plan wdrożenia
   - Zapisz wyniki do swojego konta

## 🤝 Współpraca

1. Fork projektu
2. Utwórz branch dla nowej funkcjonalności (`git checkout -b feature/nowa-funkcjonalnosc`)
3. Commit zmian (`git commit -am 'Dodano nową funkcjonalność'`)
4. Push do brancha (`git push origin feature/nowa-funkcjonalnosc`)
5. Utwórz Pull Request

## 📄 Licencja

MIT

## 👥 Autorzy

- Dariusz Gąsior - Główny Developer
- Claude Sonnet 4 - AI Assistant

## 🙏 Podziękowania

- OpenAI za udostępnienie API
- Supabase za świetną platformę
- Streamlit za framework do tworzenia aplikacji 