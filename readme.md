# FT_CONTROL_VEHICULAR  
Dessarrollo de la api en django para el Control Vehicular

# Primeros pasos

Primero clonar el repositorio desde Github y cambia al nuevo directorio:

    $ git clone git@github.com/USERNAME/{{ project_name }}.git
    $ cd {{ project_name }}
    
Active el virtualenv para su proyecto.
    
La version de python usada en el proyecto:

    $ python 3.8.10 o python 3.9.19
    
Instalar las dependencias del proyecto:

    $ pip install -r requirements.txt
    
Ejecutar el siguiente comando si hay migraciones pendientes en el proyecto:

    $ python manage.py makemigrations
        
Aplicar las migraciones del proyecto:

    $ python manage.py migrate
    
Aplicar el siguiente comando para ejecutar el proyecto:

    $ python manage.py runserver

Aplicar el siguiente comando en caso agregar o cambiar dependencias del proyecto:

    $ pip freeze > requirements.txt