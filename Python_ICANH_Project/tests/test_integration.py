import pytest


class TestCompleteWorkflow:
    """Tests de integración para flujos completos de la aplicación"""

    def test_complete_vehiculo_lifecycle(self, client, faker):
        """Test ciclo completo de vida de un vehículo"""
        # 1. Crear marca
        marca_data = {
            "nombre_marca": faker.company(),
            "pais": faker.country()
        }
        response = client.post("/api/marcas-vehiculo/", json=marca_data)
        assert response.status_code == 200
        marca_id = response.json()["id"]

        # 2. Crear vehículo
        vehiculo_data = {
            "modelo": faker.word().capitalize(),
            "marca_id": marca_id,
            "numero_puertas": 4,
            "color": faker.color_name()
        }
        response = client.post("/api/vehiculos/", json=vehiculo_data)
        assert response.status_code == 200
        vehiculo_id = response.json()["id"]

        # 3. Verificar vehículo creado
        response = client.get(f"/api/vehiculos/{vehiculo_id}")
        assert response.status_code == 200
        vehiculo = response.json()
        assert vehiculo["marca"]["id"] == marca_id

        # 4. Actualizar vehículo
        update_data = {"color": "Negro"}
        response = client.put(f"/api/vehiculos/{vehiculo_id}", json=update_data)
        assert response.status_code == 200

        # 5. Verificar actualización
        response = client.get(f"/api/vehiculos/{vehiculo_id}")
        assert response.status_code == 200
        assert response.json()["color"] == "Negro"

        # 6. Eliminar vehículo
        response = client.delete(f"/api/vehiculos/{vehiculo_id}")
        assert response.status_code == 200

        # 7. Verificar eliminación
        response = client.get(f"/api/vehiculos/{vehiculo_id}")
        assert response.status_code == 404

    def test_persona_vehiculo_relationship_workflow(self, client, faker):
        """Test flujo completo de relación persona-vehículo"""
        # 1. Crear marca y vehículo
        marca_data = {"nombre_marca": "Toyota", "pais": "Japón"}
        response = client.post("/api/marcas-vehiculo/", json=marca_data)
        marca_id = response.json()["id"]

        vehiculo_data = {
            "modelo": "Corolla",
            "marca_id": marca_id,
            "numero_puertas": 4,
            "color": "Rojo"
        }
        response = client.post("/api/vehiculos/", json=vehiculo_data)
        vehiculo_id = response.json()["id"]

        # 2. Crear dos personas
        persona1_data = {
            "nombre": faker.name(),
            "cedula": str(faker.random_number(digits=10, fix_len=True))
        }
        response = client.post("/api/personas/", json=persona1_data)
        persona1_id = response.json()["id"]

        persona2_data = {
            "nombre": faker.name(),
            "cedula": str(faker.random_number(digits=10, fix_len=True))
        }
        response = client.post("/api/personas/", json=persona2_data)
        persona2_id = response.json()["id"]

        # 3. Verificar que inicialmente no hay propietarios
        response = client.get(f"/api/vehiculos/{vehiculo_id}/propietarios")
        assert len(response.json()["propietarios"]) == 0

        response = client.get(f"/api/personas/{persona1_id}/vehiculos")
        assert len(response.json()["vehiculos"]) == 0

        # 4. Asignar primera persona como propietaria
        asignacion_data = {"persona_id": persona1_id}
        response = client.post(f"/api/vehiculos/{vehiculo_id}/propietarios/", json=asignacion_data)
        assert response.status_code == 200

        # 5. Verificar asignación desde vehículo
        response = client.get(f"/api/vehiculos/{vehiculo_id}/propietarios")
        propietarios = response.json()["propietarios"]
        assert len(propietarios) == 1
        assert propietarios[0]["id"] == persona1_id

        # 6. Verificar asignación desde persona
        response = client.get(f"/api/personas/{persona1_id}/vehiculos")
        vehiculos = response.json()["vehiculos"]
        assert len(vehiculos) == 1
        assert vehiculos[0]["id"] == vehiculo_id

        # 7. Asignar segunda persona como propietaria
        asignacion_data = {"persona_id": persona2_id}
        response = client.post(f"/api/vehiculos/{vehiculo_id}/propietarios/", json=asignacion_data)
        assert response.status_code == 200

        # 8. Verificar que ahora hay dos propietarios
        response = client.get(f"/api/vehiculos/{vehiculo_id}/propietarios")
        propietarios = response.json()["propietarios"]
        assert len(propietarios) == 2

        propietario_ids = [p["id"] for p in propietarios]
        assert persona1_id in propietario_ids
        assert persona2_id in propietario_ids

        # 9. Verificar que ambas personas tienen el vehículo
        for persona_id in [persona1_id, persona2_id]:
            response = client.get(f"/api/personas/{persona_id}/vehiculos")
            vehiculos = response.json()["vehiculos"]
            assert len(vehiculos) == 1
            assert vehiculos[0]["id"] == vehiculo_id

    def test_bulk_operations(self, client, faker):
        """Test operaciones masivas"""
        # Crear múltiples marcas
        marcas = []
        for _ in range(3):
            marca_data = {
                "nombre_marca": faker.company(),
                "pais": faker.country()
            }
            response = client.post("/api/marcas-vehiculo/", json=marca_data)
            marcas.append(response.json()["id"])

        # Crear múltiples personas
        personas = []
        for _ in range(5):
            persona_data = {
                "nombre": faker.name(),
                "cedula": str(faker.random_number(digits=10, fix_len=True))
            }
            response = client.post("/api/personas/", json=persona_data)
            personas.append(response.json()["id"])

        # Verificar que se listan correctamente
        response = client.get("/api/marcas-vehiculo/")
        assert len(response.json()) == 3

        response = client.get("/api/personas/")
        assert len(response.json()) == 5

    def test_error_handling_comprehensive(self, client):
        """Test manejo completo de errores"""
        # IDs inexistentes
        endpoints_404 = [
            "/api/marcas-vehiculo/999",
            "/api/personas/999",
            "/api/vehiculos/999",
            "/api/personas/999/vehiculos",
            "/api/vehiculos/999/propietarios"
        ]

        for endpoint in endpoints_404:
            response = client.get(endpoint)
            assert response.status_code == 404

        # Datos inválidos
        invalid_marca = {"nombre_marca": "", "pais": ""}
        response = client.post("/api/marcas-vehiculo/", json=invalid_marca)
        assert response.status_code == 422  # Validation error

        # Asignaciones inválidas
        response = client.post("/api/vehiculos/1/propietarios/", json={"persona_id": 999})
        assert response.status_code == 404

        response = client.post("/api/vehiculos/999/propietarios/", json={"persona_id": 1})
        assert response.status_code == 404

    def test_data_consistency(self, client, faker):
        """Test consistencia de datos entre operaciones"""
        # Crear datos relacionados
        marca_data = {"nombre_marca": "BMW", "pais": "Alemania"}
        response = client.post("/api/marcas-vehiculo/", json=marca_data)
        marca_id = response.json()["id"]

        vehiculo_data = {
            "modelo": "X5",
            "marca_id": marca_id,
            "numero_puertas": 5,
            "color": "Blanco"
        }
        response = client.post("/api/vehiculos/", json=vehiculo_data)
        vehiculo_id = response.json()["id"]

        persona_data = {
            "nombre": "Carlos Rodríguez",
            "cedula": "987654321"
        }
        response = client.post("/api/personas/", json=persona_data)
        persona_id = response.json()["id"]

        # Asignar propietario
        client.post(f"/api/vehiculos/{vehiculo_id}/propietarios/", json={"persona_id": persona_id})

        # Verificar consistencia desde múltiples endpoints
        # Desde vehículo
        response = client.get(f"/api/vehiculos/{vehiculo_id}/propietarios")
        propietarios = response.json()["propietarios"]
        assert len(propietarios) == 1
        assert propietarios[0]["nombre"] == "Carlos Rodríguez"

        # Desde persona
        response = client.get(f"/api/personas/{persona_id}/vehiculos")
        vehiculos = response.json()["vehiculos"]
        assert len(vehiculos) == 1
        assert vehiculos[0]["modelo"] == "X5"
        assert vehiculos[0]["marca"]["nombre_marca"] == "BMW"

        # Desde listados generales
        response = client.get("/api/vehiculos/")
        all_vehiculos = response.json()
        assert len(all_vehiculos) == 1
        assert all_vehiculos[0]["marca"]["pais"] == "Alemania"

        response = client.get("/api/personas/")
        all_personas = response.json()
        assert len(all_personas) == 1
        assert all_personas[0]["cedula"] == "987654321"
