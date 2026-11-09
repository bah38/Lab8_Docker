"""Check response contracts and prove /get_users reads the database."""
from contextlib import closing
import importlib.util
import os
from pathlib import Path
import sqlite3
import tempfile

ROOT = Path(__file__).parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hello = load("hello_app", ROOT / "hello_world" / "app.py")
response = hello.app.test_client().get("/")
assert response.status_code == 200 and response.data == b"Hello, World!\n"

with tempfile.TemporaryDirectory() as directory:
    os.environ["DATABASE_PATH"] = str(Path(directory) / "users.db")
    users = load("users_app", ROOT / "users_api" / "app.py")
    client = users.app.test_client()
    assert client.get("/get_users").get_json() == []
    with closing(sqlite3.connect(users.DATABASE)) as connection, connection:
        connection.executemany("INSERT INTO users (name) VALUES (?)", [("Batoul Hachem",), ("Test User",)])
    result = client.get("/get_users")
    assert result.status_code == 200
    assert result.get_json() == ["Batoul Hachem", "Test User"]
    with closing(sqlite3.connect(users.DATABASE)) as connection, connection:
        connection.execute("UPDATE users SET name = ? WHERE user_id = ?", ("Updated User", 2))
    assert client.get("/get_users").get_json() == ["Batoul Hachem", "Updated User"]
    assert client.post("/get_users").status_code == 405
    del os.environ["DATABASE_PATH"]

print("PASS: hello response, empty database, all names, updated database, GET-only endpoint")
