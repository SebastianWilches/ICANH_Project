<?php

namespace Tests\Feature;

use App\Models\MarcaVehiculo;
use App\Models\Vehiculo;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class MarcaVehiculoRoutesTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();

        // Para tests de API, deshabilitar middlewares que puedan interferir
        // $this->withoutMiddleware();
    }

    public function test_get_marcas_empty()
    {
        $response = $this->get('/api/marcas-vehiculo/');

        $response->assertStatus(200)
                ->assertJson([]);
    }

    public function test_create_marca_vehiculo()
    {
        $marcaData = [
            'nombre_marca' => 'Toyota',
            'pais' => 'Japón'
        ];

        $response = $this->postJson('/api/marcas-vehiculo/', $marcaData);

        $response->assertStatus(201)
                ->assertJson([
                    'nombre_marca' => 'Toyota',
                    'pais' => 'Japón'
                ])
                ->assertJsonStructure(['id']);
    }

    public function test_create_marca_duplicate_name()
    {
        // Crear primera marca
        $this->postJson('/api/marcas-vehiculo/', [
            'nombre_marca' => 'Toyota',
            'pais' => 'Japón'
        ]);

        // Intentar crear segunda marca con mismo nombre
        $response = $this->postJson('/api/marcas-vehiculo/', [
            'nombre_marca' => 'Toyota',
            'pais' => 'Corea'
        ]);

        $response->assertStatus(422)
                ->assertJsonValidationErrors(['nombre_marca']);
    }

    public function test_get_marca_by_id()
    {
        $marca = MarcaVehiculo::factory()->create();

        $response = $this->get("/api/marcas-vehiculo/{$marca->id}");

        $response->assertStatus(200)
                ->assertJson([
                    'id' => $marca->id,
                    'nombre_marca' => $marca->nombre_marca,
                    'pais' => $marca->pais
                ]);
    }

    public function test_get_marca_not_found()
    {
        $response = $this->get('/api/marcas-vehiculo/999');

        $response->assertStatus(404);
    }

    public function test_update_marca()
    {
        $marca = MarcaVehiculo::factory()->create();

        $updateData = [
            'nombre_marca' => 'Toyota Updated',
            'pais' => 'Japón Updated'
        ];

        $response = $this->putJson("/api/marcas-vehiculo/{$marca->id}", $updateData);

        $response->assertStatus(200)
                ->assertJson([
                    'nombre_marca' => 'Toyota Updated',
                    'pais' => 'Japón Updated'
                ]);
    }

    public function test_update_marca_partial()
    {
        $marca = MarcaVehiculo::factory()->create();

        $updateData = ['pais' => 'Japón Updated'];

        $response = $this->putJson("/api/marcas-vehiculo/{$marca->id}", $updateData);

        $response->assertStatus(200)
                ->assertJson([
                    'nombre_marca' => $marca->nombre_marca, // No cambió
                    'pais' => 'Japón Updated'
                ]);
    }

    public function test_delete_marca()
    {
        $marca = MarcaVehiculo::factory()->create();

        $response = $this->delete("/api/marcas-vehiculo/{$marca->id}");

        $response->assertStatus(200)
                ->assertJson(['message' => 'Marca eliminada exitosamente']);

        // Verificar que ya no existe
        $this->get("/api/marcas-vehiculo/{$marca->id}")
             ->assertStatus(404);
    }

    public function test_delete_marca_with_vehiculos()
    {
        $vehiculo = Vehiculo::factory()->create();
        $marcaId = $vehiculo->marca_id;

        $response = $this->delete("/api/marcas-vehiculo/{$marcaId}");

        $response->assertStatus(400)
                ->assertJson(['message' => 'No se puede eliminar la marca porque tiene vehículos asociados']);
    }
}
