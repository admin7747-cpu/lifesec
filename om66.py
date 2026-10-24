import requests, re, os
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0 (Android) Chrome/120.0"}

username = input("Usuario sin @ (ej: om66): ").strip().replace("@","")
tel = input("Teléfono opcional con +34 (enter si no): ").strip()

clean_tel = tel.replace("+","").replace(" ","") if tel else ""

print(f"\n[*] OSINT MAX para: @{username} {tel}\n")

# 1. TIKTOK PUBLICO
print("--- [1/4] TIKTOK ---")
try:
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers, timeout=15)
    html = r.text
    bio = re.search(r'"desc":"([^"]+)"', html)
    bio = bio.group(1).encode().decode('unicode_escape') if bio else ""
    followers = re.search(r'"followerCount":(\d+)', html)
    followers = followers.group(1) if followers else "?"
    print(f"Bio: {bio}\nFollowers: {followers}")
except:
    bio = ""
    followers = "?"
    print(f"TikTok privado o no existe")

# 2. USERNAME EN OTRAS REDES
print("\n--- [2/4] USERNAME EN OTRAS REDES ---")
sites = {
    "Instagram": f"https://www.instagram.com/{username}",
    "TikTok": f"https://www.tiktok.com/@{username}",
    "Twitter/X": f"https://twitter.com/{username}",
    "YouTube": f"https://www.youtube.com/@{username}",
    "GitHub": f"https://github.com/{username}",
    "Reddit": f"https://www.reddit.com/user/{username}",
    "Twitch": f"https://www.twitch.tv/{username}",
    "Steam": f"https://steamcommunity.com/id/{username}",
    "Telegram": f"https://t.me/{username}",
    "Facebook": f"https://www.facebook.com/{username}",
}

found = []
for name, url in sites.items():
    try:
        req = requests.get(url, headers=headers, timeout=5)
        if req.status_code == 200 and len(req.text) > 2000:
            print(f"[+] {name}: {url}")
            found.append(f"{name}: {url}")
    except:
        pass

# 3. INFO BIO
emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', bio)
links_bio = re.findall(r'https?://[^\s"\\]+', bio)

# 4. GUARDAR
with open("om66.txt", "w", encoding="utf-8") as f:
    f.write(f"INFORME OSINT MAX - om66\nFecha: {datetime.now()}\nObjetivo: @{username}\nTel: {tel}\n")
    f.write(f"--------------------------------\nBIO: {bio}\nFollowers: {followers}\n--------------------------------\n\n")
    f.write("PERFILES ENCONTRADOS:\n")
    for x in found:
        f.write(x+"\n")
    f.write(f"\nEmails: {emails}\nLinks bio: {links_bio}\n")

# 5. MOSTRAR AUTOMATICO - ESTO ES LO NUEVO
print(f"\n[✓] Guardado en om66.txt")
print("\n========== CONTENIDO DE om66.txt ==========\n")
os.system("cat om66.txt")
print("\n==========================================\n")
