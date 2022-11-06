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

## Things for v2

Here I am going to leave a list of things that I was thinking to improve in a future version:

- Add pytest suite for testing and maybe use factory-boy to generate data (for testing and for the initial data command).
