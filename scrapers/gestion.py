import feedparser
import re
import socket

# Gestión usa Arc Publishing (mismo grupo que El Comercio)
RSS_URL = "https://gestion.pe/arc/outboundfeeds/rss/category/economia/?outputType=xml"

def limpiar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto[:400]

def obtener_noticia():
    """Retorna una sola noticia de Gestión (economía), o None."""
    try:
        socket.setdefaulttimeout(8)
        feed = feedparser.parse(RSS_URL)
        socket.setdefaulttimeout(None)
        if feed.entries:
            entry = feed.entries[0]
            titulo = limpiar_texto(entry.get("title", ""))
            resumen = limpiar_texto(entry.get("summary", "") or entry.get("description", ""))
            link = entry.get("link", "https://gestion.pe")
            if titulo:
                return {
                    "seccion": "Economia",
                    "titulo": titulo,
                    "resumen": resumen or titulo,
                    "link": link,
                    "fuente": "Gestión",
                }
    except Exception as e:
        print(f"[Gestión] Error: {e}")
        socket.setdefaulttimeout(None)
    return None
