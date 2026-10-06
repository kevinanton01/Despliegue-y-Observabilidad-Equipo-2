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

* `Dockerfile`: define cómo se construye la imagen del backend.
* `requirements.txt`: contiene las dependencias de Python necesarias para ejecutar la aplicación.
* `main.py`: archivo principal de la aplicación FastAPI.
* `database.py`: contiene la configuración de conexión entre FastAPI y MySQL.

### `frontend/`

Contiene la aplicación web que será servida mediante **Nginx**.

* `Dockerfile`: define cómo se construye la imagen del frontend utilizando Nginx.
* `nginx.conf`: configuración personalizada del servidor Nginx.
* `index.html`: estructura principal de la página.
* `script.js`: lógica JavaScript del frontend.
* `styles.css`: estilos visuales de la aplicación.
* `images/`: recursos gráficos utilizados por el frontend.

### `mysql/`

Contiene los archivos relacionados con la base de datos.

* `init.sql`: script utilizado para inicializar la base de datos, crear tablas y cargar datos iniciales.

### `.env`

Contiene las variables de entorno utilizadas por Docker Compose, como las credenciales de MySQL y los puertos de los servicios.

Este archivo **no debe subirse al repositorio** porque puede contener información sensible.

### `.env.example`

Contiene un ejemplo de las variables necesarias para configurar el proyecto, pero sin información sensible.

Sirve como referencia para otros desarrolladores.

### `.gitignore`

Indica qué archivos o carpetas no deben ser incluidos en Git.

En este proyecto se utiliza principalmente para evitar subir el archivo `.env`.

### `docker-compose.yml`

Es el archivo principal de Docker Compose.

Define y coordina los tres servicios del proyecto:

* MySQL
* FastAPI
* Nginx

También configura:

* Redes Docker.
* Volúmenes.
* Variables de entorno.
* Puertos.
* Dependencias entre servicios.
* Healthcheck de MySQL.
* Construcción de las imágenes mediante los Dockerfiles.

## Arquitectura

La aplicación utiliza una arquitectura de tres servicios:

```text
                    Docker Compose
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
       Frontend        Backend          MySQL
        Nginx          FastAPI          8.0
         :80            :8000           :3306
          │               │               │
          └───────────────┴───────────────┘
                   Docker Network
```

El frontend es servido por Nginx, el backend utiliza FastAPI para procesar las solicitudes y MySQL almacena la información de la aplicación.

Los servicios se encuentran conectados mediante una red Docker definida en `docker-compose.yml`.

## Ejecución del proyecto

Para construir y ejecutar todos los servicios se utiliza un único comando:

```bash
docker compose up --build
```

También puede ejecutarse en segundo plano:

```bash
docker compose up -d --build
```

Una vez iniciados los servicios:

* Frontend: `http://localhost`
* Backend / Swagger: `http://localhost:8000/docs`
