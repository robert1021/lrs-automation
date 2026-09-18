# Reference images (external, user-maintained)

These images are **not bundled into the exe**. Keep this `images/` folder next
to the executable (or next to `main.py` when running from source) and replace
the captures with your own if your resolution differs.

## Folder layout

| Folder        | Used by                                            |
|---------------|----------------------------------------------------|
| `login/`      | login dialog (`login.py`)                          |
| `menubar/`    | LRS menu bar (`menu_bar.py`)                       |
| `file_insert/`| File Insert dialog (`file_insert.py`, `folder_update.py`) |
| `file_search/`| File Find dialog (`file_search.py`)                |
| `file_status/`| Edit Status dialog (`file_status.py`)              |
| `folder_tab/` | folder rows VOL/WAL/DB/CD (`folder_tab_window.py`) |
| `title_bar/`  | LRS window icon (`title_bar.py`)                   |
| `legacy/`     | old captures nothing references; safe to delete    |

## How to make your own set

1. Run the app and open the **Images** page to see which files are missing.
2. Capture each screenshot at your own resolution and save it over the file
   with the same name (file names are case-sensitive on some systems).
3. Keep the capture tightly cropped around the same UI element the old image
   showed — PyAutoGUI matches the pixels, not the file name.
4. Re-check the **Images** page until every row reports OK, then run the bots.
