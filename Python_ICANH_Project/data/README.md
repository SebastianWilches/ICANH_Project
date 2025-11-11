# Directorio de Datos

Este directorio contiene la persistencia de datos para la aplicación Docker.

## 📁 Contenido

- **`vehiculos.db`**: Base de datos SQLite principal (creada automáticamente por Docker)
- **`.gitkeep`**: Archivo para mantener el directorio en Git (opcional)

## 🔄 Comportamiento

- **Desarrollo**: Los datos persisten entre reinicios del contenedor
- **Producción**: Los datos se mantienen en el volumen Docker
- **Git**: Este directorio se incluye en el repositorio pero `vehiculos.db` está en `.gitignore`

## 🧹 Limpieza

Para reiniciar la base de datos:

```bash
# Detener contenedor
docker-compose down

# Eliminar base de datos
rm data/vehiculos.db

# Reiniciar contenedor (se crea nueva BD)
docker-compose up -d
```

## 📊 Backup

Para hacer backup de los datos:

```bash
# Copiar archivo de base de datos
cp data/vehiculos.db backup/vehiculos_$(date +%Y%m%d_%H%M%S).db
```
