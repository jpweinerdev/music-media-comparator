# Music Media Files Comparator for iTunes or Apple Music Library
A cross-platform Python script designed to safely compare two separate iTunes or Apple Music media libraries at the filesystem level. It helps you merge libraries without creating unwanted duplicates or losing track of your music files.

---

## 🎯 What Problem Does It Solve?
When merging two independent iTunes/Apple Music libraries, simply copying folders together leads to chaos, broken links, and hundreds of unwanted duplicate files. 

This script acts as a **smart pre-check tool**:
1. It reads two distinct music folder structures **read-only** (nothing gets deleted or modified automatically).
2. It compares albums using **bit-exact MD5 hashes** and file sizes.
3. It generates a clean, structured **CSV report** categorizing every album so you know precisely what to delete from the source library and what needs to be imported into your master library.

---

## ✨ Features
* **Cross-Platform:** Works seamlessly on **Windows** and **macOS** with intuitive graphical folder selection dialogs (`tkinter`). Fallback to console input is included if no GUI is available.
* **Bit-Exact Comparison:** Compares audio files using MD5 checksums and file sizes to ensure absolute data integrity.
* **Wide Audio Format Support:** Supports standard and legacy formats including `.mp3`, `.m4a`, `.m4p` (legacy DRM), `.m4b` (audiobooks), `.aac`, `.flac`, `.alac`, `.wav`, and `.aiff`.
* **Excel-Friendly CSV Output:** Exports results into a semicolon-separated CSV (`utf-8-sig`) with separate columns for artists and albums, making filtering and sorting in Microsoft Excel or Apple Numbers effortless.

---

## 🚀 Requirements
* **Python 3.x** installed on your system.
* No external third-party Python packages required (uses standard libraries only, `tkinter` is typically pre-installed with Python).

---

## 📖 How to Use
1. Clone or download this repository.
2. Run the script from your terminal or command prompt:
```bash
   python itunes_library_comparator.py
```
3. **Select Library A (Target / Master):** Choose the larger or more complete library folder into which music will be merged.
4. **Select Library B (Source):** Choose the secondary library you want to clean up and compare against the master.
   
   > ⚠️ **Important Note on Folder Selection:** 
   > Select the inner **`Music`** folder where the individual artist subfolders are located (e.g., `.../iTunes Media/Music` or `.../Media.localized/Music`). Do *not* select the top-level `iTunes` or `Media` folder.

5. Once completed, the script generates a file named **`itunes_library_comparison_report.csv`** in your working directory.

---

## 📊 Understanding the CSV Report
Open the generated CSV file in Excel/Numbers (ensure delimiter is set to semicolon `;`). The report uses the following columns:

| Column | Description |
| :--- | :--- |
| **Status** | Shows whether an album is an *Exact Match*, has a *Partial Overlap*, or exists *Only in Library A / Only in Library B*. |
| **Recommendation** | Actionable advice (e.g., *"Can be deleted from B (Duplicate)"* or *"Candidate for import into A"*). |
| **Artist** | Artist name extracted from the folder structure. |
| **Album** | Album name extracted from the folder structure. |
| **Tracks in B** | Number of audio tracks found in Library B. |
| **Tracks in A** | Number of audio tracks found in Library A. |

---

## 🛡️ Safety First
The script is strictly **read-only** regarding your music files. It performs no deletions or file moves. You remain in full control of your files based on the generated report.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
