import csv
import hashlib
from pathlib import Path
import sys

# Tkinter for cross-platform folder dialog
try:
  import tkinter as tk
  from tkinter import filedialog

  HAS_TKINTER = True
except ImportError:
  HAS_TKINTER = False

# Supported audio formats in iTunes / Apple Music
AUDIO_EXTENSIONS = {
    ".mp3",
    ".m4a",
    ".m4p",
    ".m4b",
    ".aac",
    ".flac",
    ".alac",
    ".wav",
    ".aiff",
}


def choose_folder(title="Select folder"):
  """Opens a cross-platform folder selection dialog (Windows & Mac)."""
  if HAS_TKINTER:
    try:
      root = tk.Tk()
      root.withdraw()  # Hides the main window
      root.attributes("-topmost", True)
      folder_selected = filedialog.askdirectory(title=title)
      root.destroy()
      if folder_selected:
        return Path(folder_selected).resolve()
    except Exception:
      pass

  # Fallback for console / if GUI is not available
  print("Folder dialog could not be opened.")
  path_input = input(
      f"Please enter the path for '{title}' manually: "
  ).strip('"\'')
  p = Path(path_input).resolve()
  if not p.is_dir():
    print(f"Invalid folder path: {p}")
    sys.exit(1)
  return p


def calculate_md5(file_path, block_size=65536):
  """Calculates the MD5 hash of a file (in memory-efficient blocks)."""
  hasher = hashlib.md5()
  try:
    with open(file_path, "rb") as f:
      for buf in iter(lambda: f.read(block_size), b""):
        hasher.update(buf)
    return hasher.hexdigest()
  except Exception as e:
    print(f"Error hashing {file_path}: {e}")
    return None


def scan_library(root_dir, compute_hashes=True):
  """Scans a library and returns a dictionary:

  Key: "artist / album" (lowercase)
  Value: Set of tuples (filename, file_size, md5_hash)
  """
  root = Path(root_dir)
  albums = {}

  if not root.exists():
    print(f"Path does not exist: {root}")
    return albums

  print(f"Scanning directory: {root} ...")
  files_found = list(root.rglob("*"))
  audio_files = [
      p for p in files_found if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
  ]

  total = len(audio_files)
  for idx, path in enumerate(audio_files, 1):
    try:
      rel_path = path.relative_to(root)
      parts = rel_path.parts

      # Expects standard structure: Artist/Album/File.ext
      if len(parts) >= 3:
        artist = parts[0].strip().lower()
        album = parts[1].strip().lower()
        album_key = f"{artist} / {album}"
      else:
        album_key = "various / single tracks"

      if album_key not in albums:
        albums[album_key] = []

      file_name = path.name.lower()
      file_size = path.stat().st_size
      file_hash = (
          calculate_md5(path) if compute_hashes else "hash_disabled"
      )

      albums[album_key].append((file_name, file_size, file_hash))

      if idx % 50 == 0 or idx == total:
        print(f"  Progress: {idx}/{total} audio files processed...", end="\r")

    except Exception as e:
      print(f"\nError at file {path}: {e}")

  print()
  return {k: set(v) for k, v in albums.items()}


def compare_libraries(lib_a_path, lib_b_path, output_csv="itunes_library_comparison_report.csv"):
  print("--- Starting analysis of Library A (Target / Master) ---")
  lib_a = scan_library(lib_a_path)

  print("\n--- Starting analysis of Library B (Source to clean up) ---")
  lib_b = scan_library(lib_b_path)

  report_rows = []

  all_albums = set(lib_a.keys()).union(set(lib_b.keys()))

  for album_key in sorted(all_albums):
    in_a = album_key in lib_a
    in_b = album_key in lib_b

    if in_a and in_b:
      files_a = lib_a[album_key]
      files_b = lib_b[album_key]

      if files_b == files_a:
        status = "Exact Match"
        recommendation = "Can be deleted from B (Duplicate)"
      else:
        status = "Partial Overlap"
        recommendation = "Manual check required (different tracks/hashes)"
    elif in_a and not in_b:
      status = "Only in Library A"
      recommendation = "Remains in A"
    else:  # not in_a and in_b
      status = "Only in Library B"
      recommendation = "Candidate for import into A"

    # Prepare info
    count_a = len(lib_a[album_key]) if in_a else 0
    count_b = len(lib_b[album_key]) if in_b else 0

    # Split artist and album for better Excel filtering
    parts = album_key.split(" / ", 1)
    artist_val = parts[0] if len(parts) > 1 or " / " in album_key else album_key
    album_val = parts[1] if len(parts) > 1 else ""

    report_rows.append({
        "Status": status,
        "Recommendation": recommendation,
        "Artist": artist_val,
        "Album": album_val,
        "Tracks in A": count_a,
        "Tracks in B": count_b,
    })

  # Write CSV report
  csv_columns = [
      "Status",
      "Recommendation",
      "Artist",
      "Album",
      "Tracks in B",
      "Tracks in A",
  ]
  try:
    with open(output_csv, mode="w", newline="", encoding="utf-8-sig") as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=csv_columns, delimiter=";")
      writer.writeheader()
      for row in report_rows:
        writer.writerow(row)
    print(f"\nReport successfully saved to: {Path(output_csv).resolve()}")
  except Exception as e:
    print(f"Error saving CSV: {e}")


if __name__ == "__main__":
  print("=== iTunes / Apple Music Library Comparison ===")
  print("Please select Library A (Target / Master Library) 'Music' folder first:")
  LIBRARY_A = choose_folder("Select Library A (Target / Master Library) 'Music' folder")
  print(f"Selected: {LIBRARY_A}\n")

  print("Next, please select Library B (Source Library) to clean up:")
  LIBRARY_B = choose_folder("Select Library B (Source Library) 'Music' folder")
  print(f"Selected: {LIBRARY_B}\n")

  compare_libraries(LIBRARY_A, LIBRARY_B)