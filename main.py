import json
from datetime import datetime
from scrapers.elcomercio import obtener_noticias as ec_noticias
from scrapers.rpp import obtener_noticias as rpp_noticias
from skills import politica, economia, tecnologia, mundo, gastronomia
from github_upload import subir_archivo

SKILLS = [
    (politica,    "noticias_politica.json"),
    (economia,    "noticias_economia.json"),
    (tecnologia,  "noticias_tecnologia.json"),
    (mundo,       "noticias_mundo.json"),
    (gastronomia, "noticias_gastronomia.json"),
]

def main():
    print(f"=== Actualizando noticias {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    # Pre-fetch una sola vez para no repetir llamadas HTTP
    print("Obteniendo noticias de El Comercio...")
    ec = ec_noticias()
    print(f"  El Comercio: {len(ec)} noticias")

    print("Obteniendo noticias de RPP...")
    rpp = rpp_noticias()
    print(f"  RPP: {len(rpp)} noticias")

    for skill_mod, nombre_archivo in SKILLS:
        nombre = nombre_archivo.replace("noticias_", "").replace(".json", "").capitalize()
        print(f"\n--- {nombre} ---")
        try:
            items = skill_mod.generar(ec, rpp)
            print(f"  Items generados: {len(items)}")
            for it in items:
                print(f"    [{it['uid']}] {it['mainText'][:70]}...")

            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"  {nombre_archivo} guardado localmente")

            subir_archivo(nombre_archivo, items)
        except Exception as e:
            print(f"  [ERROR] Skill {nombre}: {e}")

    print("\n=== Proceso completado ===")

if __name__ == "__main__":
    print("Iniciando script...")
    main()
