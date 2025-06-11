import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("Brak SUPABASE_URL lub SUPABASE_ANON_KEY w pliku .env!")
    exit(1)

try:
    supabase = create_client(url, key)
    # Próbujemy pobrać 1 rekord z dowolnej tabeli, np. 'processes'
    response = supabase.table("processes").select("*").limit(1).execute()
    print("Połączenie OK! Wynik testowego zapytania:")
    print(response.data)
except Exception as e:
    print("Błąd połączenia z Supabase:")
    print(e) 