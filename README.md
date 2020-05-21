# Introduction

The purpose of this API is to interact with a database storing actors and movies. Functionality can be added to the API in future to link actors and movies together.

# Installation

## Getting Started

### Installing Dependancies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle interactions with the database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# Testing

Unittest can be run with the following command:

```bash
python test_app.py
```

The API is accessible at the following URL:

```bash
https://udacity-heroku-project.herokuapp.com/
```

The site is hosted on Heroku and is automatically deployed from Github following a successful update. Github Actions are used to run tests before it can be deployed to Heroku.

# User Authenitcation

All user authentication is handled through [Auth0](https://www.auth0.com). Examples of the role tokens can be found in setup.sh in the project directory. The key roles are:

- Casting Assistant: Can view and edit actors.
- Casting Director: Can view, add, delete or edit actors and can view or edit movies.
- Executive Producer: Can view, add, delete or edit movies and actors.

# API Documentation

For your convenience, the following methods are available to interact with the database:

## Actors

### GET /actors/

Returns a list of all actors in JSON format from the database.

```
{
  "actors": [
    {
      "age": "21",
      "gender": "Male",
      "id": 1,
      "name": "Bart Barrowman"
    },
    {
      "age": "23",
      "gender": "Female",
      "id": 2,
      "name": "Jerry Jones"
    }
  ],
  "success": true
}
```

### POST /actors/

Creates a new actor based on request data.

#### Request

```
{
  "name": "Bob Potts",
  "age": "21",
  "gender": "Male"
}
```

#### Response

Returns success or error and the actor created.

```
{
  "actor": {
    "age": "21",
    "gender": "Male",
    "id": 5,
    "name": "Bob Potts"
  },
  "success": true
}
```

### PATCH /actors/id

Updates an actor with data passed in the request.

#### Request

```
{
  "name": "Bob Potter",
  "age": "22",
  "gender": "Female"
}
```

#### Response

Returns success or error and updated details for the actor.

```
{
  "actor": {
    "age": "22",
    "gender": "Female",
    "id": 5,
    "name": "Bob Potter"
  },
  "success": true
}
```

### DELETE /actors/id

Deletes the actor identified by ID.

#### Response

Returns success or error and ID of deleted actor.

```
{
  "deleted_id": 5,
  "success": true
}
```

## Movies

### GET /movies/

Returns a list of all movies in JSON format from the database.

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Tue, 12 May 2020 00:00:00 GMT",
      "title": "Never Say Boo"
    },
    {
      "id": 2,
      "release_date": "Mon, 11 May 2020 00:00:00 GMT",
      "title": "Never Say Die"
    }
  ],
  "success": true
}
```

### POST /movies/

Creates a new movie based on request data.

#### Request

```
{
  "title": "Away on the Farm",
  "release_date": "2020-05-01"
}
```

#### Response

Returns success or error and the actor created.

```
{
  "movie": {
    "id": 6,
    "release_date": "Fri, 01 May 2020 00:00:00 GMT",
    "title": "Away on the Farm"
  },
  "success": true
}
```

### PATCH /actors/id

Updates an actor with data passed in the request.

#### Request

```
{
  "title": "Away in a Farm",
  "release_date": "2020-06-01"
}
```

#### Response

Returns success or error and updated details for the movie.

```
{
  "movie": {
    "id": 6,
    "release_date": "Mon, 01 Jun 2020 00:00:00 GMT",
    "title": "Away in a Farm"
  },
  "success": true
}
```

### DELETE /movies/id

Deletes the movie identified by ID.

#### Response

Returns success or error and ID of deleted movie.

```
{
  "deleted_id": 6,
  "success": true
}
```

# Error Codes

When incorrect data is provided or insufficient privilages are granted, the following error codes will be returned:

- 400: Bad request: Check you are providing the right information.
- 401: Unauthorised: You have not provided credentials.
- 403: Forbidden: You do not have sufficient permission.
- 404: Not found: Check the required resource exists.
- Auth: Authenication error: Specific error, see response text.