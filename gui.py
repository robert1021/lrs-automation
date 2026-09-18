"""Modern tkinter GUI for the LRS Automation Tool.

Replaces the old ``rich`` text prompt loop. Long-running work (batch import
builds and PyAutoGUI bots) runs in background threads so the window stays
responsive, with progress streamed into the activity log.

Reference images are external: the Images page validates the ``images/``
folder next to the exe and tells the user which captures to replace for
their own resolution.
"""

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import (
    APP_ROOT,
    REQUIRED_IMAGES,
    image_path,
    imu_dashboard_path,
    ensure_image_dirs,
    validate_images,
)

BG = "#EEF2F7"
CARD = "#FFFFFF"
SIDEBAR = "#0F172A"
SIDEBAR_ACTIVE = "#1E293B"
ACCENT = "#2563EB"
ACCENT_ACTIVE = "#1D4ED8"
TEXT = "#0F172A"
MUTED = "#64748B"
SUCCESS = "#059669"
DANGER = "#DC2626"
BORDER = "#E2E8F0"

FONT_FAMILY = "Segoe UI"
TITLE_FONT = (FONT_FAMILY, 18, "bold")
SECTION_FONT = (FONT_FAMILY, 12, "bold")
BODY_FONT = (FONT_FAMILY, 10)
SMALL_FONT = (FONT_FAMILY, 9)
SIDEBAR_FONT = (FONT_FAMILY, 11)

NAV_ITEMS = (
    ("batch", "Generate\nBatch Import", "Compare LRS reports to the IMU dashboard."),
    ("parent", "Parent\nFiles RPA", "Create parent files in LRS via automation."),
    ("submission", "Submission\nFiles RPA", "Create submission files in LRS via automation."),
    ("images", "Images", "Check the external reference-image folders."),
)

EXCEL_TYPES = (("Excel workbooks", "*.xlsx"), ("All files", "*.*"))
CSV_TYPES = (("CSV reports", "*.csv"), ("All files", "*.*"))


class LRSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LRS Automation Tool")
        self.geometry("1120x720")
        self.minsize(980, 620)
        self.configure(bg=BG)

        self.log_queue: "queue.Queue[tuple[str, str]]" = queue.Queue()
        self._running = False
        self._nav_buttons: dict[str, ttk.Button] = {}
        self._pages: dict[str, ttk.Frame] = {}
        self._image_rows: ttk.Frame | None = None

        self._setup_style()
        self._build_shell()
        self._build_batch_page()
        self._build_simple_rpa_page(
            "parent",
            "Parent Files RPA",
            "Reads the LRS-PAR-TO-CREATE workbook and creates each parent "
            "file in LRS through GUI automation.",
            "Workbook with parent file data (.xlsx)",
            EXCEL_TYPES,
            self._run_parent,
        )
        self._build_simple_rpa_page(
            "submission",
            "Submission Files RPA",
            "Reads the batch-import workbook and creates each submission "
            "file in LRS through GUI automation.",
            "Batch import workbook (.xlsx)",
            EXCEL_TYPES,
            self._run_submission,
        )
        self._build_images_page()
        self.show_page("batch")
        self._refresh_image_status()
        self.after(120, self._drain_log_queue)

    # -- styling -----------------------------------------------------
    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD, relief="flat")
        style.configure("Sidebar.TFrame", background=SIDEBAR)
        style.configure("TLabel", background=BG, foreground=TEXT, font=BODY_FONT)
        style.configure("Card.TLabel", background=CARD, foreground=TEXT, font=BODY_FONT)
        style.configure("Title.TLabel", background=CARD, foreground=TEXT, font=TITLE_FONT)
        style.configure("Section.TLabel", background=CARD, foreground=TEXT, font=SECTION_FONT)
        style.configure("Muted.TLabel", background=CARD, foreground=MUTED, font=BODY_FONT)
        style.configure("MutedSmall.TLabel", background=CARD, foreground=MUTED, font=SMALL_FONT)
        style.configure("Sidebar.TLabel", background=SIDEBAR, foreground="white")
        style.configure("SidebarSub.TLabel", background=SIDEBAR, foreground="#94A3B8")
        style.configure("TButton", font=BODY_FONT, padding=8)
        style.configure("Accent.TButton", background=ACCENT, foreground="white",
                         borderwidth=0, focuscolor="none", padding=(14, 8))
        style.map("Accent.TButton",
                  background=[("active", ACCENT_ACTIVE), ("disabled", "#93C5FD")])
        style.configure("Ghost.TButton", background=CARD, foreground=TEXT, padding=(12, 6))
        style.configure("Nav.TButton", background=SIDEBAR, foreground="white",
                         font=SIDEBAR_FONT, anchor="w", padding=(16, 10),
                         borderwidth=0, focuscolor="none")
        style.map("Nav.TButton", background=[("active", SIDEBAR_ACTIVE)])
        style.configure("NavActive.TButton", background=ACCENT, foreground="white",
                         font=SIDEBAR_FONT, anchor="w", padding=(16, 10),
                         borderwidth=0, focuscolor="none")
        style.configure("TEntry", padding=6)
        self.option_add("*TCombobox*Listbox.font", BODY_FONT)

    # -- shell -------------------------------------------------------
    def _build_shell(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)

        sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = ttk.Label(sidebar, text="LRS", style="Sidebar.TLabel",
                          font=(FONT_FAMILY, 22, "bold"))
        brand.pack(anchor="w", padx=20, pady=(24, 0))
        sub = ttk.Label(sidebar, text="Automation Tool", style="SidebarSub.TLabel",
                        font=(FONT_FAMILY, 11))
        sub.pack(anchor="w", padx=20, pady=(0, 20))

        for key, title, _desc in NAV_ITEMS:
            btn = ttk.Button(sidebar, text=title.replace("\n", " "),
                             style="Nav.TButton",
                             command=lambda k=key: self.show_page(k))
            btn.pack(fill="x", padx=10, pady=3)
            self._nav_buttons[key] = btn

        foot = ttk.Label(sidebar, text="PyAutoGUI bots need\nthe LRS window visible.",
                         style="SidebarSub.TLabel", font=SMALL_FONT)
        foot.pack(side="bottom", anchor="w", padx=20, pady=20)

        main = ttk.Frame(root)
        main.pack(side="left", fill="both", expand=True)

        content_wrap = ttk.Frame(main)
        content_wrap.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        self._canvas = tk.Canvas(content_wrap, bg=BG, highlightthickness=0)
        content_scroll = ttk.Scrollbar(content_wrap, orient="vertical",
                                       command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=content_scroll.set)
        content_scroll.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._content = ttk.Frame(self._canvas)
        self._content_id = self._canvas.create_window((0, 0), window=self._content,
                                                      anchor="nw")
        self._content.bind("<Configure>",
                           lambda e: self._canvas.configure(
                               scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        self._log_card = ttk.Frame(main, style="Card.TFrame", padding=14)
        self._log_card.pack(fill="both", expand=False, padx=20, pady=(0, 6))
        log_head = ttk.Frame(self._log_card, style="Card.TFrame")
        log_head.pack(fill="x")
        ttk.Label(log_head, text="Activity log", style="Section.TLabel").pack(side="left")
        ttk.Button(log_head, text="Clear", style="Ghost.TButton",
                   command=self._clear_log).pack(side="right")
        text_frame = ttk.Frame(log_card, style="Card.TFrame")
        text_frame.pack(fill="both", expand=True, pady=(8, 0))
        self._log = tk.Text(text_frame, height=6, wrap="word", relief="flat",
                            bg=CARD, fg=TEXT, font=(FONT_FAMILY, 9),
                            highlightthickness=1, highlightbackground=BORDER,
                            state="disabled")
        scroll = ttk.Scrollbar(text_frame, command=self._log.yview)
        self._log.configure(yscrollcommand=scroll.set)
        self._log.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._log.tag_configure("info", foreground=TEXT)
        self._log.tag_configure("success", foreground=SUCCESS)
        self._log.tag_configure("error", foreground=DANGER)

        self._status_frame = ttk.Frame(main, padding=(20, 0, 20, 12))
        self._status_frame.pack(fill="x")
        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(self._status_frame, textvariable=self._status_var, font=SMALL_FONT,
                  foreground=MUTED, background=BG).pack(side="left")
        self._img_status_var = tk.StringVar(value="Checking images…")
        ttk.Label(self._status_frame, textvariable=self._img_status_var, font=SMALL_FONT,
                  foreground=MUTED, background=BG).pack(side="right")
        self._bind_global_mousewheel()

    def _card(self, parent) -> ttk.Frame:
        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))
        return card

    def _file_row(self, parent, label: str, default: str = "",
                  filetypes=EXCEL_TYPES) -> tk.StringVar:
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, style="Card.TLabel", width=26).pack(side="left")
        var = tk.StringVar(value=default or "")
        entry = ttk.Entry(row, textvariable=var)
        entry.pack(side="left", fill="x", expand=True, padx=(8, 8))
        ttk.Button(row, text="Browse…", style="Ghost.TButton",
                   command=lambda: self._browse(var, filetypes)).pack(side="right")
        return var

    def _browse(self, var: tk.StringVar, filetypes):
        chosen = filedialog.askopenfilename(filetypes=filetypes)
        if chosen:
            var.set(chosen)

    def show_page(self, key: str):
        for name, frame in self._pages.items():
            frame.pack_forget()
        self._pages[key].pack(fill="both", expand=True)
        for name, btn in self._nav_buttons.items():
            btn.configure(style="NavActive.TButton" if name == key else "Nav.TButton")
        if key == "images":
            self._log_card.pack_forget()
        else:
            self._log_card.pack(fill="both", expand=False, padx=20, pady=(0, 6),
                                before=self._status_frame)
        self._content.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._canvas.yview_moveto(0)

    # -- scrollable content ------------------------------------------
    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._content_id, width=event.width)

    def _bind_global_mousewheel(self):
        self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.bind_all("<Button-4>", self._on_mousewheel, add="+")
        self.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _on_mousewheel(self, event):
        node = event.widget
        inside_pages = False
        while node is not None:
            if node is getattr(self, "_log", None):
                return  # let the activity log scroll itself
            if node is self._canvas:
                inside_pages = True
                break
            node = getattr(node, "master", None)
        if not inside_pages:
            return
        if getattr(event, "num", None) == 5 or event.delta < 0:
            self._canvas.yview_scroll(1, "units")
        elif getattr(event, "num", None) == 4 or event.delta > 0:
            self._canvas.yview_scroll(-1, "units")
        return "break"

    # -- pages -------------------------------------------------------
    def _build_batch_page(self):
        page = ttk.Frame(self._content)
        self._pages["batch"] = page
        card = self._card(page)
        ttk.Label(card, text="Generate Batch Import", style="Title.TLabel").pack(anchor="w")
        ttk.Label(card, text="Compare the four LRS reports against the IMU dashboard "
                  "and build the parent + batch-import workbooks in Output/.",
                  style="Muted.TLabel", wraplength=760, justify="left").pack(anchor="w", pady=(4, 10))
        self._imu_var = self._file_row(card, "IMU Dashboard", imu_dashboard_path, EXCEL_TYPES)
        self._pla_var = self._file_row(card, "PLA submissions", "", CSV_TYPES)
        self._sla_var = self._file_row(card, "SLA submissions", "", CSV_TYPES)
        self._fsrn_var = self._file_row(card, "FSRN submissions", "", CSV_TYPES)
        self._cta_var = self._file_row(card, "CTA submissions", "", CSV_TYPES)
        self._batch_btn = ttk.Button(card, text="Generate batch import",
                                     style="Accent.TButton", command=self._run_batch)
        self._batch_btn.pack(anchor="e", pady=(12, 0))

    def _build_simple_rpa_page(self, key, title, blurb, file_label, filetypes, command):
        page = ttk.Frame(self._content)
        self._pages[key] = page
        card = self._card(page)
        ttk.Label(card, text=title, style="Title.TLabel").pack(anchor="w")
        ttk.Label(card, text=blurb, style="Muted.TLabel",
                  wraplength=760, justify="left").pack(anchor="w", pady=(4, 4))
        ttk.Label(card, text="Keep the LRS window visible. Move the mouse to the "
                  "top-left corner to abort (PyAutoGUI failsafe).",
                  style="MutedSmall.TLabel", wraplength=760,
                  justify="left").pack(anchor="w", pady=(0, 10))
        var = self._file_row(card, file_label, "", filetypes)
        setattr(self, f"_{key}_var", var)
        btn = ttk.Button(card, text=f"Run {title}", style="Accent.TButton", command=command)
        btn.pack(anchor="e", pady=(12, 0))
        setattr(self, f"_{key}_btn", btn)

    def _build_images_page(self):
        page = ttk.Frame(self._content)
        self._pages["images"] = page
        card = self._card(page)
        ttk.Label(card, text="Reference images", style="Title.TLabel").pack(anchor="w")
        ttk.Label(card, text="The bots find LRS controls by matching these screenshots. "
                  "They live in an images/ folder next to the exe — not inside it — "
                  "so you can re-capture them for your own resolution. File names "
                  "must stay exactly as listed.",
                  style="Muted.TLabel", wraplength=760, justify="left").pack(anchor="w", pady=(4, 10))
        ttk.Label(card, text=f"Folder: {image_path}", style="MutedSmall.TLabel",
                  wraplength=760, justify="left").pack(anchor="w", pady=(0, 8))
        btn_row = ttk.Frame(card, style="Card.TFrame")
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="Open images folder", style="Ghost.TButton",
                   command=self._open_images_folder).pack(side="left")
        ttk.Button(btn_row, text="Re-check", style="Ghost.TButton",
                   command=self._refresh_image_status).pack(side="left", padx=(8, 0))
        self._image_rows = ttk.Frame(card, style="Card.TFrame")
        self._image_rows.pack(fill="both", expand=True, pady=(10, 0))

    # -- background work ----------------------------------------------
    def _set_running(self, running: bool, message: str):
        self._running = running
        self._status_var.set(message)
        state = "disabled" if running else "normal"
        for btn in (getattr(self, "_batch_btn", None), getattr(self, "_parent_btn", None),
                    getattr(self, "_submission_btn", None)):
            if btn is not None:
                btn.configure(state=state)

    def _run_in_thread(self, label: str, func):
        if self._running:
            messagebox.showinfo("Busy", "A task is already running. Please wait.")
            return
        self._set_running(True, f"{label} — running…")
        self.log(f"{label} started.", "info")

        def emit(message: str):
            self.log_queue.put(("info", str(message)))

        def worker():
            try:
                func(emit)
            except Exception as exc:  # noqa: BLE001 - surfaced in the log
                self.log_queue.put(("error", f"{label} failed: {exc}"))
            else:
                self.log_queue.put(("success", f"{label} finished successfully."))
            finally:
                self.log_queue.put(("__done__", label))

        threading.Thread(target=worker, daemon=True).start()

    def _run_batch(self):
        paths = {
            "IMU Dashboard": self._imu_var.get(),
            "PLA submissions": self._pla_var.get(),
            "SLA submissions": self._sla_var.get(),
            "FSRN submissions": self._fsrn_var.get(),
            "CTA submissions": self._cta_var.get(),
        }
        missing = [k for k, v in paths.items() if not (v or "").strip()]
        if missing:
            messagebox.showwarning("Missing files",
                                   f"Please select: {', '.join(missing)}.")
            return

        def func(emit):
            from app import handle_generate_batch_import
            handle_generate_batch_import(paths["IMU Dashboard"], paths["PLA submissions"],
                                         paths["SLA submissions"], paths["FSRN submissions"],
                                         paths["CTA submissions"], on_log=emit)

        self._run_in_thread("Generate Batch Import", func)

    def _run_parent(self):
        source = self._parent_var.get()
        if not (source or "").strip():
            messagebox.showwarning("Missing file", "Please select the parent data workbook.")
            return
        if not messagebox.showwarning(
                "Takeover warning",
                "The bot will now control your mouse and keyboard to create "
                "parent files in LRS. Keep LRS visible and do not interfere.\n\n"
                "Continue?", type=messagebox.OKCANCEL) == "ok":
            return

        def func(emit):
            from app import handle_parent_files_rpa
            handle_parent_files_rpa(source, on_log=emit)

        self._run_in_thread("Parent Files RPA", func)

    def _run_submission(self):
        source = self._submission_var.get()
        if not (source or "").strip():
            messagebox.showwarning("Missing file", "Please select the submission workbook.")
            return
        if not messagebox.showwarning(
                "Takeover warning",
                "The bot will now control your mouse and keyboard to create "
                "submission files in LRS. Keep LRS visible and do not interfere.\n\n"
                "Continue?", type=messagebox.OKCANCEL) == "ok":
            return

        def func(emit):
            from app import handle_submission_files_rpa
            handle_submission_files_rpa(source, on_log=emit)

        self._run_in_thread("Submission Files RPA", func)

    # -- log ----------------------------------------------------------
    def log(self, message: str, kind: str = "info"):
        self.log_queue.put((kind, message))

    def _drain_log_queue(self):
        try:
            while True:
                kind, message = self.log_queue.get_nowait()
                if kind == "__done__":
                    self._set_running(False, "Ready.")
                    continue
                self._append_log(message, kind if kind in ("info", "success", "error") else "info")
        except queue.Empty:
            pass
        self.after(120, self._drain_log_queue)

    def _append_log(self, message: str, kind: str):
        self._log.configure(state="normal")
        self._log.insert("end", f"{message}\n", kind)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear_log(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

    # -- images -------------------------------------------------------
    def _refresh_image_status(self):
        missing = validate_images()
        total = sum(len(v) for v in REQUIRED_IMAGES.values())
        if not missing:
            self._img_status_var.set(f"Images: {total}/{total} found.")
        else:
            self._img_status_var.set(f"Images: {total - len(missing)}/{total} found "
                                     f"({len(missing)} missing).")
        if self._image_rows is None:
            return
        for child in self._image_rows.winfo_children():
            child.destroy()
        missing_set = set(missing)
        for folder_key in sorted(REQUIRED_IMAGES):
            folder = os.path.join(image_path, folder_key)
            names = REQUIRED_IMAGES[folder_key]
            bad = sum(1 for n in names if os.path.join(folder, n) in missing_set)
            header = ttk.Frame(self._image_rows, style="Card.TFrame")
            header.pack(fill="x", pady=(8, 2))
            ttk.Label(header, text=f"{folder_key}/", style="Section.TLabel").pack(side="left")
            badge = "OK" if bad == 0 else f"{bad} missing"
            ttk.Label(header, text=f"  {len(names) - bad}/{len(names)}  {badge}",
                      style="MutedSmall.TLabel").pack(side="left")
            for name in names:
                full = os.path.join(folder, name)
                mark = "✓" if full not in missing_set else "✗ missing"
                ttk.Label(self._image_rows, text=f"    {mark}  {name}",
                          style="MutedSmall.TLabel").pack(anchor="w")

    def _open_images_folder(self):
        try:
            os.makedirs(image_path, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(image_path)  # noqa: S606 - user-triggered local open
            elif sys.platform == "darwin":
                subprocess.Popen(["open", image_path])
            else:
                subprocess.Popen(["xdg-open", image_path])
        except Exception as exc:  # noqa: BLE001 - surfaced in dialog
            messagebox.showerror("Could not open folder", str(exc))


def launch():
    ensure_image_dirs()
    app = LRSApp()
    app.mainloop()
