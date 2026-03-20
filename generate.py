import requests
from datetime import datetime, timedelta
import pytz
import uuid

TZ = pytz.timezone("America/Sao_Paulo")

url = "https://api.openf1.org/v1/sessions"
data = requests.get(url).json()

def formatar_data(dt):
    return dt.strftime("%Y%m%dT%H%M%S")

def converter(data_iso):
    try:
        dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        return dt.astimezone(TZ)
    except:
        return None

conteudo = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
"""

for session in data:
    nome = session.get("session_name")
    inicio = session.get("date_start")
    gp = session.get("meeting_name")

    if not nome or not inicio:
        continue

    dt_inicio = converter(inicio)

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

    dt_fim = dt_inicio + timedelta(hours=dur)

    conteudo += f"""BEGIN:VEVENT
UID:{uuid.uuid4()}
DTSTAMP:{formatar_data(datetime.utcnow())}Z
DTSTART:{formatar_data(dt_inicio)}
DTEND:{formatar_data(dt_fim)}
SUMMARY:{gp} - {label}
END:VEVENT
"""

conteudo += "END:VCALENDAR"

with open("f1.ics", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("Calendário gerado corretamente")