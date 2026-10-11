import sys
import os
import json

def get_base_dir() -> str:
    """Trả về thư mục gốc chứa file .exe hoặc script main.py."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CONFIG_FILE = os.path.join(get_base_dir(), "config.json")
DEFAULT_DOWNLOAD_DIR = os.path.join(get_base_dir(), "downloads")

def load_download_path() -> str:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                path = data.get("download_path", "")
                if path:
                    return os.path.abspath(path)
        except Exception:
            pass

    save_download_path(DEFAULT_DOWNLOAD_DIR)
    return DEFAULT_DOWNLOAD_DIR

def save_download_path(path: str) -> None:
    try:
        data = {"download_path": os.path.abspath(path)}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu config: {e}")