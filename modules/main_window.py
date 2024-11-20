import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QTimer
from modules.ui.table_manager import setup_table, update_table
from modules.ui.menu_manager import setup_menu
from modules.torrent_manager import TorrentManager
from modules.settings_window import SettingsWindow
from modules.utils.settings_handler import SettingsHandler


class TorrentClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NanoTorrent")
        self.setGeometry(100, 100, 800, 400)

        logging.info(f"Main window initialized")

        # Torrent Manager
        self.torrentmanager = TorrentManager()
        logging.info(f"TorrentManager started")

        # Settings Handler
        self.settings = SettingsHandler("settings.ini")
        self.global_download_path = self.settings.get("Downloads", "download_path")
        logging.info(f"Loaded download path: {self.global_download_path}")

        # Table Setup
        self.table = setup_table(self)
        self.setCentralWidget(self.table)

        # Menu Setup
        setup_menu(self)

        # Timer for updating the UI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(1000)  # Update the UI every 1 second

    def add_torrent(self):
        """Add a new torrent to the session."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Torrent File", "", "Torrent Files (*.torrent)")
        if not file_path:
            return

        # Use global download path if available
        save_path = self.global_download_path or ""

        if not save_path:
            QMessageBox.warning(self, "Error", "Download path is not set.")
            logging.warning(f"Unable to add torrent: Download path not set!")
            return

        try:
            self.torrentmanager.add_torrent(file_path, save_path)
            self.update_table()  # Ensure immediate UI update after adding torrent
        except Exception as e:
            logging.error(f"Error happened during torrent adding: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add torrent:\n{e}")

    def update_table(self):
        """Refresh the table with torrent data."""
        torrents = self.torrentmanager.get_torrents()
        update_table(self.table, torrents)

    def open_settings(self):
        """Open the settings window."""
        self.settings_window = SettingsWindow(self, settings_handler=self.settings)
        self.settings_window.show()
        self.settings_window.accepted.connect(self.reload_settings)

    def reload_settings(self):
        """Reload settings after closing the settings window."""
        self.global_download_path = self.settings.get("Downloads", "download_path")
        logging.info(f"Reloaded download path: {self.global_download_path}")


def start_ui():
    app = QApplication(sys.argv)
    client = TorrentClient()
    client.show()
    sys.exit(app.exec())
