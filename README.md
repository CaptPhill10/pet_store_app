Pet Store API Mock Server with tests
-----

This project is a FastAPI-based mock server for a pet store, used for testing API interactions.
It covers API requests used
It includes a test suite with pytest and httpx.

	•	api/ - Contains the API routes and app inicialisation.
	•	data/ - Contains pets, store and users data for tests.
	•	tests/ - Contains tests for API requests.
	•	util/ - Utility functions and configurations for logging.
    •	conftest.py - Contains functions and configuration to start
                      FastAPI Server automatically on tests start and finish on test end.

---
API Endpoints
-----
You can find examples and detailed explanations of the API endpoints here: [Swagger Pet Store API](https://petstore.swagger.io/#/).

---
How to use
-----

To clone and run this application,
you'll need Python 3.11 or 3.12 version and Git installed on your computer.
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

---
Tests execution
-----
To run all tests
```
pytest tests/
```
To run all tests related to Pets requests
```
pytest tests/pet_test.py
```
To run all tests related to Store requests
```
pytest tests/store_test.py
```
To run all tests related to User requests
```
pytest tests/user_test.py
```
To run e2e tests related to the whole flow from add pet to sell it
```
pytest tests/various_e2e_test.py
```

Parallel tests execution implemented using pytest-xdist
---
```
pytest tests/ -n 4 -vs
```

---
Logging
-----
The project includes logging for error handling. Exceptions and other info are logged in the pet_store.log file.
