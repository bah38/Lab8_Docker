"""Add three sample users through the port-5000 API, then check port 3000."""
import json
from urllib.request import Request, urlopen

BASE = "http://localhost:5000/api/users"


def request(method, url, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = Request(url, data=body, method=method, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=15) as response:
        return response.status, json.load(response)


_, users = request("GET", BASE)
for number, name in enumerate(["Batoul Hachem", "Maya Haddad", "Omar Khalil"], 1):
    email = f"lab8-demo-{number}@example.invalid"
    existing = next((user for user in users if user["email"] == email), None)
    if existing:
        print(f"Sample user already present: {existing['name']}")
        continue
    status, user = request("POST", BASE + "/add", {
        "name": name, "email": email, "phone": "00000000",
        "address": "Sample address", "country": "Lebanon",
    })
    assert user.get("name") == name
    print(f"POST :5000/api/users/add -> {status}: {user['name']} (user_id={user['user_id']})")
_, all_users = request("GET", BASE)
status, names = request("GET", "http://localhost:3000/get_users")
assert names == [user["name"] for user in sorted(all_users, key=lambda user: user["user_id"])]
print(f"GET :3000/get_users -> {status}: {json.dumps(names)}")
print("PASS: users created through POST on port 5000 are visible on port 3000.")
