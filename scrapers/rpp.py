import feedparser
import re
import urllib.request

# RPP solo tiene un RSS general, usamos la URL del articulo para clasificar
RSS_URL = "https://rpp.pe/rss"

SECCIONES_URL = {
    "Politica":   "/politica/",
    "Economia":   "/economia/",
    "Tecnologia": "/tecnologia/",
    "Mundo":      "/mundo/",
}

def limpiar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto[:400]

def obtener_noticias():
    por_seccion = {}
    try:
        import socket
        socket.setdefaulttimeout(8)
        feed = feedparser.parse(RSS_URL)
        socket.setdefaulttimeout(None)
        for entry in feed.entries:
            link = entry.get("link", "")
            for seccion, path in SECCIONES_URL.items():
                if path in link and seccion not in por_seccion:
                    titulo  = limpiar_texto(entry.get("title", ""))
                    resumen = limpiar_texto(entry.get("description", "") or entry.get("summary", ""))
                    if titulo and resumen:
                        por_seccion[seccion] = {
                            "seccion": seccion,
                            "titulo":  titulo,
                            "resumen": resumen,
                            "link":    link,
                            "fuente":  "RPP"
                        }
                    break
    except Exception as e:
        print(f"[RPP] Error: {e}")
        import socket
        socket.setdefaulttimeout(None)
    return list(por_seccion.values())