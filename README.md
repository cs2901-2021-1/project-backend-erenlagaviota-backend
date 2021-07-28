# Ingeniería de Software
## Nombre del Grupo: Eren la gaviota

## Integrantes ✒️

* **Mario Jacobo Rios Gamboa** - [morphisjustfun - mario.rios@utec.edu.pe]
* **Luis Alfonso Berrospi Rodriguez** - [lender512 - luis.berrospi@utec.edu.pe]
* **Juan Pablo Miguel Lozada Velasco** - [IWeseI - juan.lozada@utec.edu.pe]
##Backend:

### Tecnologias utilizadas:

Spring Boot
Maven

Python 
Flask
NGINX
Gunicorn
AWS EC2
Supervisor service (Linux)

##Base de datos

Postgresql
Heroku

### Metodo de proyeccion:
Para calcular el número de alumnos que se podrían matricular en un curso, hemos definido un modelo matemático basado en regresión lineal. 

Obtuvimos el modelo de regresión lineal al definir ciertas variables que podrían afectar el número de matriculados, como el promedio de notas, el número de personas que pasaron, el promedio de veces que se lleva el curso, etc. Después, analizamos qué tanto se relacionaban las variables con el número de matriculados. Finalmente escogimos el conjunto de variables que tenían la mayor relación con el número de matriculados.

En base a las variables escogidas; nota promedio, promedio de veces que se lleva el curso y número de personas que llevaron el curso anteriormente, creamos un modelo de regresión lineal. Cada vez que se calcula una proyección, se le proporciona toda la data necesaria al modelo.

### Google Oauth:
Para poder autenticar a los usuarios que utilicen la aplicación, utilizamos Google OAuth, el cual es un servicio de autenticación que proporciona google, donde utiliza el email del usuario para verificar su identidad. 

Una vez tenemos las credenciales del usuario, decidimos utilizar una base de datos aparte, donde podemos indicar los correos electrónicos que pueden acceder al servicio de proyección. Además, también indicamos el tipo de rol que tiene un usuario específico, para personalizar las vistas de manera apropiada.

Con Google OAuth podemos verificar quien es el usuario y con la base de datos podemos decidir si el usuario debería poder acceder al servicio.

### Cache:

Dentro de nuestro data-endpoint escrito en python, cada vez que un usuario solicita la proyección de un curso en específico, la data de la proyección se puede obtener de dos formas. Podemos utilizar el modelo definido para calcular la data de la proyección, o podemos obtener la data directamente de la caché. 

Cada vez que se solicite la proyección de un curso en específico por primera vez, este será calculado utilizando el modelo definido. Además la data de la proyección será almacenada en la caché, de manera que si la misma solicitud de proyección se realiza por el cliente esta será directamente obtenida de la caché.

