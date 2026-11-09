"""Verify the actual container endpoints; clean up only this script's test data."""
import json
from pathlib import Path
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
names_url = "http://localhost:3000/get_users"
initial_names = request("GET", names_url)
assert initial_names == [user["name"] for user in sorted(original, key=lambda user: user["user_id"])]
created_id = None
try:
    user = {"name": "Lab8 Test User", "email": "lab8-test@example.invalid", "phone": "00000000", "address": "Test address", "country": "Lebanon"}
    created = request("POST", base + "/add", user)
    assert created["name"] == user["name"]
    created_id = created["user_id"]
    assert request("GET", names_url) == initial_names + [user["name"]]
    assert request("GET", base + f"/{created_id}")["name"] == user["name"]
    user.update(user_id=created_id, name="Lab8 Updated User")
    assert request("PUT", base + "/update", user)["name"] == "Lab8 Updated User"
    assert request("GET", names_url) == initial_names + ["Lab8 Updated User"]
finally:
    if created_id is not None:
        result = request("DELETE", base + f"/delete/{created_id}")
        assert result["status"] == "User deleted successfully"
assert request("GET", base) == original

assert request("GET", names_url) == initial_names
lines.append("PASS: Lab 5 CRUD and shared database names on port 3000; temporary test user removed.")
output = "\n".join(lines) + "\n"
print(output)
(EVIDENCE / "container-verification.txt").write_text(output, encoding="utf-8")
