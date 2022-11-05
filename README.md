## Documentation

Useful commands to install and run the project. First install Docker.
```
$ docker-compose -f docker-compose.yaml build
$ docker-compose -f docker-compose.yaml up
$ docker-compose -f docker-compose.yaml migrate
```

Run tests.
```
$ docker-compose -f docker-compose.yaml run --rm web python manage.py test
```
