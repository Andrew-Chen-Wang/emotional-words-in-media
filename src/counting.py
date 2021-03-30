import json
import re
from typing import TYPE_CHECKING

from . import BASE_DIR

DATA_DIR = BASE_DIR / "data"
if TYPE_CHECKING:
    from pathlib import Path


def count(file: "Path"):
    if not file.exists():
        return
    data = json.loads(file.read_text())
    saving = {"titles": [], "counter": {}}

    def save(_d: list):
        for x in _d:
            try:
                saving["titles"].append(x["title"])
            except Exception:
                continue
            words = [word.lower() for word in re.findall(r"\w+", x["title"])]
            for w in words:
                saving["counter"].setdefault(w, 0)
                saving["counter"][w] += 1

    for _p in data["entries"]:
        # I don't want to reconstruct the list
        if type(_p) == list:
            save(_p["entries"])
        for x in _p["entries"]:
            ...

    # Save in JSON
    with file.with_suffix(".json").open("w") as f:
        json.dump(saving, f)


def count_all():
    if (mainstream_yt := (DATA_DIR / "youtube")).is_dir():
        [count(file) for file in mainstream_yt.iterdir() if file.is_file()]
    else:
        print(f"YouTube folder in {BASE_DIR / 'data'} does not exist.")
