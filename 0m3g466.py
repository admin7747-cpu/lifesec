import phonenumbers
from phonenumbers import geocoder, carrier
import requests, re
from datetime import datetime
import os

# --- INPUT ---
num = input("Número con + ej: +34614963439: ").strip()
try:
    p = phonenumbers.parse(num)
except:
    print("Ponlo con +34")
    exit()

clean = num.replace("+","").replace(" ","").replace("-","")
clean_space = num.replace("+34","").strip()
pais = geocoder.description_for_number(p, 'es') or "España"
operadora = carrier.name_for_number(p, 'es') or 'OMV / Virtual (Digi, Lobster...)'
valido = phonenumbers.is_valid_number(p)
tipo = "Móvil" if phonenumbers.number_type(p)==1 else "Otro"

print(f"\n====== INFORME PARA {num} ======")
print(f"País: {pais} | Operadora: {operadora} | {tipo} | Válido: {valido}")

# --- 21 FUENTES ---
links = [
    f"WhatsApp: https://wa.me/{clean}",
    f"Telegram: https://t.me/+{clean}",
    f"Epieos (Gmail): https://epieos.com/?q={num}",
    f"Truecaller: https://www.truecaller.com/search/{num}",
    f"Sync.me: https://sync.me/search/?number={clean}",
    f"Tellows ES: https://www.tellows.es/num/{clean}",
    f"Tellows Global: https://www.tellows.com/num/{clean}",
    f"ListaSpam: https://www.listaspam.com/busca.php?Telefono={clean}",
    f"Google exacto: https://www.google.com/search?q=\"{num}\"",
    f"Google sin +: https://www.google.com/search?q=\"{clean}\"",
    f"Google TikTok: https://www.google.com/search?q=\"{clean}\" site:tiktok.com",
    f"Google TikTok2: https://www.google.com/search?q=\"{clean_space}\" site:tiktok.com",
    f"Google Instagram: https://www.google.com/search?q=\"{clean}\" site:instagram.com",
    f"Google Facebook: https://www.google.com/search?q=\"{clean}\" site:facebook.com",
    f"Google Wallapop: https://www.google.com/search?q=\"{clean}\" site:es.wallapop.com",
    f"Google Milanuncios: https://www.google.com/search?q=\"{clean}\" site:milanuncios.com",
    f"Google Vinted: https://www.google.com/search?q=\"{clean}\" site:vinted.es",
    f"Google Twitter/X: https://www.google.com/search?q=\"{clean}\" site:x.com",
    f"Google Linkedin: https://www.google.com/search?q=\"{clean}\" site:linkedin.com",
    f"Google Pastebin: https://www.google.com/search?q=\"{clean}\" site:pastebin.com",
    f"Signal: https://signal.me/#p/+{clean}",
]

print("\n--- 21 LINKS ---\n")
for l in links:
    print(l)

# --- BÚSQUEDA TIKTOK @ ---
print("\n--- BUSCANDO @ DE TIKTOK CERCA DEL NÚMERO ---")
headers = {"User-Agent": "Mozilla/5.0 (Android)"}
try:
    url = f"https://www.google.com/search?q=\"{clean}\" site:tiktok.com"
    r = requests.get(url, headers=headers, timeout=10)
    usuarios = re.findall(r'@([A-Za-z0-9._]{3,24})', r.text)
    usuarios = list(set(usuarios))[:8]
    if usuarios:
        print("Posibles @ encontrados:")
        for u in usuarios:
            print(f" -> https://www.tiktok.com/@{u}")
    else:
        print("Google no mostró @ directo. Abre el link 11 y 12, ahí sale si está en bio.")
except:
    print("No se pudo conectar a Google, abre los links a mano.")

# --- GUARDAR TODO ---
nombre = f"TODO_{clean}.txt"
with open(nombre, "w", encoding="utf-8") as f:
    f.write(f"INFORME COMPLETO OSINT\nNúmero: {num}\nFecha: {datetime.now()}\n")
    f.write(f"País: {pais}\nOperadora: {operadora}\nTipo: {tipo}\nVálido: {valido}\n")
    f.write(f"--------------------------------\n\nFUENTES (21):\n")
    for l in links:
        f.write(l+"\n")
    f.write("\n--- DORKS EXTRA TIKTOK ---\n")
    f.write(f'"{clean_space}" tiktok contacto\n')
    f.write(f'"{clean_space}" tiktok whatsapp\n')
    f.write(f'"{clean_space}" tiktok +34\n')

print(f"\n[✓] TODO guardado en: {os.getcwd()}/{nombre}")
