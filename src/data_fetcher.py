# src/data_fetcher.py
import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("THE_ODDS_API_KEY")

def fetch_odds_from_theoddsapi(sport_key):
    """Descarga partidos y cuotas de The Odds API"""
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "eu,us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error con {sport_key}: {response.status_code}")
        return pd.DataFrame()
    
    data = response.json()
    partidos = []
    
    for event in data:
        home = event['home_team']
        away = event['away_team']
        commence_time = event['commence_time'][:16].replace("T", " ")
        
        # Tomamos el mejor moneyline (h2h)
        best_home = best_away = best_draw = None
        if event.get('bookmakers'):
            bookie = event['bookmakers'][0]
            for market in bookie['markets']:
                if market['key'] == 'h2h':
                    for outcome in market['outcomes']:
                        if outcome['name'] == home:
                            best_home = outcome['price']
                        elif outcome['name'] == away:
                            best_away = outcome['price']
                        elif outcome['name'] == "Draw":
                            best_draw = outcome['price']
        
        partidos.append({
            "deporte": sport_key.split("_")[0].capitalize(),
            "liga": event['sport_title'],
            "partido": f"{home} vs {away}",
            "hora": commence_time,
            "home_odds": best_home,
            "away_odds": best_away,
            "draw_odds": best_draw,
            "event_id": event['id']
        })
    
    return pd.DataFrame(partidos)

def obtener_partidos_del_dia():
    sports = [
        "soccer_epl", "soccer_spain_la_liga", "soccer_germany_bundesliga",
        "baseball_mlb",
        "basketball_nba",
        "icehockey_nhl"
    ]
    
    all_data = pd.DataFrame()
    
    print("🔄 Descargando partidos del día...")
    for sport in sports:
        df = fetch_odds_from_theoddsapi(sport)
        if not df.empty:
            all_data = pd.concat([all_data, df], ignore_index=True)
    
    # Ordenar por hora
    if not all_data.empty:
        all_data = all_data.sort_values(by="hora")
    
    # Guardar en data/
    os.makedirs("data", exist_ok=True)
    all_data.to_csv("data/partidos_hoy.csv", index=False)
    
    print(f"✅ Se descargaron {len(all_data)} partidos")
    return all_data

if __name__ == "__main__":
    obtener_partidos_del_dia()