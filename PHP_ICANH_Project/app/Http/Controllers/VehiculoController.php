<?php

namespace App\Http\Controllers;

use App\Models\Vehiculo;
use App\Models\Persona;
use App\Http\Requests\StoreVehiculoRequest;
use App\Http\Requests\UpdateVehiculoRequest;
use App\Http\Requests\AssignPropietarioRequest;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * @OA\Tag(
 *     name="Vehículos",
 *     description="Operaciones CRUD para vehículos"
 * )
 */
class VehiculoController extends Controller
{
    /**
     * @OA\Get(
     *     path="/vehiculos",
     *     summary="Obtener todos los vehículos",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="skip",
     *         in="query",
     *         description="Número de registros a saltar (paginación)",
     *         required=false,
     *         @OA\Schema(type="integer", default=0)
     *     ),
     *     @OA\Parameter(
     *         name="limit",
     *         in="query",
     *         description="Número máximo de registros a devolver",
     *         required=false,
     *         @OA\Schema(type="integer", default=100)
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Lista de vehículos",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="modelo", type="string", example="Corolla"),
     *                 @OA\Property(property="marca_id", type="integer", example=1),
     *                 @OA\Property(property="numero_puertas", type="integer", example=4),
     *                 @OA\Property(property="color", type="string", example="Rojo"),
     *                 @OA\Property(property="created_at", type="string", format="date-time"),
     *                 @OA\Property(property="updated_at", type="string", format="date-time"),
     *                 @OA\Property(
     *                     property="marca",
     *                     type="object",
     *                     @OA\Property(property="id", type="integer", example=1),
     *                     @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                     @OA\Property(property="pais", type="string", example="Japón")
     *                 )
     *             )
     *         )
     *     )
     * )
     */
    public function index(Request $request): JsonResponse
    {
        $skip = $request->query('skip', 0);
        $limit = $request->query('limit', 100);

        $vehiculos = Vehiculo::with('marca')->skip($skip)->take($limit)->get();

        return response()->json($vehiculos);
    }

    /**
     * @OA\Post(
     *     path="/vehiculos",
     *     summary="Crear un nuevo vehículo",
     *     tags={"Vehículos"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"modelo", "marca_id", "numero_puertas", "color"},
     *             @OA\Property(property="modelo", type="string", minLength=1, example="Corolla"),
     *             @OA\Property(property="marca_id", type="integer", minimum=1, example=1),
     *             @OA\Property(property="numero_puertas", type="integer", minimum=2, maximum=5, example=4),
     *             @OA\Property(property="color", type="string", minLength=1, example="Rojo")
     *         )
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Vehículo creado exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="modelo", type="string", example="Corolla"),
     *             @OA\Property(property="marca_id", type="integer", example=1),
     *             @OA\Property(property="numero_puertas", type="integer", example=4),
     *             @OA\Property(property="color", type="string", example="Rojo"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time"),
     *             @OA\Property(
     *                 property="marca",
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                 @OA\Property(property="pais", type="string", example="Japón")
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=422,
     *         description="Error de validación",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string"),
     *             @OA\Property(property="errors", type="object")
     *         )
     *     )
     * )
     */
    public function store(StoreVehiculoRequest $request): JsonResponse
    {
        $vehiculo = Vehiculo::create($request->validated());

        return response()->json($vehiculo->load('marca'), 201);
    }

    /**
     * @OA\Get(
     *     path="/vehiculos/{vehiculo}",
     *     summary="Obtener un vehículo por ID",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="vehiculo",
     *         in="path",
     *         description="ID del vehículo",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Vehículo encontrado",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="modelo", type="string", example="Corolla"),
     *             @OA\Property(property="marca_id", type="integer", example=1),
     *             @OA\Property(property="numero_puertas", type="integer", example=4),
     *             @OA\Property(property="color", type="string", example="Rojo"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time"),
     *             @OA\Property(
     *                 property="marca",
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                 @OA\Property(property="pais", type="string", example="Japón")
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vehículo no encontrado",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo no encontrado")
     *         )
     *     )
     * )
     */
    public function show(Vehiculo $vehiculo): JsonResponse
    {
        return response()->json($vehiculo->load('marca'));
    }

    /**
     * @OA\Put(
     *     path="/vehiculos/{vehiculo}",
     *     summary="Actualizar un vehículo",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="vehiculo",
     *         in="path",
     *         description="ID del vehículo",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             @OA\Property(property="modelo", type="string", minLength=1, example="Corolla Updated"),
     *             @OA\Property(property="marca_id", type="integer", minimum=1, example=2),
     *             @OA\Property(property="numero_puertas", type="integer", minimum=2, maximum=5, example=5),
     *             @OA\Property(property="color", type="string", minLength=1, example="Azul")
     *         )
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Vehículo actualizado exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="modelo", type="string", example="Corolla Updated"),
     *             @OA\Property(property="marca_id", type="integer", example=2),
     *             @OA\Property(property="numero_puertas", type="integer", example=5),
     *             @OA\Property(property="color", type="string", example="Azul"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time"),
     *             @OA\Property(
     *                 property="marca",
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=2),
     *                 @OA\Property(property="nombre_marca", type="string", example="Honda"),
     *                 @OA\Property(property="pais", type="string", example="Japón")
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vehículo no encontrado",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo no encontrado")
     *         )
     *     ),
     *     @OA\Response(
     *         response=422,
     *         description="Error de validación",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string"),
     *             @OA\Property(property="errors", type="object")
     *         )
     *     )
     * )
     */
    public function update(UpdateVehiculoRequest $request, Vehiculo $vehiculo): JsonResponse
    {
        $vehiculo->update($request->validated());

        return response()->json($vehiculo->load('marca'));
    }

    /**
     * @OA\Delete(
     *     path="/vehiculos/{vehiculo}",
     *     summary="Eliminar un vehículo",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="vehiculo",
     *         in="path",
     *         description="ID del vehículo",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Vehículo eliminado exitosamente",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo eliminado exitosamente")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vehículo no encontrado",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo no encontrado")
     *         )
     *     )
     * )
     */
    public function destroy(Vehiculo $vehiculo): JsonResponse
    {
        $vehiculo->delete();

        return response()->json(['message' => 'Vehículo eliminado exitosamente']);
    }

    /**
     * @OA\Get(
     *     path="/vehiculos/{vehiculo}/propietarios",
     *     summary="Obtener propietarios de un vehículo",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="vehiculo",
     *         in="path",
     *         description="ID del vehículo",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Propietarios del vehículo",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="modelo", type="string", example="Corolla"),
     *             @OA\Property(property="marca_id", type="integer", example=1),
     *             @OA\Property(property="numero_puertas", type="integer", example=4),
     *             @OA\Property(property="color", type="string", example="Rojo"),
     *             @OA\Property(
     *                 property="marca",
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                 @OA\Property(property="pais", type="string", example="Japón")
     *             ),
     *             @OA\Property(
     *                 property="propietarios",
     *                 type="array",
     *                 @OA\Items(
     *                     type="object",
     *                     @OA\Property(property="id", type="integer", example=1),
     *                     @OA\Property(property="nombre", type="string", example="Juan Pérez"),
     *                     @OA\Property(property="cedula", type="string", example="123456789")
     *                 )
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vehículo no encontrado",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo no encontrado")
     *         )
     *     )
     * )
     */
    public function getPropietarios(Vehiculo $vehiculo): JsonResponse
    {
        return response()->json($vehiculo->load(['marca', 'propietarios']));
    }

    /**
     * @OA\Post(
     *     path="/vehiculos/{vehiculo}/propietarios",
     *     summary="Asignar propietario a un vehículo",
     *     tags={"Vehículos"},
     *     @OA\Parameter(
     *         name="vehiculo",
     *         in="path",
     *         description="ID del vehículo",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"persona_id"},
     *             @OA\Property(property="persona_id", type="integer", minimum=1, example=1)
     *         )
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Propietario asignado exitosamente",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Propietario asignado exitosamente al vehículo")
     *         )
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="La persona ya es propietaria o error de validación",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Esta persona ya es propietaria de este vehículo")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vehículo o persona no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Vehículo no encontrado")
     *         )
     *     )
     * )
     */
    public function assignPropietario(AssignPropietarioRequest $request, Vehiculo $vehiculo): JsonResponse
    {
        $persona = Persona::findOrFail($request->persona_id);

        // Verificar si la relación ya existe
        if ($vehiculo->propietarios()->where('persona_id', $persona->id)->exists()) {
            return response()->json([
                'message' => 'Esta persona ya es propietaria de este vehículo'
            ], 400);
        }

        $vehiculo->propietarios()->attach($persona->id);

        return response()->json(['message' => 'Propietario asignado exitosamente al vehículo']);
    }
}
