<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Vehiculo>
 */
class VehiculoFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'modelo' => ucfirst($this->faker->word()),
            'marca_id' => \App\Models\MarcaVehiculo::factory(),
            'numero_puertas' => $this->faker->numberBetween(2, 5),
            'color' => $this->faker->colorName(),
        ];
    }
}
