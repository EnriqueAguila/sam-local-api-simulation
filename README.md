# SAM API Gateway - Simulación Local


Este proyecto utiliza AWS SAM (Serverless Application Model) para crear y simular localmente una API RESTful compleja. **Está diseñado exclusivamente para desarrollo y pruebas locales y no para ser desplegado en AWS.**


El objetivo es replicar una estructura de API existente, donde una única función AWS Lambda actúa como un enrutador central para todas las rutas y métodos HTTP.


## Arquitectura Simulada

```bash
│
├── .git/                     <-- Carpeta de Git (generalmente oculta)
│
├── .gitignore                <-- Archivo para ignorar ficheros (ej. .aws-sam/)
│
├── .aws-sam/                 <-- Carpeta creada por 'sam build' con los artefactos
│   └── build.toml            <--     de construcción. No se sube a Git.
│   └── build/
│       ├── ApiRouterFunction/
│       └── template.yaml
│
├── api_handler/              <-- Carpeta que contiene el CÓDIGO de tu función Lambda.
│   ├── __init__.py           <-- Archivo vacío que hace de esta carpeta un paquete de Python.
│   ├── app.py                <-- El CÓDIGO PRINCIPAL de tu Lambda (el "enrutador").
│   └── requirements.txt      <-- Lista de dependencias de Python (si las tuvieras).
│
├── events/                   <-- Carpeta para eventos de prueba locales.
│   └── event.json            <-- Un evento JSON de ejemplo para invocar la Lambda localmente.
│
├── README.md                 <-- La DOCUMENTACIÓN de tu proyecto. Explica qué es y cómo usarlo.
│
├── samconfig.toml            <-- Archivo de configuración creado por 'sam deploy --guided'.
│                                 Guarda tus respuestas (nombre del stack, región, etc.).
│
└── template.yaml             <-- El CORAZÓN de SAM. Define tu infraestructura (API 
```


El `template.yaml` define la infraestructura que `sam local` utilizará para la simulación:


-   **API Gateway Simulada:** Un servidor local que replica la funcionalidad de Amazon API Gateway, exponiendo todos los endpoints definidos.
-   **Función Lambda en Contenedor:** Una función Python que se ejecuta dentro de un contenedor de Docker, imitando el entorno de AWS Lambda. Esta función recibe todas las peticiones y las enruta a la lógica apropiada.


## Requisitos Previos


-   [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
-   [Python 3.9+](https://www.python.org/downloads/)
-   [Docker](https://www.docker.com/products/docker-desktop/) - **Debe estar instalado y en ejecución.**


## Cómo Ejecutar el Proyecto


Este proyecto no se despliega (`sam deploy`). Toda la interacción se realiza localmente.


### 1. Construir la Función


Antes de poder ejecutar la simulación, necesitas construir los artefactos de tu función Lambda. Este paso es necesario cada vez que haces un cambio en el código Python.


```bash
sam build
```


### 2. Iniciar el Servidor de API Local


Este comando inicia un servidor web en tu máquina en `http://127.0.0.1:3000` que se comporta como la API Gateway real.


```bash
sam local start-api
```


La terminal mostrará que el servidor está escuchando. Ahora puedes usar herramientas como `curl` o Postman para enviar peticiones a tus endpoints simulados.


### Ejemplos de Peticiones con `curl`


Abre una **nueva ventana de terminal** (dejando la del servidor corriendo) y prueba los siguientes comandos:


```bash
# Probar la ruta raíz (GET)
curl http://127.0.0.1:3000/


# Probar el endpoint de login (POST con datos)
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "123"}' \
     http://127.0.0.1:3000/login


# Probar una ruta anidada
curl -X POST -d '{}' http://127.0.0.1:3000/token/transition


# Probar una ruta no existente (debería dar un 404)
curl http://127.0.0.1:3000/ruta-que-no-existe
```


Para detener el servidor local, vuelve a la terminal donde se está ejecutando y presiona `Control + C`.
