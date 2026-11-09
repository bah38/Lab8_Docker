# Lab 8 - Batoul Hachem (bah38)

## Submission files and screenshots

The screenshots are in [`evidence/`](evidence/). They are also embedded in the [Word report](Lab8_Batoul_Hachem.docx). A [PDF copy](Lab8_Batoul_Hachem.pdf) is available for viewing.

| Screenshot | Description |
| --- | --- |
| [01-docker-ps.png](evidence/01-docker-ps.png) | `docker ps -a` |
| [02-docker-stop.png](evidence/02-docker-stop.png) | Stop the hello-world container |
| [03-docker-logs.png](evidence/03-docker-logs.png) | Container logs |
| [04-stopped-container.png](evidence/04-stopped-container.png) | Confirm the stopped container |
| [05-images.png](evidence/05-images.png) | Docker image list in the terminal |
| [06-docker-desktop-images.png](evidence/06-docker-desktop-images.png) | Both required images in Docker Desktop |
| [06a-image-5000.png](evidence/06a-image-5000.png) | Port-5000 image details |
| [06b-image-3000.png](evidence/06b-image-3000.png) | Port-3000 image details |
| [07-api-results.png](evidence/07-api-results.png) | Live API responses and verification |

For Moodle, upload `Lab8_Batoul_Hachem.docx` and `Lab8_Batoul_Hachem_Submission.zip` as requested by the handout. Generate the ZIP locally with `python make_submission.py`; it includes the code, report, and screenshots. The ZIP, local virtual environment, and reference downloads are excluded from Git.

## Completion status

- `hello_world/`: introductory Flask application on port 5000, used for Activity 1.
- `users_api/`: Activity 2 GET `/get_users` application on port 3000. Reads every user's name from a copy of the repository SQLite database, ordered by user_id, and returns a JSON list. The original database has no users, so its initial result is [].
- `lab5_api/`: original Lab 5 code/database from https://github.com/bah38/Lab5_Postman_API, commit 85237839a037ce790bfec7f9f2ff5c1b525e1e5b. The only application change is binding Flask to 0.0.0.0:5000 with debugging disabled.

## Build and run both graded APIs

Start Docker Desktop with Linux containers, then run from this folder:

```powershell
python prepare_database.py
docker compose up -d --build
python demo_users.py
curl.exe http://localhost:3000/get_users
```

Both containers mount the same `runtime/database.db` at `/app/database.db`. POST requests to port 5000 therefore appear in GET `/get_users` on port 3000. `prepare_database.py` copies the original Lab 5 database only when the runtime file is missing. It never replaces existing runtime data.

`demo_users.py` adds three sample users through POST on port 5000: Batoul Hachem, Maya Haddad, and Omar Khalil. Contact fields are demonstration data. It avoids duplicate sample emails, checks the names on port 3000, and leaves these records available for grading. Expected names: `["Batoul Hachem", "Maya Haddad", "Omar Khalil"]`.

Images: `bah38/lab8-batoul_hachem:0.0.1.RELEASE` (port 5000) and `bah38/lab8-batoul_hachem:0.0.2.RELEASE` (port 3000). The tags follow the handout's Docker Desktop example.

```powershell
docker compose stop
docker compose start
```

The shared runtime database persists on the host even if the containers are removed. It is excluded from Git; the original database copies inside the image build folders remain unchanged.

## Activity 1

```powershell
docker ps -a --filter name=lab8-bah38
docker stop lab8-bah38-hello
docker logs lab8-bah38-hello
docker ps -a --filter name=lab8-bah38-hello
```

`docker ps -a` lists running and stopped containers; `--filter name=lab8-bah38` limits the screenshot to this lab. `docker stop` gracefully stops a running container without removing it. `docker logs` shows the container's captured standard output and standard error, including Flask startup and request messages. Logs remain available after stopping the container.

The handout's `<image_name>` placeholders for stop/logs should be container names or IDs. Its textual tags `0.0.1:RELEASE` / `0.0.2:RELEASE` contain an extra colon; use the valid tags `0.0.1.RELEASE` / `0.0.2.RELEASE` shown in its embedded Docker Desktop screenshot. Repository names use lowercase letters.

## Using an existing SQLite database

The users API expects a `users` table with `user_id` and `name` columns. Adapt the SQL if the Lab 5 schema differs. To use a matching database instead of the bundled database, mount its folder and set `DATABASE_PATH`:

```powershell
docker run --name lab8-bah38-users-existing -p 127.0.0.1:3000:3000 --mount "type=bind,source=C:\path\to\database-folder,target=/data" -e DATABASE_PATH=/data/users.db bah38/lab8-batoul_hachem:0.0.2.RELEASE
```

## Verification and report generation

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r hello_world/requirements.txt python-docx
.\.venv\Scripts\python.exe verify_apps.py
.\.venv\Scripts\python.exe verify_containers.py
.\.venv\Scripts\python.exe make_report.py
```

`verify_apps.py` checks the greeting, empty database, multiple names, an updated database record, and rejection of POST. Docker evidence is stored in `evidence/`; genuine screen captures are collected with `collect-evidence.ps1`. Flask's development server is used to match this local lab exercise; debug mode is disabled.

## References

- Docker container stop: https://docs.docker.com/reference/cli/docker/container/stop/
- Docker image references: https://docs.docker.com/reference/cli/docker/image/tag/
- Flask quickstart: https://flask.palletsprojects.com/en/stable/quickstart/

## Activity 2: Lab 5 API

The original Lab 5 routes support GET `/api/users`, GET `/api/users/<user_id>`, POST `/api/users/add`, PUT `/api/users/update`, and DELETE `/api/users/delete/<user_id>` on port 5000. The added port-3000 endpoint returns names from the shared database on every request.

`verify_containers.py` creates a temporary user through POST on port 5000, checks its name on port 3000, updates it through PUT, checks the changed name, and deletes it. The three demonstration users remain after verification. See `evidence/container-verification.txt` for results.

For the introductory hello-world exercise, stop the port-5000 API first to free its port:

```powershell
docker compose stop lab5-api
docker build -t flask_docker ./hello_world
docker run --name lab8-bah38-hello -p 127.0.0.1:5000:5000 -d flask_docker
curl.exe http://localhost:5000/
docker stop lab8-bah38-hello
docker compose start lab5-api
```

If the hello-world container already exists, use `docker start lab8-bah38-hello` instead of `docker run`. Flask uses its development server for this local lab, with debug mode disabled.
