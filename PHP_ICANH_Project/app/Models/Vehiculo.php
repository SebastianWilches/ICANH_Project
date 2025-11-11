<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Vehiculo extends Model
{
    use HasFactory;
    protected $table = 'vehiculo';

    protected $fillable = [
        'modelo',
        'marca_id',
        'numero_puertas',
        'color'
    ];

    /**
     * Relación con MarcaVehiculo (Many-to-One)
     */
    public function marca(): BelongsTo
    {
        return $this->belongsTo(MarcaVehiculo::class, 'marca_id');
    }

    /**
     * Relación Many-to-Many con Persona a través de vehiculo_persona
     */
    public function propietarios(): BelongsToMany
    {
        return $this->belongsToMany(Persona::class, 'vehiculo_persona', 'vehiculo_id', 'persona_id');
    }
}
