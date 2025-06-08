"""
Implementacja funkcji analizy procesów z wykorzystaniem OpenAI.
"""

from typing import Dict, List, Optional
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Inicjalizacja klienta OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Jesteś ekspertem od usprawniania pracy w małych firmach (5-50 osób). 
Analizujesz procesy biznesowe pod kątem możliwości automatyzacji, uwzględniając:
- Budżet firmy
- Umiejętności techniczne zespołu  
- Zgodność z prawem (RODO, etc.)
- Zwrot z inwestycji w perspektywie 6-12 miesięcy

Zawsze podawaj konkretne narzędzia (Zapier, n8n, Airtable) zamiast ogólnych rad.
Odpowiadaj po polsku w strukturalnym formacie JSON.
"""

def analyze_process(process_data: Dict) -> Dict:
    """
    Analiza procesu biznesowego z wykorzystaniem AI.
    
    Args:
        process_data: Dane procesu do analizy
        
    Returns:
        Dict z wynikami analizy
    """
    try:
        # Przygotowanie promptu
        user_prompt = f"""
        Przeanalizuj poniższy proces biznesowy i zaproponuj usprawnienia:
        
        Firma:
        - Wielkość: {process_data['company']['size']}
        - Branża: {process_data['company']['industry']}
        - Budżet: {process_data['company']['budget']}
        
        Proces:
        - Nazwa: {process_data['process']['name']}
        - Częstotliwość: {process_data['process']['frequency']}
        - Uczestnicy: {process_data['process']['participants']}
        - Czas: {process_data['process']['duration']} godzin
        - Opis: {process_data['process']['description']}
        
        Cele usprawnienia: {', '.join(process_data['improvement_goal'])}
        
        Zwróć odpowiedź w formacie JSON zawierającą:
        - ocena_potencjalu (1-10)
        - mozliwe_oszczednosci (czas_godziny_miesiecznie, oszczednosci_pieniadze_miesiecznie)
        - rekomendacje (lista narzędzi z czasem_wdrozenia, koszt_miesiecznie, opis)
        - plan_wdrozenia (lista kroków)
        """
        
        # Wywołanie API OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        # Parsowanie odpowiedzi
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Błąd analizy procesu: {e}")
        return {
            "ocena_potencjalu": 0,
            "mozliwe_oszczednosci": {
                "czas_godziny_miesiecznie": 0,
                "oszczednosci_pieniadze_miesiecznie": 0
            },
            "rekomendacje": [],
            "plan_wdrozenia": []
        }

def generate_recommendations(process_data: Dict) -> List[Dict]:
    """
    Generowanie rekomendacji dla procesu.
    
    Args:
        process_data: Dane procesu
        
    Returns:
        Lista rekomendacji
    """
    try:
        analysis = analyze_process(process_data)
        return analysis.get("rekomendacje", [])
    except Exception as e:
        print(f"Błąd generowania rekomendacji: {e}")
        return []

def calculate_savings(process_data: Dict) -> Dict:
    """
    Obliczanie potencjalnych oszczędności.
    
    Args:
        process_data: Dane procesu
        
    Returns:
        Dict z oszczędnościami czasu i pieniędzy
    """
    try:
        analysis = analyze_process(process_data)
        return analysis.get("mozliwe_oszczednosci", {
            "czas_godziny_miesiecznie": 0,
            "oszczednosci_pieniadze_miesiecznie": 0
        })
    except Exception as e:
        print(f"Błąd obliczania oszczędności: {e}")
        return {
            "czas_godziny_miesiecznie": 0,
            "oszczednosci_pieniadze_miesiecznie": 0
        } 