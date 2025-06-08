"""
Testy jednostkowe dla modułu ai/openai_service.py
"""
import pytest
from unittest.mock import patch
from ai import openai_service

def test_analyze_process_success():
    process_data = {
        'title': 'Testowy proces',
        'frequency': 'miesięcznie',
        'participants': 3,
        'duration': 60,
        'improvement_goals': 'Automatyzacja',
        'description': 'Opis testowy'
    }
    mock_response = type('obj', (object,), {
        'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '{"ocena_potencjalu": 8, "mozliwe_oszczednosci": {"czas_godziny_miesiecznie": 10, "oszczednosci_pieniadze_miesiecznie": 1000}, "rekomendacje": [], "plan_wdrozenia": [], "uwagi": []}'})})]
    })
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        result = openai_service.analyze_process(process_data)
        assert isinstance(result, dict)
        assert result['ocena_potencjalu'] == 8
        assert 'mozliwe_oszczednosci' in result

def test_get_process_summary_success():
    process_data = {
        'title': 'Testowy proces',
        'frequency': 'miesięcznie',
        'participants': 3,
        'duration': 60,
        'improvement_goals': 'Automatyzacja',
        'description': 'Opis testowy'
    }
    mock_response = type('obj', (object,), {
        'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Podsumowanie procesu...'})})]
    })
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        summary = openai_service.get_process_summary(process_data)
        assert isinstance(summary, str)
        assert 'Podsumowanie' in summary or len(summary) > 0 