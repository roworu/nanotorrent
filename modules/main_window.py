import sys
import logging
import libtorrent as lt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QMenu
from PyQt6.QtCore import QTimer, Qt, QPoint
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
        self.speed_unit = "kB/s"
        # Settings Handler
        self.settings = SettingsHandler("settings.ini")
        self.global_download_path = self.settings.get("Downloads", "download_path")
        logging.info(f"Loaded download path: {self.global_download_path}")

        # Torrent Manager
        self.torrentmanager = TorrentManager(settings=self.settings)
        logging.info(f"TorrentManager started with settings")

        # Table Setup
        self.table = setup_table(self)
        self.setCentralWidget(self.table)

        # Menu Setup
        setup_menu(self)

        # Timer for updating the UI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(1000)  # Update the UI every 1 second


    def closeEvent(self, event):
        """Handle application close."""
        logging.info("Application is closing.")
        self.torrentmanager.stop()  # Save torrents and clean up
        event.accept()  # Allow the application to close


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


    def show_context_menu(self, position: QPoint):
        """Show a context menu for the selected row."""
        index = self.table.indexAt(position)
        if not index.isValid():
            return

        row = index.row()

        menu = QMenu(self)
        pause_start_action = menu.addAction("Pause/Start")
        refresh_action = menu.addAction("Refresh")
        explore_files_action = menu.addAction("Explore Files")
        show_info_action = menu.addAction("Show Information")
        delete_entry_action = menu.addAction("Delete Entry")
        delete_entry_files_action = menu.addAction("Delete Entry and Files")

        action = menu.exec(self.table.viewport().mapToGlobal(position))

        if action == pause_start_action:
            self.toggle_pause_start(row)
        elif action == refresh_action:
            self.refresh_torrent(row)
        elif action == explore_files_action:
            self.explore_files(row)
        elif action == show_info_action:
            self.show_information(row)
        elif action == delete_entry_action:
            self.delete_entry(row, delete_files=False)
        elif action == delete_entry_files_action:
            self.delete_entry(row, delete_files=True)


    def toggle_pause_start(self, row: int):
        """Toggle pause/start for the selected torrent."""
        torrent = self.torrentmanager.torrents[row]
        if torrent.status().is_paused:
            torrent.resume()
            logging.info(f"Resumed torrent: {torrent.status().name}")
        else:
            torrent.pause()
            logging.info(f"Paused torrent: {torrent.status().name}")


    def refresh_torrent(self, row: int):
        """Refresh the torrent information."""
        logging.info(f"Refreshing torrent: {self.torrentmanager.torrents[row].status().name}")
        self.update_table()


    def explore_files(self, row: int):
        """Open the download folder for the selected torrent."""
        torrent = self.torrentmanager.torrents[row]
        file_path = f"{self.global_download_path}/{torrent.status().name}"
        logging.info(f"Opening file path: {file_path}")
        try:
            import subprocess
            subprocess.run(["xdg-open", file_path], check=True)
        except Exception as e:
            logging.error(f"Failed to open file: {file_path}. Error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")


    def show_information(self, row: int):
        """Show detailed information about the selected torrent."""
        torrent = self.torrentmanager.torrents[row]
        info = (
            f"Name: {torrent.status().name}\n"
            f"Progress: {torrent.status().progress * 100:.2f}%\n"
            f"Download Rate: {torrent.status().download_rate / 1000:.2f} kB/s\n"
            f"Upload Rate: {torrent.status().upload_rate / 1000:.2f} kB/s\n"
            f"Peers: {torrent.status().num_peers}\n"
        )
        QMessageBox.information(self, "Torrent Information", info)


    def delete_entry(self, row: int, delete_files: bool):
        """Delete the torrent entry, optionally removing files."""
        torrent = self.torrentmanager.torrents[row]
        try:
            if delete_files:
                self.torrentmanager.session.remove_torrent(torrent, lt.options_t.delete_files)
                logging.info(f"Deleted torrent and files: {torrent.status().name}")
            else:
                self.torrentmanager.session.remove_torrent(torrent)
                logging.info(f"Deleted torrent: {torrent.status().name}")

            # Remove the torrent from the list
            self.torrentmanager.torrents.pop(row)
            self.update_table()
        except Exception as e:
            logging.error(f"Failed to delete torrent: {e}")
            QMessageBox.critical(self, "Error", f"Failed to delete torrent:\n{e}")


def start_ui():
    app = QApplication(sys.argv)
    client = TorrentClient()
    client.show()
    sys.exit(app.exec())
