import requests, os, re
from datetime import datetime

R = "\033[91m"
G = "\033[92m"
W = "\033[97m"

headers = {"User-Agent": "Mozilla/5.0"}

def logo():
    os.system("clear")
    print(f"{R}  ____  _____ ____    _____ ___ ____ _____ ____  ")
    print(f" |  _ \\| ____|  _ \\  |_   _|_ _/ ___| ____|  _ \\ ")
    print(f" | |_) |  _| | | | |   | |  | | |  _|  _| | |_) |")
    print(f" |  _ <| |___| |_| |   | |  | | |_| | |___|  _ < ")
    print(f" |_| \\_\\_____|____/    |_| |___\\____|_____|_| \\_\\{W}")
    print(f"          om66 x Red Tiger LITE - SOLO OSINT PUBLICO\n")

def check_user(username):
    print(f"\n{G}[*] Buscando @{username} en redes:{W}")
    sites = {
        "Instagram": f"https://www.instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Twitter": f"https://twitter.com/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Telegram": f"https://t.me/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "SoundCloud": f"https://soundcloud.com/{username}"
    }
    for name, url in sites.items():
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                print(f"  [+] {name}: {url}")
            else:
                print(f"  [-] {name}: no encontrado")
        except:
            print(f"  [?] {name}: error")

def ip_lookup():
    ip = input("IP (vacia para tu IP): ").strip()
    url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
    try:
        r = requests.get(url, timeout=10).json()
        print(f"\nIP: {r.get('ip')}\nPais: {r.get('country_name')}\nCiudad: {r.get('city')}\nOrg: {r.get('org')}")
    except:
        print("Error con la IP")

while True:
    logo()
    print("1. Username Check")
    print("2. IP Lookup")
    print("3. Salir")
    op = input("\n>> ")

    if op == "1":
        u = input("Usuario sin @: ").strip()
        check_user(u)
        input("\nEnter para volver...")
    elif op == "2":
        ip_lookup()
        input("\nEnter para volver...")
    elif op == "3":
        break
