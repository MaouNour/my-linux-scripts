#!/usr/bin/env python3
import sqlite3
import os
from pathlib import Path

DB_PATH = Path.home() / ".local/share/music_index.db"
MUSIC_FOLDER = Path.home() / "Music"

SUPPORTED_EXTS = {
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
    ".wav",
    ".opus",
    ".mp4",
    ".mkv",
    ".webm",
    ".avi",
    ".mov",
    ".flv",
}


def get_files_from_disk():
    all_files = []
    for root, _, files in os.walk(MUSIC_FOLDER):
        for f in files:
            if Path(f).suffix.lower() in SUPPORTED_EXTS:
                full_path = str(Path(root) / f)
                all_files.append(full_path)
    return set(all_files)


def get_files_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT path FROM tracks")
    db_files = {row[0] for row in c.fetchall()}
    conn.close()
    return db_files


disk_files = get_files_from_disk()
db_files = get_files_from_db()

missing_in_db = sorted(disk_files - db_files)
missing_on_disk = sorted(db_files - disk_files)

print(f"🎧 Total on disk: {len(disk_files)}")
print(f"🎵 Total in DB: {len(db_files)}")
print(f"❌ Missing in DB: {len(missing_in_db)}")
print(f"⚠️ Orphaned in DB (no longer on disk): {len(missing_on_disk)}")

if missing_in_db:
    print("\n--- Missing in DB ---")
    for f in missing_in_db[:20]:
        print(f"  {f}")
    if len(missing_in_db) > 20:
        print(f"  ...and {len(missing_in_db) - 20} more")

if missing_on_disk:
    print("\n--- Orphaned in DB ---")
    for f in missing_on_disk[:20]:
        print(f"  {f}")
    if len(missing_on_disk) > 20:
        print(f"  ...and {len(missing_on_disk) - 20} more")
