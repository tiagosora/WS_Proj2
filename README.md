# Web Semântica - Proj 2

## Installing the requirements

To first be able to run the app you must install the requirements:

1. Create a virtual environment, by running one of the following commands:

    ```bash
    python<version> -m venv <virtual-environment-name>
    # (preferably)
    python -v venv venv
    ```

    or (alternatively):
    ```bash
    virtualenv <virtual-environment-name>
    # (preferably)
    virtualenv venv
    ```

2. Enter the virtual environment, running this command:

    ```bash
    source venv/bin/activate
    # or
    ./venv/scripts/activate
    ```

3. Install the requirement modules:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the following commands:

    ```bash
    python manage.py tailwind install
    
    python manage.py migrate
    ```

## How to run the app

To run the application follow these steps:

1. Have GraphDB running and the dataset `data/data_.rdf` imported in a repository named `ws_repository`.

2. Create a .env file inside the root folder with the following configuration:

    ```.env
    REPO_URL=http://127.0.0.1:7200/repositories/ws_project
    REPO_URL_UPDATE=http://127.0.0.1:7200/repositories/ws_project/statements
    ```

3. In two separated terminals, run the following commands (one in each terminal):

    ```bash
    python manage.py runserver
    ```

    ```bash
    python manage.py tailwind start
    ```

4. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

5. Register or login with one of the following accounts:

    |Permission|Id Number|Password|
    |---|---|---|
    |Student|104142|Pass.Muito.Forte123|
    |Professor|103234|Pass.Muito.Forte123|
    |Headmaster|103453|Pass.Muito.Forte123|

## Converting the data

To convert the data from the original CSV files from the original dataset, simply run the following commands:

```bash
cd data/

python data_converter.py
```
