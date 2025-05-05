import json
from pathlib import Path


def export_json(url, content):
    filename = f"output/{url.split('/')[-1]}.json"

    output_dir = Path("output")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    with open(filename, "w") as f:
        json.dump(content, f, ensure_ascii=False)
