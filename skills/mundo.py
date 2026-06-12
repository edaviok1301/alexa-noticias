from datetime import datetime, timezone
from scrapers import larepublica, peru21

NOMBRE_JSON = "noticias_mundo.json"

def _formato_alexa(noticias):
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")
    items = []
    for i, n in enumerate(noticias, start=1):
        items.append({
            "uid": f"mundo-{i:03d}",
            "updateDate": ahora,
            "titleText": "Mundo",
            "mainText": f"Mundo. {n['titulo']}. {n['resumen']}",
            "redirectionUrl": n["link"],
        })
    return items

def generar(ec_noticias, rpp_noticias):
    """
    ec_noticias: lista pre-obtenida de elcomercio.obtener_noticias()
    rpp_noticias: lista pre-obtenida de rpp.obtener_noticias()
    Retorna la lista formateada para Alexa (hasta 5 items).
    """
    candidatos = []

    # El Comercio tiene "Mundo" y "Mundial" separados; priorizamos "Mundo"
    ec = next((n for n in ec_noticias if n["seccion"] == "Mundo"), None) or \
         next((n for n in ec_noticias if n["seccion"] == "Mundial"), None)
    if ec:
        candidatos.append(ec)

    rpp = next((n for n in rpp_noticias if n["seccion"] == "Mundo"), None)
    if rpp:
        candidatos.append(rpp)

    for fn in [larepublica.obtener_noticia, peru21.obtener_noticia]:
        try:
            n = fn("Mundo")
            if n:
                candidatos.append(n)
        except Exception as e:
            print(f"[Mundo] Error en scraper: {e}")

    return _formato_alexa(candidatos[:5])
