# SmartFlow - Plan implementacji serwisu OpenAI

## Przegląd

Ten dokument opisuje implementację serwisu OpenAI dla aplikacji SmartFlow. Projekt został zoptymalizowany pod kątem prostoty MVP przy wykorzystaniu GPT-4o z structured JSON outputs.

## Architektura serwisu

### Główne założenia
- Synchroniczna analiza procesów (użytkownik czeka na wynik)
- GPT-4o model dla wysokiej jakości analiz
- Strict JSON schema z function calling
- Minimalna złożoność dla szybkiej implementacji
- Deterministyczne wyniki (temperature 0.0)

### Komponenty
1. **AIService** - główna klasa do komunikacji z OpenAI
2. **PromptTemplate** - szablon prompta systemowego
3. **JSONSchema** - struktura oczekiwanej odpowiedzi
4. **ErrorHandler** - podstawowa obsługa błędów
5. **TokenCounter** - liczenie tokenów przed wysłaniem

## Struktura plików

```
smartflow/
├── ai/
│   ├── __init__.py
│   ├── openai_service.py      # Główny serwis
│   ├── prompt_template.py     # Szablon prompta
│   ├── json_schema.py         # Schema dla function calling
│   └── utils.py               # Utility functions
├── .env                       # OPENAI_API_KEY
└── requirements.txt           # openai>=1.12.0
```

## JSON Schema definicja

### Struktura odpowiedzi
```python
ANALYSIS_SCHEMA = {
    "name": "analyze_business_process",
    "description": "Analizuje proces biznesowy i generuje rekomendacje automatyzacji",
    "parameters": {
        "type": "object",
        "properties": {
            "ocena_potencjalu": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10,
                "description": "Ocena potencjału automatyzacji od 1 do 10"
            },
            "mozliwe_oszczednosci": {
                "type": "object",
                "properties": {
                    "czas_godziny_miesiecznie": {
                        "type": "number",
                        "description": "Szacowane oszczędności czasu w godzinach miesięcznie"
                    },
                    "oszczednosci_pieniadze_miesiecznie": {
                        "type": "number",
                        "description": "Szacowane oszczędności pieniędzy w PLN miesięcznie"
                    }
                },
                "required": ["czas_godziny_miesiecznie", "oszczednosci_pieniadze_miesiecznie"]
            },
            "rekomendacje": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "narzedzie": {
                            "type": "string",
                            "description": "Nazwa konkretnego narzędzia lub rozwiązania"
                        },
                        "czas_wdrozenia": {
                            "type": "string",
                            "description": "Szacowany czas wdrożenia"
                        },
                        "koszt_miesiecznie": {
                            "type": "number",
                            "description": "Koszt miesięczny w PLN"
                        },
                        "opis": {
                            "type": "string",
                            "description": "Szczegółowy opis implementacji"
                        }
                    },
                    "required": ["narzedzie", "czas_wdrozenia", "koszt_miesiecznie", "opis"]
                },
                "minItems": 1,
                "maxItems": 3
            },
            "plan_wdrozenia": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Konkretny krok wdrożenia"
                },
                "minItems": 2,
                "maxItems": 5
            },
            "uwagi": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Ważne uwagi i zastrzeżenia"
                },
                "maxItems": 3
            }
        },
        "required": ["ocena_potencjalu", "mozliwe_oszczednosci", "rekomendacje", "plan_wdrozenia"]
    }
}
```

## Prompt Template

### System prompt
```python
SYSTEM_PROMPT = """
Jesteś ekspertem od usprawniania pracy w małych firmach (5-50 osób) w Polsce. 
Analizujesz procesy biznesowe pod kątem możliwości automatyzacji, uwzględniając:

KONTEKST POLSKI:
- Budżet firmy w PLN
- Umiejętności techniczne zespołu (podstawowe/średnie)
- Zgodność z prawem polskim (RODO, KSH, etc.)
- Zwrot z inwestycji w perspektywie 6-12 miesięcy
- Polskie narzędzia i dostawców

ZASADY ANALIZY:
1. Zawsze podawaj konkretne narzędzia (Zapier, n8n, Airtable, ClickUp) zamiast ogólnych rad
2. Realistyczne szacunki kosztów w PLN
3. Uwzględniaj czas na naukę i wdrożenie dla zespołu
4. Priorytetyzuj rozwiązania no-code/low-code
5. Oceniaj realny wpływ na codzienną pracę

STRUKTURA ODPOWIEDZI:
- Ocena potencjału: 1-10 (gdzie 10 = bardzo wysoki potencjał automatyzacji)
- Konkretne oszczędności w godzinach i PLN
- Maksymalnie 3 najlepsze rekomendacje
- Plan wdrożenia krok po kroku
- Ważne uwagi i ograniczenia

Odpowiadaj po polsku, używając polskich nazw narzędzi gdy dostępne.
"""

USER_PROMPT_TEMPLATE = """
DANE FIRMY:
- Wielkość: {company_size}
- Branża: {industry}  
- Budżet na usprawnienia: {budget_range}

PROCES DO ANALIZY:
- Nazwa: {process_name}
- Częstotliwość: {frequency}
- Liczba uczestników: {participants}
- Czas trwania: {duration} godzin
- Opis: {description}

CELE USPRAWNIENIA: {improvement_goals}

Przeanalizuj ten proces i wygeneruj rekomendacje automatyzacji dopasowane do możliwości tej firmy.
"""
```

## Implementacja AIService

### Główna klasa serwisu
```python
import openai
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ProcessAnalysisRequest:
    company_size: str
    industry: str
    budget_range: str
    process_name: str
    frequency: str
    participants: str
    duration: float
    description: str
    improvement_goals: list

class OpenAIService:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
        
    def analyze_process(self, request: ProcessAnalysisRequest) -> Dict[str, Any]:
        """
        Analizuje proces biznesowy używając OpenAI GPT-4o
        
        Args:
            request: Dane procesu do analizy
            
        Returns:
            Dict z wynikami analizy
            
        Raises:
            OpenAIError: Gdy analiza się nie powiedzie
        """
        try:
            # Sprawdź długość inputu
            self._validate_input_length(request)
            
            # Przygotuj prompt
            user_prompt = self._prepare_user_prompt(request)
            
            # Wywołaj OpenAI API
            response = self._call_openai_api(user_prompt)
            
            # Parsuj odpowiedź
            result = self._parse_response(response)
            
            # Dodaj metadane
            result["metadata"] = {
                "model_used": self.model,
                "generated_at": datetime.utcnow().isoformat(),
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            self.logger.info(f"Process analysis completed. Tokens used: {response.usage.total_tokens}")
            return result
            
        except Exception as e:
            self.logger.error(f"Process analysis failed: {str(e)}")
            raise
    
    def _validate_input_length(self, request: ProcessAnalysisRequest) -> None:
        """Sprawdza czy input nie przekracza limitów tokenów"""
        # Prosty heurystyk: 4 znaki = 1 token
        total_chars = (
            len(request.description) + 
            len(request.process_name) + 
            len(str(request.improvement_goals))
        )
        
        estimated_tokens = total_chars // 4
        if estimated_tokens > 4000:  # Zostawiamy miejsce na prompt i odpowiedź
            raise ValueError(f"Input zbyt długi: ~{estimated_tokens} tokenów. Maksimum: 4000")
    
    def _prepare_user_prompt(self, request: ProcessAnalysisRequest) -> str:
        """Przygotowuje user prompt z danych procesu"""
        improvement_goals_str = ", ".join(request.improvement_goals)
        
        return USER_PROMPT_TEMPLATE.format(
            company_size=request.company_size,
            industry=request.industry,
            budget_range=request.budget_range,
            process_name=request.process_name,
            frequency=request.frequency,
            participants=request.participants,
            duration=request.duration,
            description=request.description,
            improvement_goals=improvement_goals_str
        )
    
    def _call_openai_api(self, user_prompt: str) -> Any:
        """Wywołuje OpenAI API z function calling"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=[ANALYSIS_SCHEMA],
            function_call={"name": "analyze_business_process"},
            temperature=0.0,  # Deterministyczne wyniki
            max_tokens=2000,
            timeout=60  # 60 sekund timeout
        )
        
        return response
    
    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """Parsuje odpowiedź z OpenAI API"""
        try:
            function_call = response.choices[0].message.function_call
            if function_call.name != "analyze_business_process":
                raise ValueError("Unexpected function name in response")
                
            result = json.loads(function_call.arguments)
            return result
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {str(e)}")
```

## Error Handling

### Strategia obsługi błędów
```python
import time
from functools import wraps

def retry_on_failure(max_retries: int = 2, delay: float = 1.0):
    """Decorator dla retry logic z exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except openai.RateLimitError as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (2 ** attempt)
                        time.sleep(wait_time)
                        continue
                    break
                except openai.APITimeoutError as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(delay)
                        continue
                    break
                except Exception as e:
                    # Nie retry dla innych błędów
                    raise e
                    
            raise last_exception
        return wrapper
    return decorator

# Dodaj decorator do metody _call_openai_api
@retry_on_failure(max_retries=2, delay=1.0)
def _call_openai_api(self, user_prompt: str) -> Any:
    # ... kod jak wyżej
```

## Integracja ze Streamlit

### Wykorzystanie w aplikacji
```python
# W streamlit_app.py
import streamlit as st
from ai.openai_service import OpenAIService, ProcessAnalysisRequest

def analyze_process_with_ai(form_data: dict) -> dict:
    """Analizuje proces używając AI i zwraca wyniki"""
    
    # Inicjalizacja serwisu
    api_key = st.secrets["OPENAI_API_KEY"]  # lub os.getenv()
    ai_service = OpenAIService(api_key=api_key)
    
    # Przygotowanie requestu
    request = ProcessAnalysisRequest(
        company_size=form_data["company"]["size"],
        industry=form_data["company"]["industry"],
        budget_range=form_data["company"]["budget"],
        process_name=form_data["process"]["name"],
        frequency=form_data["process"]["frequency"],
        participants=form_data["process"]["participants"],
        duration=form_data["process"]["duration"],
        description=form_data["process"]["description"],
        improvement_goals=form_data["improvement_goal"]
    )
    
    # Analiza z progress bar
    with st.spinner("Analizuję proces za pomocą AI..."):
        try:
            result = ai_service.analyze_process(request)
            st.success("Analiza zakończona pomyślnie!")
            return result
        except Exception as e:
            st.error(f"Błąd analizy: {str(e)}")
            return None

# W formularzu procesu
if submitted:
    process_data = {
        "company": {
            "size": company_size,
            "industry": industry,
            "budget": budget
        },
        "process": {
            "name": process_name,
            "frequency": frequency,
            "participants": participants,
            "duration": duration,
            "description": description
        },
        "improvement_goal": improvement_goal
    }
    
    # Analiza AI
    analysis_result = analyze_process_with_ai(process_data)
    
    if analysis_result:
        # Zapisz do session state i bazy danych
        st.session_state.current_analysis = analysis_result
        # TODO: Zapisz do Supabase
        st.rerun()
```

## Konfiguracja i środowisko

### Zmienne środowiskowe
```bash
# .env
OPENAI_API_KEY=sk-twoj_klucz_openai
OPENAI_MODEL=gpt-4o
OPENAI_TIMEOUT=60
```

### Zależności
```txt
# requirements.txt (dodaj do istniejących)
openai>=1.12.0
tiktoken>=0.6.0
```

## Testowanie

### Testy jednostkowe
```python
import pytest
from unittest.mock import Mock, patch
from ai.openai_service import OpenAIService, ProcessAnalysisRequest

class TestOpenAIService:
    
    @pytest.fixture
    def ai_service(self):
        return OpenAIService(api_key="test-key")
    
    @pytest.fixture
    def sample_request(self):
        return ProcessAnalysisRequest(
            company_size="11-25 osób",
            industry="Marketing",
            budget_range="500-2000 zł/miesiąc",
            process_name="Wystawianie faktur",
            frequency="raz w tygodniu",
            participants="2-3 osoby",
            duration=4.0,
            description="Ręczne tworzenie faktur w Excelu",
            improvement_goals=["szybkość", "mniej błędów"]
        )
    
    @patch('openai.OpenAI')
    def test_analyze_process_success(self, mock_openai, ai_service, sample_request):
        # Mock response
        mock_response = Mock()
        mock_response.choices[0].message.function_call.name = "analyze_business_process"
        mock_response.choices[0].message.function_call.arguments = json.dumps({
            "ocena_potencjalu": 8,
            "mozliwe_oszczednosci": {
                "czas_godziny_miesiecznie": 16,
                "oszczednosci_pieniadze_miesiecznie": 2400
            },
            "rekomendacje": [{
                "narzedzie": "Zapier + InvoiceNinja",
                "czas_wdrozenia": "1 tydzień",
                "koszt_miesiecznie": 400,
                "opis": "Automatyczne faktury"
            }],
            "plan_wdrozenia": ["Krok 1", "Krok 2"]
        })
        mock_response.usage.total_tokens = 1500
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test
        result = ai_service.analyze_process(sample_request)
        
        # Assertions
        assert result["ocena_potencjalu"] == 8
        assert len(result["rekomendacje"]) == 1
        assert "metadata" in result
    
    def test_input_validation_too_long(self, ai_service):
        request = ProcessAnalysisRequest(
            # ... normalne pola
            description="x" * 20000,  # Zbyt długi opis
            # ... pozostałe pola
        )
        
        with pytest.raises(ValueError, match="Input zbyt długi"):
            ai_service.analyze_process(request)
```

### Testy integracyjne
```python
def test_real_openai_integration():
    """Test z prawdziwym API (tylko dla dev/staging)"""
    import os
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    
    service = OpenAIService(api_key=api_key)
    request = ProcessAnalysisRequest(
        # ... prawdziwe dane testowe
    )
    
    result = service.analyze_process(request)
    
    # Sprawdź strukturę odpowiedzi
    assert isinstance(result["ocena_potencjalu"], int)
    assert 1 <= result["ocena_potencjalu"] <= 10
    assert isinstance(result["rekomendacje"], list)
    assert len(result["rekomendacje"]) > 0
```

## Monitoring i logging

### Podstawowe logowanie
```python
import logging

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_service.log'),
        logging.StreamHandler()
    ]
)

# W AIService
def analyze_process(self, request: ProcessAnalysisRequest) -> Dict[str, Any]:
    start_time = time.time()
    
    try:
        self.logger.info(f"Starting analysis for process: {request.process_name}")
        result = # ... analiza
        
        duration = time.time() - start_time
        self.logger.info(
            f"Analysis completed in {duration:.2f}s. "
            f"Tokens: {result['metadata']['total_tokens']}, "
            f"Score: {result['ocena_potencjalu']}"
        )
        
        return result
        
    except Exception as e:
        self.logger.error(f"Analysis failed after {time.time() - start_time:.2f}s: {str(e)}")
        raise
```

## Bezpieczeństwo

### Ochrona API key
```python
# Nigdy nie hardcode API key
# Używaj zmiennych środowiskowych
import os
from streamlit import secrets

def get_openai_api_key():
    # W Streamlit Cloud
    if hasattr(st, 'secrets'):
        return st.secrets.get("OPENAI_API_KEY")
    
    # Lokalnie
    return os.getenv("OPENAI_API_KEY")
    
# Walidacja przed użyciem
api_key = get_openai_api_key()
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
```

### Filtrowanie wrażliwych danych
```python
import re

def sanitize_description(description: str) -> str:
    """Usuwa potencjalnie wrażliwe informacje z opisu procesu"""
    
    # Usuń numery kart kredytowych
    description = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[KARTA]', description)
    
    # Usuń emaile
    description = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', description)
    
    # Usuń numery telefonu
    description = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{3}\b', '[TELEFON]', description)
    
    return description
```

## Deployment i konfiguracja

### Streamlit secrets.toml
```toml
# .streamlit/secrets.toml
[secrets]
OPENAI_API_KEY = "sk-twoj_klucz_openai"
OPENAI_MODEL = "gpt-4o"
```

### Environment-specific config
```python
import os

class Config:
    def __init__(self):
        self.env = os.getenv("ENVIRONMENT", "development")
        self.openai_model = self._get_model_for_env()
        self.openai_timeout = int(os.getenv("OPENAI_TIMEOUT", "60"))
        self.max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "2"))
    
    def _get_model_for_env(self):
        if self.env == "production":
            return "gpt-4o"
        elif self.env == "staging":
            return "gpt-4o-mini"  # Tańszy dla testów
        else:
            return "gpt-4o-mini"  # Development
```

## Harmonogram implementacji

### Faza 1: Podstawowy serwis (2-3 godziny)
1. Stworzenie struktury folderów i plików
2. Implementacja AIService z podstawową funkcjonalnością
3. Definicja JSON schema i prompt template
4. Podstawowe testy jednostkowe

### Faza 2: Integracja (1-2 godziny)
1. Integracja ze Streamlit
2. Obsługa błędów i retry logic
3. Konfiguracja environment variables
4. Pierwsze testy z prawdziwymi danymi

### Faza 3: Finalizacja (1 godzina)
1. Logging i monitoring
2. Walidacja inputów
3. Dokumentacja API
4. Testy integracyjne

## Metryki sukcesu

### KPI serwisu AI
- **Czas odpowiedzi:** < 60 sekund dla 95% zapytań
- **Success rate:** > 95% udanych analiz
- **Jakość analiz:** Ocena użytkowników > 4/5
- **Koszt miesięczny:** < 200 PLN dla 100 analiz

### Monitoring w produkcji
- Liczba zapytań dziennie/miesięcznie
- Średni koszt na zapytanie
- Rozkład ocen potencjału (czy AI nie daje zawsze wysokich ocen)
- Najczęstsze błędy i failure reasons

---

**Autor:** Sesja planistyczna z AI (10xDevs)  
**Data:** 8 czerwca 2025  
**Status:** Gotowy do implementacji