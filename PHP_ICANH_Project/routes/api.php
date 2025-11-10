<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\GeneralController;
use App\Http\Controllers\MarcaVehiculoController;
use App\Http\Controllers\PersonaController;
use App\Http\Controllers\VehiculoController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

// Endpoints generales
Route::get('/', [GeneralController::class, 'welcome'])->name('welcome');
Route::get('/health', [GeneralController::class, 'health'])->name('health');

// Rutas para Marcas de Vehículo
Route::prefix('marcas-vehiculo')->group(function () {
    Route::get('/', [MarcaVehiculoController::class, 'index'])->name('marcas-vehiculo.index');
    Route::post('/', [MarcaVehiculoController::class, 'store'])->name('marcas-vehiculo.store');
    Route::get('/{marca_vehiculo}', [MarcaVehiculoController::class, 'show'])->name('marcas-vehiculo.show');
    Route::put('/{marca_vehiculo}', [MarcaVehiculoController::class, 'update'])->name('marcas-vehiculo.update');
    Route::delete('/{marca_vehiculo}', [MarcaVehiculoController::class, 'destroy'])->name('marcas-vehiculo.destroy');
});

// Rutas para Personas
Route::prefix('personas')->group(function () {
    Route::get('/', [PersonaController::class, 'index'])->name('personas.index');
    Route::post('/', [PersonaController::class, 'store'])->name('personas.store');
    Route::get('/{persona}', [PersonaController::class, 'show'])->name('personas.show');
    Route::put('/{persona}', [PersonaController::class, 'update'])->name('personas.update');
    Route::delete('/{persona}', [PersonaController::class, 'destroy'])->name('personas.destroy');

    // Ruta adicional para obtener vehículos de una persona
    Route::get('/{persona}/vehiculos', [PersonaController::class, 'getVehiculos'])->name('personas.vehiculos');
});

// Rutas para Vehículos
Route::prefix('vehiculos')->group(function () {
    Route::get('/', [VehiculoController::class, 'index'])->name('vehiculos.index');
    Route::post('/', [VehiculoController::class, 'store'])->name('vehiculos.store');
    Route::get('/{vehiculo}', [VehiculoController::class, 'show'])->name('vehiculos.show');
    Route::put('/{vehiculo}', [VehiculoController::class, 'update'])->name('vehiculos.update');
    Route::delete('/{vehiculo}', [VehiculoController::class, 'destroy'])->name('vehiculos.destroy');

    // Rutas adicionales para propietarios
    Route::get('/{vehiculo}/propietarios', [VehiculoController::class, 'getPropietarios'])->name('vehiculos.propietarios');
    Route::post('/{vehiculo}/propietarios', [VehiculoController::class, 'assignPropietario'])->name('vehiculos.assign-propietario');
});

// Rutas de documentación Swagger
Route::get('/docs', function () {
    return redirect('/api/documentation');
})->name('docs');

Route::get('/redoc', function () {
    return redirect('/api/documentation');
})->name('redoc');
