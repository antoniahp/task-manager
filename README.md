# ⚙️ Instalación del proyecto


### Como arrancar el proyecto
```bash
docker-compose up --build
```
### Como crear super usuario
```bash
docker-compose exec web python app/manage.py createsuperuser
```
### Como crear migraciones del proyecto
```bash
docker-compose exec web python app/manage.py makemigrations
```
### Como aplicar migraciones del proyecto
```bash
docker-compose exec web python app/manage.py migrate
```

### Como acceder a la documentación de la API [Swagger]
Una vez arrancado el proyecto, accede a la documentación de la API en la siguente [URL](http://localhost:8000/api/docs).

![Captura de pantalla 2024-10-06 a las 22 06 22](https://github.com/user-attachments/assets/90032ff5-2d74-4c16-8289-10a276ecac5e)

Recuerda obtener un token de acceso para utilizar los endpoints autenticados
![Captura de pantalla 2024-10-06 a las 22 08 44](https://github.com/user-attachments/assets/a736e13f-c664-4c99-94e4-20c634c497f8)


# 📚 Modelos de la base de datos
![diagram-db](https://github.com/user-attachments/assets/a9c4c991-42fd-43de-ade8-3d99fc6b8768)

# 🔄 Cosas a mejorar
- Algunos endpoints tienen filtros que no tienen por que utilizarse por los posibles clientes del back-end.
- Hay que añadir mas checks para que un usuario no cree datos en compañias que no le pertenezca.
- Cuando se crea una empresa, el usuario deberia de añadirse a esa empresa. Actualmente esa operación se hace manualmente desde el Django admin.
- Añadir tests de integración y test unitarios.

