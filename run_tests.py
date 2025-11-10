#!/usr/bin/env python3
"""
Script para ejecutar las pruebas automatizadas del proyecto ICANH
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Ejecuta un comando y retorna el código de salida"""
    print(f"\n🔧 {description}")
    print("=" * 60)

    result = subprocess.run(command, shell=True, capture_output=False, text=True)

    if result.returncode == 0:
        print(f"✅ {description} - EXITOSO")
    else:
        print(f"❌ {description} - FALLÓ (código: {result.returncode})")

    return result.returncode == 0


def main():
    """Función principal para ejecutar todas las pruebas"""
    print("🚀 Ejecutando pruebas automatizadas - API ICANH")
    print("=" * 60)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("tests"):
        print("❌ Error: Directorio 'tests' no encontrado. Ejecuta desde la raíz del proyecto.")
        sys.exit(1)

    if not os.path.exists("requirements.txt"):
        print("❌ Error: Archivo 'requirements.txt' no encontrado.")
        sys.exit(1)

    # 1. Verificar que las dependencias de testing están instaladas
    success = run_command(
        f"{sys.executable} -c \"import pytest, httpx, faker; print('Dependencias de testing instaladas')\"",
        "Verificando dependencias de testing"
    )

    if not success:
        print("\n💡 Instala las dependencias ejecutando:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    # 2. Ejecutar tests unitarios
    success = run_command(
        f"{sys.executable} -m pytest tests/test_models.py tests/test_schemas.py -v",
        "Ejecutando tests unitarios (Modelos y Esquemas)"
    )

    # 3. Ejecutar tests de rutas
    if success:
        success = run_command(
            f"{sys.executable} -m pytest tests/test_routes.py -v",
            "Ejecutando tests de rutas (Endpoints)"
        )

    # 4. Ejecutar tests de integración
    if success:
        success = run_command(
            f"{sys.executable} -m pytest tests/test_integration.py -v",
            "Ejecutando tests de integración"
        )

    # 5. Ejecutar todos los tests con cobertura
    if success:
        success = run_command(
            f"{sys.executable} -m pytest --cov=app --cov-report=term-missing --cov-report=html",
            "Ejecutando cobertura completa"
        )

    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n📊 Reporte de cobertura generado en: htmlcov/index.html")
        print("\n💡 Comandos útiles:")
        print("   pytest tests/                          # Ejecutar todos los tests")
        print("   pytest tests/test_models.py -v        # Solo tests de modelos")
        print("   pytest --cov=app --cov-report=html    # Generar reporte HTML")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\n🔧 Para ejecutar tests específicos:")
        print("   pytest tests/test_models.py -v")
        print("   pytest tests/test_routes.py -v")
        print("   pytest tests/test_integration.py -v")
        sys.exit(1)


if __name__ == "__main__":
    main()
