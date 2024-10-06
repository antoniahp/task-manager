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

# 📚 Modelos de la base de datos

# 🔄 Cosas a mejorar
- Algunos endpoints tienen filtros que no tienen por que utilizarse por los posibles clientes del back-end.
- Hay que añadir mas checks para que un usuario no cree datos en compañias que no le pertenezca.
- Cuando se crea una empresa, el usuario deberia de añadirse a esa empresa. Actualmente esa operación se hace manualmente desde el Django admin.
- Añadir tests de integración y test unitarios.

