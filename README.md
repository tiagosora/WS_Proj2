# Web Semântica - Proj 2

Later in the instruction, you have the possibility of running using a bash file.

## Installing the requirements

To first be able to run the app you must install the requirements:

1. Create a virtual environment, by running one of the following commands:

    ```bash
    python<version> -m venv <virtual-environment-name>
    # (preferably)
    python -m venv venv
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
    # or, for windows
    ./venv/scripts/activate
    ```

3. Install the requirement modules:

    ```bash
    pip install -r requirements.txt
    ```

4. Go to the webproj directory:

    ```
    cd webproj
    ```

5. Run the following commands:

    ```bash
    python manage.py tailwind install
    
    python manage.py migrate
    ```

## How to run the app

To run the application follow these steps:

1. Have GraphDB running. Import the dataset `data/completed_data.rdf` and the ontology `data/ontology.owl` imported in a repository named `ws_project`, with ruleset OWL2-RL (Optimized).

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

Note: This step is not necessary, and simply serves as informative. These files are already created.

To convert the data from the original CSV files from the original dataset, simply run the following commands:

```bash
cd data/

python data_converter.py
```

# Alternative Run

1. Create a .env file inside the root folder with the following configuration:

    ```.env
    REPO_URL=http://graphdb:7200/repositories/ws_project
    REPO_URL_UPDATE=http://graphdb:7200/repositories/ws_project/statements
    ```

2. Run the following bash file:

    ```sh
    ./start_docker_compose
    ```

    **OR**

    ```sh
    chmod -x ./start_docker_compose.sh && ./start_docker_compose.sh
    ```

3. **Just in case** docker doens't have the required permissions:

    ```sh
    sudo chmod -R 755 path/to/.docker/buildx
    ```

    **On MacOS**

    ```sh
    sudo chmod -R 755 /Users/{user}/.docker/buildx
    ```