<?php

namespace Tests\Feature\Models;

use App\Models\MarcaVehiculo;
use App\Models\Vehiculo;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class MarcaVehiculoTest extends TestCase
{
    use RefreshDatabase;

    public function test_create_marca_vehiculo()
    {
        $marca = MarcaVehiculo::factory()->create([
            'nombre_marca' => 'Toyota',
            'pais' => 'Japón'
        ]);

        $this->assertInstanceOf(MarcaVehiculo::class, $marca);
        $this->assertNotNull($marca->id);
        $this->assertEquals('Toyota', $marca->nombre_marca);
        $this->assertEquals('Japón', $marca->pais);
    }

    public function test_marca_vehiculo_unique_constraint()
    {
        MarcaVehiculo::create([
            'nombre_marca' => 'Toyota',
            'pais' => 'Japón'
        ]);

        $this->expectException(\Illuminate\Database\QueryException::class);

        MarcaVehiculo::create([
            'nombre_marca' => 'Toyota',
            'pais' => 'Corea'
        ]);
    }

    public function test_marca_vehiculo_relationship_with_vehiculos()
    {
        $marca = MarcaVehiculo::factory()->create();
        $vehiculo = Vehiculo::factory()->create(['marca_id' => $marca->id]);

        $this->assertCount(1, $marca->vehiculos);
        $this->assertEquals($vehiculo->id, $marca->vehiculos->first()->id);

        // Verificar la relación inversa
        $this->assertEquals($marca->id, $vehiculo->marca->id);
        $this->assertEquals($marca->nombre_marca, $vehiculo->marca->nombre_marca);
    }
}
