<?php

namespace App\Http\Controllers;

use App\Models\MarcaVehiculo;
// use App\Http\Requests\StoreMarcaVehiculoRequest;
use App\Http\Requests\UpdateMarcaVehiculoRequest;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

/**
 * @OA\Tag(
 *     name="Marcas de Vehículo",
 *     description="Operaciones CRUD para marcas de vehículo"
 * )
 */
class MarcaVehiculoController extends Controller
{
    /**
     * @OA\Get(
     *     path="/marcas-vehiculo",
     *     summary="Obtener todas las marcas de vehículo",
     *     tags={"Marcas de Vehículo"},
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
     *         description="Lista de marcas de vehículo",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(
     *                 type="object",
     *                 @OA\Property(property="id", type="integer", example=1),
     *                 @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *                 @OA\Property(property="pais", type="string", example="Japón"),
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

        $marcas = MarcaVehiculo::skip($skip)->take($limit)->get();

        return response()->json($marcas);
    }

    /**
     * @OA\Post(
     *     path="/marcas-vehiculo",
     *     summary="Crear una nueva marca de vehículo",
     *     tags={"Marcas de Vehículo"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"nombre_marca", "pais"},
     *             @OA\Property(property="nombre_marca", type="string", minLength=1, example="Toyota"),
     *             @OA\Property(property="pais", type="string", minLength=1, example="Japón")
     *         )
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Marca creada exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *             @OA\Property(property="pais", type="string", example="Japón"),
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
    public function store(Request $request): JsonResponse
    {
        // Debug temporal
        return response()->json([
            'debug_request_all' => $request->all(),
            'debug_request_content' => $request->getContent(),
            'debug_headers' => [
                'content_type' => $request->header('Content-Type'),
                'accept' => $request->header('Accept'),
            ],
            'debug_method' => $request->method(),
            'debug_is_json' => $request->isJson(),
            'debug_wants_json' => $request->wantsJson(),
        ]);

        // Validación manual
        // $validated = $request->validate([
        //     'nombre_marca' => 'required|string|min:1|unique:marca_vehiculo,nombre_marca',
        //     'pais' => 'required|string|min:1'
        // ]);

        // $marca = MarcaVehiculo::create($validated);
        // return response()->json($marca, 201);
    }

    /**
     * @OA\Get(
     *     path="/marcas-vehiculo/{marca_vehiculo}",
     *     summary="Obtener una marca de vehículo por ID",
     *     tags={"Marcas de Vehículo"},
     *     @OA\Parameter(
     *         name="marca_vehiculo",
     *         in="path",
     *         description="ID de la marca",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Marca encontrada",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *             @OA\Property(property="pais", type="string", example="Japón"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Marca no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Marca no encontrada")
     *         )
     *     )
     * )
     */
    public function show(MarcaVehiculo $marca_vehiculo): JsonResponse
    {
        return response()->json($marca_vehiculo);
    }

    /**
     * @OA\Put(
     *     path="/marcas-vehiculo/{marca_vehiculo}",
     *     summary="Actualizar una marca de vehículo",
     *     tags={"Marcas de Vehículo"},
     *     @OA\Parameter(
     *         name="marca_vehiculo",
     *         in="path",
     *         description="ID de la marca",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             @OA\Property(property="nombre_marca", type="string", minLength=1, example="Toyota Updated"),
     *             @OA\Property(property="pais", type="string", minLength=1, example="Japón Updated")
     *         )
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Marca actualizada exitosamente",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="id", type="integer", example=1),
     *             @OA\Property(property="nombre_marca", type="string", example="Toyota"),
     *             @OA\Property(property="pais", type="string", example="Japón"),
     *             @OA\Property(property="created_at", type="string", format="date-time"),
     *             @OA\Property(property="updated_at", type="string", format="date-time")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Marca no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Marca no encontrada")
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
    public function update(UpdateMarcaVehiculoRequest $request, MarcaVehiculo $marca_vehiculo): JsonResponse
    {
        $marca_vehiculo->update($request->validated());

        return response()->json($marca_vehiculo);
    }

    /**
     * @OA\Delete(
     *     path="/marcas-vehiculo/{marca_vehiculo}",
     *     summary="Eliminar una marca de vehículo",
     *     tags={"Marcas de Vehículo"},
     *     @OA\Parameter(
     *         name="marca_vehiculo",
     *         in="path",
     *         description="ID de la marca",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Marca eliminada exitosamente",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Marca eliminada exitosamente")
     *         )
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="No se puede eliminar por tener vehículos asociados",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="No se puede eliminar la marca porque tiene vehículos asociados")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Marca no encontrada",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Marca no encontrada")
     *         )
     *     )
     * )
     */
    public function destroy(MarcaVehiculo $marca_vehiculo): JsonResponse
    {
        // Verificar si hay vehículos asociados
        if ($marca_vehiculo->vehiculos()->count() > 0) {
            return response()->json([
                'message' => 'No se puede eliminar la marca porque tiene vehículos asociados'
            ], 400);
        }

        $marca_vehiculo->delete();

        return response()->json(['message' => 'Marca eliminada exitosamente']);
    }
}
