# Proyecto 1 Etapa 2 - Inteligencia de Negocios

Objetivos del proyecto:

- Automatizar un proceso replicable para aplicar la metodología de analítica de textos en
  la construcción de modelos analíticos
- Desarrollar una aplicación que utiliza un modelo analítico basado en aprendizaje
  automático y es de interés para un rol dentro de una organización.

## Instalación Aplicación

Para poder ejecutar el API del proyecto tendremos que descargar las dependencias requeridas, para esto utilice el comando:

`pip install -r requirements.txt`

## Despliegue Aplicación

Una vez descargadas las dependecias del proyecto, tenemos que ejecutar el servidor. Para esto realizaremos una serie de pasos, primero tendremos que ubicarnos en la carpeta donde se encuentra la aplicación la cual es "meditrials", en esta carpeta ejecutar la terminal y ejecutar los siguientes comandos:

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

Luego de estos comandos la aplicación se encontrará corriendo en la dirección: http://127.0.0.1:8000/

## Funcionamiento Aplicación

Una vez estemos en la aplicación, su uso es bastante intuitivo. Para introducir un diagnostico, este tiene que seguir cierta estructura la cual es, por ejemplo:

`study interventions are Stem cell transplantation . hodgkin lymphoma diagnosis and history of congenital hematologic immunologic or metabolic disorder which in the estimation of the pi poses prohibitive risk to the recipient`
