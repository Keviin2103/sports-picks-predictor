# src/predictions.py
import pandas as pd

def generar_pick(row):
    """Genera pick principal y secundario de forma básica"""
    if pd.isna(row['home_odds']) or pd.isna(row['away_odds']):
        return "Sin datos", "Sin datos"
    
    # Pick principal: el favorito según las cuotas
    if row['home_odds'] < row['away_odds']:
        principal = f"{row['partido'].split(' vs ')[0]} gana"
    else:
        principal = f"{row['partido'].split(' vs ')[1]} gana"
    
    # Pick secundario simple (puede mejorarse después)
    secundario = "Más de 2.5 goles" if "soccer" in row['deporte'].lower() else "Más de total"
    
    return principal, secundario

def crear_picks_del_dia():
    df = pd.read_csv("data/partidos_hoy.csv")
    
    picks = []
    for _, row in df.iterrows():
        principal, secundario = generar_pick(row)
        picks.append({
            "Deporte": row['deporte'],
            "Liga": row['liga'],
            "Partido": row['partido'],
            "Hora": row['hora'],
            "Pick Principal": principal,
            "Pick Secundario": secundario
        })
    
    df_picks = pd.DataFrame(picks)
    df_picks.to_csv("data/picks_hoy.csv", index=False)
    return df_picks