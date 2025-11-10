<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Persona extends Model
{
    protected $table = 'persona';

    protected $fillable = [
        'nombre',
        'cedula'
    ];

    /**
     * Relación Many-to-Many con Vehiculo a través de vehiculo_persona
     */
    public function vehiculos(): BelongsToMany
    {
        return $this->belongsToMany(Vehiculo::class, 'vehiculo_persona', 'persona_id', 'vehiculo_id');
    }
}
