import feedparser
import re
import socket

# La República: intentamos primero Arc Publishing, luego estilo WordPress
RSS_SECCIONES = {
    "Politica": [
        "https://larepublica.pe/arc/outboundfeeds/rss/category/politica/?outputType=xml",
        "https://larepublica.pe/politica/feed/",
    ],
    "Economia": [
        "https://larepublica.pe/arc/outboundfeeds/rss/category/economia/?outputType=xml",
        "https://larepublica.pe/economia/feed/",
    ],
    "Tecnologia": [
        "https://larepublica.pe/arc/outboundfeeds/rss/category/tecnologia/?outputType=xml",
        "https://larepublica.pe/tecnologia/feed/",
    ],
    "Mundo": [
        "https://larepublica.pe/arc/outboundfeeds/rss/category/mundo/?outputType=xml",
        "https://larepublica.pe/mundo/feed/",
    ],
    "Gastronomia": [
        "https://larepublica.pe/arc/outboundfeeds/rss/category/gastronomia/?outputType=xml",
        "https://larepublica.pe/gastronomia/feed/",
        "https://larepublica.pe/vida-estilo/feed/",
    ],
}

def limpiar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto[:400]

def obtener_noticia(seccion):
    """Retorna una sola noticia de La República para la sección indicada, o None."""
    urls = RSS_SECCIONES.get(seccion, [])
    for url in urls:
        try:
            socket.setdefaulttimeout(8)
            feed = feedparser.parse(url)
            socket.setdefaulttimeout(None)
            if feed.entries:
                entry = feed.entries[0]
                titulo = limpiar_texto(entry.get("title", ""))
                resumen = limpiar_texto(entry.get("summary", "") or entry.get("description", ""))
                link = entry.get("link", "https://larepublica.pe")
                if titulo:
                    return {
                        "seccion": seccion,
                        "titulo": titulo,
                        "resumen": resumen or titulo,
                        "link": link,
                        "fuente": "La República",
                    }
        except Exception as e:
            print(f"[La República] Error en {seccion} ({url}): {e}")
            socket.setdefaulttimeout(None)
    return None
