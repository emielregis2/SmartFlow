"""
Moduł integracji z OpenAI dla SmartFlow.
"""
import os
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_process(process_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza procesu biznesowego z wykorzystaniem GPT-4.
    
    Args:
        process_data: Dane procesu do analizy
        
    Returns:
        Dict zawierający wyniki analizy
    """
    # Przygotowanie promptu
    prompt = f"""
    Przeanalizuj poniższy proces biznesowy i zwróć wyniki w formacie JSON:
    
    Nazwa procesu: {process_data.get('title', 'Nieznany proces')}
    Częstotliwość: {process_data.get('frequency', 'Nieznana')}
    Liczba uczestników: {process_data.get('participants', 0)}
    Czas trwania: {process_data.get('duration', 0)} minut
    Cele optymalizacji: {process_data.get('improvement_goals', 'Nieokreślone')}
    Opis procesu: {process_data.get('description', 'Brak opisu')}
    
    Zwróć analizę w następującym formacie JSON:
    {{
        "ocena_potencjalu": <liczba od 1 do 10>,
        "mozliwe_oszczednosci": {{
            "czas_godziny_miesiecznie": <liczba>,
            "oszczednosci_pieniadze_miesiecznie": <liczba>
        }},
        "rekomendacje": [
            {{
                "narzedzie": <nazwa narzędzia>,
                "opis": <opis narzędzia>,
                "czas_wdrozenia": <szacowany czas>,
                "koszt_miesiecznie": <szacowany koszt>
            }}
        ],
        "plan_wdrozenia": [
            <lista kroków do wdrożenia>
        ],
        "uwagi": [
            <lista ważnych uwag>
        ]
    }}
    """
    
    try:
        # Wywołanie API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem w optymalizacji procesów biznesowych."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parsowanie odpowiedzi
        analysis_text = response.choices[0].message.content
        analysis = eval(analysis_text)  # TODO: Zamienić na bezpieczniejsze parsowanie JSON
        
        return analysis
        
    except Exception as e:
        raise ValueError(f"Błąd podczas analizy procesu: {str(e)}")

def get_process_summary(process_data: Dict[str, Any]) -> str:
    """
    Generowanie podsumowania procesu.
    
    Args:
        process_data: Dane procesu
        
    Returns:
        Tekst podsumowania
    """
    prompt = f"""
    Wygeneruj krótkie podsumowanie poniższego procesu biznesowego:
    
    Nazwa: {process_data.get('title', 'Nieznany proces')}
    Częstotliwość: {process_data.get('frequency', 'Nieznana')}
    Liczba uczestników: {process_data.get('participants', 0)}
    Czas trwania: {process_data.get('duration', 0)} minut
    Cele optymalizacji: {process_data.get('improvement_goals', 'Nieokreślone')}
    Opis: {process_data.get('description', 'Brak opisu')}
    
    Podsumowanie powinno zawierać:
    1. Główny cel procesu
    2. Kluczowe wyzwania
    3. Potencjalne obszary optymalizacji
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem w analizie procesów biznesowych."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise ValueError(f"Błąd podczas generowania podsumowania: {str(e)}") 