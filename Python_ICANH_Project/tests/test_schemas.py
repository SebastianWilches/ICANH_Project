import pytest
from pydantic import ValidationError

from app.schemas.schemas import (
    MarcaVehiculo, MarcaVehiculoCreate, MarcaVehiculoUpdate,
    Persona, PersonaCreate, PersonaUpdate,
    Vehiculo, VehiculoCreate, VehiculoUpdate,
    VehiculoConPropietarios, PersonaConVehiculos,
    AsignarPropietario
)


class TestMarcaVehiculoSchemas:
    """Tests para los esquemas de MarcaVehiculo"""

    def test_marca_vehiculo_create_valid(self):
        """Test crear marca con datos válidos"""
        data = {"nombre_marca": "Toyota", "pais": "Japón"}
        marca = MarcaVehiculoCreate(**data)

        assert marca.nombre_marca == "Toyota"
        assert marca.pais == "Japón"

    def test_marca_vehiculo_create_missing_required_field(self):
        """Test crear marca sin campos requeridos"""
        with pytest.raises(ValidationError):
            MarcaVehiculoCreate()

        with pytest.raises(ValidationError):
            MarcaVehiculoCreate(nombre_marca="Toyota")  # Falta pais

        with pytest.raises(ValidationError):
            MarcaVehiculoCreate(pais="Japón")  # Falta nombre_marca

    def test_marca_vehiculo_update_optional_fields(self):
        """Test actualizar marca con campos opcionales"""
        # Todos los campos opcionales
        update_data = MarcaVehiculoUpdate()
        assert update_data.nombre_marca is None
        assert update_data.pais is None

        # Solo algunos campos
        update_data = MarcaVehiculoUpdate(nombre_marca="Toyota Updated")
        assert update_data.nombre_marca == "Toyota Updated"
        assert update_data.pais is None

    def test_marca_vehiculo_response_schema(self, sample_marca):
        """Test el esquema de respuesta completo"""
        marca_data = {
            "id": sample_marca.id,
            "nombre_marca": sample_marca.nombre_marca,
            "pais": sample_marca.pais
        }

        marca = MarcaVehiculo(**marca_data)

        assert marca.id == sample_marca.id
        assert marca.nombre_marca == sample_marca.nombre_marca
        assert marca.pais == sample_marca.pais


class TestPersonaSchemas:
    """Tests para los esquemas de Persona"""

    def test_persona_create_valid(self):
        """Test crear persona con datos válidos"""
        data = {"nombre": "Juan Pérez", "cedula": "123456789"}
        persona = PersonaCreate(**data)

        assert persona.nombre == "Juan Pérez"
        assert persona.cedula == "123456789"

    def test_persona_create_missing_required_field(self):
        """Test crear persona sin campos requeridos"""
        with pytest.raises(ValidationError):
            PersonaCreate()

        with pytest.raises(ValidationError):
            PersonaCreate(nombre="Juan Pérez")  # Falta cedula

        with pytest.raises(ValidationError):
            PersonaCreate(cedula="123456789")  # Falta nombre

    def test_persona_update_optional_fields(self):
        """Test actualizar persona con campos opcionales"""
        update_data = PersonaUpdate()
        assert update_data.nombre is None
        assert update_data.cedula is None

        update_data = PersonaUpdate(nombre="Juan Pérez Updated")
        assert update_data.nombre == "Juan Pérez Updated"
        assert update_data.cedula is None

    def test_persona_response_schema(self, sample_persona):
        """Test el esquema de respuesta completo"""
        persona_data = {
            "id": sample_persona.id,
            "nombre": sample_persona.nombre,
            "cedula": sample_persona.cedula
        }

        persona = Persona(**persona_data)

        assert persona.id == sample_persona.id
        assert persona.nombre == sample_persona.nombre
        assert persona.cedula == sample_persona.cedula


class TestVehiculoSchemas:
    """Tests para los esquemas de Vehiculo"""

    def test_vehiculo_create_valid(self, sample_marca):
        """Test crear vehículo con datos válidos"""
        data = {
            "modelo": "Corolla",
            "marca_id": sample_marca.id,
            "numero_puertas": 4,
            "color": "Rojo"
        }
        vehiculo = VehiculoCreate(**data)

        assert vehiculo.modelo == "Corolla"
        assert vehiculo.marca_id == sample_marca.id
        assert vehiculo.numero_puertas == 4
        assert vehiculo.color == "Rojo"

    def test_vehiculo_create_missing_required_field(self):
        """Test crear vehículo sin campos requeridos"""
        with pytest.raises(ValidationError):
            VehiculoCreate()

    def test_vehiculo_create_invalid_numero_puertas(self):
        """Test crear vehículo con numero_puertas inválido (debe ser entero)"""
        data = {
            "modelo": "Corolla",
            "marca_id": 1,
            "numero_puertas": "cuatro",  # Debería ser int
            "color": "Rojo"
        }

        with pytest.raises(ValidationError):
            VehiculoCreate(**data)

    def test_vehiculo_update_optional_fields(self):
        """Test actualizar vehículo con campos opcionales"""
        update_data = VehiculoUpdate()
        assert update_data.modelo is None
        assert update_data.marca_id is None
        assert update_data.numero_puertas is None
        assert update_data.color is None

        update_data = VehiculoUpdate(modelo="Corolla Updated")
        assert update_data.modelo == "Corolla Updated"
        assert update_data.marca_id is None

    def test_vehiculo_response_schema(self, sample_vehiculo, sample_marca):
        """Test el esquema de respuesta completo"""
        vehiculo_data = {
            "id": sample_vehiculo.id,
            "modelo": sample_vehiculo.modelo,
            "marca_id": sample_vehiculo.marca_id,
            "numero_puertas": sample_vehiculo.numero_puertas,
            "color": sample_vehiculo.color,
            "marca": {
                "id": sample_marca.id,
                "nombre_marca": sample_marca.nombre_marca,
                "pais": sample_marca.pais
            },
            "propietarios": []
        }

        vehiculo = Vehiculo(**vehiculo_data)

        assert vehiculo.id == sample_vehiculo.id
        assert vehiculo.modelo == sample_vehiculo.modelo
        assert vehiculo.marca.id == sample_marca.id
        assert len(vehiculo.propietarios) == 0


class TestRelationshipSchemas:
    """Tests para los esquemas de relaciones"""

    def test_vehiculo_con_propietarios_schema(self, vehiculo_con_propietario, sample_persona):
        """Test el esquema VehiculoConPropietarios"""
        vehiculo_data = {
            "id": vehiculo_con_propietario.id,
            "modelo": vehiculo_con_propietario.modelo,
            "marca_id": vehiculo_con_propietario.marca_id,
            "numero_puertas": vehiculo_con_propietario.numero_puertas,
            "color": vehiculo_con_propietario.color,
            "marca": {
                "id": vehiculo_con_propietario.marca.id,
                "nombre_marca": vehiculo_con_propietario.marca.nombre_marca,
                "pais": vehiculo_con_propietario.marca.pais
            },
            "propietarios": [{
                "id": sample_persona.id,
                "nombre": sample_persona.nombre,
                "cedula": sample_persona.cedula
            }]
        }

        vehiculo = VehiculoConPropietarios(**vehiculo_data)

        assert vehiculo.id == vehiculo_con_propietario.id
        assert len(vehiculo.propietarios) == 1
        assert vehiculo.propietarios[0].id == sample_persona.id

    def test_persona_con_vehiculos_schema(self, vehiculo_con_propietario, sample_persona):
        """Test el esquema PersonaConVehiculos"""
        persona_data = {
            "id": sample_persona.id,
            "nombre": sample_persona.nombre,
            "cedula": sample_persona.cedula,
            "vehiculos": [{
                "id": vehiculo_con_propietario.id,
                "modelo": vehiculo_con_propietario.modelo,
                "marca_id": vehiculo_con_propietario.marca_id,
                "numero_puertas": vehiculo_con_propietario.numero_puertas,
                "color": vehiculo_con_propietario.color,
                "marca": {
                    "id": vehiculo_con_propietario.marca.id,
                    "nombre_marca": vehiculo_con_propietario.marca.nombre_marca,
                    "pais": vehiculo_con_propietario.marca.pais
                },
                "propietarios": []
            }]
        }

        persona = PersonaConVehiculos(**persona_data)

        assert persona.id == sample_persona.id
        assert len(persona.vehiculos) == 1
        assert persona.vehiculos[0].id == vehiculo_con_propietario.id

    def test_asignar_propietario_schema(self):
        """Test el esquema AsignarPropietario"""
        data = {"persona_id": 1}
        asignacion = AsignarPropietario(**data)

        assert asignacion.persona_id == 1

    def test_asignar_propietario_missing_field(self):
        """Test AsignarPropietario sin persona_id"""
        with pytest.raises(ValidationError):
            AsignarPropietario()
