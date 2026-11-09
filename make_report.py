from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).parent
EVIDENCE = ROOT / "evidence"
doc = Document()
section = doc.sections[0]
section.top_margin = section.bottom_margin = Inches(0.65)
section.left_margin = section.right_margin = Inches(0.7)
doc.core_properties.author = "Batoul Hachem"
doc.core_properties.title = "Lab 8 - Docker, Containers and Images"
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(7)
doc.add_heading("Lab 8 — Docker, Containers and Images", 0)
doc.add_paragraph("Batoul Hachem | AUB username: bah38")
doc.add_paragraph("Software Tools Laboratory | 9 November 2026")
doc.add_heading("Introduction", 1)
doc.add_paragraph("A Docker image is a packaged application containing its code, runtime, libraries and configuration. A container is an instance of an image. The Dockerfile defines how to build the image. This lab builds a Flask hello-world image, runs the original Lab 5 API on port 5000, and adds a database-backed names API on port 3000.")
doc.add_paragraph("Lab 5 source: https://github.com/bah38/Lab5_Postman_API (commit 85237839a037ce790bfec7f9f2ff5c1b525e1e5b). The repository database initially contains no users. The original files were preserved; working copies were used for containerization.")


def code(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)


def snapshot(name, caption):
    path = EVIDENCE / name
    if path.exists():
        doc.add_picture(str(path), width=Inches(6.8))
        p = doc.add_paragraph(caption)
        p.runs[0].italic = True
    else:
        doc.add_paragraph("Screenshot not yet captured: " + caption)


doc.add_heading("Introductory Flask container", 1)
doc.add_paragraph("The app returns Hello, World! at GET /. Flask listens on 0.0.0.0:5000 so it accepts Docker-forwarded traffic. The Dockerfile copies requirements.txt, installs Flask, copies app.py and runs python app.py. Python 3.12 Alpine is used as a maintained replacement for the handout's Python 3.8 example. A focused requirements file avoids copying unrelated local packages into the image.")
code("docker build -t flask_docker ./hello_world\ndocker run --name lab8-bah38-hello -p 127.0.0.1:5000:5000 -d flask_docker\ncurl.exe http://localhost:5000/")
doc.add_heading("Activity 1 — Commands and explanations", 1)
doc.add_paragraph("The handout's <image_name> placeholders for stop and logs refer to a container name or ID. The container used below is named lab8-bah38-hello; its image is flask_docker.")
for title, command, explanation, filename, caption in [
    ("1. List containers", "docker ps -a --filter name=lab8-bah38", "Lists running and stopped containers, including their IDs, images, commands, status, port mappings and names. The -a flag includes containers that are no longer running. The name filter limits this screenshot to the Lab 8 containers.", "01-docker-ps.png", "Figure 1. docker ps -a with a name filter showing only Lab 8 containers."),
    ("2. Stop the Flask container", "docker stop lab8-bah38-hello", "Requests a graceful shutdown of the running container. Docker prints its name when it stops. The container remains available and can be restarted; stopping it does not delete its image or filesystem.", "02-docker-stop.png", "Figure 2. Actual output of docker stop."),
    ("3. View the container logs", "docker logs lab8-bah38-hello", "Displays the container's captured standard output and standard error. Flask startup and HTTP request messages appear here. Logs can still be read after the container has stopped.", "03-docker-logs.png", "Figure 3. Actual Flask container logs after stopping.")
]:
    doc.add_heading(title, 2)
    code(command)
    doc.add_paragraph(explanation)
    snapshot(filename, caption)
doc.add_heading("Confirm stopped state", 2)
doc.add_paragraph("In this run, Exited (137) indicates that Docker forcefully terminated the development server after its stop grace period. The container is still retained and its logs remain readable.")
code("docker ps -a --filter name=lab8-bah38-hello")
snapshot("04-stopped-container.png", "Figure 4. The hello-world container remains listed with an Exited status.")

doc.add_heading("Activity 2 — Two application images", 1)
table = doc.add_table(rows=1, cols=3)
table.style = "Light Shading Accent 1"
for cell, value in zip(table.rows[0].cells, ["Image", "Port", "Application"]):
    cell.text = value
for values in [
    ("bah38/lab8-batoul_hachem:0.0.1.RELEASE", "5000", "Original Lab 5 Postman/API application"),
    ("bah38/lab8-batoul_hachem:0.0.2.RELEASE", "3000", "GET /get_users returns every user's name")
]:
    for cell, value in zip(table.add_row().cells, values):
        cell.text = value
doc.add_paragraph("The handout's embedded Docker Desktop screenshot uses tags 0.0.1.RELEASE and 0.0.2.RELEASE. These valid tags are used here because the textual 0.0.1:RELEASE and 0.0.2:RELEASE forms contain an extra colon. Repository names use lowercase letters.")
doc.add_heading("Image 1: Lab 5 API on port 5000", 2)
doc.add_paragraph("The original Lab 5 application and database are copied into lab5_api/. The application retains its existing GET, POST, PUT and DELETE routes. Its only application-code change is app.run(host=\"0.0.0.0\", port=5000, debug=False), allowing requests through the published container port. Flask and Flask-CORS are installed from requirements.txt.")
code("docker build -t bah38/lab8-batoul_hachem:0.0.1.RELEASE ./lab5_api\npython prepare_database.py\ndocker compose up -d --build")
doc.add_paragraph("The introductory container is stopped before running this container because both use host port 5000.")
doc.add_heading("Image 2: Names API on port 3000", 2)
doc.add_paragraph("GET /get_users executes SELECT name FROM users ORDER BY user_id against a copy of the Lab 5 SQLite database and returns a JSON list of names. The result comes from the database on each request. An empty database returns []. SQLite connections are closed after use. For this demonstration, Docker Compose mounts the same runtime/database.db file into both containers. Users added through POST /api/users/add on port 5000 therefore appear immediately in GET /get_users on port 3000. The three sample users are Batoul Hachem, Maya Haddad and Omar Khalil; their contact fields are demonstration data. The original bundled databases remain unchanged.")
code("docker build -t bah38/lab8-batoul_hachem:0.0.2.RELEASE ./users_api\npython demo_users.py\ncurl.exe http://localhost:3000/get_users")
snapshot("06-docker-desktop-images.png", "Figure 5. Docker Desktop Images view showing both required image tags.")
snapshot("06a-image-5000.png", "Figure 6. Docker Desktop image details for the port-5000 application.")
snapshot("06b-image-3000.png", "Figure 7. Docker Desktop image details for the port-3000 application.")
snapshot("07-api-results.png", "Figure 8. Three users added through POST on port 5000 and their names retrieved on port 3000.")
doc.add_heading("Verification", 1)
doc.add_paragraph("Application checks cover the hello-world response, an empty users database, multiple user names, an updated record and rejection of POST to /get_users. Container verification performs the original Lab 5 create/read/update/delete workflow and checks that creating and updating a temporary user through port 5000 changes the names returned on port 3000. That temporary verification user is removed afterward; the three demonstration users remain in the shared runtime database; the bundled database files remain unchanged.")
verification = EVIDENCE / "container-verification.txt"
if verification.exists():
    code(verification.read_text(encoding="utf-8"))
else:
    doc.add_paragraph("Container verification has not yet been completed.")
doc.add_heading("References", 1)
for reference in [
    "Original Lab 5 repository: https://github.com/bah38/Lab5_Postman_API",
    "Docker stop: https://docs.docker.com/reference/cli/docker/container/stop/",
    "Docker image references: https://docs.docker.com/reference/cli/docker/image/tag/",
    "Flask quickstart: https://flask.palletsprojects.com/en/stable/quickstart/"
]:
    doc.add_paragraph(reference)
doc.save(ROOT / "Lab8_Batoul_Hachem.docx")
print("Created Lab8_Batoul_Hachem.docx")
