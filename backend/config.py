import json
import os

from .constants import CONFIG_FILE, SETTINGS_FILE

DEFAULT_CATEGORIES = ["Work"]
DEFAULT_SETTINGS = {"daily_goal": 240}


def load_categories():
    """Loads categories from config.json, falling back to a safe default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                cats = data.get("categories", DEFAULT_CATEGORIES)
                return cats if cats else DEFAULT_CATEGORIES
        except (json.JSONDecodeError, OSError):
            return DEFAULT_CATEGORIES
    return DEFAULT_CATEGORIES


def save_categories(categories):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"categories": categories}, f, indent=2)


def load_settings():
    """Loads persisted app settings (currently just the daily goal)."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except (json.JSONDecodeError, OSError):
            return dict(DEFAULT_SETTINGS)
    return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
