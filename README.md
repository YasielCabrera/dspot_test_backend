This is the backend project for the fullstack test @ DSpot

## Getting Started

In order to run the development server for first time you must:

- Create a virtual environment (it is optional but highly recommended for python apps). You can follow my [tutorial](https://github.com/YasielCabrera/cabyas.com/blob/master/src/pages/virtualenv-python/index.md#activate-the-env-in-posix-platforms)

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Create the database (A Sqlite DB for simplicity)

```bash
python manage.py migrate
```

- Fill the DB with fake data randomly generated (optional)

```bash
# Note that <count> is the number of how many profiles do you want to create
python manage.py fill_db <count>
```

- Run the project

```bash
python manage.py runserver
```

Open [http://localhost:8000/api/v1/swagger](http://localhost:8000/api/v1/swagger) with your browser to see the result.

## Django Admin

The [Django admin](http://localhost:8000/admin/) module was enabled to allow an easy way to mutate the data.

Create an user to sign in:

```bash
python manage.py createsuperuser
```

Thanks for the opportunity 😊
