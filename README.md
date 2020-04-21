# Package Status Control

## Server documentation

The server has two main endpoints: one for package status control and one for statistics.

### Status control

The server allows package addition with it's associated status, check a package's last status and update said status.

#### Package addition

Packages can be added by sending an HTTP as follows:

```http request
POST /packages
{
  "id": "package_id",
  "inputs": [
    {
      "status": "string",
      "substatus": "nullable string"
    }
  ]
}
```

The server's response for said request will be as follows:

```http request
{"pacakge": "status message"}
```

Where `package` will be the message associated to the package's last known status.

#### Last known status

It is possible to get a package's last known status by doing the following HTTP request:

```http request
GET /packages/<package_id>
```

In this case, the server's answer will be the same as before.

#### Package status update

It is possible to update a package's status (always going forward in the path to delivery) by doing an HTTP request
with the following characteristics:

```http request
PATCH /packages
{
  "id": "package_id",
  "inputs": [
    {
      "status": "string",
      "substatus": "nullable string"
    }
  ]
}
```
The answer, again, will be as in the first scenario.

**Note:** Probably, the most logical solution here would be to send the package ID as a path parameter, leaving the
body just for the input list. Anyway, to avoid two different mappings in this simple solution, the request schema
is the same as in the `POST` request.

**Delivery tracking:** This endpoint allows to update a package's status as it progresses in it's way to be delivered.

### Statistics

It's possible to query some general information about the registered information in the server by doing the following
HTTP request:

```http request
GET /packages/statistics
```

In this case, the answer will be as follows:

```
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
Where `packages_count` indicates the number of packages currently stored in the database and the rest of the fields in
the response refer to each category.

**Note:** In this implementation, the server queries the database every time a request is received in this endpoint. A
way to ease the burden on the connection between the server and the database would be to calculate these statistics
periodically, with a relatively small period, and return directly a value stored in memory. Although there would be
eventual inconsistencies, in those cases where the amount of data in the database is larger, a lot of time would be
saved on each request and a heavy load on the link between server and database would be avoided.

**Note 2:** Even though the server stores only the last known status of each package, it would be an option to store
every known status, in the order they were received, to have also statistics of events lost in the way of the delivery
process. Moreover, these stored object could have timestamps which could be used to calculate some statistics about
time taken between status changes.

### Health Check

The server has exposed the endpoint `/health/health-check`, created with the sole purpose of health control. The 
response is always an HTTP status OK (200).

## Local Execution

### Docker

To start the server locally with `Docker` and `docker-compose`, it's necessary to have both of these things installed.
You can get them from:

* [Docker - Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Docker - Mac](https://docs.docker.com/docker-for-mac/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

Once all this is installed, it's simply needed to execute `docker-compose up --build` in the project's root folder. 
Background execution needs the addition of one docker parameter, resulting in `docker-compose up --build -d`. In this
second scenario, run `docker-compose down` to stop it.

When running the server with Docker, the container will create a volume where it will host the MongoDB server and will
start the server in question as a Docker service.

### Makefile

It's also possible to start the server by executing:

* `make prepare`
* `make run`

To do this, it's necessary to:

* Have `python 3.8` installed in your system.
* Have `mongo`  installed in your system, running on port 27017.

### Testing

#### Test Execution

To execute the tests, run the following commands:

* `make prepare`
* `make test`

To do this, it's neecessary to:
Se debe tener en cuenta que es necesario:

* Have `python 3.8` installed in your system.
* Have `mongo` installed in your system, running on port 27017. This is necessary for integration tests due to the lack
of an `::inmemory` option for MongoDB in Python.

#### Coverage

Similar to the previous case, once prepared the environment, execute command `make coverage`

## Online Server

The server is running on a [Heroku](https://www.heroku.com/) instance. The base URL for it is 
`https://package-status.herokuapp.com`. Being it hosted with a free tier account, it's possible for the first request
to take some time as it "awakes" the instance; after this, the response speed goes back to normal. I believe the
inactivity time to sleep for a Heroku instance is about 30 minutes.

## Geolocation

A possible way of implementing geolocation for a package would be to add the endpoint `/packages/<package_id>/location`,
which would receive a body as follows:

```
{
  "lat": -34.547244,
  "lon": -58.489286
}
```

Requests could be made periodically to this endpoint in order to register the movement of a package and store either:

* It's last position, to save storage space.
* All registered positions, to be able to create a path if it was necessary and to be able to analyze all possible
lost or disordered requests.

## Server scalability

One of the parameters the server can receive is `--proc`; this parameter lets the user indicate how many processes will
the server have, being `0` equal to as many processes as cores the machine processor has. This, in addition to 
`Tornado`'s usage of Python's coroutines to handle as many simultaneous requests, allows the server to easily answer a 
great number of requests.

Because of the problem's characteristics, it's possible to add multiple independent instances connected to the same
database to increase the availability of the service. This would be easy as the database connection parameters are
loaded when the server starts.

Regarding the request concurrence, this solution didn't take into account the case where more than one update request
for the same package is received. In this case, a race condition could take place where the database ends up with an
invalid status for a package (only the last received request will have stored it's update). To avoid this (and make
the server scalable), a distributed lock server could be set up to avoid clashes between requests that try to update
the same package. One example of such server is [etcd](https://etcd.io/).