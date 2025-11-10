import pytest
from sqlalchemy.exc import IntegrityError

from app.models.models import MarcaVehiculo, Persona, Vehiculo, Base


class TestMarcaVehiculo:
    """Tests para el modelo MarcaVehiculo"""

    def test_create_marca_vehiculo(self, db_session, faker):
        """Test crear una marca de vehículo"""
        marca = MarcaVehiculo(
            nombre_marca=faker.company(),
            pais=faker.country()
        )

        db_session.add(marca)
        db_session.commit()
        db_session.refresh(marca)

        assert marca.id is not None
        assert marca.nombre_marca is not None
        assert marca.pais is not None

    def test_marca_vehiculo_unique_constraint(self, db_session):
        """Test que el nombre de marca sea único"""
        marca1 = MarcaVehiculo(nombre_marca="Toyota", pais="Japón")
        db_session.add(marca1)
        db_session.commit()

        # Intentar crear otra marca con el mismo nombre
        marca2 = MarcaVehiculo(nombre_marca="Toyota", pais="Corea")

        with pytest.raises(IntegrityError):
            db_session.add(marca2)
            db_session.commit()

    def test_marca_vehiculo_relationship_with_vehiculos(self, db_session, sample_marca, sample_vehiculo):
        """Test la relación entre marca y vehículos"""
        # Verificar que la marca tiene el vehículo
        assert len(sample_marca.vehiculos) == 1
        assert sample_marca.vehiculos[0].id == sample_vehiculo.id

        # Verificar que el vehículo tiene la marca correcta
        assert sample_vehiculo.marca.id == sample_marca.id
        assert sample_vehiculo.marca.nombre_marca == sample_marca.nombre_marca


class TestPersona:
    """Tests para el modelo Persona"""

    def test_create_persona(self, db_session, faker):
        """Test crear una persona"""
        persona = Persona(
            nombre=faker.name(),
            cedula=str(faker.random_number(digits=10, fix_len=True))
        )

        db_session.add(persona)
        db_session.commit()
        db_session.refresh(persona)

        assert persona.id is not None
        assert persona.nombre is not None
        assert persona.cedula is not None

    def test_persona_unique_cedula_constraint(self, db_session):
        """Test que la cédula sea única"""
        persona1 = Persona(nombre="Juan Pérez", cedula="123456789")
        db_session.add(persona1)
        db_session.commit()

        # Intentar crear otra persona con la misma cédula
        persona2 = Persona(nombre="María García", cedula="123456789")

        with pytest.raises(IntegrityError):
            db_session.add(persona2)
            db_session.commit()

    def test_persona_relationship_with_vehiculos_empty(self, db_session, sample_persona):
        """Test que una persona nueva no tenga vehículos"""
        assert len(sample_persona.vehiculos) == 0


class TestVehiculo:
    """Tests para el modelo Vehiculo"""

    def test_create_vehiculo(self, db_session, sample_marca, faker):
        """Test crear un vehículo"""
        vehiculo = Vehiculo(
            modelo=faker.word().capitalize(),
            marca_id=sample_marca.id,
            numero_puertas=4,
            color=faker.color_name()
        )

        db_session.add(vehiculo)
        db_session.commit()
        db_session.refresh(vehiculo)

        assert vehiculo.id is not None
        assert vehiculo.modelo is not None
        assert vehiculo.marca_id == sample_marca.id
        assert vehiculo.numero_puertas == 4
        assert vehiculo.color is not None

    def test_vehiculo_foreign_key_constraint(self, db_session):
        """Test que falle al crear vehículo con marca inexistente"""
        vehiculo = Vehiculo(
            modelo="Corolla",
            marca_id=999,  # ID inexistente
            numero_puertas=4,
            color="Rojo"
        )

        with pytest.raises(IntegrityError):
            db_session.add(vehiculo)
            db_session.commit()

    def test_vehiculo_relationship_with_marca(self, db_session, sample_vehiculo, sample_marca):
        """Test la relación entre vehículo y marca"""
        assert sample_vehiculo.marca.id == sample_marca.id
        assert sample_vehiculo.marca.nombre_marca == sample_marca.nombre_marca

    def test_vehiculo_relationship_with_propietarios_empty(self, db_session, sample_vehiculo):
        """Test que un vehículo nuevo no tenga propietarios"""
        assert len(sample_vehiculo.propietarios) == 0


class TestVehiculoPersonaRelationship:
    """Tests para la relación Many-to-Many entre Vehiculo y Persona"""

    def test_assign_propietario_to_vehiculo(self, db_session, sample_vehiculo, sample_persona):
        """Test asignar un propietario a un vehículo"""
        # Asignar propietario
        sample_vehiculo.propietarios.append(sample_persona)
        db_session.commit()

        # Verificar la relación desde vehículo
        db_session.refresh(sample_vehiculo)
        assert len(sample_vehiculo.propietarios) == 1
        assert sample_vehiculo.propietarios[0].id == sample_persona.id

        # Verificar la relación desde persona
        db_session.refresh(sample_persona)
        assert len(sample_persona.vehiculos) == 1
        assert sample_persona.vehiculos[0].id == sample_vehiculo.id

    def test_multiple_propietarios_same_vehiculo(self, db_session, sample_vehiculo, multiple_personas):
        """Test asignar múltiples propietarios al mismo vehículo"""
        # Asignar múltiples propietarios
        for persona in multiple_personas:
            sample_vehiculo.propietarios.append(persona)

        db_session.commit()
        db_session.refresh(sample_vehiculo)

        assert len(sample_vehiculo.propietarios) == 3

        # Verificar que cada persona tiene el vehículo
        for persona in multiple_personas:
            db_session.refresh(persona)
            assert len(persona.vehiculos) == 1
            assert persona.vehiculos[0].id == sample_vehiculo.id

    def test_same_persona_multiple_vehiculos(self, db_session, sample_persona, multiple_marcas):
        """Test que una persona pueda tener múltiples vehículos"""
        vehiculos = []
        for marca in multiple_marcas:
            vehiculo = Vehiculo(
                modelo="Modelo Test",
                marca_id=marca.id,
                numero_puertas=4,
                color="Azul"
            )
            db_session.add(vehiculo)
            vehiculos.append(vehiculo)

        db_session.commit()

        # Asignar todos los vehículos a la misma persona
        for vehiculo in vehiculos:
            sample_persona.vehiculos.append(vehiculo)

        db_session.commit()
        db_session.refresh(sample_persona)

        assert len(sample_persona.vehiculos) == 3
