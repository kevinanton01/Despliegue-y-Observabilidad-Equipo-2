# Utiliza una imagen liviana de Nginx basada en Alpine
FROM nginx:alpine

# Copia los archivos del frontend al directorio
# utilizado por Nginx para servir contenido web
COPY . /usr/share/nginx/html

# Reemplaza la configuración predeterminada de Nginx
# por nuestra configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Documenta el puerto HTTP utilizado por Nginx
EXPOSE 80

# Ejecuta Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]