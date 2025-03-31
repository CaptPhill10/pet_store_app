Pet Store API Mock Server with tests
-----

This project is a FastAPI-based mock server for a pet store, used for testing API interactions.
It includes a test suite with pytest and httpx.

Parallel tests execution implemented using pytest-xdist
---


---
How to use
-----

To clone and run this application, 
you'll need Python 3.9 or 3.10 version and Git installed on your computer. 
From your command line/Python IDE Terminal:

Clone this repository
```
$ git clone https://github.com/CaptPhill10/pet_store_app.git
```

Go into the repository
```
$ cd pet_store_app
```

Install virtual environment pipenv. Use your user
```
$ pip install --user pipenv   # To install pipenv

or

$ python -m venv venv   # To use venv
```

Check that pipenv installed (if pipenv was chosen as virtual env)
```
$ pipenv --version
```

Activate virtual environment
```
$ pipenv shell   # To activate pipenv

or to activate venv use

$ source venv/bin/activate   # MacOS/Linux
$ venv\Scripts\activate      # Windows
```

Install dependencies. Please, use specified versions
```
$ pip install -r requirements.txt
```