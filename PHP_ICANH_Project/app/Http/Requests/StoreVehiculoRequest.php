<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreVehiculoRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return false;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'modelo' => 'required|string|min:1',
            'marca_id' => 'required|integer|min:1|exists:marca_vehiculo,id',
            'numero_puertas' => 'required|integer|min:2|max:5',
            'color' => 'required|string|min:1'
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
            'modelo.required' => 'El modelo es obligatorio',
            'marca_id.required' => 'La marca es obligatoria',
            'marca_id.exists' => 'La marca especificada no existe',
            'numero_puertas.required' => 'El número de puertas es obligatorio',
            'numero_puertas.min' => 'El número de puertas debe ser al menos 2',
            'numero_puertas.max' => 'El número de puertas no puede ser mayor a 5',
            'color.required' => 'El color es obligatorio'
        ];
    }
}
