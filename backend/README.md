## Available Scripts

In the project directory, you can run:

### `source venv/Scripts/activate`

Runs the Fast API server with uvicorn.\

### `uvicorn main:app --reload`

> The command uvicorn main:app refers to:
>
> main: the file main.py (the Python "module").
> app: the object created inside of main.py with the line app = FastAPI().
> --reload: make the server restart after code changes. Only use for development.

Open [http://localhost:8000](http://localhost:8000) to view the root in your browser, or use the router path to get another result.\

See the documentation on [http://localhost:8000/docs](http://localhost:8000/docs) or different style documentation at [http://localhost:8000/redoc](http://localhost:8000/redoc).
