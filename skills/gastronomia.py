from datetime import datetime, timezone
from scrapers import larepublica, peru21

SECCION     = "Gastronomia"
NOMBRE_JSON = "noticias_gastronomia.json"

def _formato_alexa(noticias):
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")
    items = []
    for i, n in enumerate(noticias, start=1):
        items.append({
            "uid": f"gastronomia-{i:03d}",
            "updateDate": ahora,
            "titleText": "Gastronomía",
            "mainText": f"Gastronomía. {n['titulo']}. {n['resumen']}",
            "redirectionUrl": n["link"],
        })
    return items

def generar(ec_noticias, rpp_noticias):
    """
    ec_noticias: lista pre-obtenida de elcomercio.obtener_noticias()
    rpp_noticias: lista pre-obtenida de rpp.obtener_noticias()  (RPP no tiene gastronomía)
    Retorna la lista formateada para Alexa (hasta 5 items).
    """
    candidatos = []

    ec = next((n for n in ec_noticias if n["seccion"] == SECCION), None)
    if ec:
        candidatos.append(ec)

    for fn in [larepublica.obtener_noticia, peru21.obtener_noticia]:
        try:
            n = fn(SECCION)
            if n:
                candidatos.append(n)
        except Exception as e:
            print(f"[Gastronomia] Error en scraper: {e}")

    return _formato_alexa(candidatos[:5])
