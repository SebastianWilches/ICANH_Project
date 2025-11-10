import pytest
from fastapi import HTTPException

from app.models.models import MarcaVehiculo, Persona, Vehiculo


class TestMarcaVehiculoRoutes:
    """Tests para los endpoints de MarcaVehiculo"""

    def test_get_marcas_empty(self, client):
        """Test obtener marcas cuando no hay ninguna"""
        response = client.get("/api/marcas-vehiculo/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_create_marca_vehiculo(self, client, faker):
        """Test crear una marca de vehículo"""
        marca_data = {
            "nombre_marca": faker.company(),
            "pais": faker.country()
        }

        response = client.post("/api/marcas-vehiculo/", json=marca_data)
        assert response.status_code == 200

        data = response.json()
        assert data["nombre_marca"] == marca_data["nombre_marca"]
        assert data["pais"] == marca_data["pais"]
        assert "id" in data

    def test_create_marca_duplicate_name(self, client):
        """Test crear marca con nombre duplicado"""
        marca_data = {"nombre_marca": "Toyota", "pais": "Japón"}

        # Crear primera marca
        response1 = client.post("/api/marcas-vehiculo/", json=marca_data)
        assert response1.status_code == 200

        # Intentar crear segunda marca con mismo nombre
        marca_data2 = {"nombre_marca": "Toyota", "pais": "Corea"}
        response2 = client.post("/api/marcas-vehiculo/", json=marca_data2)
        assert response2.status_code == 400
        assert "Ya existe una marca con ese nombre" in response2.json()["detail"]

    def test_get_marca_by_id(self, client, sample_marca):
        """Test obtener marca por ID"""
        response = client.get(f"/api/marcas-vehiculo/{sample_marca.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sample_marca.id
        assert data["nombre_marca"] == sample_marca.nombre_marca
        assert data["pais"] == sample_marca.pais

    def test_get_marca_not_found(self, client):
        """Test obtener marca inexistente"""
        response = client.get("/api/marcas-vehiculo/999")
        assert response.status_code == 404
        assert "Marca no encontrada" in response.json()["detail"]

    def test_update_marca(self, client, sample_marca):
        """Test actualizar una marca"""
        update_data = {
            "nombre_marca": "Toyota Updated",
            "pais": "Japón Updated"
        }

        response = client.put(f"/api/marcas-vehiculo/{sample_marca.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["nombre_marca"] == "Toyota Updated"
        assert data["pais"] == "Japón Updated"

    def test_update_marca_partial(self, client, sample_marca):
        """Test actualizar parcialmente una marca"""
        update_data = {"pais": "Japón Updated"}

        response = client.put(f"/api/marcas-vehiculo/{sample_marca.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["nombre_marca"] == sample_marca.nombre_marca  # No cambió
        assert data["pais"] == "Japón Updated"

    def test_delete_marca(self, client, sample_marca):
        """Test eliminar una marca"""
        response = client.delete(f"/api/marcas-vehiculo/{sample_marca.id}")
        assert response.status_code == 200
        assert "eliminada exitosamente" in response.json()["message"]

        # Verificar que ya no existe
        response = client.get(f"/api/marcas-vehiculo/{sample_marca.id}")
        assert response.status_code == 404

    def test_delete_marca_with_vehiculos(self, client, sample_vehiculo):
        """Test que no se pueda eliminar marca con vehículos asociados"""
        marca_id = sample_vehiculo.marca_id

        response = client.delete(f"/api/marcas-vehiculo/{marca_id}")
        assert response.status_code == 400
        assert "tiene vehículos asociados" in response.json()["detail"]


class TestPersonaRoutes:
    """Tests para los endpoints de Persona"""

    def test_get_personas_empty(self, client):
        """Test obtener personas cuando no hay ninguna"""
        response = client.get("/api/personas/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_persona(self, client, faker):
        """Test crear una persona"""
        persona_data = {
            "nombre": faker.name(),
            "cedula": str(faker.random_number(digits=10, fix_len=True))
        }

        response = client.post("/api/personas/", json=persona_data)
        assert response.status_code == 200

        data = response.json()
        assert data["nombre"] == persona_data["nombre"]
        assert data["cedula"] == persona_data["cedula"]
        assert "id" in data

    def test_create_persona_duplicate_cedula(self, client):
        """Test crear persona con cédula duplicada"""
        persona_data = {"nombre": "Juan Pérez", "cedula": "123456789"}

        # Crear primera persona
        response1 = client.post("/api/personas/", json=persona_data)
        assert response1.status_code == 200

        # Intentar crear segunda persona con misma cédula
        persona_data2 = {"nombre": "María García", "cedula": "123456789"}
        response2 = client.post("/api/personas/", json=persona_data2)
        assert response2.status_code == 400
        assert "Ya existe una persona con esa cédula" in response2.json()["detail"]

    def test_get_persona_by_id(self, client, sample_persona):
        """Test obtener persona por ID"""
        response = client.get(f"/api/personas/{sample_persona.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sample_persona.id
        assert data["nombre"] == sample_persona.nombre
        assert data["cedula"] == sample_persona.cedula

    def test_get_persona_vehiculos_empty(self, client, sample_persona):
        """Test obtener vehículos de una persona sin vehículos"""
        response = client.get(f"/api/personas/{sample_persona.id}/vehiculos")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sample_persona.id
        assert data["vehiculos"] == []

    def test_update_persona(self, client, sample_persona, faker):
        """Test actualizar una persona"""
        update_data = {
            "nombre": faker.name(),
            "cedula": str(faker.random_number(digits=10, fix_len=True))
        }

        response = client.put(f"/api/personas/{sample_persona.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["nombre"] == update_data["nombre"]
        assert data["cedula"] == update_data["cedula"]

    def test_delete_persona(self, client, sample_persona):
        """Test eliminar una persona"""
        response = client.delete(f"/api/personas/{sample_persona.id}")
        assert response.status_code == 200
        assert "eliminada exitosamente" in response.json()["message"]

        # Verificar que ya no existe
        response = client.get(f"/api/personas/{sample_persona.id}")
        assert response.status_code == 404

    def test_delete_persona_with_vehiculos(self, client, vehiculo_con_propietario):
        """Test que no se pueda eliminar persona con vehículos asociados"""
        persona_id = vehiculo_con_propietario.propietarios[0].id

        response = client.delete(f"/api/personas/{persona_id}")
        assert response.status_code == 400
        assert "tiene vehículos asociados" in response.json()["detail"]


class TestVehiculoRoutes:
    """Tests para los endpoints de Vehiculo"""

    def test_get_vehiculos_empty(self, client):
        """Test obtener vehículos cuando no hay ninguno"""
        response = client.get("/api/vehiculos/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_vehiculo(self, client, sample_marca, faker):
        """Test crear un vehículo"""
        vehiculo_data = {
            "modelo": faker.word().capitalize(),
            "marca_id": sample_marca.id,
            "numero_puertas": faker.random_element([2, 3, 4, 5]),
            "color": faker.color_name()
        }

        response = client.post("/api/vehiculos/", json=vehiculo_data)
        assert response.status_code == 200

        data = response.json()
        assert data["modelo"] == vehiculo_data["modelo"]
        assert data["marca_id"] == vehiculo_data["marca_id"]
        assert data["numero_puertas"] == vehiculo_data["numero_puertas"]
        assert data["color"] == vehiculo_data["color"]
        assert "id" in data

    def test_create_vehiculo_invalid_marca(self, client):
        """Test crear vehículo con marca inexistente"""
        vehiculo_data = {
            "modelo": "Corolla",
            "marca_id": 999,  # Marca inexistente
            "numero_puertas": 4,
            "color": "Rojo"
        }

        response = client.post("/api/vehiculos/", json=vehiculo_data)
        assert response.status_code == 400
        assert "La marca especificada no existe" in response.json()["detail"]

    def test_get_vehiculo_by_id(self, client, sample_vehiculo):
        """Test obtener vehículo por ID"""
        response = client.get(f"/api/vehiculos/{sample_vehiculo.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sample_vehiculo.id
        assert data["modelo"] == sample_vehiculo.modelo
        assert data["marca"]["id"] == sample_vehiculo.marca.id

    def test_get_vehiculo_propietarios_empty(self, client, sample_vehiculo):
        """Test obtener propietarios de un vehículo sin propietarios"""
        response = client.get(f"/api/vehiculos/{sample_vehiculo.id}/propietarios")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sample_vehiculo.id
        assert data["propietarios"] == []

    def test_assign_propietario_to_vehiculo(self, client, sample_vehiculo, sample_persona):
        """Test asignar propietario a vehículo"""
        asignacion_data = {"persona_id": sample_persona.id}

        response = client.post(
            f"/api/vehiculos/{sample_vehiculo.id}/propietarios/",
            json=asignacion_data
        )
        assert response.status_code == 200
        assert "Propietario asignado exitosamente" in response.json()["message"]

        # Verificar que la asignación se realizó
        response = client.get(f"/api/vehiculos/{sample_vehiculo.id}/propietarios")
        assert response.status_code == 200
        data = response.json()
        assert len(data["propietarios"]) == 1
        assert data["propietarios"][0]["id"] == sample_persona.id

        # Verificar desde la persona
        response = client.get(f"/api/personas/{sample_persona.id}/vehiculos")
        assert response.status_code == 200
        data = response.json()
        assert len(data["vehiculos"]) == 1
        assert data["vehiculos"][0]["id"] == sample_vehiculo.id

    def test_assign_duplicate_propietario(self, client, sample_vehiculo, sample_persona):
        """Test asignar el mismo propietario dos veces"""
        asignacion_data = {"persona_id": sample_persona.id}

        # Primera asignación
        response1 = client.post(
            f"/api/vehiculos/{sample_vehiculo.id}/propietarios/",
            json=asignacion_data
        )
        assert response1.status_code == 200

        # Segunda asignación (debería fallar)
        response2 = client.post(
            f"/api/vehiculos/{sample_vehiculo.id}/propietarios/",
            json=asignacion_data
        )
        assert response2.status_code == 400
        assert "ya es propietaria" in response2.json()["detail"]

    def test_assign_propietario_invalid_persona(self, client, sample_vehiculo):
        """Test asignar propietario inexistente"""
        asignacion_data = {"persona_id": 999}

        response = client.post(
            f"/api/vehiculos/{sample_vehiculo.id}/propietarios/",
            json=asignacion_data
        )
        assert response.status_code == 404
        assert "Persona no encontrada" in response.json()["detail"]

    def test_assign_propietario_invalid_vehiculo(self, client, sample_persona):
        """Test asignar propietario a vehículo inexistente"""
        asignacion_data = {"persona_id": sample_persona.id}

        response = client.post("/api/vehiculos/999/propietarios/", json=asignacion_data)
        assert response.status_code == 404
        assert "Vehículo no encontrado" in response.json()["detail"]

    def test_update_vehiculo(self, client, sample_vehiculo, faker):
        """Test actualizar un vehículo"""
        update_data = {
            "modelo": faker.word().capitalize(),
            "color": faker.color_name()
        }

        response = client.put(f"/api/vehiculos/{sample_vehiculo.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["modelo"] == update_data["modelo"]
        assert data["color"] == update_data["color"]
        assert data["numero_puertas"] == sample_vehiculo.numero_puertas  # No cambió

    def test_delete_vehiculo(self, client, sample_vehiculo):
        """Test eliminar un vehículo"""
        response = client.delete(f"/api/vehiculos/{sample_vehiculo.id}")
        assert response.status_code == 200
        assert "eliminado exitosamente" in response.json()["message"]

        # Verificar que ya no existe
        response = client.get(f"/api/vehiculos/{sample_vehiculo.id}")
        assert response.status_code == 404


class TestGeneralEndpoints:
    """Tests para endpoints generales"""

    def test_health_check(self, client):
        """Test endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data

    def test_root_endpoint(self, client):
        """Test endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "documentation" in data
