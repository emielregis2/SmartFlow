"""
Moduł integracji z OpenAI do analizy procesów.
"""

from .ai import (
    analyze_process,
    generate_recommendations,
    calculate_savings
)

__all__ = [
    'analyze_process',
    'generate_recommendations',
    'calculate_savings'
] 