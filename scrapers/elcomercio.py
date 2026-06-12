import feedparser
import re

# El Comercio tiene RSS por seccion
RSS_SECCIONES = {
    "Politica":    "https://elcomercio.pe/arc/outboundfeeds/rss/category/politica/?outputType=xml",
    "Economia":    "https://elcomercio.pe/arc/outboundfeeds/rss/category/economia/?outputType=xml",
    "Tecnologia":  "https://elcomercio.pe/arc/outboundfeeds/rss/category/tecnologia/?outputType=xml",
    "Mundo":       "https://elcomercio.pe/arc/outboundfeeds/rss/category/mundo/?outputType=xml",
    "Mundial":     "https://elcomercio.pe/arc/outboundfeeds/rss/category/mundial/?outputType=xml",
    "Gastronomia": "https://elcomercio.pe/arc/outboundfeeds/rss/category/gastronomia/?outputType=xml",
}

def limpiar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto[:400]

def obtener_noticias():
    noticias = []
    for seccion, url in RSS_SECCIONES.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry   = feed.entries[0]
                titulo  = limpiar_texto(entry.get("title", ""))
                resumen = limpiar_texto(entry.get("summary", "") or entry.get("description", ""))
                link    = entry.get("link", "https://elcomercio.pe")
                if titulo:
                    noticias.append({
                        "seccion": seccion,
                        "titulo":  titulo,
                        "resumen": resumen or titulo,
                        "link":    link,
                        "fuente":  "El Comercio"
                    })
        except Exception as e:
            print(f"[El Comercio] Error en {seccion}: {e}")
    return noticias

def obtener_noticias_fusionadas():
    """Igual que obtener_noticias pero fusiona Mundo y Mundial en una sola."""
    noticias = obtener_noticias()
    
    mundo   = next((n for n in noticias if n["seccion"] == "Mundo"), None)
    mundial = next((n for n in noticias if n["seccion"] == "Mundial"), None)
    resto   = [n for n in noticias if n["seccion"] not in ("Mundo", "Mundial")]

    # Elegir la más reciente entre Mundo y Mundial
    # Si hay Mundial la priorizamos, si no usamos Mundo
    if mundial:
        fusionada = {**mundial, "seccion": "Mundo y Mundial"}
    elif mundo:
        fusionada = {**mundo, "seccion": "Mundo y Mundial"}
    else:
        return resto

    return resto + [fusionada]