# MovieRec - Sistema de Recomendación de Películas

Un sistema de recomendación de películas basado en grafos que utiliza Neo4j para analizar las relaciones entre películas, actores, directores y géneros, proporcionando recomendaciones personalizadas basadas en las preferencias del usuario.

## Descripción del Proyecto

MovieRec es un sistema desarrollado como proyecto del curso Algoritmos y Estructuras de Datos que combina una base de datos de grafos Neo4j con un backend en Flask y un frontend en React. El sistema aprende de las interacciones del usuario para generar recomendaciones personalizadas utilizando el algortimo de Personalized Page Rank. Esto lo hara mediante la interacción de "Likes" o "Dislikes" del usuario, los cuales, dictarán el rumbo de las recomendaciones.

## Equipo de Desarrollo

- Jose Alberto Abril Suchite - 24585
- José Manuel Sanchez Hernández - 24092
- Josué Antonio Isaac García Barrera - 24918

## Arquitectura del Sistema

El proyecto está estructurado en tres capas principales:

- **Frontend**: Aplicación React con Tailwind CSS
- **Backend**: API REST desarrollada en Flask
- **Base de Datos**: Neo4j para almacenamiento y consultas de grafos

## Requisitos del Sistema

### Software Necesario

- Python 3.8 o superior
- Node.js 16 o superior
- Neo4j Database (versión 4.0+)
- npm o yarn para gestión de paquetes

### Dependencias Python

```
flask
flask-cors
neo4j
python-dotenv
bcrypt
uuid
```

### Dependencias Node.js

```
react
react-dom
tailwindcss
lucide-react
```

## Instalación y Configuración

### 1. Configuración de la Base de Datos Neo4j

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables para manetener seguros los datos:

```env
NEO4J_URI=neo4j+ssc://ffa5f2ba.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=K-xGvEhiLdkV-Jzgq6Y7Pg4VhLWQqsSOt-q1CgoBZY8
```

Para Neo4j Aura, usa la URI proporcionada en tu panel de control.

### 2. Configuración del Backend

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd movie-recommendation-system/src

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install flask flask-cors neo4j python-dotenv bcrypt
```

### 3. Configuración del Frontend

```bash
# Navegar al directorio del frontend
cd movie-frontend

# Instalar dependencias
npm install

# Verificar instalación
npm ls react lucide-react tailwindcss
```

## Ejecutar el Proyecto

### 1. Iniciar el Backend

```bash
# Desde la raíz del proyecto, con el entorno virtual activado
python main.py
```

El servidor Flask se ejecutará en `http://localhost:5001`

### 2. Iniciar el Frontend

```bash
# En una nueva terminal, navegar al directorio frontend
cd movie-frontend

# Iniciar el servidor de desarrollo
npm start
```

La aplicación React se ejecutará en `http://localhost:3000`

### 3. Verificar la Conexión

1. Abre tu navegador en `http://localhost:3000`
2. Deberías ver la pantalla de login/registro
3. Crea una cuenta nueva o inicia sesión
4. Verifica que puedas ver la lista de películas

## Uso de la Aplicación

### Registro e Inicio de Sesión

1. Accede a la aplicación en tu navegador
2. Haz clic en "Crear cuenta nueva" si es tu primera vez
3. Completa el formulario con email, contraseña y nombre
4. Una vez registrado, podrás iniciar sesión

### Explorar Películas

1. En la pestaña "Explorar", verás una lista de películas disponibles
2. Usa la barra de búsqueda para encontrar películas específicas
3. Haz clic en "Me gusta" o "No me gusta" en las películas que conozcas

### Ver Recomendaciones

1. Ve a la pestaña "Recomendadas"
2. Después de marcar algunas preferencias, verás películas recomendadas
3. Las recomendaciones se actualizan automáticamente con cada interacción

## API Endpoints

### Autenticación
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión

### Películas
- `GET /movies` - Listar películas
- `GET /movies/{id}` - Obtener película específica
- `GET /movies/search?q={query}` - Buscar películas

### Interacciones
- `POST /interact` - Registrar like/dislike
- `GET /users/{id}/interactions` - Ver interacciones del usuario

### Recomendaciones
- `GET /recommendations/{user_id}` - Obtener recomendaciones personalizadas

## Resolución de Problemas

### Error de Conexión a Neo4j

```bash
# Verificar que Neo4j esté ejecutándose
# Verificar las credenciales en .env
```

### Frontend no se conecta al Backend

```bash
# Verificar que Flask esté ejecutándose en puerto 5001
# Verificar configuración de CORS en app.py
# Confirmar API_BASE_URL en App.js
```

### No aparecen recomendaciones

1. Asegúrate de haber marcado al menos 3-5 películas como "me gusta"
2. Verifica que haya datos en la base de datos Neo4j
3. Revisa los logs del backend para errores

### Error al instalar dependencias

```bash
# Para Python, actualizar pip:
python -m pip install --upgrade pip

# Para Node.js, limpiar cache:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Tecnologías Utilizadas

- **Backend**: Flask, Neo4j Python Driver, bcrypt
- **Frontend**: React, Tailwind CSS, Lucide React
- **Base de Datos**: Neo4j
- **Autenticación**: Hash de contraseñas con bcrypt
- **Estilo**: Principios de Clean Code