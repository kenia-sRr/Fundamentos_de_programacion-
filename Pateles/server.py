"""
Servidor local para Pastelería AURA
Ejecuta este archivo con: python server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Forzar codificación UTF-8 para evitar errores en terminales de Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Desactivar caché local para desarrollo
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        try:
            sys.stdout.write(f"[AURA Web] {self.address_string()} - {format % args}\n")
            sys.stdout.flush()
        except Exception:
            pass

def run():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=================================================================")
        print("PASTELERIA AURA - SERVIDOR LOCAL ACTIVO")
        print("=================================================================")
        print(f" -> Enlace directo: {url}")
        print(" -> Abriendo automaticamente en tu navegador preferido...")
        print(" -> Presiona Ctrl + C para detener el servidor.")
        print("=================================================================")
        
        try:
            webbrowser.open(url)
        except Exception:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor cerrado correctamente.")

if __name__ == "__main__":
    run()
