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

## Build and run

Start Docker Desktop with Linux containers, then run from this folder:

```powershell
docker build -t flask_docker ./hello_world
docker run --name lab8-bah38-hello -p 127.0.0.1:5000:5000 -d flask_docker
curl.exe http://localhost:5000/

docker build -t bah38/lab8-batoul_hachem:0.0.2.RELEASE ./users_api
docker run --name lab8-bah38-api3000 -p 127.0.0.1:3000:3000 -d bah38/lab8-batoul_hachem:0.0.2.RELEASE
curl.exe http://localhost:3000/get_users
```

Expected initial responses: `Hello, World!` and `[]`.
If these container names already exist, use `docker start <container-name>` to restart them rather than running another container with the same name.

## Activity 1

```powershell
docker ps -a
docker stop lab8-bah38-hello
docker logs lab8-bah38-hello
docker ps -a --filter name=lab8-bah38-hello
```

`docker ps -a` lists running and stopped containers. `docker stop` gracefully stops a running container without removing it. `docker logs` shows the container's captured standard output and standard error, including Flask startup and request messages. Logs remain available after stopping the container.

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

The supplied `lab5_repo+screenshots (2).pdf` was checked against the containerized Lab 5 code. Its repository link, five API routes, response fields, empty initial list, and deletion message match. No application changes were needed. The comparison is documented in the Word report and `evidence/lab5-pdf-comparison.md`.

- Docker container stop: https://docs.docker.com/reference/cli/docker/container/stop/
- Docker image references: https://docs.docker.com/reference/cli/docker/image/tag/
- Flask quickstart: https://flask.palletsprojects.com/en/stable/quickstart/

## Activity 2: original Lab 5 image

Stop the introductory container to free host port 5000, then run:

```powershell
docker stop lab8-bah38-hello
docker build -t bah38/lab8-batoul_hachem:0.0.1.RELEASE ./lab5_api
docker run --name lab8-bah38-api5000 -p 127.0.0.1:5000:5000 -d bah38/lab8-batoul_hachem:0.0.1.RELEASE
curl.exe http://localhost:5000/api/users
```

The original Lab 5 routes support GET /api/users, GET /api/users/<user_id>, POST /api/users/add, PUT /api/users/update, and DELETE /api/users/delete/<user_id>.
The two images use independent copies of the original empty database; they do not share live changes. Container database edits survive stop/start, but removing the container loses those edits unless you use a volume or bind mount. Original repository and Downloads files were not modified.

`verify_containers.py` exercises Lab 5 CRUD and verifies names retrieval against temporary database records. All test records are removed afterward. `Lab8_Batoul_Hachem.docx` contains the report and actual screenshots. `Lab8_Batoul_Hachem_Submission.zip` packages code, report, and evidence for Moodle.

The image tags 0.0.1.RELEASE and 0.0.2.RELEASE follow the handout's embedded Docker Desktop screenshot. The applications use Flask's development server for this local lab, with debug mode disabled. Nothing has been pushed to Docker Hub or submitted to Moodle.
