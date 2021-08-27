# iCargo BACKEND

Proyecto backend para iCargo desarrollado con [FastAPI](https://fastapi.tiangolo.com/)

## EJECUTAR LOCALMENTE

#### Pre-requisitos

- Python 3.7
- Pip 3
- Instalar las dependencias especificadas en [requirements.txt]:
```
pip install -r requirements.txt
```
- Asegurarse de que las variables de la base de datos en [app/db/\_\_init__.py] estén apuntando a los datos locales

### Ejecutar

```
uvicorn main:app --reload
```
- El backend estará disponible en `http://localhost:8000`

## EJECUTAR CON DOCKER
- Asegurarse de que las variables de la base de datos en [app/db/\_\_init__.py] estén apuntando a los datos del docker
- Ejecutar
```
docker-compose up --build
```
- El backend estará disponible en `http://localhost:8091`

## SWAGGER
- FastAPI trae integrado un swagger para probar los servicios, disponible en `http://localhost:8000/docs`

## MIGRACIONES
- Las migraciones a la base de datos se realizan con [Alembic](https://alembic.sqlalchemy.org/en/latest/). Para correr las migraciones asegurarse de que los datos de configuración de la base de datos en [app/alembic.ini] sean correctas, y ejecutar:
```
alembic upgrade head
```
- Este comando ejecuta las revisiones definidas en [app/migrations/versions]




