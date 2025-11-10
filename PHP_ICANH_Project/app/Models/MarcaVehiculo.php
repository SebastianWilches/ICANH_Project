<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class MarcaVehiculo extends Model
{
    protected $table = 'marca_vehiculo';

    protected $fillable = [
        'nombre_marca',
        'pais'
    ];

    /**
     * Relación con Vehiculo (One-to-Many)
     */
    public function vehiculos(): HasMany
    {
        return $this->hasMany(Vehiculo::class, 'marca_id');
    }
}
