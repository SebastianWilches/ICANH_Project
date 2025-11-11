<?php

/**
 * @OA\Schema(
 *     schema="MarcaVehiculo",
 *     type="object",
 *     title="MarcaVehiculo",
 *     description="Modelo de Marca de Vehículo",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="nombre_marca", type="string", example="Toyota"),
 *     @OA\Property(property="pais", type="string", example="Japón"),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time")
 * )
 *
 * @OA\Schema(
 *     schema="Persona",
 *     type="object",
 *     title="Persona",
 *     description="Modelo de Persona",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="nombre", type="string", example="Juan Pérez"),
 *     @OA\Property(property="cedula", type="string", example="123456789"),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time")
 * )
 *
 * @OA\Schema(
 *     schema="Vehiculo",
 *     type="object",
 *     title="Vehiculo",
 *     description="Modelo de Vehículo",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="modelo", type="string", example="Corolla"),
 *     @OA\Property(property="marca_id", type="integer", example=1),
 *     @OA\Property(property="numero_puertas", type="integer", example=4),
 *     @OA\Property(property="color", type="string", example="Rojo"),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time"),
 *     @OA\Property(
 *         property="marca",
 *         ref="#/components/schemas/MarcaVehiculo",
 *         description="Información de la marca del vehículo"
 *     ),
 *     @OA\Property(
 *         property="propietarios",
 *         type="array",
 *         @OA\Items(ref="#/components/schemas/Persona"),
 *         description="Lista de propietarios del vehículo"
 *     )
 * )
 *
 * @OA\Schema(
 *     schema="StoreMarcaVehiculoRequest",
 *     type="object",
 *     title="StoreMarcaVehiculoRequest",
 *     description="Datos para crear una marca de vehículo",
 *     required={"nombre_marca", "pais"},
 *     @OA\Property(property="nombre_marca", type="string", minLength=1, example="Toyota"),
 *     @OA\Property(property="pais", type="string", minLength=1, example="Japón")
 * )
 *
 * @OA\Schema(
 *     schema="UpdateMarcaVehiculoRequest",
 *     type="object",
 *     title="UpdateMarcaVehiculoRequest",
 *     description="Datos para actualizar una marca de vehículo",
 *     @OA\Property(property="nombre_marca", type="string", minLength=1, example="Toyota Updated"),
 *     @OA\Property(property="pais", type="string", minLength=1, example="Japón Updated")
 * )
 *
 * @OA\Schema(
 *     schema="StorePersonaRequest",
 *     type="object",
 *     title="StorePersonaRequest",
 *     description="Datos para crear una persona",
 *     required={"nombre", "cedula"},
 *     @OA\Property(property="nombre", type="string", minLength=1, example="Juan Pérez"),
 *     @OA\Property(property="cedula", type="string", minLength=1, example="123456789")
 * )
 *
 * @OA\Schema(
 *     schema="UpdatePersonaRequest",
 *     type="object",
 *     title="UpdatePersonaRequest",
 *     description="Datos para actualizar una persona",
 *     @OA\Property(property="nombre", type="string", minLength=1, example="Juan Pérez Updated"),
 *     @OA\Property(property="cedula", type="string", minLength=1, example="987654321")
 * )
 *
 * @OA\Schema(
 *     schema="StoreVehiculoRequest",
 *     type="object",
 *     title="StoreVehiculoRequest",
 *     description="Datos para crear un vehículo",
 *     required={"modelo", "marca_id", "numero_puertas", "color"},
 *     @OA\Property(property="modelo", type="string", minLength=1, example="Corolla"),
 *     @OA\Property(property="marca_id", type="integer", minimum=1, example=1),
 *     @OA\Property(property="numero_puertas", type="integer", minimum=2, maximum=5, example=4),
 *     @OA\Property(property="color", type="string", minLength=1, example="Rojo")
 * )
 *
 * @OA\Schema(
 *     schema="UpdateVehiculoRequest",
 *     type="object",
 *     title="UpdateVehiculoRequest",
 *     description="Datos para actualizar un vehículo",
 *     @OA\Property(property="modelo", type="string", minLength=1, example="Corolla Updated"),
 *     @OA\Property(property="marca_id", type="integer", minimum=1, example=2),
 *     @OA\Property(property="numero_puertas", type="integer", minimum=2, maximum=5, example=5),
 *     @OA\Property(property="color", type="string", minLength=1, example="Azul")
 * )
 *
 * @OA\Schema(
 *     schema="AssignPropietarioRequest",
 *     type="object",
 *     title="AssignPropietarioRequest",
 *     description="Datos para asignar propietario a vehículo",
 *     required={"persona_id"},
 *     @OA\Property(property="persona_id", type="integer", minimum=1, example=1)
 * )
 */
