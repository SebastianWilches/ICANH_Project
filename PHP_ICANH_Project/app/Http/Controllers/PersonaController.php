<?php

namespace App\Http\Controllers;

use App\Models\Persona;
use App\Http\Requests\StorePersonaRequest;
use App\Http\Requests\UpdatePersonaRequest;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * @OA\Tag(
 *     name="Personas",
 *     description="Operaciones CRUD para personas"
 * )
 */
class PersonaController extends Controller
{
    /**
     * @OA\Get(
     *     path="/personas",
     *     summary="Obtener todas las personas",
     *     tags={"Personas"},
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
     *         description="Lista de personas",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="nombre", type="string", example="Juan Pérez"),
     *                 @OA\Property(property="cedula", type="string", example="123456789"),
     *                 @OA\Property(property="created_at", type="string", format="date-time"),
     *                 @OA\Property(property="updated_at", type="string", format="date-time")
     *             )
     *         )
     *     )
     * )
     */
    public function index(Request $request): JsonResponse
    {
        $skip = $request->query('skip', 0);
        $limit = $request->query('limit', 100);

        $personas = Persona::skip($skip)->take($limit)->get();

        return response()->json($personas);
    }

    /**
     * @OA\Post(
     *     path="/personas",
     *     summary="Crear una nueva persona",
     *     tags={"Personas"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"nombre", "cedula"},
     *             @OA\Property(property="nombre", type="string", minLength=1, example="Juan Pérez"),
     *             @OA\Property(property="cedula", type="string", minLength=1, example="123456789")
     *         )
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Persona creada exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre", type="string", example="Juan Pérez"),
     *             @OA\Property(property="cedula", type="string", example="123456789"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time")
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
    public function store(StorePersonaRequest $request): JsonResponse
    {
        $persona = Persona::create($request->validated());

        return response()->json($persona, 201);
    }

    /**
     * @OA\Get(
     *     path="/personas/{persona}",
     *     summary="Obtener una persona por ID",
     *     tags={"Personas"},
     *     @OA\Parameter(
     *         name="persona",
     *         in="path",
     *         description="ID de la persona",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Persona encontrada",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre", type="string", example="Juan Pérez"),
     *             @OA\Property(property="cedula", type="string", example="123456789"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Persona no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Persona no encontrada")
     *         )
     *     )
     * )
     */
    public function show(Persona $persona): JsonResponse
    {
        return response()->json($persona);
    }

    /**
     * @OA\Put(
     *     path="/personas/{persona}",
     *     summary="Actualizar una persona",
     *     tags={"Personas"},
     *     @OA\Parameter(
     *         name="persona",
     *         in="path",
     *         description="ID de la persona",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             @OA\Property(property="nombre", type="string", minLength=1, example="Juan Pérez Updated"),
     *             @OA\Property(property="cedula", type="string", minLength=1, example="987654321")
     *         )
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Persona actualizada exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre", type="string", example="Juan Pérez Updated"),
     *             @OA\Property(property="cedula", type="string", example="987654321"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Persona no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Persona no encontrada")
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
    public function update(UpdatePersonaRequest $request, Persona $persona): JsonResponse
    {
        $persona->update($request->validated());

        return response()->json($persona);
    }

    /**
     * @OA\Delete(
     *     path="/personas/{persona}",
     *     summary="Eliminar una persona",
     *     tags={"Personas"},
     *     @OA\Parameter(
     *         name="persona",
     *         in="path",
     *         description="ID de la persona",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Persona eliminada exitosamente",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Persona eliminada exitosamente")
     *         )
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="No se puede eliminar por tener vehículos asociados",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="No se puede eliminar la persona porque tiene vehículos asociados")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Persona no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Persona no encontrada")
     *         )
     *     )
     * )
     */
    public function destroy(Persona $persona): JsonResponse
    {
        // Verificar si la persona tiene vehículos asociados
        if ($persona->vehiculos()->count() > 0) {
            return response()->json([
                'message' => 'No se puede eliminar la persona porque tiene vehículos asociados'
            ], 400);
        }

        $persona->delete();

        return response()->json(['message' => 'Persona eliminada exitosamente']);
    }

    /**
     * @OA\Get(
     *     path="/personas/{persona}/vehiculos",
     *     summary="Obtener vehículos de una persona",
     *     tags={"Personas"},
     *     @OA\Parameter(
     *         name="persona",
     *         in="path",
     *         description="ID de la persona",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Vehículos de la persona",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre", type="string", example="Juan Pérez"),
     *             @OA\Property(property="cedula", type="string", example="123456789"),
     *             @OA\Property(
     *                 property="vehiculos",
     *                 type="array",
     *                 @OA\Items(
     *                     type="object",
     *                     @OA\Property(property="id", type="integer", example=1),
     *                     @OA\Property(property="modelo", type="string", example="Corolla"),
     *                     @OA\Property(property="marca_id", type="integer", example=1),
     *                     @OA\Property(property="numero_puertas", type="integer", example=4),
     *                     @OA\Property(property="color", type="string", example="Rojo"),
     *                     @OA\Property(
     *                         property="marca",
     *                         type="object",
     *                         @OA\Property(property="id", type="integer", example=1),
     *                         @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                         @OA\Property(property="pais", type="string", example="Japón")
     *                     )
     *                 )
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Persona no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Persona no encontrada")
     *         )
     *     )
     * )
     */
    public function getVehiculos(Persona $persona): JsonResponse
    {
        $persona->load(['vehiculos.marca']);

        return response()->json($persona);
    }
}
