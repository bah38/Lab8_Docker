"""Verify the actual container endpoints; clean up only this script's test data."""
import json
from pathlib import Path
import subprocess
from urllib.request import Request, urlopen

EVIDENCE = Path(__file__).parent / "evidence"
EVIDENCE.mkdir(exist_ok=True)
lines = []


def request(method, url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=15) as response:
        result = json.load(response)
        lines.append(f"{method} {url} -> {response.status}: {json.dumps(result)}")
        return result


base = "http://localhost:5000/api/users"
original = request("GET", base)
created_id = None
try:
    user = {"name": "Lab8 Test User", "email": "lab8-test@example.invalid", "phone": "00000000", "address": "Test address", "country": "Lebanon"}
    created = request("POST", base + "/add", user)
    assert created["name"] == user["name"]
    created_id = created["user_id"]
    assert request("GET", base + f"/{created_id}")["name"] == user["name"]
    user.update(user_id=created_id, name="Lab8 Updated User")
    assert request("PUT", base + "/update", user)["name"] == "Lab8 Updated User"
finally:
    if created_id is not None:
        result = request("DELETE", base + f"/delete/{created_id}")
        assert result["status"] == "User deleted successfully"
assert request("GET", base) == original


def sql(code):
    result = subprocess.run(["docker", "exec", "-i", "lab8-bah38-api3000", "python", "-"], input=code, text=True, capture_output=True, check=True)
    return result.stdout.strip()


names_url = "http://localhost:3000/get_users"
initial_names = request("GET", names_url)
test_id = None
try:
    test_id = int(sql("""import sqlite3
with sqlite3.connect('/app/database.db') as c:
 cur=c.execute('INSERT INTO users (name,email,phone,address,country) VALUES (?,?,?,?,?)',('Lab8 Test User','lab8-test@example.invalid','00000000','Test address','Lebanon'))
 print(cur.lastrowid)
"""))
    assert request("GET", names_url) == initial_names + ["Lab8 Test User"]
    sql(f"""import sqlite3
with sqlite3.connect('/app/database.db') as c:
 c.execute('UPDATE users SET name=? WHERE user_id=?',('Lab8 Updated User',{test_id}))
""")
    assert request("GET", names_url) == initial_names + ["Lab8 Updated User"]
finally:
    if test_id is not None:
        sql(f"""import sqlite3
with sqlite3.connect('/app/database.db') as c:
 c.execute('DELETE FROM users WHERE user_id=?',({test_id},))
""")
assert request("GET", names_url) == initial_names
lines.append("PASS: Lab 5 CRUD and port-3000 database-backed names; all test records removed.")
output = "\n".join(lines) + "\n"
print(output)
(EVIDENCE / "container-verification.txt").write_text(output, encoding="utf-8")
