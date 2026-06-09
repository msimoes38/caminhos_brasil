import json
from pathlib import Path
from typing import Any


SAVE_PATH = Path("caminhos_brasil_save.json")
WEB_SAVE_KEY = "caminhos_brasil_save_v1"


class ProgressStore:
    def __init__(self, level_count: int):
        self.level_count = level_count

    def load(self) -> dict[str, Any]:
        web_progress = self._load_from_web()
        if web_progress is not None:
            return web_progress

        return self._load_from_file()

    def save(
        self,
        highest_unlocked_level: int,
        collection_entries: list[tuple[str, str]],
        completed_levels: set[int],
    ):
        data = self._progress_payload(
            highest_unlocked_level,
            collection_entries,
            completed_levels,
        )

        if self._save_to_web(data):
            return

        self._save_to_file(data)

    def _load_from_web(self) -> dict[str, Any] | None:
        window = self._get_browser_window()
        if window is None:
            return None

        raw_data, helper_available = self._read_from_web_helper(window)
        if not helper_available:
            storage = self._get_web_storage(window)
            if storage is None:
                return None

            try:
                raw_data = storage.getItem(WEB_SAVE_KEY)
            except Exception:
                return None

        if not raw_data:
            return self._empty_progress()

        try:
            data = json.loads(str(raw_data))
        except (TypeError, json.JSONDecodeError):
            return self._empty_progress()

        return self._normalize_progress(data)

    def _save_to_web(self, data: dict[str, Any]) -> bool:
        window = self._get_browser_window()
        if window is None:
            return False

        raw_data = json.dumps(data, ensure_ascii=False)
        helper_saved, helper_available = self._write_to_web_helper(window, raw_data)
        if helper_available:
            return helper_saved

        storage = self._get_web_storage(window)
        if storage is None:
            return False

        try:
            storage.setItem(WEB_SAVE_KEY, raw_data)
        except Exception:
            return False

        return True

    def _load_from_file(self) -> dict[str, Any]:
        try:
            with SAVE_PATH.open("r", encoding="utf-8") as save_file:
                data = json.load(save_file)
        except (OSError, json.JSONDecodeError):
            return self._empty_progress()

        return self._normalize_progress(data)

    def _save_to_file(self, data: dict[str, Any]):
        try:
            with SAVE_PATH.open("w", encoding="utf-8") as save_file:
                json.dump(data, save_file, ensure_ascii=False, indent=2)
        except OSError:
            return

    def _get_browser_window(self):
        try:
            import platform

            return getattr(platform, "window", None)
        except Exception:
            return None

    def _get_web_storage(self, window):
        try:
            return getattr(window, "localStorage", None) if window else None
        except Exception:
            return None

    def _read_from_web_helper(self, window) -> tuple[Any, bool]:
        try:
            helper = getattr(window, "caminhosReadSave", None)
        except Exception:
            return None, False

        if helper is None:
            return None, False

        try:
            return helper(), True
        except Exception:
            return None, False

    def _write_to_web_helper(self, window, raw_data: str) -> tuple[bool, bool]:
        try:
            helper = getattr(window, "caminhosWriteSave", None)
        except Exception:
            return False, False

        if helper is None:
            return False, False

        try:
            result = helper(raw_data)
        except Exception:
            return False, False

        return self._truthy_web_result(result), True

    def _truthy_web_result(self, result) -> bool:
        if isinstance(result, bool):
            return result
        return str(result).strip().lower() in ("true", "1", "yes")

    def _progress_payload(
        self,
        highest_unlocked_level: int,
        collection_entries: list[tuple[str, str]],
        completed_levels: set[int],
    ) -> dict[str, Any]:
        return {
            "highest_unlocked_level": max(
                0,
                min(highest_unlocked_level, self.level_count - 1),
            ),
            "completed_levels": sorted(completed_levels),
            "collection_entries": [
                [level_title, info] for level_title, info in collection_entries
            ],
        }

    def _normalize_progress(self, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
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

    def _empty_progress(self) -> dict[str, Any]:
        return {
            "highest_unlocked_level": 0,
            "collection_entries": [],
            "completed_levels": set(),
        }
