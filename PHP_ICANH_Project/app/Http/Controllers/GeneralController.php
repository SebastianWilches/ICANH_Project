<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;

/**
 * @OA\Info(
 *     title="API de Gestión de Vehículos - ICANH",
 *     description="API RESTful para la gestión de vehículos, marcas, personas y sus relaciones",
 *     version="1.0.0",
 *     @OA\Contact(
 *         name="Jhoan Sebastian Wilches Jimenez",
 *         email="sebastianwilches2@gmail.com"
 *     ),
 *     @OA\License(name="MIT")
 * )
 * @OA\Server(
 *     url="http://localhost:8000/api",
 *     description="Servidor de desarrollo"
 * )
 */
class GeneralController extends Controller
{
    /**
     * @OA\Get(
     *     path="/",
     *     summary="Bienvenida",
     *     tags={"General"},
     *     @OA\Response(
     *         response=200,
     *         description="Mensaje de bienvenida",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Bienvenido a la API de Gestión de Vehículos - ICANH"),
     *             @OA\Property(property="version", type="string", example="1.0.0"),
     *             @OA\Property(property="documentation", type="string", example="/docs"),
     *             @OA\Property(property="redoc", type="string", example="/redoc")
     *         )
     *     )
     * )
     */
    public function welcome(): JsonResponse
    {
        return response()->json([
            'message' => 'Bienvenido a la API de Gestión de Vehículos - ICANH',
            'version' => config('app.version', '1.0.0'),
            'documentation' => '/docs',
            'redoc' => '/redoc'
        ]);
    }

    /**
     * @OA\Get(
     *     path="/health",
     *     summary="Health Check",
     *     tags={"General"},
     *     @OA\Response(
     *         response=200,
     *         description="Estado de salud de la API",
     *         @OA\JsonContent(
     *             @OA\Property(property="status", type="string", example="healthy"),
     *             @OA\Property(property="message", type="string", example="API funcionando correctamente")
     *         )
     *     )
     * )
     */
    public function health(): JsonResponse
    {
        return response()->json([
            'status' => 'healthy',
            'message' => 'API funcionando correctamente'
        ]);
    }
}
