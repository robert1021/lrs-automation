"""External image layout + GUI conversion regression tests (stdlib only).

These tests intentionally avoid importing the RPA modules (pyautogui/pandas)
so they run anywhere. They inspect source text and the on-disk layout.
"""

import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


class ImageLayoutTest(unittest.TestCase):
    def test_config_does_not_bundle_images(self):
        src = read("config.py")
        self.assertNotIn("_MEIPASS", src)
        self.assertNotIn("sys._MEIPASS", src)
        # External folder next to the exe in frozen mode.
        self.assertIn("sys.executable", src)
        for folder in ("login", "menubar", "file_insert", "file_search",
                       "file_status", "folder_tab", "title_bar"):
            self.assertIn(folder, src)

    def test_required_images_exist_on_disk(self):
        import config

        missing = config.validate_images()
        self.assertEqual(missing, [], f"missing reference images: {missing}")

    def test_image_folders_logically_separated(self):
        # No loose captures at the images/ root (except docs); every bot has
        # its own folder and login is no longer at the root.
        root_files = [f for f in os.listdir(os.path.join(ROOT, "images"))
                      if os.path.isfile(os.path.join(ROOT, "images", f))]
        self.assertEqual(sorted(root_files), ["README.md"])
        for folder in ("login", "menubar", "file_insert", "file_search",
                       "file_status", "folder_tab", "title_bar"):
            path = os.path.join(ROOT, "images", folder)
            self.assertTrue(os.path.isdir(path), f"missing folder: {path}")
            self.assertTrue(os.listdir(path), f"empty folder: {path}")

    def test_login_and_titlebar_paths(self):
        login_src = read("login.py")
        self.assertIn("login_image_path", login_src)
        title_src = read("title_bar.py")
        # Must match the real file name exactly (case-sensitive filesystems).
        self.assertIn("lrs_icon2.png", title_src)
        self.assertTrue(os.path.isfile(
            os.path.join(ROOT, "images", "title_bar", "lrs_icon2.png")))

    def test_packaging_excludes_images(self):
        for script in ("package_app.py", "package_discontinuation_bot.py",
                       "package_parent_bot.py", "package_submission_bot.py"):
            src = read(script)
            self.assertNotIn("images;images", src, script)
            self.assertNotIn("images:images", src, script)

    def test_gui_replaces_tui(self):
        gui_src = read("gui.py")
        self.assertIn("tkinter", gui_src)
        self.assertIn("ttk", gui_src)
        self.assertIn("validate_images", gui_src)
        self.assertNotIn("from rich", gui_src)
        self.assertNotIn("import rich", gui_src)
        # Pages region must scroll: long pages (Images) overflow small windows.
        self.assertIn("scrollregion", gui_src)
        self.assertIn("MouseWheel", gui_src)
        self.assertIn("_on_mousewheel", gui_src)
        # Activity log is hidden on the Images page (not needed there).
        self.assertIn("_log_card", gui_src)
        app_src = read("app.py")
        self.assertNotIn("from rich", app_src)
        self.assertNotIn("Prompt.ask", app_src)
        for symbol in ("handle_generate_batch_import", "handle_parent_files_rpa",
                       "handle_submission_files_rpa", "run_app"):
            self.assertIn(symbol, app_src)
        req = read("requirements.txt")
        self.assertNotIn("rich", req.lower())


if __name__ == "__main__":
    unittest.main()
