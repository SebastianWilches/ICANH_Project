# Usar imagen base de PHP con Apache
FROM php:8.4-apache

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    sqlite3 \
    libsqlite3-dev \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip pdo_sqlite

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Configurar Apache
RUN a2enmod rewrite
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Establecer directorio de trabajo
WORKDIR /var/www/html

# Copiar todo el código de la aplicación
COPY . .

# Instalar dependencias de PHP
RUN composer install --no-dev --optimize-autoloader --no-interaction

# Crear directorio para base de datos SQLite
RUN mkdir -p database && touch database/database.sqlite

# Configurar permisos
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 775 /var/www/html/storage \
    && chmod -R 775 /var/www/html/bootstrap/cache

# Configurar Apache para servir desde /var/www/html/public
RUN sed -i 's|/var/www/html|/var/www/html/public|g' /etc/apache2/sites-available/000-default.conf && \
    sed -i '/DocumentRoot/a \\n    <Directory /var/www/html/public>\n        AllowOverride All\n        Require all granted\n    </Directory>' /etc/apache2/sites-available/000-default.conf

# Crear archivo .env básico
RUN cp .env.example .env || echo "APP_NAME=\"API de Gestión de Vehículos - ICANH\"\nAPP_ENV=production\nAPP_DEBUG=false\nAPP_URL=http://localhost:8080\nAPP_KEY=\n\nDB_CONNECTION=sqlite\nDB_DATABASE=/var/www/html/database/database.sqlite\n\nCACHE_DRIVER=file\nQUEUE_CONNECTION=sync\nSESSION_DRIVER=file" > .env

# Generar key de la aplicación
RUN php artisan key:generate

# Ejecutar migraciones
RUN php artisan migrate --force

# Generar documentación Swagger
RUN php artisan l5-swagger:generate

# Exponer puerto 80 (Apache)
EXPOSE 80

# Comando para iniciar Apache
CMD ["apache2-foreground"]

