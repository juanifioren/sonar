# Sonar Technical Challenge

![Screenshot 2022-11-07 at 00 22 52](https://user-images.githubusercontent.com/5168681/200219973-9c2b3c93-3767-4d01-88f8-f1092471c4da.png)

## Stack

- Python 3.
- Django 4.
- TailwindCSS, HTML5 and CSS3.
- JQuery.
- Docker and Docker compose.

## Documentation

Useful commands to install and run the project. First install Docker.
```
$ docker-compose -f docker-compose.yaml build
$ docker-compose -f docker-compose.yaml up
$ docker-compose -f docker-compose.yaml run --rm web python manage.py migrate
$ docker-compose -f docker-compose.yaml run --rm web python manage.py createfakedata
```

Run tests.
```
$ docker-compose -f docker-compose.yaml run --rm web python manage.py test
```

## Things for v2

Here I am going to leave a list of things that I was thinking to improve in a future version:

- Add pytest suite to create some tests and maybe use factory-boy to generate data (for testing and for the initial data command).
- Use translate tag on templates and generate translation files (also ensure is used on views).
- Maybe cache views count.
- Improve post view count logic, maybe using some cache system to stop hitting db to check if was viewed already.
- Improve dashboard data with caching system.
- Generate better data for Activity Logs when using manage command.

_Created by Juan Ignacio Fiorentino._
