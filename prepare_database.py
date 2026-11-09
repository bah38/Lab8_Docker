"""Create the shared runtime database without changing the original Lab 5 copy."""
from pathlib import Path
import shutil

root = Path(__file__).parent
database = root / "runtime" / "database.db"
database.parent.mkdir(exist_ok=True)
if not database.exists():
    shutil.copy2(root / "lab5_api" / "database.db", database)
    print("Created shared runtime/database.db from the original Lab 5 database.")
else:
    print("Keeping existing shared runtime/database.db.")
