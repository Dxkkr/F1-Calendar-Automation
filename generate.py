import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

TZ = pytz.timezone("America/Sao_Paulo")
calendar = Calendar()

# API OpenF1 (estável)
url = "https://api.openf1.org/v1/sessions"

try:
    response = requests.get(url, timeout=10)
    data = response.json()
except:
    print("Erro ao acessar API")
    exit(1)

def converter(data_iso):
    try:
        dt = datetime.fromisoformat(data_iso.replace("Z", ""))
        return pytz.utc.localize(dt).astimezone(TZ)
    except:
        return None

for session in data:
    nome = session.get("session_name")
    inicio = session.get("date_start")

    if not nome or not inicio:
        continue

    dt_inicio = converter(inicio)
    if not dt_inicio:
        continue

    # Mapeando nomes
    if "Practice 1" in nome:
        label = "Qui (Treino Livre 1)"
        dur = 1
    elif "Practice 2" in nome:
        label = "Sex (Treino Livre 2)"
        dur = 1
    elif "Practice 3" in nome:
        label = "Sab (Treino Livre 3)"
        dur = 1
    elif "Qualifying" in nome:
        label = "Sab (Classificação)"
        dur = 1
    elif "Race" in nome:
        label = "Dom (Corrida)"
        dur = 2
    elif "Sprint" in nome:
        label = "Sab (Sprint)"
        dur = 1
    else:
        continue

    evento = Event()
    evento.name = f"{session.get('meeting_name')} - {label}"
    evento.begin = dt_inicio
    evento.duration = timedelta(hours=dur)

    calendar.events.add(evento)

with open("f1.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("Calendário gerado com sucesso")