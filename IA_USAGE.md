# Uso de IA en el Desarrollo del Proyecto ICANH

## Herramientas y Modelos Utilizados

Para el desarrollo de este proyecto, decidí usar **Cursor** como mi IDE principal, aprovechando su integración nativa con modelos de IA. Específicamente utilicé el modelo **grok-code-fast-1** para la asistencia en el desarrollo de código, depuración y refinamiento de implementaciones.

**Cursor** ofrece:
- Integración fluida con modelos de IA
- Asistencia contextual en tiempo real
- Capacidades de refactorización inteligente
- Soporte para múltiples lenguajes de programación

**grok-code-fast-1** proporcionó:
- Generación rápida de código
- Análisis inteligente de problemas
- Sugerencias precisas para corrección de errores
- Ayuda en la implementación de mejores prácticas

## Prompts Claves y Análisis Críticos

### 1. Inicialización del Proyecto PHP con Laravel

**Prompt utilizado:**
> "Entendido, ahora necesito que hagamos lo siguiente, en base a la funcionalidad completa del proyecto de python con fastAPI necesito que repliquemos exactamente los mismos endpoints, estructura de base de datos, la misma estructura para los .env necesito que en la carpeta de PHP_ICANH_Project crees el API RESTful pero ahora haciendo uso de Laravel con un gestor de dependencias de Composer, una base de datos SQLite manteniendo exactamente la misma documentacion en swagger y creando tambien los mismos test pero haciendo uso de PHPUnit."

**Problema crítico identificado:**
Tuve un problema bastante recurrente que me costó darme cuenta y era que al usar `composer` para inicializar el proyecto, tomaba una ruta completamente diferente a la que estábamos trabajando en el contexto, por lo que tuve que indicar la ruta absoluta de donde quería que hiciera esto ya que generaba un proyecto inicial bastante alejado de lo que se quería hacer.

**Análisis:**
El modelo de IA inicialmente asumió que quería crear el proyecto en el directorio raíz o en una ubicación estándar, pero necesitaba especificar explícitamente la ruta absoluta `C:\Users\Sebastian Wilches\Documents\Proyectos Software\ICANH_Prueba tecnica\ICANH_Project\ICANH_Project\PHP_ICANH_Project\` para que `composer create-project` funcionara correctamente en el contexto de trabajo actual.

**Solución implementada:**
- Especificar rutas absolutas en comandos de terminal
- Usar `cd` para cambiar al directorio correcto antes de ejecutar comandos
- Verificar la ubicación actual del proyecto antes de inicializar

### 2. Refinamiento del Endpoint `/api/personas/{persona_id}/vehiculos`

**Prompt utilizado:**
> "En caso de que usemos el endpoint de /api/personas/{persona_id}/vehiculos y no tengo vehiculos asociados una persona no deberia romperse."

**Problema identificado:**
Durante las pruebas manuales, el endpoint se rompía cuando una persona no tenía vehículos asociados, lo que causaba errores en la aplicación.

**Análisis crítico:**
El modelo de IA inicialmente generó código que no manejaba correctamente los casos donde las relaciones many-to-many no existían. Fue necesario refinar la lógica para:
- Manejar consultas que retornan listas vacías
- Implementar validaciones apropiadas para casos edge
- Asegurar que la respuesta sea consistente independientemente de si existen relaciones o no

**Solución implementada:**
- Agregar manejo de excepciones para consultas vacías
- Implementar validación de existencia de persona antes de consultar vehículos
- Retornar arrays vacíos en lugar de errores cuando no hay relaciones
- Mejorar el manejo de errores en los controladores

## Uso en Desafíos Opcionales

La IA fue particularmente útil en los desafíos opcionales que no manejaba con la misma profundidad que otros lenguajes:

### Generación de Tests Automatizados
- **Desafío**: Crear tests completos para endpoints PHP usando PHPUnit
- **Ayuda de IA**: Generó automáticamente la estructura completa de tests, incluyendo:
  - Tests de modelos con constraints únicos
  - Tests de endpoints REST completos
  - Tests de validación con Form Request Classes
  - Tests de relaciones Many-to-Many
- **Beneficio**: Ahorro significativo de tiempo en un lenguaje que no domino completamente

### Configuración de Docker
- **Desafío**: Crear configuración completa de Docker para el proyecto PHP
- **Ayuda de IA**: Generó archivos Docker completos incluyendo:
  - Dockerfile optimizado para Laravel
  - docker-compose.yml con configuración de servicios
  - Scripts de inicio para diferentes sistemas operativos
  - Manejo de volúmenes y persistencia de datos
- **Beneficio**: Eliminó la necesidad de investigar manualmente las mejores prácticas de Docker para Laravel

### Optimización de Rendimiento
- **Ayuda de IA**: Sugirió optimizaciones como:
  - Uso apropiado de eager loading en Eloquent
  - Configuración correcta de índices en migraciones
  - Implementación de caching para consultas frecuentes

## Lecciones Aprendidas

1. **Especificidad en Prompts**: Los prompts deben ser extremadamente específicos sobre rutas, contextos y requisitos exactos para evitar interpretaciones erróneas.

2. **Verificación de Resultados**: Siempre es necesario probar manualmente las implementaciones generadas por IA, especialmente en casos edge y manejo de errores.

3. **Iteración Continua**: El proceso de desarrollo con IA es iterativo - cada respuesta puede requerir refinamiento basado en pruebas reales.

4. **Contexto Completo**: Proporcionar el contexto completo del proyecto ayuda a la IA a generar código más preciso y consistente.

## Recomendaciones para Uso Futuro

- Mantener consistencia en la estructura de prompts
- Probar inmediatamente las implementaciones generadas
- Documentar problemas encontrados y soluciones aplicadas
- Usar la IA como complemento, no como reemplazo del conocimiento técnico

---

**Proyecto desarrollado con asistencia de IA para optimizar el proceso de desarrollo**
