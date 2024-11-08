
# Proyecto FastAPI para Gestión de Usuarios, KPIs y Registros

Este proyecto es una API desarrollada con **FastAPI** que permite gestionar usuarios, roles, KPIs y registros. La API ofrece endpoints para crear y consultar usuarios, KPIs y registros, utilizando **Pydantic** para la validación de datos.

## Requisitos

Asegúrate de tener **Python 3.10** o superior instalado en tu sistema.

### Dependencias

Instala las dependencias del proyecto con el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
Proyecto/
│
├── app/
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── models/
│   │   ├── users.py           # Modelos para usuarios
│   │   ├── roles.py           # Modelos para roles de usuario
│   │   ├── records.py         # Modelos para registros
│   │   └── kpis.py            # Modelos para KPIs
│   └── __init__.py            # Inicialización del paquete
└── requirements.txt           # Lista de dependencias
```

## Instalación y Configuración

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone <URL_del_repositorio>
   cd Proyecto
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicia el servidor en development:

   ```bash
   fastapi dev
   ```

   El servidor estará disponible en `http://127.0.0.1:8000`.

## Uso de la API

### Endpoints principales

- **GET /**: Muestra un mensaje de bienvenida.
- **POST /users**: Crea un nuevo usuario.
- **GET /users/**: Lista todos los usuarios.
- **GET /users/{id}**: Obtiene los datos de un usuario específico.
- **POST /kpis**: Crea un nuevo KPI.
- **POST /records**: Crea un nuevo registro asociado a un usuario y a uno o más KPIs.

### Documentación

La documentación de la API generada automáticamente estará disponible en:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Contribuciones

Para contribuir al proyecto, por favor haz un fork del repositorio y envía un pull request con tus cambios.

## Notas

Si deseas agregar o modificar modelos, asegúrate de hacerlo en el directorio `app/models/`, y actualiza los endpoints correspondientes en `main.py`.

---

Este archivo proporciona una guía para la instalación, configuración y uso de la API para nuevos usuarios del proyecto.
