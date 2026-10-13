# Estructura de carpetas recomendada

La siguiente estructura organiza el proyecto Docker de manera clara, separando el frontend, backend y base de datos.

```text
Docker-TP/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── database.py
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   └── images/
│
├── mysql/
│   └── init.sql
│
├── .env
├── .env.example
├── .gitignore
└── docker-compose.yml
```

## Descripción de la estructura

### `backend/`

Contiene la aplicación desarrollada con **FastAPI**.

- `Dockerfile`: define cómo se construye la imagen del backend.
- `requirements.txt`: contiene las dependencias de Python necesarias para ejecutar la aplicación, incluyendo el SDK de Sentry.
- `main.py`: archivo principal de la aplicación FastAPI. Contiene los endpoints y la configuración de Sentry para registrar errores.
- `database.py`: contiene la configuración de conexión entre FastAPI y la base de datos MySQL compatible.

### `frontend/`

Contiene la aplicación web que será servida mediante **Nginx**.

- `Dockerfile`: define cómo se construye la imagen del frontend utilizando Nginx.
- `nginx.conf`: configuración personalizada del servidor Nginx.
- `index.html`: estructura principal de la página.
- `script.js`: lógica JavaScript del frontend y solicitudes al backend para obtener los datos de los usuarios.
- `styles.css`: estilos visuales de la aplicación.
- `images/`: recursos gráficos utilizados por el frontend.

### `mysql/`

Contiene los archivos relacionados con la base de datos local.

- `init.sql`: script utilizado para inicializar la base de datos, crear tablas y cargar datos iniciales.

En el entorno de despliegue se configuró una base de datos externa mediante **TiDB Cloud**, por lo que la aplicación publicada no depende de la instancia local de MySQL.

### `.env`

Contiene las variables de entorno utilizadas por Docker Compose y el backend, como las credenciales de la base de datos y el DSN de Sentry.

Entre estas variables se encuentran las relacionadas con la conexión a la base de datos y `SENTRY_DSN`, utilizado para enviar los eventos a Sentry.

Este archivo **no debe subirse al repositorio** porque puede contener información sensible.

### `.env.example`

Contiene un ejemplo de las variables necesarias para configurar el proyecto, pero sin información sensible.

Sirve como referencia para otros desarrolladores que necesiten ejecutar la aplicación en otro entorno.

### `.gitignore`

Indica qué archivos o carpetas no deben ser incluidos en Git.

En este proyecto se utiliza principalmente para evitar subir el archivo `.env` y otros archivos locales que no deben formar parte del repositorio.

### `docker-compose.yml`

Es el archivo principal de Docker Compose.

Define y coordina los tres servicios del entorno local:

- MySQL.
- FastAPI.
- Nginx.

También configura:

- Redes Docker.
- Volúmenes.
- Variables de entorno.
- Puertos.
- Dependencias entre servicios.
- Healthcheck de MySQL.
- Construcción de las imágenes mediante los Dockerfiles.

Además, se configuró la variable `SENTRY_DSN` para que el backend pueda acceder al DSN de Sentry mediante una variable de entorno.

Para el entorno desplegado, las variables de conexión a la base de datos se configuran según el proveedor externo utilizado.

## Arquitectura

La aplicación utiliza una arquitectura de tres servicios en el entorno local:

```text
                    Docker Compose
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
       Frontend        Backend           MySQL
        Nginx          FastAPI           8.0
         :80            :8000            :3306
          |               |               |
          +---------------+---------------+
                    Docker Network
```

El frontend es servido por Nginx, el backend utiliza FastAPI para procesar las solicitudes y la base de datos MySQL almacena la información de la aplicación.

Los servicios se encuentran conectados mediante una red Docker definida en `docker-compose.yml`.

### Arquitectura del entorno desplegado

Para permitir que la aplicación funcione fuera del entorno local, se incorporaron servicios externos para el despliegue y la persistencia de datos.

```text
                 Usuario
                    |
                    v
               Aplicación
                 en Vercel
                    |
                    v
             Backend FastAPI
                    |
          +---------+---------+
          |                   |
          v                   v
      TiDB Cloud            Sentry
     Base de datos       Monitoreo de
       externa              errores
```

**Vercel** permite acceder a la aplicación publicada mediante una URL pública. **TiDB Cloud** proporciona la base de datos externa utilizada por el backend y **Sentry** permite registrar y consultar errores de la aplicación.

## Ejecución del proyecto

Para construir y ejecutar todos los servicios locales se utiliza un único comando:

```bash
docker compose up --build
```

También puede ejecutarse en segundo plano:

```bash
docker compose up -d --build
```

Una vez iniciados los servicios:

- Frontend: `http://localhost`
- Backend / Swagger: `http://localhost:8000/docs`

## Despliegue de la aplicación

Para permitir el acceso a la aplicación desde Internet, se configuró el despliegue en **Vercel**.

URL pública:


| Componente | URL |
|---|---|
| Frontend (página con el mensaje de bienvenida) | https://despliegue-y-observabilidad-equipo-five.vercel.app |
| Backend (API FastAPI) | https://despliegue-y-observabilidad-equipo.vercel.app |
| Documentación interactiva de la API (Swagger) | https://despliegue-y-observabilidad-equipo.vercel.app/docs |
| Ruta que provoca el error a propósito (para Sentry) | https://despliegue-y-observabilidad-equipo.vercel.app/probar-sentry |
| Repositorio de GitHub | https://github.com/kevinanton01/Despliegue-y-Observabilidad-Equipo-2 |


El backend utiliza las variables de entorno configuradas en el entorno de despliegue para conectarse a la base de datos externa de TiDB Cloud.

Las variables necesarias deben configurarse en los ajustes del proyecto desplegado. El archivo `.env` local no se carga automáticamente en Vercel.

## Configuración de la base de datos externa

Se configuró **TiDB Cloud** para que la aplicación pudiera utilizar una base de datos accesible desde el entorno desplegado.

Para ello, se adaptó la configuración de conexión del backend mediante variables de entorno, incluyendo el host, puerto, usuario, contraseña y nombre de la base de datos.

De esta manera, el backend puede consultar los usuarios almacenados en la base de datos externa sin depender de la instancia MySQL que se ejecuta localmente con Docker.

Las credenciales deben mantenerse privadas y configurarse de forma segura en el entorno de despliegue.

## Integración con Sentry

Se incorporó **Sentry** para monitorear y registrar los errores que ocurren en el backend.

La configuración se realizó mediante los siguientes pasos:

1. Se agregó `sentry-sdk` al archivo `requirements.txt`.
2. Se importó la biblioteca y se inicializó Sentry en `main.py`.
3. Se configuró el DSN mediante la variable de entorno `SENTRY_DSN`.
4. Se agregó esta variable al entorno del backend en `docker-compose.yml`.
5. Se guardó el DSN en el archivo `.env`, evitando escribirlo directamente en el código.

Desde el panel de Sentry se pueden consultar los errores registrados y obtener información técnica para facilitar su diagnóstico.

### Variables de entorno

Las credenciales no están en el código ni en GitHub. Se configuran como variables de entorno en el panel de Vercel (el archivo `.env` está en el `.gitignore`).

| Variable | Contenido |
|---|---|
| `MYSQL_HOST` | Host de la base de datos en TiDB Cloud |
| `MYSQL_PORT` | Puerto de conexión (en TiDB Cloud es el 4000) |
| `MYSQL_USER` | Usuario de la base de datos |
| `MYSQL_PASSWORD` | Contraseña de la base de datos |
| `MYSQL_DATABASE` | Nombre de la base de datos |
| `SENTRY_DSN` | Dirección privada del proyecto en Sentry |
## Tecnologías utilizadas

- **Python:** lenguaje utilizado para desarrollar el backend.
- **FastAPI:** framework para crear la API.
- **SQLAlchemy:** biblioteca para gestionar la conexión y las consultas a la base de datos.
- **PyMySQL:** controlador para conectarse a bases de datos compatibles con MySQL.
- **HTML, CSS y JavaScript:** tecnologías utilizadas para desarrollar el frontend.
- **Nginx:** servidor web utilizado para servir el frontend localmente mediante Docker.
- **Docker y Docker Compose:** herramientas para contenerizar y ejecutar los servicios.
- **TiDB Cloud:** servicio externo utilizado para alojar la base de datos.
- **Vercel:** plataforma utilizada para publicar la aplicación.
- **Sentry:** herramienta de monitoreo y registro de errores.
- **Git y GitHub:** herramientas utilizadas para el control de versiones y el almacenamiento del código fuente.
icios:

* Frontend: `http://localhost`
* Backend / Swagger: `http://localhost:8000/docs`
