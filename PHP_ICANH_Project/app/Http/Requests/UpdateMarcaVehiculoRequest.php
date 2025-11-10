<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateMarcaVehiculoRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        $marcaId = $this->route('marca_vehiculo');

        return [
            'nombre_marca' => 'sometimes|string|min:1|unique:marca_vehiculo,nombre_marca,' . $marcaId,
            'pais' => 'sometimes|string|min:1'
        ];
    }

    /**
     * Get custom messages for validator errors.
     *
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'nombre_marca.unique' => 'Ya existe una marca con ese nombre',
        ];
    }
}
