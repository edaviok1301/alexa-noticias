import json
import base64
import requests
from datetime import datetime

GITHUB_TOKEN = "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"
GITHUB_REPO  = "edaviok1301/alexa-noticias"

def subir_archivo(nombre_archivo, contenido_json):
    """Sube un JSON a GitHub. Retorna True si tuvo éxito."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{nombre_archivo}"

    r = requests.get(url, headers=headers, timeout=15)
    sha = r.json().get("sha") if r.status_code == 200 else None

    contenido_b64 = base64.b64encode(
        json.dumps(contenido_json, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": f"Actualizar {nombre_archivo} {datetime.now().strftime('%Y-%m-%d')}",
        "content": contenido_b64,
    }
    if sha:
        payload["sha"] = sha

    r2 = requests.put(url, headers=headers, json=payload, timeout=15)

    if r2.status_code in [200, 201]:
        print(f"[GitHub] {nombre_archivo} actualizado correctamente")
        return True
    else:
        print(f"[GitHub] Error al subir {nombre_archivo}: {r2.status_code} - {r2.text[:200]}")
        return False
