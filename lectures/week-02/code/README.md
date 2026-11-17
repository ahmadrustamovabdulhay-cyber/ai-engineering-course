# Library setup and homework starter

- [library.sql](library.sql) creates `books`, `members`, and `loans`, then adds the classroom rows.
- [main.py](main.py) supplies the FastAPI app, session dependency, and a working `GET /books`. The `Loan` mapping and `/loans` route are the homework.
- [requirements.txt](requirements.txt) lists the Python dependencies.

## Live sessions in postgres.new

Open [postgres.new](https://postgres.new/) and start a fresh database. In Session 03, run the statements in the lesson as you reach them. For a clean starting point in Session 04, run the seed script in a fresh database. The seed script expects empty tables to be created from scratch. After loading it, `SELECT id, title FROM books ORDER BY id;` should list three books.

## Homework database

Use an empty hosted PostgreSQL database for your assignment. You can use the instructor’s teaching database if you’ve been given access. Run `library.sql` once in that database using the provider’s SQL editor, or ask the instructor whether the shared data is already loaded. Use the application connection string provided for that database.

Copy `main.py` and `requirements.txt` to your assignment folder. Run the commands below from that folder. Use a PostgreSQL URL beginning with `postgresql+psycopg://` to select the Psycopg driver in SQLAlchemy. If the provider gives you a URL beginning with `postgresql://` or `postgres://`, change that prefix and keep the credentials, host, database name, and any options supplied by your provider. Set the real value in your shell and keep it out of Git.

### Windows / PowerShell

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DATABASE_URL = 'postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require'
.venv/bin/python -m uvicorn main:app --reload
```

Open [the local API docs](http://127.0.0.1:8000/docs) and run `GET /books`. The starter should return books `1`, `2`, and `3`. Then follow [Homework 04](../assignment04.md) to complete `GET /loans`.
