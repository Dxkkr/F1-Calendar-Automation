import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

TZ = pytz.timezone("America/Sao_Paulo")
calendar = Calendar()

url = "https://api.motorsportsinfo.app/api/races/f1"

try:
    response = requests.get(url)
    data = response.json()
except:
    print("Erro ao acessar API")
    exit(1)

def parse_data(data_iso):
    try:
        dt_utc = datetime.fromisoformat(data_iso.replace("Z", ""))
        return pytz.utc.localize(dt_utc).astimezone(TZ)
    except:
        return None

mapa = {
    "fp1": ("Qui (Treino Livre 1)", 1),
    "fp2": ("Sex (Treino Livre 2)", 1),
    "fp3": ("Sab (Treino Livre 3)", 1),
    "qualifying": ("Sab (Classificação)", 1),
    "sprint": ("Sab (Sprint)", 1),
    "gp": ("Dom (Corrida)", 2)
}

for race in data:
    nome_gp = race.get("name", "F1")
    sessions = race.get("sessions", {})

    for key, (label, duracao) in mapa.items():
        if key in sessions and sessions[key]:
            inicio = parse_data(sessions[key])
            if not inicio:
                continue

            e = Event()
            e.name = f"{nome_gp} - {label}"
            e.begin = inicio
            e.duration = timedelta(hours=duracao)

            calendar.events.add(e)

with open("f1.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("Calendário gerado com sucesso")