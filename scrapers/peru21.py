import feedparser
import re
import socket

# Peru21 usa Arc Publishing (mismo grupo que El Comercio)
RSS_SECCIONES = {
    "Politica":   "https://peru21.pe/arc/outboundfeeds/rss/category/politica/?outputType=xml",
    "Economia":   "https://peru21.pe/arc/outboundfeeds/rss/category/economia/?outputType=xml",
    "Tecnologia": "https://peru21.pe/arc/outboundfeeds/rss/category/tecnologia/?outputType=xml",
    "Mundo":      "https://peru21.pe/arc/outboundfeeds/rss/category/mundo/?outputType=xml",
    "Gastronomia":"https://peru21.pe/arc/outboundfeeds/rss/category/gastronomia/?outputType=xml",
}

def limpiar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto[:400]

def obtener_noticia(seccion):
    """Retorna una sola noticia de Peru21 para la sección indicada, o None."""
    url = RSS_SECCIONES.get(seccion)
    if not url:
        return None
    try:
        socket.setdefaulttimeout(8)
        feed = feedparser.parse(url)
        socket.setdefaulttimeout(None)
        if feed.entries:
            entry = feed.entries[0]
            titulo = limpiar_texto(entry.get("title", ""))
            resumen = limpiar_texto(entry.get("summary", "") or entry.get("description", ""))
            link = entry.get("link", "https://peru21.pe")
            if titulo:
                return {
                    "seccion": seccion,
                    "titulo": titulo,
                    "resumen": resumen or titulo,
                    "link": link,
                    "fuente": "Peru21",
                }
    except Exception as e:
        print(f"[Peru21] Error en {seccion}: {e}")
        socket.setdefaulttimeout(None)
    return None
