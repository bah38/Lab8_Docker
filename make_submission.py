from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).parent
archive = ROOT / "Lab8_Batoul_Hachem_Submission.zip"
folders = ["hello_world", "lab5_api", "users_api"]
files = ["Lab8_Batoul_Hachem.docx", "Lab8_Batoul_Hachem.pdf", "README.md", "compose.yaml", "prepare_database.py", "demo_users.py", "verify_apps.py", "verify_containers.py", "make_report.py", "make_submission.py", "capture-screen.ps1", "collect-evidence.ps1", "capture-api.ps1", "desktop-ui.ps1"]
evidence = ["01-docker-ps", "02-docker-stop", "03-docker-logs", "04-stopped-container", "05-images", "06-docker-desktop-images", "06a-image-5000", "06b-image-3000", "07-api-results"]
paths = [ROOT / filename for filename in files]
for folder in folders:
    paths.extend(path for path in (ROOT / folder).iterdir() if path.is_file())
for name in evidence:
    paths.extend(path for path in (ROOT / "evidence").glob(name + ".*") if path.is_file())
paths.append(ROOT / "evidence" / "container-verification.txt")
with ZipFile(archive, "w", ZIP_DEFLATED) as output:
    for path in paths:
        output.write(path, path.relative_to(ROOT))
with ZipFile(archive) as output:
    assert output.testzip() is None
    print(f"Created {archive.name}: {len(output.namelist())} files, {archive.stat().st_size:,} bytes")
