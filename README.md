# Package Status Control

## Documentación del servidor

El servidor tiene dos endpoints principales: el de control de estados de paquetes y
el de estadísticas.

### Control de estados

El servidor permite añadir paquetes y sus estados, ver su último estado y 
actualizar el mismo.

#### Añadido de paquetes

Los paquetes se añaden realizando un HTTP request del estilo:

```http request
POST /packages
{
  "id": String,
  "inputs": [
    {
      "status": String,
      "substatus": Optional[String]
    }
  ]
}
```

La respuesta a dicho request será del estilo:

```http request
{"pacakge": String}
```

Donde `package` será el mensaje asociado al último estado conocido del paquete.

#### Consulta de último estado conocido

Es posible ver el último estado conocido de un paquete haciendo un request HTTP con
la forma:

```http request
GET /packages/<package_id>
```

La respuesta a este request será igual al caso anterior.

#### Actualización de estado de un paquete

Es posible actualizar el estado de un paquete (siempre avanzando en el camino a
su entrega) realizando un request HTTP con la forma:

```http request
PATCH /packages
{
  "id": String,
  "inputs": [
    {
      "status": String,
      "substatus": Optional[String]
    }
  ]
}
```

La respuesta, nuevamente, será igual al primer caso.

**Nota:** Tal vez lo más lógico acá sería que el package id fuera un path param
y el body sólo trajera los inputs; pero para evitar definir dos mapeos distintos,
en este caso se optó por usar la misma modalidad que en el `POST`.

**Seguimiento de un envío:** Este endpoint permite actualizar el estado de un
paquete a medida que el mismo va progresando en su envío.

### Estadísticas

Se podrá consultar información general sobre los paquetes registrados en el 
servidor realizando el siguiente request HTTP:

```http request
GET /packages/statistics
```

En este caso, la respuesta será de la forma:

```http request
{
  "packages_count": 1,
  "count_by_category": {
    "Delivered": 1,
    "Handling": 0,
    "Lost": 0,
    "Manufacturing": 0,
    "Printed": 0,
    "ReadyToPrint": 0,
    "Shipped": 0,
    "SoonDeliver": 0,
    "Stolen": 0,
    "WaitingForWithdrawal": 0
  }
}
```

Donde el número indica la cantidad de paquetes que actualmente se encuentran en la
base de datos para cada una de las categorías (y en total).

**Nota:** Si bien el servidor almacena sólo el último estado conocido de cada paquete,
se podrían almacenar todos los estados, en el orden en que se recibieron, para
poder obtener también estadísticas sobre eventos no recibidos. Extendiendo esto, 
se podría también añadir timestamps al registro de cada evento, para determinar
tiempos entre los cambios de estado.

### Health Check

El servidor también tiene expuesto el endpoint `/health/health-check`, que permite
realizar un control sobre la salud del mismo. La respuesta es simplemente un 
HTTP status OK.

## Ejecución local

### Docker

Para levantar el server localmente con `Docker` y `docker-compose`, es necesario 
tener instaladas ambas cosas. Las cuales se pueden obtener en:

* [Docker - Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Docker - Mac](https://docs.docker.com/docker-for-mac/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

Con esto instalado, simplemente se debe ejecutar el comando 
`docker-compose up --build` en el root del proyecto. Si se quisiera correr en 
background, ejecutar `docker-compose up --build -d`. Para apagarlo en este segundo
escenario, ejecutar `docker-compose down`.

En este caso, el contenedor Docker tendrá un volumen donde alojará la base de datos
MongoDB e iniciará el servidor como un servicio.

### Makefile

Es posible iniciar el servidor ejecutando los comandos:

* `make prepare`
* `make run`

Para esto, es necesario:

* Tener instalado `python 3.8` en el sistema.
* Tener instalado `mongo` en el sistema, corriendo en el puerto 27017.

### Testing

#### Ejecución de tests

Para correr los tests, se deben ejecutar los comandos:

* `make prepare`
* `make test`

Se debe tener en cuenta que es necesario:

* Tener instalado `python 3.8` en el sistema.
* Tener instalado `mongo` en el sistema, corriendo en el puerto 27017. Esto es
necesario para ejecutar algunos tests de integración, ya que no existe un simil
`::inmemory` para mongo.

#### Coverage
Similar al caso anterior, una vez preparado el entorno, se debe ejecutar el comando
`make coverage`.

## Online Server

El servidor está corriendo en una instancia de [Heroku](https://www.heroku.com/).
La url base de la misma es https://package-status.herokuapp.com. Por ser el free
tier, es probable que el primer request que se realice despues de un tiempo
"despierte" al servidor, por lo cual tarde un tiempo relativamente largo; luego,
la velocidad vuelve a la normalidad (el timeout para "dormir" el server es de unos
30 minutos).

## Geolocalización

Una posible forma de implementar la geolocalización de un paquete sería añadir
un endpoint `/packages/<package_id>/location` con un body del estilo:

```http request
{
  "lat": -34.547244,
  "lon": -58.489286
}
```

Se podrían hacer requests periódicos al mismo para registrar el movimiento del
paquete y almacenar o:

* La última posición, para ahorrar espacio de almacenamiento
* Todas las posiciones registradas, para poder crear un camino si fuera necesario
y para poder analizar posibles requests perdidos o que lleguen en orden indeseado.