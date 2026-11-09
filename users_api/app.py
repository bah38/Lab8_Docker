from contextlib import closing
import os
from pathlib import Path
import sqlite3

from flask import Flask, jsonify

app = Flask(__name__)
DATABASE = Path(os.environ.get("DATABASE_PATH", str(Path(__file__).parent / "database.db")))


def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE)) as connection, connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
        )


@app.get("/get_users")
def get_users():
    with closing(sqlite3.connect(DATABASE)) as connection, connection:
        names = [row[0] for row in connection.execute("SELECT name FROM users ORDER BY user_id")]
    return jsonify(names)


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
