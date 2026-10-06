# Utiliza Python 3.11 en una imagen liviana basada en Debian
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt .

# Instala las dependencias necesarias para ejecutar FastAPI
# --no-cache-dir evita almacenar archivos de caché innecesarios
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del backend al directorio de trabajo
COPY . .

# Documenta que la aplicación utilizará el puerto 8000
EXPOSE 8000

# Ejecuta la aplicación FastAPI mediante Uvicorn
# --host 0.0.0.0 permite recibir conexiones desde fuera del contenedor
# --port 8000 indica el puerto utilizado por la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]