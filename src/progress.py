import json
from pathlib import Path
from typing import Any


SAVE_PATH = Path("caminhos_brasil_save.json")


class ProgressStore:
    def __init__(self, level_count: int):
        self.level_count = level_count

    def load(self) -> dict[str, Any]:
        try:
            with SAVE_PATH.open("r", encoding="utf-8") as save_file:
                data = json.load(save_file)
        except (OSError, json.JSONDecodeError):
            return self._empty_progress()

        highest = data.get("highest_unlocked_level", 0)
        entries = data.get("collection_entries", [])
        completed_levels = data.get("completed_levels", [])
        if not isinstance(highest, int):
            highest = 0
        if not isinstance(entries, list):
            entries = []
        if not isinstance(completed_levels, list):
            completed_levels = []

        clean_entries = []
        seen = set()
        for entry in entries:
            if not isinstance(entry, list) or len(entry) != 2:
                continue
            level_title, info = entry
            if not isinstance(level_title, str) or not isinstance(info, str):
                continue
            key = (level_title, info)
            if key in seen:
                continue
            seen.add(key)
            clean_entries.append((level_title, info))

        return {
            "highest_unlocked_level": max(0, min(highest, self.level_count - 1)),
            "collection_entries": clean_entries,
            "completed_levels": {
                level
                for level in completed_levels
                if isinstance(level, int) and 0 <= level < self.level_count
            },
        }

    def save(
        self,
        highest_unlocked_level: int,
        collection_entries: list[tuple[str, str]],
        completed_levels: set[int],
    ):
        data = {
            "highest_unlocked_level": max(
                0,
                min(highest_unlocked_level, self.level_count - 1),
            ),
            "completed_levels": sorted(completed_levels),
            "collection_entries": [
                [level_title, info] for level_title, info in collection_entries
            ],
        }

        try:
            with SAVE_PATH.open("w", encoding="utf-8") as save_file:
                json.dump(data, save_file, ensure_ascii=False, indent=2)
        except OSError:
            return

    def _empty_progress(self) -> dict[str, Any]:
        return {
            "highest_unlocked_level": 0,
            "collection_entries": [],
            "completed_levels": set(),
        }
