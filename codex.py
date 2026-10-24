import os
import sys
import subprocess
import requests

# Colores para la terminal
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Configuración de directorios
SAVE_DIR = os.path.expanduser("~/codex/projects")
EXPORT_DIR = "/sdcard/Codex"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# Variables de estado
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-1.5-flash"
current_code = ""
current_filename = "index.html"

def banner():
    print(f"""{RED}
 ██████╗ ██████╗ ██████╗ ███████╗  
██╔════╝██╔═══██╗██╔══██╗██╔════╝     
██║     ██║   ██║██║  ██║█████╗       
██║     ██║   ██║██║  ██║██╔══╝       
╚██████╗╚██████╔╝██████╔╝███████╗     
 ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝     
{RESET}")
    print(f"{CYAN}[ AI CODE ENGINE ] model: {MODEL}{RESET}")
    print(f"{YELLOW}Comandos:{RESET} /new /paste /edit /open /run /save /list /key /quit\n")

def call_gemini(prompt):
    if not API_KEY:
        print(f"{RED}[ERROR] No hay una API Key configurada. Usa el comando /key para ingresarla.{RESET}")
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    data = {
        "contents": [{
            "parts": [{"text": f"Genera únicamente código limpio, funcional y completo según la petición, sin texto de relleno ni explicaciones: {prompt}"}]
        }]
    }
    
    try:
        print(f"{CYAN}[INFO] Consultando a la IA...{RESET}")
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            code = result['candidates'][0]['content']['parts'][0]['text']
            # Limpiar marcas markdown si las trae
            code = code.replace("```html", "").replace("```python", "").replace("```javascript", "").replace("```", "").strip()
            return code
        else:
            print(f"{RED}[ERROR API] {response.text}{RESET}")
            return None
    except Exception as e:
        print(f"{RED}[ERROR DE RED] {e}{RESET}")
        return None

def main():
    global current_code, current_filename, API_KEY
    banner()
    
    while True:
        try:
            command = input(f"{RED}codex@termux > {RESET}").strip()
            if not command:
                continue
                
            if command == "/quit":
                print("Saliendo de Codex...")
                break
                
            elif command == "/help":
                banner()
                
            elif command == "/key":
                key = input(f"{CYAN}Introduce tu Gemini API Key: {RESET}").strip()
                if key:
                    API_KEY = key
                    os.environ["GEMINI_API_KEY"] = key
                    print(f"{GREEN}[OK] API Key actualizada correctamente.{RESET}")
                    
            elif command == "/new":
                prompt = input(f"{CYAN}¿Qué deseas crear? > {RESET}")
                if prompt:
                    code = call_gemini(prompt)
                    if code:
                        current_code = code
                        current_filename = prompt.replace(" ", "_").lower()[:20] + ".html"
                        print(f"{GREEN}[GENERATED] Código generado con éxito.{RESET}")
                        print(current_code[:300] + "\n... [código truncado en vista previa]")
                        
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
                    
                print(f"{GREEN}[SAVE] {filepath}{RESET}")
                print(f"{GREEN}[EXPORT] Almacenamiento interno: {export_path}{RESET}")
                
            elif command == "/list":
                print(f"{CYAN}--- Archivos en {SAVE_DIR} ---{RESET}")
                files = os.listdir(SAVE_DIR)
                for f in files:
                    print(f" - {f}")
                    
            elif command == "/run":
                if not current_code:
                    print(f"{RED}[WARN] No hay código activo para ejecutar.{RESET}")
                    continue
                # Guardar temporalmente y ejecutar si es python, o avisar si es html
                temp_file = os.path.join(SAVE_DIR, "temp_run.py")
                with open(temp_file, "w") as f:
                    f.write(current_code)
                print(f"{CYAN}[RUN] Ejecutando script de prueba...{RESET}")
                try:
                    subprocess.run([sys.executable, temp_file])
                except Exception as e:
                    print(f"{RED}[ERROR] No se pudo ejecutar: {e}{RESET}")
                    
            elif command.startswith("/"):
                print(f"{RED}[ERROR] Comando desconocido. Escribe /help para ver los comandos.{RESET}")
            else:
                # Si escribe texto plano sin barra, actúa como un prompt directo
                code = call_gemini(command)
                if code:
                    current_code = code
                    print(f"{GREEN}[RESULTADO]:\n{code}{RESET}")

        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
            break

if __name__ == "__main__":
    main()

