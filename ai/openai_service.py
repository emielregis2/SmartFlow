"""
Moduł integracji z OpenAI dla SmartFlow.
"""
import os
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv
import json
import time

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def analyze_process(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizuje proces biznesowy używając OpenAI"""
        prompt = self._prepare_prompt(process_data)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Jesteś ekspertem od automatyzacji procesów biznesowych w polskich firmach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return self._parse_response(response.choices[0].message.content)
        except Exception as e:
            return self._get_mock_analysis()

    def _prepare_prompt(self, data: Dict[str, Any]) -> str:
        form_data = data.get('form_data', {})
        company = form_data.get('company', {})
        process = form_data.get('process', {})
        return f"""
        Przeanalizuj proces biznesowy i podaj rekomendacje automatyzacji:
        
        FIRMA:
        - Wielkość: {company.get('size', 'Nieznana')}
        - Branża: {company.get('industry', 'Nieznana')}
        - Budżet: {company.get('budget', 'Nieznany')}
        
        PROCES:
        - Nazwa: {process.get('name', 'Nieznany')}
        - Częstotliwość: {process.get('frequency', 'Nieznana')}
        - Czas: {process.get('duration', 0)} godzin
        - Opis: {process.get('description', 'Brak opisu')}
        
        Odpowiedz w formacie JSON z polami:
        - ocena_potencjalu (1-10)
        - mozliwe_oszczednosci (czas_godziny_miesiecznie, oszczednosci_pieniadze_miesiecznie)
        - rekomendacje (lista narzędzi z opisem)
        - plan_wdrozenia (lista kroków)
        """

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parsuje odpowiedź AI do struktury"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        return self._get_mock_analysis()

    def _get_mock_analysis(self) -> Dict[str, Any]:
        """Mock analiza dla testów"""
        return {
            "ocena_potencjalu": 8,
            "mozliwe_oszczednosci": {
                "czas_godziny_miesiecznie": 16,
                "oszczednosci_pieniadze_miesiecznie": 2400
            },
            "rekomendacje": [
                {
                    "narzedzie": "Zapier + Airtable",
                    "opis": "Automatyzacja zbierania i przetwarzania danych",
                    "koszt_miesiecznie": 300,
                    "czas_wdrozenia": "2 tygodnie"
                }
            ],
            "plan_wdrozenia": [
                "Tydzień 1: Konfiguracja Airtable",
                "Tydzień 2: Połączenie przez Zapier",
                "Tydzień 3: Testowanie i wdrożenie"
            ],
            "uwagi": ["Wymaga podstawowej wiedzy o automatyzacji"]
        }

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