import requests

# Configuración del servidor local de Ollama (Sin API Key)
LOCAL_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:1.5b"

def query_local_ai(prompt_text):
    """
    Envía una petición al motor local de Ollama y devuelve la respuesta limpia.
    """
    data = {
        "model": MODEL,
        "prompt": f"Genera únicamente código limpio y funcional según esta petición, sin explicaciones largas: {prompt_text}",
        "stream": False
    }
    
    try:
        response = requests.post(LOCAL_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            code = result.get("response", "")
            # Limpiar etiquetas markdown o bloques de razonamiento si los trae el modelo local
            code = code.replace("```html", "").replace("```python", "").replace("```", "").strip()
            return code
        else:
            print(f"\n[ERROR MÓDULO IA] Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"\n[ERROR DE CONEXIÓN] Asegúrate de que 'ollama serve' esté encendido. Detalle: {e}")
        return None

