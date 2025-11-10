<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreMarcaVehiculoRequest extends FormRequest
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
        return [
            'nombre_marca' => 'required|string|min:1|unique:marca_vehiculo,nombre_marca',
            'pais' => 'required|string|min:1'
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
            'nombre_marca.required' => 'El nombre de la marca es obligatorio',
            'nombre_marca.unique' => 'Ya existe una marca con ese nombre',
            'pais.required' => 'El país de origen es obligatorio'
        ];
    }
}
