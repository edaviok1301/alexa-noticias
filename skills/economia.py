from datetime import datetime, timezone
from scrapers import larepublica, peru21, gestion

SECCION     = "Economia"
NOMBRE_JSON = "noticias_economia.json"

def _formato_alexa(noticias):
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")
    items = []
    for i, n in enumerate(noticias, start=1):
        items.append({
            "uid": f"economia-{i:03d}",
            "updateDate": ahora,
            "titleText": "Economía",
            "mainText": f"Economía. {n['titulo']}. {n['resumen']}",
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

    ec = next((n for n in ec_noticias if n["seccion"] == SECCION), None)
    if ec:
        candidatos.append(ec)

    rpp = next((n for n in rpp_noticias if n["seccion"] == SECCION), None)
    if rpp:
        candidatos.append(rpp)

    for fn, args in [
        (larepublica.obtener_noticia, (SECCION,)),
        (peru21.obtener_noticia,      (SECCION,)),
        (gestion.obtener_noticia,     ()),
    ]:
        try:
            n = fn(*args)
            if n:
                candidatos.append(n)
        except Exception as e:
            print(f"[Economia] Error en scraper: {e}")

    return _formato_alexa(candidatos[:5])
