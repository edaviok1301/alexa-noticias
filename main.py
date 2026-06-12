import json
import base64
import requests
from datetime import datetime, timezone
from scrapers.rpp import obtener_noticias as rpp_noticias
from scrapers.elcomercio import obtener_noticias_fusionadas as ec_noticias
# ── CONFIGURACION ──────────────────────
GITHUB_TOKEN = "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"
GITHUB_REPO  = "edaviok1301/alexa-noticias"
GITHUB_FILE  = "noticias.json"
# ───────────────────────────────────────

SECCIONES_PRIORIDAD = [
    "Politica",
    "Economia",
    "Tecnologia",
    "Mundo y Mundial",
    "Gastronomia",
]

def recolectar_noticias():
    por_seccion = {}
    for n in rpp_noticias():
        if n["seccion"] not in por_seccion:
            por_seccion[n["seccion"]] = n
    for n in ec_noticias():
        if n["seccion"] not in por_seccion:
            por_seccion[n["seccion"]] = n

    resultado = []
    for sec in SECCIONES_PRIORIDAD:
        if sec in por_seccion:
            resultado.append(por_seccion[sec])
        if len(resultado) == 5:
            break
    return resultado

def formatear_para_alexa(noticias):
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")
    items = []
    for i, n in enumerate(noticias, start=1):
        items.append({
            "uid": f"noticia-{i:03d}",
            "updateDate": ahora,
            "titleText": n["seccion"],
            "mainText": f"{n['seccion']}. {n['titulo']}. {n['resumen']}",
            "redirectionUrl": n["link"]
        })
    return items

def subir_a_github(contenido_json):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Error al obtener SHA: {r.status_code}")
        return False
    sha = r.json().get("sha")

    contenido_b64 = base64.b64encode(
        json.dumps(contenido_json, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    r2 = requests.put(url, headers=headers, json={
        "message": f"Actualizar noticias {datetime.now().strftime('%Y-%m-%d')}",
        "content": contenido_b64,
        "sha": sha
    })

    if r2.status_code in [200, 201]:
        print("Noticias actualizadas en GitHub correctamente")
        return True
    else:
        print(f"Error al subir: {r2.status_code} - {r2.text}")
        return False

def main():
    print(f"=== Actualizando noticias {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    noticias = recolectar_noticias()
    print(f"Noticias recolectadas: {len(noticias)}")
    for n in noticias:
        print(f"  [{n['seccion']}] {n['titulo'][:60]}")

    alexa_json = formatear_para_alexa(noticias)

    with open("noticias.json", "w", encoding="utf-8") as f:
        json.dump(alexa_json, f, ensure_ascii=False, indent=2)
    print("noticias.json guardado localmente")

    subir_a_github(alexa_json)

if __name__ == "__main__":
    print("Iniciando script...")
    main()