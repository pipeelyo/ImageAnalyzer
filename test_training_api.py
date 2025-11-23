#!/usr/bin/env python3
"""
Script para probar el API de entrenamiento del modelo
Uso: python test_training_api.py
"""

import requests
import json

# URL del API
API_URL = "http://localhost:8000/api/train/"

def test_training_with_defaults():
    """Prueba el entrenamiento usando las rutas por defecto"""
    print("🚀 Iniciando entrenamiento con rutas por defecto...")
    print(f"   URL: {API_URL}")
    print()
    
    try:
        response = requests.post(API_URL, json={})
        
        print(f"📊 Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Entrenamiento exitoso!")
            print(json.dumps(data, indent=2))
        else:
            print("❌ Error en el entrenamiento:")
            print(json.dumps(response.json(), indent=2))
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que Django esté corriendo:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_training_with_custom_paths(train_path, test_path):
    """Prueba el entrenamiento con rutas personalizadas"""
    print(f"🚀 Iniciando entrenamiento con rutas personalizadas...")
    print(f"   Train: {train_path}")
    print(f"   Test: {test_path}")
    print()
    
    data = {
        "train_path": train_path,
        "test_path": test_path
    }
    
    try:
        response = requests.post(API_URL, json=data)
        
        print(f"📊 Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Entrenamiento exitoso!")
            print(json.dumps(result, indent=2))
        else:
            print("❌ Error en el entrenamiento:")
            print(json.dumps(response.json(), indent=2))
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que Django esté corriendo:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("   PRUEBA DE API DE ENTRENAMIENTO")
    print("=" * 60)
    print()
    
    # Probar con rutas por defecto
    test_training_with_defaults()
    
    # Descomentar para probar con rutas personalizadas:
    # test_training_with_custom_paths(
    #     train_path="/Users/andresgarcia/Downloads/train",
    #     test_path="/Users/andresgarcia/Downloads/test"
    # )
