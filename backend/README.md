## Available Scripts

First install virtual environment

```cmd
pip install virtualenv
```

create virtual environment

```cmd
virtualenv venv
```

run virtual environment:

if using gitbash

```cmd
source venv/Scripts/activate
```

if using windows powershell

change ExecutionPolicy

```cmd
Set-ExecutionPolicy Unrestricted -scope process
```

then to activate do

```cmd
.\venv\Scrips\activate
```

Install the required lib

```cmd
pip install -r requirements.txt
```

Runs the Fast API server with uvicorn.\

```cmd
uvicorn main:app
```

Open [http://localhost:8000](http://localhost:8000) to view the root in your browser, or use the router path to get another result.\

See the documentation on [http://localhost:8000/docs](http://localhost:8000/docs) or different style documentation at [http://localhost:8000/redoc](http://localhost:8000/redoc).
