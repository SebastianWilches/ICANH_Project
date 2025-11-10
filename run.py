#!/usr/bin/env python3
"""
Script para ejecutar la API de Gestión de Vehículos - ICANH
Este script facilita la ejecución de la aplicación con configuración desde variables de entorno.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno
    load_dotenv()

    # Obtener configuración del servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", "8000")
    reload = os.getenv("RELOAD", "True").lower() == "true"

    print("🚀 Iniciando API de Gestión de Vehículos - ICANH")
    print(f"📍 Servidor: http://{host}:{port}")
    print(f"📚 Documentación: http://{host}:{port}/docs")
    print(f"🔄 Recarga automática: {'Activada' if reload else 'Desactivada'}")
    print("-" * 50)

    # Comando para ejecutar uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", host,
        "--port", port
    ]

    if reload:
        cmd.append("--reload")

    # Ejecutar el comando
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
